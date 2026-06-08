from pathlib import Path


class TreeBuilder:

    def build(self, files):

        tree = {}

        for file in files:

            parts = file.path.parts

            current = tree

            for part in parts[:-1]:
                current = current.setdefault(part, {})

            current[parts[-1]] = None

        return tree