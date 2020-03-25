#!/usr/bin/python
import time

#zabbix版本
version = '4.0'

#创建时间
date = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.localtime())

#group
group = 'Templates/IPMI'

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

unit_trigger_lower1 = {}
unit_trigger_higher1 = {}
unit_trigger_lower1['°C'] = '温度低'
unit_trigger_lower1['Volts'] = '电压低'
unit_trigger_lower1['RPM'] = '转速低'
unit_trigger_higher1['°C'] = '温度高'
unit_trigger_higher1['Volts'] = '电压高'
unit_trigger_higher1['RPM'] = '转速高'

unit_trigger_lower2 = {}
unit_trigger_higher2 = {}
unit_trigger_lower2['°C'] = '温度较低'
unit_trigger_lower2['Volts'] = '电压较低'
unit_trigger_lower2['RPM'] = '转速较低'
unit_trigger_higher2['°C'] = '温度较高'
unit_trigger_higher2['Volts'] = '电压较高'
unit_trigger_higher2['RPM'] = '转速较高'

unit_trigger_lower3 = {}
unit_trigger_higher3 = {}
unit_trigger_lower3['°C'] = '温度过低'
unit_trigger_lower3['Volts'] = '电压过低'
unit_trigger_lower3['RPM'] = '转速过低'
unit_trigger_higher3['°C'] = '温度过高'
unit_trigger_higher3['Volts'] = '电压过高'
unit_trigger_higher3['RPM'] = '转速过高'
