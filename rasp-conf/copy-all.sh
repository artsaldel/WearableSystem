route=/media/arturo/ca9d85c9-4d09-4716-8044-b0373e0475fc
cp 99-i2c.rules $route/etc/udev/rules.d
cp config.txt $route/boot
cp inittab $route/etc
cp interfaces $route/etc/network
cp modules $route/etc
cp wpa_supplicant.conf $route/etc
cp start-wearable.sh $route/etc/init.d
cp ../python/blescan/blescan.py $route/home/root
cp ../python/blescan/scan-beacon.py $route/home/root
cp ../python/sense-hat/leds-ok.py $route/home/root