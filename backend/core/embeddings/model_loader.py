from sentence_transformers import SentenceTransformer


class EmbeddingModelLoader:

    def load(self):

        return SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )