from pathlib import Path


class TreeBuilder:

    def build(
        self,
        files,
        root
    ):

        tree = {}

        for file in files:

            parts = (
                file.path
                .relative_to(root)
                .parts
            )

            current = tree

            for part in parts[:-1]:

                current = current.setdefault(
                    part,
                    {}
                )

            current[parts[-1]] = None

        return tree