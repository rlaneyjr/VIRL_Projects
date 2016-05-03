#!/bin/bash
# create-cumulus-vx-image.sh
# HS-Fulda - sebastian.rieger@informatik.hs-fulda.de
#
# changelog:
#
# V0.2    added support to delete existing image with the same name and generating the default nova flavor
# V0.3    checking whether it is safe to unmount the working directory
# V0.31   added support for newer glance releases (e.g. kilo) used in VIRL 1.0.0

# usage
if [ ! $# -eq 2 ] ; then
  echo -e "usage: $0 <CumulusVX.qcow2> <new glance image name>, e.g.:\n"
  echo "$0 CumulusVX-2.5.3-f3df86c478e1a4ef.qcow2 CumulusVX"
  exit -1
fi

# sudo check
if [ ! $UID -eq 0 ] ; then
  echo "Insufficient privileges. Please consider using sudo -s."
  exit -1
fi

CUMULUS_QCOW2=$1
CUMULUS_QCOW2_BASENAME=$(basename -s .qcow2 $1)
CUMULUS_PATCHED_QCOW2=$1-patched.qcow2
GLANCE_IMAGE_NAME=$2
GLANCE_IMAGE_RELEASE=$CUMULUS_QCOW2_BASENAME
TMP_NAME="CumulusVX-$GLANCE_IMAGE_RELEASE"
TIMESTAMP=$(date +%Y%m%d%H%M%S)

function safe_unmount() {
  echo -n "Unmounting $1..."
  RETRY=0
  until umount $1 &>/dev/null
  do
    echo -n "."
    sleep 1
    RETRY=$((RETRY+1))
    if [ "$RETRY" -ge "5" ] ; then
      echo
      echo "ERROR: unable to unmount working directory $1"
      exit 1
    fi
  done
  echo
  return 0
}

# check for an existing image with the same name and offer to delete it prior to creating a new one
CHECK_FOR_EXISTING_IMAGE=$(glance image-show $GLANCE_IMAGE_NAME 2>&1)
if [ $? == 0 ] ; then
  glance image-show $GLANCE_IMAGE_NAME
  echo
  echo
  read -r -p "There is already an image with the same name in glance. Do you want to overwrite it? [y/N] " RESPONSE
  if [[ $RESPONSE =~ ^([yY][eE][sS]|[yY])$ ]] ; then
    echo "Deleting existing image $GLANCE_IMAGE_NAME..."
    echo "==========================================================="

    glance image-delete $GLANCE_IMAGE_NAME
  else
    echo "An image with the same name already exists. Either delete this image or choose another name."
    exit 1
  fi
fi

echo
echo "Creating CumulusVX image..."
echo "==========================================================="

qemu-img convert -O raw $CUMULUS_QCOW2 $CUMULUS_QCOW2_BASENAME.raw
LOOPDEV=$(kpartx -av $CUMULUS_QCOW2_BASENAME.raw)
LOOPDEV_PART1=$(echo "$LOOPDEV" | sed '1q;d' | cut -d " " -f 3)
LOOPDEV_PART2=$(echo "$LOOPDEV" | sed '2q;d' | cut -d " " -f 3)

mkdir cumulusvx-boot-$TIMESTAMP
mkdir cumulusvx-root-$TIMESTAMP

echo
echo "Injecting changes to use serial console and startup script to get switch config..."
echo "=================================================================================="

mount /dev/mapper/$LOOPDEV_PART1 cumulusvx-boot-$TIMESTAMP
mount /dev/mapper/$LOOPDEV_PART2 cumulusvx-root-$TIMESTAMP
# changing grub and inittab to use a serial console on kernel command line
sed -i.bak -e s/"linux \/bzImage root=\/dev\/sda2"/"linux \/bzImage root=\/dev\/sda2 console=ttyS0 console=tty0"/g cumulusvx-root-$TIMESTAMP/vbox_grub.cfg
sed -i.bak -e s/"linux \/bzImage root=\/dev\/sda2"/"linux \/bzImage root=\/dev\/sda2 console=ttyS0 console=tty0"/g cumulusvx-boot-$TIMESTAMP/grub/grub.cfg
sed -i.bak -e s/"# S0:3:respawn:\/sbin\/getty -L \$(get-cmdline-console) vt100"/"S0:3:respawn:\/sbin\/getty -L \$(get-cmdline-console) vt100"/g cumulusvx-root-$TIMESTAMP/etc/inittab
# append a script to import the configuration defined in VM Maestro to rc.local
sed -i.bak -e s/"^exit 0$"/""/g cumulusvx-root-$TIMESTAMP/etc/rc.local
cat << EOF >> cumulusvx-root-$TIMESTAMP/etc/rc.local
mkdir /virl-config
mount /dev/sdb1 /virl-config
chmod +x /virl-config/cumulusvx.sh
/virl-config/cumulusvx.sh >/var/log/virl-startup.log
EOF

#DEBUG:
#  run bash to allow manual changes to the image before packing
#
#bash

safe_unmount cumulusvx-boot-$TIMESTAMP
safe_unmount cumulusvx-root-$TIMESTAMP

rm -rf cumulusvx-boot-$TIMESTAMP
rm -rf cumulusvx-root-$TIMESTAMP
kpartx -d $CUMULUS_QCOW2_BASENAME.raw

echo
echo "Saving CumulusVX image..."
echo "==========================================================="

qemu-img convert -O qcow2 $CUMULUS_QCOW2_BASENAME.raw $CUMULUS_PATCHED_QCOW2

# use e1000 for now as with virtio we get dhcp errors due to "bad udp checksum" in Debian
glance image-create --container-format bare --disk-format qcow2 --visibility public --name $GLANCE_IMAGE_NAME \
  --file $CUMULUS_PATCHED_QCOW2 --property hw_disk_bus=ide --property serial=1 \
  --property hw_vif_model=e1000 --property hw_cdrom_type=ide --property release="$GLANCE_IMAGE_RELEASE" --property subtype=CumulusVX --property config_disk_type=disk

# create default flavor
CHECKING_FOR_EXISTING_FLAVOR=$(nova flavor-show CumulusVX.small 2>&1)
if [ $? == 1 ]; then
  echo "Creating default flavor CumulusVX.small..."
  echo "==========================================================="

  nova flavor-create --is-public true CumulusVX.small auto 256 0 1
fi
      
echo
echo "Cleaning up..."
echo "==========================================================="

rm $CUMULUS_QCOW2_BASENAME.raw
