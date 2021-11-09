
# Raspberry Pi Setup Playbook

## Usage

### Create SD card & Wifi setup

1. (Optional) Create vars.yml
    1. `cp vars.template.yml vars.yml`
    2. Rewrite the necessary variables in the file. (Variables not defined in this file will be entered interactively.)
    3. `make encrypt-vars`
2. Insert SD card and create (on macOS or Raspberry PI)
    - `make create-sd`
3. Insert the SD card into the Raspberry Pi and connect it with an ethernet cable.
4. Configure
    - `make configure`
5. Set a static IP address
6. Set ~/.ssh/config
7. Provisioning
    - `make setup-dev`
    - `make setup-timelapse`
    - `make setup-epaper`

## Logs

<details><summary>make create-sd</summary>

```
$ make create-sd
ansible-playbook -i hosts create-sd.yml --ask-become-pass
BECOME password:

PLAY [localhost] *****************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************
[WARNING]: Platform darwin on host localhost is using the discovered Python interpreter at /usr/bin/python, but future installation of another Python
interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-core/2.11/reference_appendices/interpreter_discovery.html for
more information.
ok: [localhost]

TASK [create-sd/download-os-image : Download image] ******************************************************************************************************
ok: [localhost]

TASK [create-sd/download-os-image : Unzip] ***************************************************************************************************************
ok: [localhost]

TASK [create-sd/create : Diskutil list] ******************************************************************************************************************
changed: [localhost]

TASK [create-sd/create : Show diskutil list] *************************************************************************************************************
ok: [localhost] => {
    "diskutil_list.stdout_lines": [
        ...
        "/dev/disk2 (external, physical):",
        "   #:                       TYPE NAME                    SIZE       IDENTIFIER",
        "   0:     FDisk_partition_scheme                        *32.0 GB    disk2",
        "   1:             Windows_FAT_32 ⁨boot⁩                    268.4 MB   disk2s1",
        "   2:                      Linux ⁨⁩                        31.7 GB    disk2s2"
    ]
}

TASK [create-sd/create : disk_number] ********************************************************************************************************************
[create-sd/create : disk_number]
Enter the disk number:
2^Mok: [localhost]

TASK [create-sd/create : Format] *************************************************************************************************************************
changed: [localhost]

TASK [create-sd/create : Unmount] ************************************************************************************************************************
changed: [localhost]

TASK [create-sd/create : Flash] **************************************************************************************************************************
changed: [localhost]

TASK [create-sd/create : Eject] **************************************************************************************************************************
changed: [localhost]

TASK [create-sd/create : Mount] **************************************************************************************************************************
[create-sd/create : Mount]
Re-insert the SD card and press Enter:
^Mok: [localhost]

TASK [create-sd/create : Enable SSH] *********************************************************************************************************************
changed: [localhost]

TASK [create-sd/create : Eject] **************************************************************************************************************************
changed: [localhost]

PLAY RECAP ***********************************************************************************************************************************************
localhost                  : ok=13   changed=7    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
</details>

<details><summary>make configure</summary>

```
$ make configure
ansible-playbook -i hosts configure.yml --extra-vars "@vars.yml" --ask-vault-pass
Vault password:
Hostname: pi3a

PLAY [raspberrypi] ***************************************************************************************************************************************

TASK [configure/rfkill : Copy rfkill-unblock-wifi.service] ***********************************************************************************************
[DEPRECATION WARNING]: Distribution debian 10.9 on host raspberrypi.local should use /usr/bin/python3, but is using /usr/bin/python for backward
compatibility with prior Ansible releases. A future Ansible release will default to using the discovered platform python for this host. See
https://docs.ansible.com/ansible-core/2.11/reference_appendices/interpreter_discovery.html for more information. This feature will be removed in version
2.12. Deprecation warnings can be disabled by setting deprecation_warnings=False in ansible.cfg.
changed: [raspberrypi.local]

TASK [configure/rfkill : Daemon reload] ******************************************************************************************************************
ok: [raspberrypi.local]

TASK [configure/rfkill : Service enable] *****************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/rfkill : Service start] ******************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/wpa : Generate WPA supplicant config] ****************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/wpa : Edit wpa_supplicant.conf] **********************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/wpa : WPA reconfigure] *******************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/wpa : Reboot] ****************************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/timesyncd : Edit /etc/systemd/timesyncd.conf] ********************************************************************************************
changed: [raspberrypi.local] => (item={'regexp': '^#NTP=', 'line': 'NTP=ntp.jst.mfeed.ad.jp ntp.nict.jp'})
changed: [raspberrypi.local] => (item={'regexp': '^#FallbackNTP=', 'line': 'FallbackNTP=time.google.com'})

TASK [configure/timesyncd : timedatectl set-ntp true] ****************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/timesyncd : Daemon reload] ***************************************************************************************************************
ok: [raspberrypi.local]

