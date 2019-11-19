#!/usr/bin/python
#命令输入格式 py ipmiToTemp.py  ipmi数据文件名  模板可见名称
#示例：python ipmiToTemp.py  "ipmi_demo.txt" "IPMI#TEST.xml"
#模板可见名称  建议 IPMI#设备厂商及型号，生成的模板名称将#替换成空格 。
#zabbix 版本4.0，其它版本模板格式可能不匹配
import sys
import time
import xml_module
import data
import os

units = {}

alarm_lower1 = {}
alarm_lower2 = {}
alarm_lower3 = {}
alarm_higher1 = {}
alarm_higher2 = {}
alarm_higher3 = {}    

'''
读取文件
文件内容为ipmitool获取到的数据
filename:读取的文件名，不加路径
'''
def read_file(filename):
    input = open(filename, 'r')
    for line in input:
        line = line.replace('\n','')
        line_list = line.split('|')

        line_list[0] = line_list[0].strip()
        line_list[2] = line_list[2].strip()
        #检测有效数据
        if 'ok' in line_list[3]:

            #替换单位值
            if line_list[2] in data.unit_trans.keys(): #if unit_trans.has_key(line_list[2]) 2.2之前？
                units[line_list[0]]=data.unit_trans[line_list[2]]
            else:
                units[line_list[0]]=line_list[2]

            if line_list[6].strip()!='na':
                alarm_lower1[line_list[0]]=line_list[6].strip()
            if line_list[5].strip()!='na':
                alarm_lower2[line_list[0]]=line_list[5].strip()
            if line_list[4].strip()!='na':
                alarm_lower3[line_list[0]]=line_list[4].strip()
            if line_list[7].strip()!='na':
                alarm_higher1[line_list[0]]=line_list[7].strip()
            if line_list[8].strip()!='na':
                alarm_higher2[line_list[0]]=line_list[8].strip()
            if line_list[9].strip()!='na':
                alarm_higher3[line_list[0]]=line_list[9].strip()
            
            
            
            

'''
产生xml 文本
xml_name 默认和模板可见名称一致
'''
def generate_xml(xml_name):
    xml_name = xml_name.replace('.xml','')
    header = xml_module.generate_header(xml_name)
    applications = xml_module.generate_applications(units)
    items = xml_module.generate_items(units)
    triggers = xml_module.generate_triggers(units,alarm_lower1,alarm_lower2,alarm_lower3,alarm_higher1,alarm_higher2,alarm_higher3)

    return '\n'.join([header,applications,items,triggers])

'''
生成模板文件
filename为模板文件名，加不加'.xml'均可
template为要写入文件的模板内容
'''
def generate_file(filename,template):
    file = open(os.getcwd()+'\\'+filename.replace('.xml','')+'.xml','w',encoding = 'utf-8')
    file.write(template)
    file.close()


if __name__ == '__main__':
    data_file = sys.argv[1]
    filename = sys.argv[2]

    read_file(data_file)
    # read_file('c:/Users/kdgz/Desktop/ipmi-py/ipmi_demo.txt')


    # template = generate_xml('text.xml')
    template = generate_xml(filename)


    # generate_file(sys.argv[2],template)
    generate_file(filename, template)



    print(units)
    print(alarm_lower1)
    print(alarm_lower2)
    print(alarm_lower3)
    print(alarm_higher1)
    print(alarm_higher2)
    print(alarm_higher3)



