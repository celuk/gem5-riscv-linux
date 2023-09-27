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

### Booting
In a terminal run disk image and the bootloader as an example:

```bash
gem5/build/RISCV/gem5.opt \
gem5/configs/example/riscv/fs_linux.py \
--caches --l1i_size=16kB --l1d_size=16kB \
--l2cache --l2_size=256kB \
--mem-type=DDR4_2400_8x8 \
--mem-size=1GB \
--cpu-type=TimingSimpleCPU \
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

### Required Downloads
Download bootloader image from here: http://dist.gem5.org/dist/v22-1/kernels/riscv/static/bootloader-vmlinux-5.10

Download riscv64 linux image from here: https://cdimage.ubuntu.com/releases/22.04.3/release/ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img.xz

Extract the disk image `ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img.xz`:

```bash
xz -d -v ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img.xz
```

### Booting

To boot ubuntu, either you can use [riscv-linux.py](riscv-linux.py) python script by setting `kernel` and `disk_image` paths of the downloaded images:

```bash
build/RISCV/gem5.opt ./riscv-linux.py
```

or you can also use command line that does same thing exactly as script:

```bash
gem5/build/RISCV/gem5.opt \
gem5/configs/example/riscv/fs_linux.py \
--caches --l1i_size=16kB --l1d_size=16kB \
--l2cache --l2_size=256kB \
--mem-type=DDR4_2400_8x8 \
--mem-size=3GB \
--cpu-type=TimingSimpleCPU \
--kernel=riscv-imgs/ubuntu/bootloader-vmlinux-5.10 \
--disk-image=riscv-imgs/ubuntu/ubuntu-22.04.3-preinstalled-server-riscv64+unmatched.img \
--command-line="console=ttyS0 root=/dev/vda1 ro"
```

In the above command the most important thing is `root=/dev/vda1` part in `command-line` flag and also `root_partition=1` parameter in [riscv-linux.py](riscv-linux.py). Default root partition is 0 and if you do not set this flag, either in the script or command line, ubuntu cannot boot like other os images.

For booting any os image you can determine the root partition via `fdisk -l <your-disk-image>` command. Here is an example:

```bash
shc@karpuz:~/projects/imgextract$ fdisk -l ./ubuntu.img
Disk ./ubuntu.img: 4,5 GiB, 4831838208 bytes, 9437184 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 1FFAD53A-DA06-4DAA-96B2-7D6029A8F4E0

Device      	Start 	End Sectors  Size Type
./ubuntu.img1  235520 9437150 9201631  4,4G Linux filesystem
./ubuntu.img12 227328  235519	8192	4M Linux filesystem
./ubuntu.img13 	34	2081	2048	1M HiFive FSBL
./ubuntu.img14   2082   10239	8158	4M HiFive BBL
./ubuntu.img15  10240  227327  217088  106M EFI System

Partition table entries are not in disk order.
```

As you can see above, `Linux filesystem` (the one with biggest size) shows in device `ubuntu.img``1` and `1` indicates that `root_partition=``1` or in the other words `root` should be mounted at `dev/vda``1`. (It was `0` (`dev/vda`) for other os images I mentioned above.)

### Controlling

Is same like others, I mentioned above.

## Editing Disk Images (e.g placing your own files and boot after)

If you want to edit any disk image and place your own files, either you can use `qemu`, boot the os and e.g. copy your files from host with `scp` command:

Install qemu:

```bash
sudo apt install qemu-system-misc opensbi u-boot-qemu qemu-utils
```

Run qemu with your disk image:

```bash
qemu-system-riscv64 \
-machine virt \
-nographic \
-m 16384 \
-smp 8 \
-bios /usr/lib/riscv64-linux-gnu/opensbi/generic/fw_jump.elf \
-kernel /usr/lib/u-boot/qemu-riscv64_smode/uboot.elf \
-device virtio-net-device,netdev=eth0 \
-netdev user,id=eth0,hostfwd=tcp::5555-:22 \
-drive file=myubuntu.img,format=raw,if=virtio
```
For example, copy your file from host:

```bash
scp -P 5555 /home/shc/myfile ubuntu@localhost:/home/ubuntu
```

then exit from qemu, now your disk image is modified and you can boot your disk image as I explained for e.g. ubuntu, and you can see your file on running gem5 system.

OR

easily you can mount disk image, edit and unmount it:

Look for partitions with  `fdisk -l <your-disk-image>` command. Look for start addresses of them;

if there is not then your offset is 0 and mount as:

```bash
mkdir mnt
sudo mount -o loop ./your-disk-image ./mnt
```

Then edit system files in mnt directory, if you cannot, use `sudo chmod 777 <file-to-be-edit>` command or for all `sudo chmod -R 777 ./mnt`.

If you see as given example for ubuntu, look for linux filesystem start address which is `235520` in the example. Now, multiply the address with `512` and your offset is should be `512` * `235520` = `120586240
` and mount as:

```bash
mkdir mnt
sudo mount -o loop,offset=120586240 ./your-disk-image ./mnt
```

Then edit the files in mnt directory.

Lastly, unmount your image:

```bash
sudo umount ./mnt
```

Now your disk image is modified and you can boot your disk image as I explained for e.g. ubuntu, and you can see your file on running gem5 system.
