from core.plugin import InfoPlugin
from core.utils import run, safe_json


class PythonPackagesPlugin(InfoPlugin):

    name = "python_packages"
    section = "software"

    def pip_json(self):

        commands = [
            "pip3 list --format=json",
            "python3 -m pip list --format=json"
        ]

        for cmd in commands:

            out = run(cmd)

            if not out:
                continue

            data = safe_json(out)

            if isinstance(data, list):
                return data

        return None

    def pip_text(self):

        commands = [
            "pip3 list",
            "python3 -m pip list"
        ]

        for cmd in commands:

            out = run(cmd)

            if not out:
                continue

            lines = out.splitlines()

            if len(lines) < 3:
                continue

            pkgs = []

            for line in lines[2:]:  # skip header

                parts = line.split()

                if len(parts) < 2:
                    continue

                pkgs.append({
                    "name": parts[0],
                    "version": parts[1]
                })

            if pkgs:
                return pkgs

        return None

    def python_metadata(self):

        try:

            import importlib.metadata as metadata

            pkgs = []

            for dist in metadata.distributions():

                pkgs.append({
                    "name": dist.metadata["Name"],
                    "version": dist.version
                })

            return pkgs

        except Exception:
            return None

    def gather(self, context=None):

        pkgs = self.pip_json()

        if not pkgs:
            pkgs = self.pip_text()

        if not pkgs:
            pkgs = self.python_metadata()

        return {
            "python_packages": pkgs or []
        }
