route=/media/arturo/2e3a42bb-d529-44ae-b93f-bea240bbe1b0
cp 99-i2c.rules $route/etc/udev/rules.d
cp config.txt $route/boot
cp inittab $route/etc
cp interfaces $route/etc/network
cp modules $route/etc
cp wpa_supplicant.conf $route/etc
cp start-wearable.sh $route/etc/init.d
cp ../python/rpi/* $route/home/root