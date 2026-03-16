from core.plugin import InfoPlugin
from core.utils import run


class DebPackagesPlugin(InfoPlugin):

    name = "deb_packages"
    section = "software"

    def gather(self, context=None):

        out = run("dpkg-query -W -f='${Package} ${Version}\n'")

        pkgs = []

        if out:

            for line in out.splitlines():

                parts = line.split()

                if len(parts) == 2:
                    pkgs.append({
                        "name": parts[0],
                        "version": parts[1]
                    })

        return {"deb_packages": pkgs}
