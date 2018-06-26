bitbake -c menuconfig virtual/kernel
bitbake -c cleanall rpi-basic-image
bitbake -c clean rpi-basic-image
bitbake rpi-basic-image
