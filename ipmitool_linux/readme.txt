解压
tar -zxvf ipmitool-1.8.13.tar.gz

需要gcc环境，离线安装包略

编译
cd ipmitool-1.8.13
./configure
sudo make
sudo make install

获取数据
ipmitool -I lanplus -H xxx.xxx.xxx.xxx -U xxx -P xxx -L user sensor list


当以上命令报错：
Error loading interface lanplus
指令修改为：ipmitool -I lan -H xxx.xxx.xxx.xxx -U xxx -P xxx -L user sensor list