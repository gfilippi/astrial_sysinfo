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
the output structure is separated in sections: hardware, software, metadata, here is a (reduced) example of the output

```
hardware:
  cpu:
    lscpu:
  accelerators:
    hailo:
  memory:
  storage:
    rootfs: 
    filesystems:

software:
  apps:
  deb_packages:
  python_packages:
   yocto:
    release: 5.15-kirkstone (kirkstone)
    distro: NXP i.MX Release Distro
    distro_id: fsl-imx-xwayland
    distro_codename: kirkstone
    os_release:
      id: fsl-imx-xwayland
      name: NXP i.MX Release Distro
      version: 5.15-kirkstone (kirkstone)
      version_id: 5.15-kirkstone
      pretty_name: NXP i.MX Release Distro 5.15-kirkstone (kirkstone)
      distro_codename: kirkstone
    issue: NXP i.MX Release Distro 5.15-kirkstone
    uname:
      sysname: Linux
      nodename: astrial-8gb-imx8mp
      release: 5.15.71+g5ef6222cf
      version: '#1 SMP PREEMPT Fri Feb 21 13:47:25 UTC 2025'
      machine: aarch64
    kernel:
      kernel_version: 5.15.71+g5ef6222cf
      kernel_full: 'Linux version 5.15.71+g5ef6222cf (oe-user@oe-host) (aarch64-poky-linux-gcc
        (GCC) 11.3.0, GNU ld (GNU Binutils) 2.38.20220708) #1 SMP PREEMPT Fri Feb
        21 13:47:25 UTC 2025'
      cmdline: console=ttymxc0,115200 root=/dev/mmcblk2p2 rootwait rw
    build:
      distro: fsl-imx-xwayland
      distro_version: 5.15-kirkstone
      datetime: '20250514064200'
      distro_name: NXP i.MX Release Distro
      image_basename: system-astrial-image
      machine: astrial-8gb-imx8mp
      tune_pkgarch: armv8a
      machine_features: usbgadget usbhost vfat alsa touchscreen pci wifi bluetooth
        nxp8987 nxp8987 linux-imx-signature imx-boot-signature u-boot-imx-signature
        optee jailhouse  rtc qemu-usermode
      distro_features: acl alsa argp bluetooth debuginfod ext2 ipv4 ipv6 largefile
        pcmcia usbgadget usbhost wifi xattr nfs zeroconf pci 3g nfc x11 vfat seccomp
        largefile opengl ptest multiarch  vulkan  systemd jailhouse virtualization
        x11 wayland pam pulseaudio gobject-introspection-data ldconfig
      common_features: ''
      image_features: debug-tweaks hwcodecs nfs-server package-management splash ssh-server-openssh
        tools-debug tools-profile tools-sdk tools-testapps weston
      tune_features: aarch64 armv8a crc crypto
      target_fpu: ''
    layers:
      meta: HEAD:24a3f7b3648185e33133f5d96b184a6cb6524f3d
      meta-poky: HEAD:24a3f7b3648185e33133f5d96b184a6cb6524f3d
      meta-oe: HEAD:744a4b6eda88b9a9ca1cf0df6e18be384d9054e3
      meta-multimedia: HEAD:744a4b6eda88b9a9ca1cf0df6e18be384d9054e3
      meta-python: HEAD:744a4b6eda88b9a9ca1cf0df6e18be384d9054e3
      meta-freescale: HEAD:c82d4634e7aba8bc0de73ce1dfc997b630051571
      meta-freescale-3rdparty: HEAD:5977197340c7a7db17fe3e02a4e014ad997565ae
      meta-freescale-distro: HEAD:d5bbb487b2816dfc74984a78b67f7361ce404253
      meta-bsp: HEAD:9174c61f4dc80b14e0bfdaec9200ed58fb41615f
      meta-sdk: HEAD:9174c61f4dc80b14e0bfdaec9200ed58fb41615f
      meta-ml: HEAD:9174c61f4dc80b14e0bfdaec9200ed58fb41615f
      meta-v2x: HEAD:9174c61f4dc80b14e0bfdaec9200ed58fb41615f
      meta-nxp-demo-experience: HEAD:52eaf8bf42f8eda2917a1c8c046003c8c2c8f629
      meta-chromium: HEAD:e232c2e21b96dc092d9af8bea4b3a528e7a46dd6
      meta-clang: HEAD:c728c3f9168c8a4ed05163a51dd48ca1ad8ac21d
      meta-gnome: HEAD:744a4b6eda88b9a9ca1cf0df6e18be384d9054e3
      meta-networking: HEAD:744a4b6eda88b9a9ca1cf0df6e18be384d9054e3
      meta-filesystems: HEAD:744a4b6eda88b9a9ca1cf0df6e18be384d9054e3
      meta-qt6: HEAD:ed785a25d12e365d1054700d4fc94a053176eb14
      meta-virtualization: HEAD:9482648daf0bb42ff3475e7892542cf99f3b8d48
      meta-intel-realsense: HEAD:25d59f0c12ff41181b7e66bb93d443c81a09c058
      meta-hailo-accelerator: HEAD:3a2665df39d1464e1808b5c95a8ce44994fae8b5
      meta-hailo-libhailort: HEAD:3a2665df39d1464e1808b5c95a8ce44994fae8b5
      meta-hailo-tappas: HEAD:3a2665df39d1464e1808b5c95a8ce44994fae8b5
      meta-imx8mp-isp-imx219: HEAD:b496ceff816023647414a4a9a6074c2ba8aa9be3
      meta-secure-boot: HEAD:7158fbae750517a278a89e18cf4466f8c9d1c610
      meta-sysele-nxp-5.15.71: HEAD:45684bf0a27f891b77df0f36952c889fdd4577ab
    bitbake_version: null
metadata:
  device_fingerprint: 7b0b741539f5295b6e65a1e4afa62585da6ab151d89f63d8b7474239c70427f2
```