TASK [configure/timesyncd : Service restart] *************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/apt : Update] ****************************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/apt : Upgrade] ***************************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/apt : Upgrade dist] **********************************************************************************************************************
ok: [raspberrypi.local]

TASK [configure/python : Unlink python2 and link python3] ************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/python : Install pip] ********************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/python : Link pip3] **********************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/raspi-config : hostname] *****************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/raspi-config : timezone] *****************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/raspi-config : locale] *******************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/password : chpasswd] *********************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/ifconfig : command] **********************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/ifconfig : Show ifconfig] ****************************************************************************************************************
ok: [raspberrypi.local] => {
    "interface_config.stdout_lines": [
        ...
    ]
}

TASK [configure/sshd : Add authorized_key] ***************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/sshd : Edit /etc/ssh/sshd_config] ********************************************************************************************************
changed: [raspberrypi.local] => (item={'regexp': '^#PermitRootLogin.*$', 'line': 'PermitRootLogin no'})
changed: [raspberrypi.local] => (item={'regexp': '^#PubkeyAuthentication.*$', 'line': 'PubkeyAuthentication yes'})
changed: [raspberrypi.local] => (item={'regexp': '^#PasswordAuthentication.*$', 'line': 'PasswordAuthentication no'})

TASK [configure/sshd : Service restart] ******************************************************************************************************************
changed: [raspberrypi.local]

TASK [configure/reboot-exit : Reboot] ********************************************************************************************************************
fatal: [raspberrypi.local]: FAILED! => {"msg": "Failed to connect to the host via ssh: ssh: Could not resolve hostname raspberrypi.local: nodename nor servname provided, or not known"}

PLAY RECAP ***********************************************************************************************************************************************
raspberrypi.local          : ok=27   changed=23   unreachable=0    failed=1    skipped=0    rescued=0    ignored=0

make: *** [configure] Error 2
```
</details>

<details><summary>make setup-dev</summary>

```
$ make setup-dev
ansible-playbook -i hosts setup-dev.yml

PLAY [targets] *****************************************************************************************************************************************

TASK [dev/tools : Install tools] ***********************************************************************************************************************
changed: [pi3a]

TASK [dev/dotfiles : Clone dotfiles] *******************************************************************************************************************
changed: [pi3a]

TASK [dev/dotfiles : Change shell] *********************************************************************************************************************
changed: [pi3a]

TASK [dev/dotfiles : Write config file] ****************************************************************************************************************
changed: [pi3a]

PLAY RECAP *********************************************************************************************************************************************
pi3a                       : ok=4    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
</details>

<details><summary>make setup-timelapse</summary>

```
$ make setup-timelapse
ansible-playbook -i hosts setup-timelapse.yml --extra-vars "@vars.yml" --ask-vault-pass
Vault password:

PLAY [targets] ***********************************************************************************************

TASK [configure/enable-camera : Enable camera] ***************************************************************
changed: [pi3a]

TASK [configure/samba-client : Install samba-client, cifs-utils] *********************************************
ok: [pi3a]

TASK [configure/samba-client : Creates mount directory] ******************************************************
ok: [pi3a]

TASK [configure/samba-client : Edit /etc/fstab] **************************************************************
ok: [pi3a]

TASK [configure/reboot : Reboot] *****************************************************************************
changed: [pi3a]

TASK [dev/picamera : Install picamera] ***********************************************************************
ok: [pi3a]

TASK [dev/opencv-python : Install dependencies] **************************************************************
ok: [pi3a]

TASK [dev/opencv-python : Install opencv-contrib-python] *****************************************************
ok: [pi3a]

TASK [utility/timelapse : Copy timelapse.service] ************************************************************
ok: [pi3a]

TASK [utility/timelapse : Creates mount directory] ***********************************************************
ok: [pi3a]

TASK [utility/timelapse : touch /etc/sysconfig/pi] ***********************************************************
changed: [pi3a]

TASK [utility/timelapse : Set env] ***************************************************************************
changed: [pi3a]

TASK [utility/timelapse : Creates directory] *****************************************************************
changed: [pi3a]

TASK [utility/timelapse : Copy timelapse.py] *****************************************************************
changed: [pi3a]

TASK [utility/timelapse : Creates work directory] ************************************************************
ok: [pi3a]

TASK [utility/timelapse : Create a symbolic link for work directory] *****************************************
changed: [pi3a]

TASK [utility/timelapse : Daemon reload] *********************************************************************
ok: [pi3a]

TASK [utility/timelapse : Service enable] ********************************************************************
changed: [pi3a]

TASK [utility/timelapse : Service start] *********************************************************************
changed: [pi3a]

PLAY RECAP ***************************************************************************************************
pi3a                       : ok=19   changed=9    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
</details>

<details><summary>make setup-epaper</summary>

```
```
</details>