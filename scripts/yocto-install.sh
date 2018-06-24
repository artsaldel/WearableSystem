cd
git clone -b rocko git://git.yoctoproject.org/poky.git poky-rocko
cd poky-rocko
git clone -b rocko git://git.openembedded.org/meta-openembedded
git clone -b rocko https://github.com/meta-qt5/meta-qt5
git clone -b rocko git://git.yoctoproject.org/meta-security
git clone -b rocko git://git.yoctoproject.org/meta-raspberrypi
mkdir rpi
git clone -b rocko git://github.com/jumpnow/meta-rpi