# gem5-riscv-linux

For running any riscv based linux on gem5, you need to install dependencies and build gem5.

## Installing gem5 Dependencies

```
sudo apt install \
build-essential \
git \
m4 \
scons \
zlib1g \
zlib1g-dev \
libprotobuf-dev \
protobuf-compiler \
libprotoc-dev \
libgoogle-perftools-dev \
python3-dev \
python3-six \
python-is-python3 \
libboost-all-dev \
pkg-config
```

## Building gem5

```
git clone https://github.com/gem5/gem5

cd gem5

scons build/RISCV/gem5.opt -j$(nproc)

```

## UCanLinux

## Fedora

### Required Downloads

Download prebuilt fedora riscv disk image from here:

https://fedorapeople.org/groups/risc-v/disk-images

Download prebuilt bootloader from here:

https://github.com/UCanLinux/riscv64-sample/blob/master/bbl

Extract the riscv disk image `stage4-disk.img.xz`:

```bash
xz -d -v stage4-disk.img.xz
```

### Running
In a terminal run disk image and the bootloader as an example:

```bash
gem5/build/RISCV/gem5.opt \
-re \
gem5/configs/example/riscv/fs_linux.py \
--caches --l1i_size=16kB --l1d_size=16kB \
--l2cache --l2_size=256kB \
--mem-type=DDR4_2400_8x8 \
--mem-size=1GB \
--cpu-type=TimingSimpleCPU
--kernel=riscv-imgs/fedora/bbl \
--disk-image=riscv-imgs/fedora/stage4-disk.img
```

### Controlling
After running via gem5, you can control and see the boot process by connecting to default port `3456`.

Either you can connect via `telnet`:

```bash
telnet localhost 3456
```

or after building (one time) `m5term`, you can connect via it:

```bash
cd gem5/util/term
make
```

```bash
gem5/util/term/m5term localhost 3456
```

## Ubuntu

```bash
build/RISCV/gem5.opt ./riscv-linux.py
```
