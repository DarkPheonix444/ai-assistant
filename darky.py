# nova_assistant_fixed.py
import sys
import threading
import time
import re
import os
import datetime
import webbrowser
import subprocess
import traceback

# ---- Core deps (your existing engine) ----
import speech_recognition as sr
import pyttsx3
import pyautogui
import cv2
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ---- New deps for GUI and features ----
from PyQt6 import QtCore, QtGui, QtWidgets
import wikipedia
from pymongo import MongoClient

# ---------------- MongoDB (safe connect) ----------------
# ---------------- MongoDB Connection ----------------
from pymongo import MongoClient
import datetime

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    client.admin.command("ping")  # test connection
    db = client["nova_assistant"]
    convo_collection = db["conversations"]
    print("✅ Connected to MongoDB")
except Exception as e:
    convo_collection = None
    print("⚠️ MongoDB not connected:", e)


def save_conversation(user_text, nova_text):
    """Store chat pairs into MongoDB safely."""
    if convo_collection is None:
        return
    try:
        convo_collection.insert_one({
            "user": user_text,
            "nova": nova_text,
            "timestamp": datetime.datetime.utcnow()
        })
    except Exception as e:
        print("❌ MongoDB save error:", e)

def load_recent_conversations(limit=20):
    if convo_collection is None:
        return []
    try:
        history = list(convo_collection.find().sort("timestamp", -1).limit(limit))
        history.reverse()  # oldest first
        return history
    except Exception as e:
        print("❌ MongoDB load error:", e)
        return []


# ---------------- DIALOGPT SETUP ----------------
print("Loading tokenizer & model (this may take a while)...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

# Ensure pad token exists (DialoGPT sometimes doesn't have it set)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Put model on device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()
print(f"Model loaded on device: {device}")

# Extended memory (20-turn rolling history)
MAX_HISTORY = 20
conversation_history = []

# ---------------- SPEAK FUNCTION (threaded + re-init) ----------------
def speak(text):
    # Keep a printed log (useful for debugging)
    print(f"NOVA: {text}")

    def _run(tt=text):
        try:
            # use default init, but prefer sapi5 on Windows if available
            try:
                engine = pyttsx3.init(driverName="sapi5")
            except Exception:
                engine = pyttsx3.init()
            engine.setProperty("rate", 175)
            voices = engine.getProperty("voices")
            if voices:
                engine.setProperty("voice", voices[0].id)
            # sanitize text a bit (avoid problematic characters)
            safe_text = re.sub(r"[^\x00-\x7F]+", " ", tt).strip()
            if not safe_text:
                safe_text = "I am doing well, thanks for asking."
            engine.say(safe_text)
            engine.runAndWait()
        except Exception as e:
            # avoid raising in background thread
            print("TTS error:", e)

    threading.Thread(target=_run, daemon=True).start()


# ---------------- LISTEN FUNCTION ----------------
def listen(timeout=5):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎧 Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            time.sleep(0.25)  # let TTS finish before mic opens
            audio = r.listen(source, phrase_time_limit=timeout)
    except Exception as e:
        print("[STT] Microphone error:", e)
        return ""

    try:
        query = r.recognize_google(audio, language="en-in").lower()
        print(f"You said: {query}")
        return query
    except Exception as e:
        print(f"[STT] Recognition error: {e}")
        return ""


# ---------------- GREETING ----------------
def greet():
    speak("Initializing Nova voice.")
    hour = int(datetime.datetime.now().hour)
    if 6 <= hour < 12:
        speak("Good morning Jainam!")
    elif 12 <= hour < 18:
        speak("Good afternoon Jainam!")
    else:
        speak("Good evening Jainam!")
    speak("Nova is online. Say 'Nova' to wake me up.")


# ---------------- CAMERA FUNCTION ----------------
def open_camera():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Could not open the webcam.")
            return
    except Exception as e:
        speak("Could not access webcam.")
        print("Webcam open error:", e)
        return

    speak("Camera is active. Press 'c' to capture, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Nova Camera", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            fname = f"nova_capture_{int(time.time())}.png"
            cv2.imwrite(fname, frame)
            speak(f"Captured image saved as {fname}")
        elif key == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


# ---------------- OPEN APP FUNCTION ----------------
apps = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vscode": r"C:\Program Files\Microsoft VS Code\Code.exe",
    "file": r"C:\Windows\explorer.exe",
    "notepad": r"C:\Windows\System32\notepad.exe",
    "whatsapp": r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2539.2.0_x64__cv1g1gvanyjgm\WhatsApp.exe",
    "chatgpt": r"C:\Program Files\WindowsApps\OpenAI.ChatGPT-Desktop_1.2025.258.0_x64__2p2nqsd0c76g0\app\ChatGPT.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "spotify": r"C:\Users\kanan\AppData\Roaming\Spotify\Spotify.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
    "youtube": r"www.youtube.com"
}


def open_app(app_name):
    app_name = app_name.lower()
    if app_name in apps:
        speak(f"Opening {app_name}")
        time.sleep(0.3)
        try:
            subprocess.Popen(apps[app_name])
        except Exception as e:
            speak(f"Failed to open {app_name}")
            print("open_app error:", e)
    elif app_name in ["camera", "webcam"]:
        speak("Opening camera.")
        time.sleep(0.3)
        open_camera()
    else:
        speak(f"Sorry, I could not find {app_name}")


# ---------------- DIALOGPT RESPONSE WITH MEMORY ----------------
def get_chat_response(user_input):
    global conversation_history

    conversation_history.append(f"User: {user_input}")
    prompt = "\n".join(conversation_history[-10:]) + "\nNova:"

    try:
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        output_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=120,
            pad_token_id=tokenizer.eos_token_id,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.2,
        )

        generated = output_ids[0, input_ids.shape[-1]:]
        response = tokenizer.decode(generated, skip_special_tokens=True).strip()

        if not response:
            response = "I'm doing fine, thanks for asking."

    except Exception as e:
        print("Error generating response:", e)
        response = "Sorry, I faced an issue processing that."

    conversation_history.append(f"Nova: {response}")
    save_conversation(user_input, response)
    return response

