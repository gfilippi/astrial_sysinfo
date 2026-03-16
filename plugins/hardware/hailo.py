import re
from core.plugin import InfoPlugin
from core.utils import run


class HailoPlugin(InfoPlugin):

    name = "hailo"

    def _sanitize(self, text):
        if not text:
            return None

        # remove null chars
        text = text.replace("\x00", "")

        # normalize line endings
        text = text.replace("\r", "")

        return text.strip()

    def _parse_identify(self, text):

        result = {}

        if not text:
            return result

        for line in text.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip().lower().replace(" ", "_")
            value = value.strip()

            result[key] = value

        return result

    def _detect_device_type(self, parsed):

        name = parsed.get("board_name") or parsed.get("device_architecture")

        if not name:
            return None

        name = name.lower()

        if "hailo-8" in name or "hailo8" in name:
            return "hailo-8"

        if "hailo-15" in name or "hailo15" in name:
            return "hailo-15"

        if "hailo-10" in name or "hailo10" in name:
            return "hailo-10"

        return name

    def gather(self, context=None):

        identify_raw = run("hailortcli fw-control identify")

        identify_raw = self._sanitize(identify_raw)

        if not identify_raw:
            return {}

        parsed = self._parse_identify(identify_raw)

        device = self._detect_device_type(parsed)

        firmware = parsed.get("firmware_version")

        result = {

            "accelerators": {

                "hailo": {

                    "device": device,
                    "firmware_version": firmware,
                    "device_architecture": parsed.get("device_architecture"),
                    "board_name": parsed.get("board_name"),
                    "control_protocol": parsed.get("control_protocol_version"),
                    "serial_number": parsed.get("serial_number"),
                    "pci_device": parsed.get("executing_on_device"),

                    # parsed structured data
                    "identify": parsed,

                    # cleaned raw text for debugging
                    "identify_raw": identify_raw

                }

            }

        }

        return result
