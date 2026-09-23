import re


class ErrorAnalyzer:

    def analyze(self, build_result: dict):

        if build_result["success"]:
            return {
                "has_error": False,
                "file": None,
                "repair_file": None,
                "repair_action": None,
                "error": None
            }

        error_text = build_result.get(
            "error",
            ""
        )

        file_path = self._find_file(
            error_text
        )

        repair_file = self._find_repair_file(
            error_text
        )

        repair_action = self._find_repair_action(
            error_text
        )

        return {
            "has_error": True,
            "file": file_path,
            "repair_file": repair_file,
            "repair_action": repair_action,
            "error": error_text
        }

    def _find_file(
        self,
        error_text: str
    ):

        patterns = [
            r"failed to load config from\s+(.+?vite\.config\.js)",
            r"Could not resolve entry module\s+[\"'](.+?)[\"']",
            r"([A-Za-z]:[\\/].*?src[\\/].+?\.jsx)",
            r"([A-Za-z]:[\\/].*?src[\\/].+?\.js)",
            r"([A-Za-z]:[\\/].*?src[\\/].+?\.css)",
            r"([A-Za-z]:[\\/].+?vite\.config\.js)",
            r"([A-Za-z]:[\\/].+?postcss\.config\.[cm]?js)",
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                error_text,
                re.IGNORECASE
            )

            if match:

                path = match.group(1)

                if (
                    "node_modules"
                    not in path.lower()
                ):
                    return path

        return None

    def _find_repair_file(
        self,
        error_text: str
    ):

        error_lower = error_text.lower()

        # Tailwind 4 requires @tailwindcss/postcss.
        if (
            "trying to use `tailwindcss` directly"
            in error_lower
            or
            "postcss plugin has moved"
            in error_lower
        ):
            return "postcss.config.cjs"

        # Missing autoprefixer/postcss/tailwind package.
        if (
            "cannot find package"
            in error_lower
            or
            "cannot find module"
            in error_lower
            or
            "module not found"
            in error_lower
        ):
            return "package.json"

        if (
            "eresolve"
            in error_lower
            or
            "unable to resolve dependency tree"
            in error_lower
        ):
            return "package.json"

        if (
            "could not resolve entry module"
            in error_lower
        ):

            match = re.search(
                r'Could not resolve entry module\s+[\'"](.+?)[\'"]',
                error_text
            )

            if match:
                return match.group(1)

        if "node_modules" in error_lower:
            return None

        return None

    def _find_repair_action(
        self,
        error_text: str
    ):

        error_lower = error_text.lower()

        # Old CommonJS config using .js inside
        # an ESM project.
        if (
            "module is not defined in es module scope"
            in error_lower
            and
            "postcss.config.js"
            in error_lower
        ):
            return {
                "type": "rename",
                "source": "postcss.config.js",
                "destination": "postcss.config.cjs"
            }

        # Tailwind 4 configuration repair.
        if (
            "trying to use `tailwindcss` directly"
            in error_lower
            or
            "postcss plugin has moved"
            in error_lower
        ):
            return {
                "type": "rewrite",
                "file": "postcss.config.cjs"
            }

        return None