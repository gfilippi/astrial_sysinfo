import hashlib
from core.plugin import InfoPlugin
from core.utils import read_file


class FingerprintPlugin(InfoPlugin):

    name = "fingerprint"
    section = "metadata"

    def gather(self, context=None):

        data = ""

        for f in [
            "/proc/cpuinfo",
            "/etc/os-release",
            "/proc/device-tree/model"
        ]:

            content = read_file(f)

            if content:
                data += content

        fingerprint = hashlib.sha256(
            data.encode()
        ).hexdigest()

        return {

            "device_fingerprint": fingerprint

        }
