route=/media/arturo/df74d677-c894-4a19-a261-b94e05146ef8
cp 99-i2c.rules $route/etc/udev/rules.d
cp config.txt $route/boot
cp inittab $route/etc
cp interfaces $route/etc/network
cp modules $route/etc
cp wpa_supplicant.conf $route/etc
cp start-wearable.sh $route/etc/init.d

cp ../python/sense-hat/leds-error.py $route/home/root
cp ../python/rpi/* $route/home/root