import os
from core.plugin import InfoPlugin
from core.utils import read_file, read_bin, run


class CPUPlugin(InfoPlugin):

    name = "cpu"

    def detect_soc_from_device_tree(self):

        model = read_bin("/proc/device-tree/model")
        compatible = read_bin("/proc/device-tree/compatible")

        soc = None

        if compatible:

            compat = compatible.lower()

            if "imx8mp" in compat:
                soc = "imx8mp"

            elif "imx8mq" in compat:
                soc = "imx8mq"

            elif "imx95" in compat:
                soc = "imx95"

            elif "hailo15" in compat or "hailo-15" in compat:
                soc = "hailo-15"

        return {
            "device_tree_model": model,
            "device_tree_compatible": compatible,
            "soc": soc
        }

    def detect_soc_sysfs(self):

        family = read_file("/sys/devices/soc0/family")
        machine = read_file("/sys/devices/soc0/machine")
        soc_id = read_file("/sys/devices/soc0/soc_id")
        revision = read_file("/sys/devices/soc0/revision")

        return {
            "soc_family": family,
            "soc_machine": machine,
            "soc_id": soc_id,
            "soc_revision": revision
        }

    def parse_cpuinfo(self):

        cpuinfo = read_file("/proc/cpuinfo")

        result = {
            "cpu_implementer": None,
            "cpu_architecture": None,
            "cpu_variant": None,
            "cpu_part": None,
            "cpu_revision": None
        }

        if not cpuinfo:
            return result

        for line in cpuinfo.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip().lower()
            value = value.strip()

            if key == "cpu implementer":
                result["cpu_implementer"] = value

            elif key == "cpu architecture":
                result["cpu_architecture"] = value

            elif key == "cpu variant":
                result["cpu_variant"] = value

            elif key == "cpu part":
                result["cpu_part"] = value

            elif key == "cpu revision":
                result["cpu_revision"] = value

        return result

    def detect_lscpu(self):

        out = run("lscpu")

        data = {}

        if not out:
            return data

        for line in out.splitlines():

            if ":" not in line:
                continue

            k, v = line.split(":", 1)

            data[k.strip().lower().replace(" ", "_")] = v.strip()

        return data

    def gather(self, context=None):

        arch = os.uname().machine
        cores = os.cpu_count()

        dt = self.detect_soc_from_device_tree()

        sysfs = self.detect_soc_sysfs()

        cpuinfo = self.parse_cpuinfo()

        lscpu = self.detect_lscpu()

        return {

            "cpu": {

                "architecture": arch,
                "cores": cores,

                "soc": dt.get("soc"),

                "device_tree_model": dt.get("device_tree_model"),
                "device_tree_compatible": dt.get("device_tree_compatible"),

                "soc_family": sysfs.get("soc_family"),
                "soc_machine": sysfs.get("soc_machine"),
                "soc_id": sysfs.get("soc_id"),
                "soc_revision": sysfs.get("soc_revision"),

                "cpuinfo": cpuinfo,

                "lscpu": lscpu

            }

        }
