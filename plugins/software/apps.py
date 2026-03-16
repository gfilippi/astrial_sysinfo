import os
from core.plugin import InfoPlugin


class AppsPlugin(InfoPlugin):

    name = "apps"
    section = "software"

    APPS_DIR = "/root/apps"

    def gather(self, context=None):

        apps = []

        if not os.path.isdir(self.APPS_DIR):
            return {"apps": []}

        try:

            for entry in os.scandir(self.APPS_DIR):

                if not entry.is_dir():
                    continue

                stat = entry.stat()

                apps.append({

                    "name": entry.name,
                    "path": entry.path,
                    "last_modified": int(stat.st_mtime)

                })

        except Exception:
            return {"apps": []}

        apps.sort(key=lambda x: x["name"])

        return {
            "apps": apps
        }
