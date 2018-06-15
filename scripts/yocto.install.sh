cd
git clone git://git.yoctoproject.org/poky
git checkout tags/yocto-2.4.1 -b poky_2.4.1
cd ~/poky
git checkout -b rocko origin/rocko
source oe-init-build-env
