sudo apt-get install build-essential
sudo apt-get install libreadline5-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tgz
tar -xvf Python-2.7.3.tgz && cd Python-2.7.3/
./configure --prefix=/usr
make
sudo make install