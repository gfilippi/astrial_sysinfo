import subprocess
import json


def run(cmd, timeout=2):

    try:

        out = subprocess.check_output(
            cmd,
            shell=True,
            timeout=timeout,
            stderr=subprocess.DEVNULL
        )

        return out.decode().strip()

    except:
        return None


def read_file(path):

    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None


def read_bin(path):

    try:
        with open(path, "rb") as f:
            return f.read().decode(errors="ignore").replace("\x00", "")
    except:
        return None


def safe_json(data):

    try:
        return json.loads(data)
    except:
        return None