# ---------------- Wikipedia helper ----------------
def fetch_wikipedia_summary(query, sentences=3):
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=sentences)
        return summary
    except Exception as e:
        print("Wikipedia error:", e)
        return f"Sorry, I couldn't fetch Wikipedia info for '{query}'."


# ---------------- GUI: Main Window ----------------
class NovaWindow(QtWidgets.QWidget):
    wakeSignal = QtCore.pyqtSignal()  # emitted by background wake listener

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nova Assistant")
        self.setWindowIcon(QtGui.QIcon())
        self.setFixedSize(500, 580)
        self.setStyleSheet(
            """
            QWidget { background: #121417; color: #EDEFF2; }
            QPushButton#mic {
                background: #1F6FEB; border-radius: 28px; color: white; padding: 10px;
            }
            QPushButton#mic:hover { background: #2B7AEF; }
            QTextEdit, QPlainTextEdit {
                background: #161A1F; border: 1px solid #22262B; border-radius: 8px;
            }
            QLabel#headline { font-size: 16px; font-weight: bold; }
        """
        )

        # Headline
        self.headline = QtWidgets.QLabel("Nova is online — click mic or say 'Nova'")
        self.headline.setObjectName("headline")

        # Chat area
        self.chat = QtWidgets.QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setPlaceholderText("Conversation appears here...")

        # Mic button
        self.mic_btn = QtWidgets.QPushButton("🎙️", self)
        self.mic_btn.setObjectName("mic")
        self.mic_btn.setFixedSize(56, 56)
        self.mic_btn.clicked.connect(self.on_mic_clicked)

        # Wikipedia panel (hidden by default)
        self.wiki_panel = QtWidgets.QPlainTextEdit()
        self.wiki_panel.setReadOnly(True)
        self.wiki_panel.setFixedHeight(160)
        self.wiki_panel.hide()

        # Close panel button
        self.close_panel_btn = QtWidgets.QPushButton("Close")
        self.close_panel_btn.clicked.connect(self.hide_wiki_panel)
        self.close_panel_btn.hide()

        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.headline)
        layout.addWidget(self.chat)
        hl = QtWidgets.QHBoxLayout()
        hl.addStretch(1)
        hl.addWidget(self.mic_btn)
        hl.addStretch(1)
        layout.addLayout(hl)
        layout.addWidget(self.wiki_panel)
        layout.addWidget(self.close_panel_btn)

        # Wake word signal
        self.wakeSignal.connect(self.wake_from_signal)

        # Start wake listener in background
        self.wake_thread = threading.Thread(target=self.wake_listener, daemon=True)
        self.wake_thread.start()

    # Wake word background listener
    def wake_listener(self):
        while True:
            text = listen(timeout=4)
            if text and ("nova" in text or "no va" in text or "novaa" in text or "nava" in text):
                # emit signal to main thread
                self.wakeSignal.emit()
            time.sleep(0.25)

    @QtCore.pyqtSlot()
    def wake_from_signal(self):
        self.append_chat("🟢 Wake word detected: Nova")
        speak("Yes Jainam, I’m listening.")
        self.activate_nova()

    def append_chat(self, text):
        self.chat.append(text)
        cursor = self.chat.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        self.chat.setTextCursor(cursor)

    def on_mic_clicked(self):
        self.append_chat("🎧 Listening...")
        threading.Thread(target=self.handle_interaction, daemon=True).start()

    # Main interaction handler
    def handle_interaction(self):
        query = listen(timeout=6)
        if not query:
            self.append_chat("❌ Didn't catch that.")
            return
        self.append_chat(f"🧑 You: {query}")

        # Intent routing: Wikipedia search vs normal chat vs commands
        if query.startswith("wikipedia") or "search wikipedia for" in query or "wikipedia for" in query:
            topic = (
                query.replace("search wikipedia for", "")
                .replace("wikipedia for", "")
                .replace("wikipedia", "")
                .strip()
            )
            if not topic:
                speak("What topic should I look up on Wikipedia?")
                self.append_chat("❓ What topic should I look up on Wikipedia?")
                topic = listen(timeout=5)
                if not topic:
                    self.append_chat("❌ No topic provided.")
                    return
            summary = fetch_wikipedia_summary(topic, sentences=3)
            self.show_wiki_panel(summary)
            speak(f"Here's what I found about {topic}.")
            self.append_chat(f"📖 Wikipedia ({topic}):\n{summary}")
            # Auto-hide after 12s
            QtCore.QTimer.singleShot(12000, self.hide_wiki_panel)
            return

        # Commands
        if "time" in query:
            time_str = datetime.datetime.now().strftime("%I:%M %p")
            msg = f"The time is {time_str}"
            self.append_chat(f"🕒 {msg}")
            speak(msg)
            return

        if query.startswith("open "):
            app_name = query.replace("open", "").strip()
            self.append_chat(f"🗂️ Opening {app_name}...")
            open_app(app_name)
            return

        if "screenshot" in query:
            file_name = f"screenshot_{int(time.time())}.png"
            try:
                pyautogui.screenshot().save(file_name)
                msg = f"Screenshot saved as {file_name}"
                self.append_chat(f"📸 {msg}")
                speak(msg)
            except Exception as e:
                self.append_chat("❌ Screenshot failed.")
                speak("Screenshot failed.")
                print("screenshot error:", e)
            return

        if "search" in query and not query.startswith("search wikipedia"):
            q = query.replace("search", "").strip()
            if not q:
                speak("What do you want me to search?")
                self.append_chat("❓ What should I search?")
                q = listen(timeout=5)
            if q:
                msg = f"Opening Google for {q}"
                self.append_chat(f"🔎 {msg}")
                speak(msg)
                webbrowser.open(f"https://www.google.com/search?q={q}")
            else:
                self.append_chat("❌ No search query provided.")
            return

        if "shutdown" in query or "exit" in query:
            speak("Goodbye Jainam, powering off.")
            QtCore.QCoreApplication.quit()
            return

        # Chat response
        response = get_chat_response(query)
        self.append_chat(f"🤖 Nova: {response}")
        speak(response)

    def show_wiki_panel(self, text):
        self.wiki_panel.setPlainText(text)
        self.wiki_panel.show()
        self.close_panel_btn.show()

    def hide_wiki_panel(self):
        self.wiki_panel.hide()
        self.close_panel_btn.hide()

    # Manual activation entry (used by wake word)
    def activate_nova(self):
        self.on_mic_clicked()


