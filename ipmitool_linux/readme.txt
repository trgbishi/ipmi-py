解压
tar -zxvf ipmitool-1.8.13.tar.gz

编译
cd ipmitool-1.8.13
./configure
sudo make
sudo make install

获取数据
ipmitool -I lanplus -H xxx.xxx.xxx.xxx -U xxx -P xxx -L user sensor list