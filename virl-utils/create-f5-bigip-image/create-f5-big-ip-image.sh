#!/bin/bash
# create-f5-big-ip-image.sh
# HS-Fulda - sebastian.rieger@informatik.hs-fulda.de
#
# changelog:
#
# V0.1    initial version

# usage
if [ ! $# -eq 2 ] ; then
  echo -e "usage: $0 <BIGIP-12.0.0.0.0.606.qcow2> <new glance image name>, e.g.:\n"
  echo "$0 BIGIP-12.0.0.0.0.606.qcow2 F5-BIGIP"
  exit -1
fi

# sudo check
if [ ! $UID -eq 0 ] ; then
  echo "Insufficient privileges. Please consider using sudo -s."
  exit -1
fi

BIGIP_QCOW2=$1
BIGIP_QCOW2_BASENAME=$(basename -s .qcow2 $1)
BIGIP_PATCHED_QCOW2=$1-patched.qcow2
GLANCE_IMAGE_NAME=$2
GLANCE_IMAGE_RELEASE=$BIGIP_QCOW2_BASENAME
TMP_NAME="BIGIP-$GLANCE_IMAGE_RELEASE"
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
echo "Creating F5 BIGIP image..."
echo "==========================================================="

qemu-img convert -O raw $BIGIP_QCOW2 $BIGIP_QCOW2_BASENAME.raw
LOOPDEV=$(kpartx -av $BIGIP_QCOW2_BASENAME.raw)
LOOPDEV_PART1=$(echo "$LOOPDEV" | sed '1q;d' | cut -d " " -f 3)
LOOPDEV_PART2=$(echo "$LOOPDEV" | sed '2q;d' | cut -d " " -f 3)
LOOPDEV_PART3=$(echo "$LOOPDEV" | sed '3q;d' | cut -d " " -f 3)

mkdir bigip-part1-boot-$TIMESTAMP
# part2 is swap
#mkdir bigip-part3-lvm-dat.log.1-$TIMESTAMP
#mkdir bigip-part3-lvm-dat.maint.1-$TIMESTAMP
#mkdir bigip-part3-lvm-dat.share.1-$TIMESTAMP
#mkdir bigip-part3-lvm-dat.swapvol.1-$TIMESTAMP
mkdir bigip-part3-lvm-set.1._config-$TIMESTAMP
#mkdir bigip-part3-lvm-set.1._usr-$TIMESTAMP
#mkdir bigip-part3-lvm-set.1._var-$TIMESTAMP
#mkdir bigip-part3-lvm-set.1.root-$TIMESTAMP

echo
echo "Injecting changes to use serial console and startup script to get config..."
echo "=================================================================================="

mount /dev/mapper/$LOOPDEV_PART1 bigip-part1-boot-$TIMESTAMP
# scan for new lvm volumes in part3
pvscan
# activate the new volume groups
vgchange -ay
mount /dev/mapper/vg--db--hda-set.1._config bigip-part3-lvm-set.1._config-$TIMESTAMP

## change grub to add kernel config console=ttyS0
sed -i.bak -e s/"^splashimage="/"#splashimage="/g bigip-part1-boot-$TIMESTAMP/grub/grub.conf
sed -i.bak -e s/"^timeout=8"/"timeout=8\nserial --unit=0 --speed=115200\nterminal --timeout=2 serial console"/g bigip-part1-boot-$TIMESTAMP/grub/grub.conf
sed -i.bak -e s/"default_cpu_order   quiet"/"default_cpu_order   quiet console=ttyS0"/g bigip-part1-boot-$TIMESTAMP/grub/grub.conf

## append call to userscript in /config/startup
cat << EOF >> bigip-part3-lvm-set.1._config-$TIMESTAMP/startup
mkdir /virl-config
mount /dev/hdd1 /virl-config
chmod +x /virl-config/bigip-config.sh
/virl-config/bigip-config.sh >/var/log/virl-startup.log
EOF

#DEBUG:
#  run bash to allow manual changes to the image before packing
#
#bash

safe_unmount bigip-part1-boot-$TIMESTAMP
#part2 is swap
#safe_unmount bigip-part3-lvm-dat.log.1-$TIMESTAMP
#safe_unmount bigip-part3-lvm-dat.maint.1-$TIMESTAMP
#safe_unmount bigip-part3-lvm-dat.share.1-$TIMESTAMP
#safe_unmount bigip-part3-lvm-dat.swapvol.1-$TIMESTAMP
safe_unmount bigip-part3-lvm-set.1._config-$TIMESTAMP
#safe_unmount bigip-part3-lvm-set.1._usr-$TIMESTAMP
#safe_unmount bigip-part3-lvm-set.1._var-$TIMESTAMP
#safe_unmount bigip-part3-lvm-set.1.root-$TIMESTAMP

rm -rf bigip-part1-boot-$TIMESTAMP
#part2 is swap
#rm -rf bigip-part3-lvm-dat.log.1-$TIMESTAMP
#rm -rf bigip-part3-lvm-dat.maint.1-$TIMESTAMP
#rm -rf bigip-part3-lvm-dat.share.1-$TIMESTAMP
#rm -rf bigip-part3-lvm-dat.swapvol.1-$TIMESTAMP
rm -rf bigip-part3-lvm-set.1._config-$TIMESTAMP
#rm -rf bigip-part3-lvm-set.1._usr-$TIMESTAMP
#rm -rf bigip-part3-lvm-set.1._var-$TIMESTAMP
#rm -rf bigip-part3-lvm-set.1.root-$TIMESTAMP

# deactive part3 volume groups
vgchange -an
kpartx -d $BIGIP_QCOW2_BASENAME.raw

echo
echo "Saving F5 BIGIP image..."
echo "==========================================================="

qemu-img convert -O qcow2 $BIGIP_QCOW2_BASENAME.raw $BIGIP_PATCHED_QCOW2

# use recommendations from https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-ve-kvm-setup-11-3-0/2.html#r_ve_vmware_1022_esx_mach_reqs
glance image-create --container-format bare --disk-format qcow2 --visibility public --name $GLANCE_IMAGE_NAME \
  --file $BIGIP_PATCHED_QCOW2 --property hw_disk_bus=virtio --property serial=1 \
  --property hw_vif_model=virtio --property hw_cdrom_type=ide --property release="$GLANCE_IMAGE_RELEASE" --property subtype=F5-BIGIP --property config_disk_type=disk

# create default flavor
CHECKING_FOR_EXISTING_FLAVOR=$(nova flavor-show F5-BIGIP.small 2>&1)
if [ $? == 1 ]; then
  echo "Creating default flavor F5-BIGIP.small..."
  echo "==========================================================="

  nova flavor-create --is-public true F5-BIGIP.small auto 4096 0 2
fi

echo
echo "Cleaning up..."
echo "==========================================================="

rm $BIGIP_QCOW2_BASENAME.raw
