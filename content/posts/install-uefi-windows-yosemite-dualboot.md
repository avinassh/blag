---
title: "Install Windows 8 UEFI on Legacy BIOS with Clover (and Dual boot with Yosemite)"
date: "2014-12-28T16:20:00+05:30"
categories: ["tutorial"]
tags: ["hackintosh", "osx", "uefi"]
slug: "install-uefi-windows-yosemite-dualboot"
summary: "This tutorial will help you install Windows 8 on a Legacy BIOS in UEFI mode using Clover and dual boot with Yosemite."
---

In this tutorial I am going to explain how to install Windows 8 on a Legacy BIOS in UEFI mode (Yes! It's possible!!) using Clover and dual boot with Yosemite. Technically this tutorial should work for Windows 7 and Mavericks also, but I haven't tried. 

This tutorial was originally written for Insanely Mac Forums. Check the [original thread](http://www.insanelymac.com/forum/topic/303615-guide-install-windows-8-uefi-on-legacy-bios-with-clover-and-dual-boot-with-yosemite/). 

### What you get?
You have a machine with Legacy BIOS and at the end of tutorial, you would have Yosemite OS X and Windows 8.1, in UEFI mode, on a GPT  partition with Clover as Bootloader. Isn't that amazing? This tutorial covers installation of both Yosemite and Windows 8.

### Why GPT/UEFI?
1. You can have multiple Recovery Partitions in GPT
2. Depending on BIOS, sometimes Clover doesn't play well in Non-UEFI. You may face all sorts of weird boot/BCD errors
3. GPT can support more than 2TB space (MBR cannot)
4. You can have upto 128 partitions (woot!) in GPT (as opposed ONLY 4 primary partitions in MBR/Hybrid MBR partition scheme)
5. GPT disk provides greater reliability due to replication and cyclical redundancy check (CRC) protection of the partition table.
6. UEFI enables better use of bigger hard drives.
7. Technical changes abound in UEFI. UEFI has room for more useful and usable features than could ever be crammed into the BIOS. Among these are cryptography, network authentication, support for extensions stored on non-volatile media, an integrated boot manager, and even a shell environment for running other EFI applications such as diagnostic utilities or flash updates. In addition, both the architecture and the drivers are CPU-independent, which opens the door to a wider variety of processors (including those using the ARM architecture, for example).
8. GPT/UEFI is the future ;-)


### Credits:
A big thanks to [fusion71au](http://www.insanelymac.com/forum/user/846696-fusion71au/), he guided me and helped me to install UEFI Windows on my laptop and made it possible. In fact, this tutorial is actually combination of several of his posts (check Sources section).

### Prerequisites:
- A pendrive of 200MB (or more) for test Clover config (optional)
- Two pendrives of 8GB (or more), one for OS X and another for Windows installation media. OR a single pen drive of 16GB (or more).
- A running OS X machine in real Mac or Hackintosh or as virtual OS.
- `Install OS X Yosemite.app` downloaded and present in `Applications`
- Windows 8 ISO
- Latest Clover, Clover Configurator, Kext Wizard, Rufus, HFSPlus.efi and FakeSMC.kext (and other kexts based on your machine)

### Downloads:
- [Clover](http://sourceforge.net/projects/cloverefiboot/files/latest/download)
- [Clover Configurator](http://www.hackintoshosx.com/files/file/49-clover-configurator/)
- [Kext Wizard](http://www.hackintoshosx.com/files/file/2136-kext-wizard-3-7-10/)
- [Rufus](https://rufus.akeo.ie/)
- [HFSPlus.efi](https://github.com/JrCs/CloverGrowerPro/raw/master/Files/HFSPlus/X64/HFSPlus.efi)

### Test Clover Config (Optional):
*This is an optional part and only applies to people who already have a hackintosh running. And also for first time users of Clover. Feel free to skip it if it doesn't apply to you.*

Before installing Yosemite/Clover, it's better to test Clover on currently installed Hackintosh. First, it saves all the trouble of post-installation and second, you will be proceeding to install Yosemite once you have confirmed everything is working properly (and no dirty surprises). For this, you do NOT need to install Clover on your current HDD, it may mess up your current installation. Idea is to install Clover on a different HDD(or a test HDD) and without harming current installation.

1. Plug in the 200MB (or more) pen drive. Open disk utility, select this drive, under `Erase` tab choose `Format` as `MS-DOS(FAT)` and give name `CLOVER`(or whatever you want) and hit `Erase`:

    ![Erasing test usb](//i.imgur.com/Bc2948b.png)

2. Go to `Partition` tab, select `1 Partition` in `Partition Layout`, Give name as `CLOVER`, format as `MS-DOS(FAT)`. Click `Options` at the bottom and select `Master Boot Record`. Hit `Apply`.

    ![Partition](//i.imgur.com/sDcdcik.png)
    ![Master Boot Record](//i.imgur.com/9UoOKPK.png)

    Your drive is formatted properly now. It can have Clover installed for test USB drive.

3. Run Clover and change install location to this drive, `CLOVER` and customize by selecting `Bootloader` > `Install boot0ss in MBR`, `CloverEFI` > `CloverEFI 64-bits SATA` and `Drivers64UEFI` > `EmuVariableUefi-64`. Perform installation:

    ![install location](//i.imgur.com/cOtGzUY.png)
    ![boot0ss and SATA](//i.imgur.com/ZPpE5h5.png)
    ![drivers](//i.imgur.com/Otd8odM.png)  

4. Clover is installed to the drive. However you need to copy few more files. You will need `config.plist`, `DSDT.aml` which are specific to your system.

    - Put `config.plist` in `EFI/CLOVER` directory
    - Put `DSDT.aml` in `EFI/CLOVER/ACPI/patched`
    - Put `HFSPlus.efi` in `EFI/CLOVER/drivers64` & `EFI/CLOVER/drivers64UEFI`
    - Delete `VBoxHfs-64.efi` in `EFI/CLOVER/drivers64` & `EFI/CLOVER/drivers64UEFI`
    - Put `FakeSMC.kext` and other kexts required in `EFI/CLOVER/kexts/10.10`

    That's all and your Clover test drive is ready! Now boot using this USB and boot into your Hackintosh. Make sure everything working and once confirmed, proceed next to installation of Yosemite.

### Creating Installation Media:

We will prepare a single USB drive which can be used to install Yosemite, Windows (and even Ubuntu if you fancy!). We have will format this to GPT, create 2 partitions, one for OS X and another for Windows installation files. This drive needs to be more than 16GB so that it can have all three installation files.

1. Erase the USB drive, using Disk Utility. Make 3 partitions for OS X (call it `Yosemite`), Windows (call it `WIN81`) and Ubuntu. Select OS X Partition as `Mac OS Extended Journaled`,  Windows partition as `MS-DOS(FAT)` and Ubuntu partition as `ext4`. (If you don't want Ubuntu, make only two partitions). Make sure you are giving 7GB (or more) for each OS X and Windows installation partitions. Select ‘GPT (GUID Partition Table)’ under `Options`.

    ![partition](//i.imgur.com/BcE2FG5.png)
    ![GUID](//i.imgur.com/lH2FkxY.png)

2. Mount Windows 8 installation ISO and copy Windows 8 installation files to this FAT32 Windows Partition, `WIN81`. 

3. Install Clover into the EFI partition of this USB by targeting the `OSX` partition and customize by selecting `Install Clover in the ESP`, `Bootloader` > `Install boot0ss in MBR`, `CloverEFI` > `CloverEFI 64-bits SATA` and `Drivers64UEFI` > `EmuVariableUefi-64`. Perform installation:

    ![Yosemite drive](//i.imgur.com/7p2hE0w.png)
    ![ESP, boot0ss](//i.imgur.com/7aLwnHZ.png)
    ![drivers etc](//i.imgur.com/Kk0xNm6.png)

    Once clover is installed EFI partition will be mounted automatically. Open it and now you need put few more files. You will need `config.plist`, `DSDT.aml` which are specific to your system.

    - Put `config.plist` in `EFI/CLOVER` directory
    - Put `DSDT.aml` in `EFI/CLOVER/ACPI/patched`
    - Put `HFSPlus.efi` in `EFI/CLOVER/drivers64` & `EFI/CLOVER/drivers64UEFI`
    - Delete `VBoxHfs-64.efi` in `EFI/CLOVER/drivers64` & `EFI/CLOVER/drivers64UEFI`
    - Put `FakeSMC.kext` and other kexts required in `EFI/CLOVER/kexts/10.10`

4. Now we need to copy Yosemite installation file to USB drive. Make sure `/Applications/Install OS X Yosemite.app` exists and run following in terminal:

       sudo /Applications/Install\ OS\ X\ Yosemite.app/Contents/Resources/createinstallmedia --volume /Volumes/Yosemite --applicationpath /Applications/Install\ OS\ X\ Yosemite.app --no interaction

    Above command assumes your partition for OS X installation files is named as `Yosemite`.

Your USB installation drive is ready. This can be used to install both Yosemite and Windows 8. 

### Installation of Yosemite:

We will create appropriate partitions and install Yosemite. 

**NOTE**: The Yosemite Installation section here is very concise and brief. You should actually refer to the thread relevant your machine/laptop. For starters, check [this](http://www.insanelymac.com/forum/topic/298027-guide-aio-guides-for-hackintosh) All In One Guides of Hackintosh. Next, try either [here](http://www.insanelymac.com/forum/forum/137-osx86-installation/) or [here](http://www.insanelymac.com/forum/forum/213-notebooks/). It'd be better if you post all your Yosemite installation doubts in those threads/forums.

1. Boot with USB drive, Clover should be loaded. Click on ‘Install Yosemite from Install Yosemite’.

3. Installation setup should appear. Use Disk Utility from Utilities and format the target drive. Create 2 partitions, for first partition where OS X will be installed, select `Mac OS Extended (Journaled)`. Leave second partition as `Free Space` (and Windows installation will format it properly)

4. Proceed to Yosemite installation. Once done, it will reboot.

5. Boot again using the USB and boot into Clover. Click on ‘Install Yosemite from Install Yosemite’ to complete the installation. 

### Post installation and setup of Clover:

So far I have covered installation of Yosemite. Now post installation, we will install Clover and all required kexts. At the end of this section Yosemite will be ready to use and kicking. 

1. Boot with USB drive, into Clover Menu. Select `Yosemite`(or whatever name you gave), to boot into freshly installed Yosemite

2. Install Clover into the EFI partition of the HDD by targeting the `Yosemite` partition (or whatever you called it) and customize by selecting `Install Clover in the ESP`, `Bootloader` > `Install boot0ss in MBR`, `CloverEFI` > `CloverEFI 64-bits SATA`, `Drivers64UEFI` > `EmuVariableUefi-64`, `Install RC Scripts on target volume` and `Install Clover Preference Pane`. Perform installation:

    ![Yosemite drive](//i.imgur.com/3nLmQKE.png)
    ![ESP, boot0ss](//i.imgur.com/9g6ZuVM.png)
    ![drivers etc](//i.imgur.com/KKUFAqa.png)

3. Once clover is installed, EFI partition will be mounted automatically. Open it and now you need put few more files. You will need `config.plist`, `DSDT.aml` which are specific to your system.

    - Put `config.plist` in `EFI/CLOVER` directory
    - Put `DSDT.aml` in `EFI/CLOVER/ACPI/patched`
    - Put `HFSPlus.efi` in `EFI/CLOVER/drivers64` & `EFI/CLOVER/drivers64UEFI`
    - Delete `VBoxHfs-64.efi` in `EFI/CLOVER/drivers64` & `EFI/CLOVER/drivers64UEFI`
    - Put `FakeSMC.kext` and other kexts required in `EFI/CLOVER/kexts/10.10`

### Installation of Windows 8:

Boot into your machine with HDD's Clover and select `Boot UEFI external from WIN81`, hit spacebar, select and enter `Run bootx64.efi`. It should load into Windows installation. (*image credits: fusion71au*)

![clover bootmenu](//i.imgur.com/essjmDT.png)
![boot windows 8](//i.imgur.com/Ja4W7c1.png)


Proceed Windows installation and complete it. Now you have Windows 8 UEFI on a Legacy BIOS!

### Extras/Troubleshooting (Optional):
1. Sometimes you want to mount EFI partition manually. There are two ways:

    - If you are paranoid using Terminal, download Clover Configurator. It will ask to mount EFI partition when you open it. And you can also mount manually, see the sidebar at left side, under Tools, Mount EFI.
    - By default, all partitions are not visible in Disk Utility. If you enable Debug Menu, you get an option to show all partitions. To enable, run the following in Terminal:

            defaults write com.apple.DiskUtility DUDebugMenuEnabled 1 

    Then you should see an extra Debug Menu in the Disk Utility:

    ![debug menu](//i.imgur.com/emmNXYn.png)

2. If the Windows ISO size is more than 4GB, then most probably `/source/install.wim` size will be more than 4GB and copying it to FAT partition will fail. For this we have to split this file. 

   - Boot into Windows 8, create a new directory called `wim` in `C:\` drive. Copy `install.wim` to `C:\wim` directory.
   - Open command prompt in admin mode and run following:

         Dism /Split-Image /ImageFile:c:\wim\install.wim /SWMFile:c:\wim\install.swm /FileSize:3500

   - You should now see two files in `C:\wim` directory.
   - Replace `install.wim` by these two files. 

   Now you can copy Windows installation ISO files to FAT partition of the USB.

3. When you want to install Windows, in Clover menu, if nothing happens when you click on Windows Installation in clover, then you have to copy `bootmgfw.efi` into `WIN81/efi/microsoft/boot`

   - Use 7-zip in Windows, open `install.wim` navigate to `sources/install.wim/1/Windows/Boot/EFI/bootmgfw.efi` and extract `bootmgfw.efi` (you don't need to extract this big ass file)
   - Rename `cdboot.efi` in `WIN81/efi/microsoft/boot` directory to `cdboot.BAK`
   - Copy `bootmgfw.efi` into `WIN81/efi/microsoft/boot`

   Now boot again with this drive. This time select `Run bootmgfw.efi` in options (as opposed to `Run bootx64.efi`), now it should boot fine into Windows 8 installation.

4. Even after following above advice, still Windows installation gives some error, then prepare Windows 8 installation media on a separate USB drive using Rufus. You can find instructions [here](http://www.eightforums.com/tutorials/15458-uefi-bootable-usb-flash-drive-create-windows.html). Use this USB drive instead and perform installation.

5. In Clover installations, you do NOT need to install `Drivers64UEFI` > `EmuVariableUefi-64`, it's not necessary for legacy BIOS. However my setup wouldn't work without it and I have no idea why. Since it does not affect the installation, I have included it anyway.

6. Instead of `CloverEFI 64-bits SATA`, you could try installing `CloverEFI 64-bits BiosBlockIO` to speed up boot. However it may not work on few machines. So make sure you have test USB drive handy (first section of this tutorial).

7. Disk partitioning guides: How to convert a Hybrid MBR drive to GPT and How to Convert MBR Windows to UEFI Windows Without Reinstalling - [link](http://www.insanelymac.com/forum/topic/298027-guide-aio-guides-for-hackintosh/page-18#entry2098111).

### Sources:

1. Following posts immensely helped me and you should probably read them if you want to learn more: [1](http://www.insanelymac.com/forum/topic/303149-os-x-installation-on-separate-hdd-and-windows-on-another/), [2](http://www.insanelymac.com/forum/topic/190780-guide-making-a-dsdtaml-for-dell-xps-m1330-xps-m1530-and-xps-m1730/page-81#entry1977838), [3](http://www.insanelymac.com/forum/topic/190780-guide-making-a-dsdtaml-for-dell-xps-m1330-xps-m1530-and-xps-m1730/page-81#entry1978003), [4](http://www.insanelymac.com/forum/topic/190780-guide-making-a-dsdtaml-for-dell-xps-m1330-xps-m1530-and-xps-m1730/page-81#entry1979105), [5](http://www.insanelymac.com/forum/topic/293574-beginners-guide-to-uefi-tripledual-boot-os-x-windows-and-linux-kali-on-an-single-true-gpt-ssd/page-4#entry1992190), [6](http://www.insanelymac.com/forum/topic/293574-beginners-guide-to-uefi-tripledual-boot-os-x-windows-and-linux-kali-on-an-single-true-gpt-ssd/page-4#entry1992190).
2. Why GPT/UEFI? [1](http://www.insanelymac.com/forum/topic/298027-guide-aio-guides-for-hackintosh/page-18#entry2097821), [2](https://wiki.manjaro.org/index.php?title=Some_basics_of_MBR_v/s_GPT_and_BIOS_v/s_UEFI#MBR_vs._GPT), [3](http://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface#Advantages), [4](http://technet.microsoft.com/en-us/library/dn336946.aspx).
3. BiosBlockIO to speedup! - [1](http://www.insanelymac.com/forum/topic/284656-clover-general-discussion/page-239#entry2033327), [2](http://clover-wiki.zetam.org/Installation#Using-the-installer).
4. [Clover Wiki](http://clover-wiki.zetam.org/Home). 
5. [Clover Instructions](http://www.insanelymac.com/forum/topic/282787-clover-v2-instructions/).
6. [Sample Configurations](http://www.insanelymac.com/forum/topic/295549-clover-config/).