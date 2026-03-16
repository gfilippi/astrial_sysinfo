# astrial_sysinfo
This is a simple script to create a json or yaml output with a detailed description of ASTRIAL platform. Uself to gather info when downloading/installing 3rd party apps, checking for missing packages or veryfying hw/sw requirements.

how to use:
```
python3 ./sysinfo.py --format yaml > ./info.yaml
```
or
```
python3 ./sysinfo.py --format json > ./info.json
```
the output structure is separated in sections: hardware, software, metadata
