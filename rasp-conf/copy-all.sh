route=/media/arturo/rpi
cp 99-i2c.rules $route/etc/udev/rules.d
cp config.txt $route/boot
cp inittab $route/etc
cp interfaces $route/etc/network
cp modules $route/etc
cp wpa_supplicant.conf $route/etc
cp ntp.drift $route/var/lib/ntp
cp start-wearable.sh $route/etc/init.d
cp ../python/rpi/* $route/home/root