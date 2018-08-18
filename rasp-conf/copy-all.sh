route=/media/arturo/b0ea1ea9-a0b3-4227-a579-cec125f2c2db
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
cp ../python/main/sense_hat_data.py $route/home/root
cp ../python/main/wearable_app.py $route/home/root