# ---------------- GUI: Floating Orb ----------------
# ---------------- GUI: Floating Orb ----------------
class FloatingOrb(QtWidgets.QWidget):
    def __init__(self, main_window: NovaWindow):
        super().__init__()
        self.main_window = main_window
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowStaysOnTopHint
            | QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(100, 100)
        self.dragging = False
        self.pos_delta = QtCore.QPoint(0, 0)

        # Animation timer for movement
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move_step)
        self.timer.start(30)  # smoother animation

        # Movement parameters
        self.dx = 3
        self.dy = 2

        # Start near bottom-right
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self.move(screen.width() - 150, screen.height() - 200)

        # For pulse glow animation
        self.glow_radius = 30
        self.glow_growing = True

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Center of orb
        center = QtCore.QPointF(self.width() / 2, self.height() / 2)

        # Animate glow pulsation
        if self.glow_growing:
            self.glow_radius += 0.6
            if self.glow_radius > 36:
                self.glow_growing = False
        else:
            self.glow_radius -= 0.6
            if self.glow_radius < 28:
                self.glow_growing = True

        # Glow layers
        for r, alpha in [(self.glow_radius + 8, 40), (self.glow_radius + 4, 80), (self.glow_radius, 130)]:
            color = QtGui.QColor(31, 111, 235, alpha)
            p.setBrush(color)
            p.setPen(QtCore.Qt.PenStyle.NoPen)
            p.drawEllipse(center, r, r)

        # Core circle
        p.setBrush(QtGui.QColor(31, 111, 235))
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.drawEllipse(center, 18, 18)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = True
            self.pos_delta = event.globalPosition().toPoint() - self.pos()
        elif event.button() == QtCore.Qt.MouseButton.RightButton:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.pos_delta)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.dragging = False
            # Left click toggles main window
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def move_step(self):
        if self.dragging:
            return
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        x, y = self.x(), self.y()
        w, h = self.width(), self.height()

        x += self.dx
        y += self.dy

        # Bounce effect
        if x <= 0 or x + w >= screen.width():
            self.dx = -self.dx
        if y <= 0 or y + h >= screen.height():
            self.dy = -self.dy

        self.move(x, y)
        self.update()


# Load last 20 full conversations from MongoDB (if available)
recent_convos = load_recent_conversations(20)
conversation_history = []
for convo in recent_convos:
    conversation_history.append(convo.get("user", ""))
    conversation_history.append(convo.get("nova", ""))


# ---------------- Entry point ----------------
def main():
    greet()
    app = QtWidgets.QApplication(sys.argv)

    # Main window and floating orb
    main_window = NovaWindow()
    orb = FloatingOrb(main_window)
    orb.show()

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
