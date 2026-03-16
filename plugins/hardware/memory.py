import re
from core.plugin import InfoPlugin
from core.utils import read_file, run, safe_json


class MemoryPlugin(InfoPlugin):

    name = "memory"

    def parse_meminfo(self):

        meminfo = read_file("/proc/meminfo")

        result = {}

        if not meminfo:
            return result

        for line in meminfo.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip().lower().replace(" ", "_")

            # value like "4096000 kB"
            parts = value.strip().split()

            if len(parts) >= 1:

                try:
                    v = int(parts[0])
                except:
                    continue

                if len(parts) > 1 and parts[1].lower() == "kb":
                    v *= 1024

                result[key] = v

        return result

    def parse_df(self):

        df = run("df -B1 --output=source,fstype,size,used,avail,target")

        filesystems = []

        if not df:
            return filesystems

        lines = df.splitlines()

        if len(lines) < 2:
            return filesystems

        for line in lines[1:]:

            parts = re.split(r"\s+", line.strip(), maxsplit=5)

            if len(parts) < 6:
                continue

            try:
                size = int(parts[2])
                used = int(parts[3])
                avail = int(parts[4])
            except:
                continue

            filesystems.append({

                "device": parts[0],
                "fstype": parts[1],
                "size_bytes": size,
                "used_bytes": used,
                "available_bytes": avail,
                "mountpoint": parts[5]

            })

        return filesystems

    def parse_lsblk(self):

        out = run("lsblk -b -J -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE")

        data = safe_json(out)

        if not data:
            return []

        return data.get("blockdevices", [])

    def gather(self, context=None):

        meminfo = self.parse_meminfo()

        total_ram = meminfo.get("memtotal")

        available_ram = meminfo.get("memavailable")

        filesystems = self.parse_df()

        block_devices = self.parse_lsblk()

        rootfs = None

        for fs in filesystems:

            if fs["mountpoint"] == "/":
                rootfs = fs

        return {

            "memory": {

                "ram_total_bytes": total_ram,
                "ram_available_bytes": available_ram,

                "meminfo": meminfo

            },

            "storage": {

                "rootfs": rootfs,

                "filesystems": filesystems,

                "block_devices": block_devices

            }

        }
