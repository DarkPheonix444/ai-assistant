class TreeFormatter:

    def format(
        self,
        tree: dict
    ) -> str:

        lines = []

        self._build_lines(
            tree,
            lines,
            ""
        )

        return "\n".join(lines)

    def _build_lines(
        self,
        tree: dict,
        lines: list[str],
        prefix: str
    ):

        for name, value in tree.items():

            if value is None:

                lines.append(
                    f"{prefix}{name}"
                )

            else:

                lines.append(
                    f"{prefix}{name}/"
                )

                self._build_lines(
                    value,
                    lines,
                    prefix + "    "
                )