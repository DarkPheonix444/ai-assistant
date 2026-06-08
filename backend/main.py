from tools.file_editor.editor import FileEditor
from tools.file_editor.backup import BackupManager
from tools.file_editor.rollback import RollbackManager


editor = FileEditor()
backup = BackupManager()
rollback = RollbackManager()

file_path = "test.txt"

# Create file
editor.write(
    file_path,
    "Original Content"
)

# Backup
backup_dir = backup.create_backup(
    task_id="001",
    files=[file_path]
)

# Modify
editor.write(
    file_path,
    "Modified Content"
)

print(
    editor.read(file_path)
)

# Rollback
rollback.rollback(
    backup_dir
)

print(
    editor.read(file_path)
)