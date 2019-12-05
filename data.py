#!/usr/bin/python
import time

#zabbix版本
version = '4.0'

#创建时间
date = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime())

#group
group = 'ipmi'

#默认模板名称，当可见名称不按规则来无法解析时用
default_temp_name = 'IPMI Template'

#更新间隔
delay = '60'
#历史数据保留时长
history = '90d'
#趋势存储时间
trends = '365d'


#需要替换的单位列表，如 degreesC 替换成 °C
unit_trans = {}
unit_trans['degrees C'] = '°C'

#单位代表的应用集，不在此内的归于Other集
unit_applications = {}
unit_applications['°C'] = 'Temperature'
unit_applications['Watts'] = 'Power Supply'
unit_applications['Volts'] = 'Voltage'
unit_applications['RPM'] = 'Fans'
application_other = 'Other'

unit_trigger_lower = {}
unit_trigger_higher = {}
unit_trigger_lower['°C'] = '温度过低'
unit_trigger_lower['Volts'] = '电压过低'
unit_trigger_lower['RPM'] = '转速过低'
unit_trigger_higher['°C'] = '温度过高'
unit_trigger_higher['Volts'] = '电压过高'
unit_trigger_higher['RPM'] = '转速过高'

