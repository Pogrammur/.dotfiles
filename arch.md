# BlackArch

## Installation

To install BlackArch on my machine I will need a USB drive to write the ISO image to, and the image itself.

I started by downloading the ISO image I wanted from [BlackArch](https://blackarch.org/downloads.html) so I could burn the ISO to a bootable USB Drive.

I am using a 32GB PNY USB drive. It is USB 3.2 and I am going to burn the Netinstall ISO to it.

I check all the available drives on my computer using the fdisk command. I had to add sudo in order to see the drive information and determined that my USB was at /dev/sdc.
`$ sudo fdisk -l`

Write the ISO to the USB.
`# Example Image Writing
$ sudo dd bs=512M status=progress if=file.iso of=/dev/sdx`

The default login for all BlackArch ISOs and OVA is root:blackarch

I am installing BA on a laptop. I make sure the laptop is completely shutdown. I plug in the USB drive with my live ISO. I turn on the laptop(0wlvu) and begin tapping esc, in order to enter the BIOS menu.

Once in the BIOS menu, I select boot menu from the list. THe shortcut for Boot Menu is F9 on my laptop.

In the boot menu my USB drive is listed as the second option and I select the USB drive as the boot option.

The BA boot options appear and I choose the BA netinstall option.

Once the laptop is booted up I am at a login terminal and I login using the default login info.

I am now at the command line.

THe install guide says to simply run a pacman command after ISO bootup. I ran that command and found I didnt have internet (duh) but also NetworkManager doesnt seem to be part of the ISO so I ran iwctl to start IWD. IWD would get stuck on starting and not actually start.

The instructions for blackarch are a mess as there are several different pages that all say different things. The command I needed to move forward was:
`$ blackarch-install`

I am prompted to choose 1 of 3 options. install from:
1. repository(online)
2.full-iso(offline)
3. from source(online)

I am selecting 1.

WHile going through the install script the installer fell into a loop of not being able to chroot into passwd and after letting the loop run for a while, I used <CTL-c> to cancel the process. When I tried to run the script again I then got and error saying that the file system could not be created as /dev/sda2 was still in use by the system.

I used the umount command, with -l(lazy) and a(all) flags and all of the active drives were unmounted.
`umount -la`

I rebooted my laptop.

# Arch Linux

## Installation

I am going to be installing Arch Linux on my HP Elitebook.

I download the latest archlinux ISO from [Arch linux](archlinux.org)


I check all the available drives on my computer, in order to double check the name of the USB I will be writing the ISO to, using the fdisk command. I had to add sudo in order to see the drive information and determined that my USB was at /dev/sdc.
`$ sudo fdisk -l`

Write the ISO to the USB.
`# Example Image Writing
$ sudo dd bs=512M status=progress if=file.iso of=/dev/sdx`

Once the image is written to the USB drive I am ready to plug it into my laptop, while its shutdown.

Turn on the computer and use the esc button while the laptop is loading in order to enter the BIOS boot menu.

Boot into live usb.

First set the key map. You can display all available keymaps with this command:
`ls /usr/share/kbd/keymaps/**/*.map.gz | less`

Set keymap with: `loadkeys <keymap>`

Use iwctl to connect to the internet.
`$ station wlan0 connect ssid`

set system clock, important or some apps wont run:
`timedatectl set-ntp true`
Verify with `timedatectl status`

Set up disk partitions:

Use `lsblk` to list available drives
To actually setup the partitions use `fdisk /dev/sdx` to enter the partition setup
`p` to print current layout
`g` to create empty gpt partition table
`n` to create a new partition.
    create 3 partitions

# Basic File System
    -1 +550M
    -2 +2G
    -3 +remaining
    Partition 1 is going to be our EFI Boot file system.
    Partition 2 is going to be our swap file.
    Partition 3 is going to be our linux file system.
    t to change type
    select part.1
    change type to 1 EFI System

    t to change type
    select part.2
    change type to 19 Linux Swap

    Part.3 remains as Linux File System



# LVM Partition table
    -1 +1G
    -2 +1G
    -3 +remaining
    Partition 3 is going to be an LVM so the partition type must be changed
    `t` to change type
    select partition 3
    change type to `44` Linux LVM
    `p` to verify partition layout is correct
    `w` to write new partition table

# Format Partitions

# Basic File System Without Encryption
    Format sda1:
    `mkfs.fat -F32 /dev/sda1`
    Format sda2:
    `mkswap /dev/sda2`
    `swapon /dev/sda2`
    Format sda3:
    `mkfs.ext4 /dev/sda3`


# LVM Partition Formating With Encryption
Format sda1:
`mkfs.fat -F32 /dev/sda1`
Format sda2:
`mkfs.ext4 /dev/sda2`
Set up, but do not yet format sda3 (LVM encrypted):
`cryptsetup luksFormat /dev/sda3`
set passwd for encrypted drive
My sda3 is now an encrypted drive and will require passwd on startup

# Setup LVM
    First open the LVM partition:
`cryptsetup open --type luks /dev/sda3 lvm`
enter passwd
Next create a physical volume for LVM
`pvcreate /dev/mapper/lvm`
Create a volume group:
`vgcreate volgroup0 /dev/mapper/lvm`
Create a logical volume
`lvcreate -L 30GB volgroup0 -n lv_root`
`lvcreate -L 195GB volgroup0 -n lv_home`
To verify everything use:
`vgdisplay` to display volume groups
`lvdisplay` to display logical volumes

`modprobe dm_mod`

`vgscan`
`vgchange -ay` to activate all volume groups

Format the logcail volumes:
`mkfs.ext4 /dev/volgroup0/lv_root`
`mkfs.ext4 /dev/volgroup0/lv_home`

# Mount the partitions

# Mount Basic File System
`mount /dev/sda3 /mnt`
``

# Mount LVM
Mount sda2 to boot directory
`mount /dev/volgroup0/lv_root /mnt`
`mkdir /mnt/boot`
`mount /dev/sda2 /mnt/boot` (yes, partition 2 is being mounted before partition 1, roll with it.
Next mount the home directory:
`mkdir /mnt/home`
`mount /dev/volgroup0/lv_home /mnt/home`

# Install required packages
Install the base packages needed for arch linux:
`pacstrap -i /mnt base linux linux-firmware linux-headers vim git`

Gen fstab:
`genfstab -U -p /mnt >> /mnt/etc/fstab`
Check filesystem for correctness by running:
`cat /mnt/etc/fstab`

# Chroot
Chroot into the system by running:
`arch-chroot /mnt`

set local time:
`ln  -sf /usr/share/zoneinfo/America/Los-Angeles /etc/localtime`
if unsure of zone info run`ls /usr/share/zoneinfo/`

set hardware clock:
`hwclock --systohc`

set the locale by editing the locale.gen file:
`vim /etc/locale.gen`
Uncomment en_US...UTF8
run: `locale-gen`

Set hostname:
`vim /etc/hostname`
Ex:
`lappy`

Set localhost:
`vim /etc/hosts`
add following lines to hosts file:
`127.0.0.1  localhost
::1        localhost
127.0.1.1 lappy.localdomain lappy`

# Users and Passwords
set root password:
`passwd`

make new user:
`useradd username`

user passwd:
`passwd username`

Add user to groups:
`usermod -aG wheel,audio,video,optical,storage user`

Install sudo:
`pacman -S sudo`

Edit the visudo file to give user sudo privledge:
(in order to not edit in vi run):
`EDITOR=vim visudo`

Scroll down to the wheel group and uncomment the line that says:
`"%wheel ALL=(ALL:ALL) ALL`

Install grub:
`pacman -S grub efibootmgr dosfstool os-prober mtools base-devel lvm2 networkmanager openssh`

Enable SSH:
`systemctl enable sshd`

# Steps to Set Up Encryption
Add encrypt and lvm2 to hooks in mkinitcpio or the kernal wont understand the file system:
`vim /etc/mkinitcpio.conf`
Add "encrypt" and "lvm2" after "block" on the HOOKS line

Gen linux kernal:
`mkinitcpio -p linux`
Make sure encrypt and lvm2 are part of the build hooks.

Add encrypted drive to grub and install grub:
`vim /etc/default/grub`
Find line "GRUB_CMDLINE_LINUX_DEFAULT="..."
Add "cryptdevice=/dev/sda3:volgroup0"
Get this line right or your system may not boot


# Finish EFI Partition Basic
`mkdir /boot/EFI`
`mount /dev/sda1 /boot/EFI`
`grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck`
`grub-mkconfig -o /boot/grub/grub.cfg`

# Finish EFI Partition LVM
`mkdir /boot/EFI`
`mount /dev/sda1 /boot/EFI`
`grub-install --target=x86_64-efi --bootloader-id=grub_uefi --recheck`
`cp /usr/share/locale/en\@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo`
`grub-mkconfig -o /boot/grub/grub.cfg`

Enable Netowrk Manager
`systemctl enable NetworkManager`

Exit out of chroot by giving the command: `exit`

Unmount:
`umount -l /mnt`

Reboot


# Booting Into Your New System

# Basic System

# LVM SYstem
First things is first. Make our signature directory.
make sure to change the owner of the directory after creating it.
`chown -hR user /home`

# Download and setup nvim, yay, wpaperd.

Before booting into our graphical environment we need to  install yay, several dependencies are required from the AUR, and download our stadard packages and .dotfiles.

To install yay we need to git clone the yay repo from github.
`git clone https://aur.archlinux.org/yay.git`
`makepkg -si`

`yay -S wlroots python-pywlroots grim wpaperd`

Next setup Neovim. We like to do this from source.
make sure to move back to the home directory to avoid having to move the file.
`cd && git clone https://github.comneovim/neovim.git`
`cd neovim`
`make CMAKE_BUILD_TYPE=RelWithDebInfo`
`sudo make install`

# Xorg Graphical Environment
First we install some software
`sudo pacman -S xorg xorg-xinit arandr nitrogen picom awesome alacritty firefox dmenu pulseaudio alsa-utils element ninja openvpn pcmanfm plocate rustup tmux unzip virtualbox wget `
Make an xinitrc file:
`cp /etc/X11/xinit/xinitrc /home/andrew/.xinitrc`
`nvim .xinitrc`
Deleted the last 5 lines and add your own programs
`nitrogen --restore &
picom &
exec awesome`




pacman -S









# Hyprland Build
I built my graphical environment using wayland with hyprland as my wm. I have had to change some of my standard programs as wayland does not support them. awesome > hyperland. alacritty. dmenu > tofi. gBar. nitrogen not necessary. picom not necessary.

danyspin97/wpaperd

