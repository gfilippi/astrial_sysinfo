import os
import platform
import re

from core.plugin import InfoPlugin
from core.utils import read_file, run


class YoctoPlugin(InfoPlugin):

    name = "yocto"
    section = "software"

    # -------------------------
    # sanitation helpers
    # -------------------------

    def sanitize(self, text):

        if not text:
            return None

        text = text.replace("\x00", "")
        text = text.replace("\r", "")
        text = text.strip()

        return text

    def clean_issue(self, text):

        if not text:
            return None

        text = self.sanitize(text)

        # remove common escape placeholders
        text = text.replace("\\n", "").replace("\\l", "")

        return text.strip()

    # -------------------------
    # parsing helpers
    # -------------------------

    def parse_key_values(self, text):

        data = {}

        if not text:
            return data

        for line in text.splitlines():

            if "=" not in line:
                continue

            k, v = line.split("=", 1)

            k = k.strip().lower()
            v = v.strip().strip('"')

            data[k] = v

        return data

    def parse_build_configuration(self, text):

        config = {}
        layers = {}

        if not text:
            return config, layers

        section = None

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if "Build Configuration" in line:
                section = "config"
                continue

            if "Layer Revisions" in line:
                section = "layers"
                continue

            if section == "config":

                if "=" in line:

                    k, v = line.split("=", 1)

                    config[k.strip().lower()] = v.strip()

            elif section == "layers":

                if "=" in line:

                    k, v = line.split("=", 1)

                    layers[k.strip()] = v.strip()

        return config, layers

    # -------------------------
    # system information
    # -------------------------

    def gather_uname(self):

        uname = os.uname()

        return {
            "sysname": uname.sysname,
            "nodename": uname.nodename,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine
        }

    def gather_kernel(self):

        return {

            "kernel_version": platform.release(),

            "kernel_full":
                self.sanitize(read_file("/proc/version")),

            "cmdline":
                self.sanitize(read_file("/proc/cmdline"))
        }

    def gather_os_release(self):

        text = read_file("/etc/os-release")

        return self.parse_key_values(text)

    def gather_build_files(self):

        paths = [
            "/etc/build",
            "/etc/version",
            "/etc/yocto-release"
        ]

        raw = {}

        for p in paths:

            txt = read_file(p)

            if txt:
                raw[os.path.basename(p)] = self.sanitize(txt)

        return raw

    # -------------------------
    # main gather
    # -------------------------

    def gather(self, context=None):

        os_release = self.gather_os_release()

        uname = self.gather_uname()

        kernel = self.gather_kernel()

        issue = self.clean_issue(read_file("/etc/issue"))

        build_files = self.gather_build_files()

        build_config = {}
        layers = {}

        if "build" in build_files:

            build_config, layers = \
                self.parse_build_configuration(build_files["build"])

        bitbake_version = run("bitbake --version")

        if bitbake_version:
            bitbake_version = self.sanitize(bitbake_version)

        return {

            "yocto": {

                "release": os_release.get("version"),

                "distro": os_release.get("name"),
                "distro_id": os_release.get("id"),
                "distro_codename": os_release.get("distro_codename"),

                "os_release": os_release,

                "issue": issue,

                "uname": uname,

                "kernel": kernel,

                "build":

                    build_config,

                "layers":

                    layers,

                "bitbake_version":

                    bitbake_version

            }

        }
