route=/media/arturo/c5ab9b60-a104-4a8b-b6f2-9cdc6f75f780
cp 99-i2c.rules $route/etc/udev/rules.d
cp config.txt $route/boot
cp inittab $route/etc
cp interfaces $route/etc/network
cp modules $route/etc
cp wpa_supplicant.conf $route/etc
cp start-wearable.sh $route/etc/init.d
cp ../python/rpi/* $route/home/root