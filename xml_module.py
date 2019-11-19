#!/usr/bin/python
import data

'''
生成模板的头部说明内容
'''
def generate_header(template_name):
    header ='<?xml version="1.0" encoding="UTF-8"?>\n'\
            '<zabbix_export>\n'\
            '    <version>{0}</version>\n'\
            '    <date>{1}</date>\n'\
            '    <groups>\n'\
            '        <group>\n'\
            '            <name>{2}</name>\n'\
            '        </group>\n'\
            '    </groups>\n'\
            '    <templates>\n'\
            '        <template>\n'\
            '            <template>{3}</template>\n'\
            '            <name>{4}</name>\n'\
            '            <description/>\n'\
            '            <groups>\n'\
            '                <group>\n'\
            '                    <name>{5}</name>\n'\
            '                </group>\n'\
            '            </groups>'.format(data.version, data.date, data.group,
                                           data.default_temp_name, template_name, data.group)
    return header

'''
通过监控项名称 生成 监控项键值
'''
def get_zabbix_key(name):
    return 'ipmi.' + name.replace(' ', '_').lower()

'''
生成模板应用集部分内容
'''
def generate_applications(units):
    apps = []
    for unit in units.values():
        if(unit in data.unit_applications.keys()):
            apps.append(data.unit_applications[unit])
        else:
            apps.append(data.application_other)
    apps = set(apps)    

    applications_list=[]
    applications_list.append('            <applications>')
    for app in apps:
        applications_list.append('                <application>\n'\
                                 '                    <name>{0}</name>\n'
                                 '                </application>'.format(app))
    applications_list.append('            </applications>')

    return '\n'.join(applications_list)

'''
生成模板监控项内容部分
'''
def generate_items(units):
    items_list=[]
    items_list.append('            <items>')
    for name in units:
        app = ''
        if units[name] in data.unit_applications.keys():
            app = data.unit_applications[units[name]]
        else:
            app = data.application_other

        items_list.append('                <item>\n'
                          '                    <name>{0}</name>\n'
                          '                    <type>12</type>\n'
                          '                    <snmp_community/>\n'
                          '                    <snmp_oid/>\n'
                          '                    <key>{1}</key>\n'
                          '                    <delay>{2}</delay>\n'
                          '                    <history>{3}</history>\n'
                          '                    <trends>{4}</trends>\n'
                          '                    <status>0</status>\n'
                          '                    <value_type>0</value_type>\n'
                          '                    <allowed_hosts/>\n'
                          '                    <units>Volts</units>\n'
                          '                    <snmpv3_contextname/>\n'
                          '                    <snmpv3_securityname/>\n'
                          '                    <snmpv3_securitylevel>0</snmpv3_securitylevel>\n'
                          '                    <snmpv3_authprotocol>0</snmpv3_authprotocol>\n'
                          '                    <snmpv3_authpassphrase/>\n'
                          '                    <snmpv3_privprotocol>0</snmpv3_privprotocol>\n'
                          '                    <snmpv3_privpassphrase/>\n'
                          '                    <params/>\n'
                          '                    <ipmi_sensor>+1.5 V</ipmi_sensor>\n'
                          '                    <authtype>0</authtype>\n'
                          '                    <username/>\n'
                          '                    <password/>\n'
                          '                    <publickey/>\n'
                          '                    <privatekey/>\n'
                          '                    <port/>\n'
                          '                    <description/>\n'
                          '                    <inventory_link>0</inventory_link>\n'
                          '                    <applications>\n'
                          '                        <application>\n'
                          '                            <name>{5}</name>\n'
                          '                        </application>\n'
                          '                    </applications>\n'
                          '                    <valuemap/>\n'
                          '                    <logtimefmt/>\n'
                          '                    <preprocessing/>\n'
                          '                    <jmx_endpoint/>\n'
                          '                    <timeout>3s</timeout>\n'
                          '                    <url/>\n'
                          '                    <query_fields/>\n'
                          '                    <posts/>\n'
                          '                    <status_codes>200</status_codes>\n'
                          '                    <follow_redirects>1</follow_redirects>\n'
                          '                    <post_type>0</post_type>\n'
                          '                    <http_proxy/>\n'
                          '                    <headers/>\n'
                          '                    <retrieve_mode>0</retrieve_mode>\n'
                          '                    <request_method>0</request_method>\n'
                          '                    <output_format>0</output_format>\n'
                          '                    <allow_traps>0</allow_traps>\n'
                          '                    <ssl_cert_file/>\n'
                          '                    <ssl_key_file/>\n'
                          '                    <ssl_key_password/>\n'
                          '                    <verify_peer>0</verify_peer>\n'
                          '                    <verify_host>0</verify_host>\n'
                          '                    <master_item/>\n'
                          '                </item>'.format(name,get_zabbix_key(name), data.delay, data.history, data.trends, app))
    items_list.append('            </items>\n'
                      '            <discovery_rules/>\n'
                      '            <httptests/>\n'
                      '            <macros/>\n'
                      '            <templates/>\n'
                      '            <screens/>\n'
                      '        </template>\n'
                      '    </templates>')

    return '\n'.join(items_list)

    

'''
生成触发器部分内容
触发器名称逻辑：
温度过高、过低
电压过高、过低
转速过高、过低

其它未录入的单位显示 过高、过低
无阈值的监控项需要手动建立触发器
'''
def generate_triggers(units,alarm_lower1,alarm_lower2,alarm_lower3,alarm_higher1,alarm_higher2,alarm_higher3):


    # apps = []
    # for unit in units.values():
    #     if(unit in data.unit_applications.keys()):
    #         apps.append(data.unit_applications[unit])
    #     else:
    #         apps.append(data.application_other)
    # apps = set(apps)    

    trigger_list=[]
    trigger_list.append('    <triggers>')
    for name in units:
        #lower1
        if name in alarm_lower1:
            trigger_list.append('        <trigger>\n'
                                '            <expression>{{{0}:{1}.last()}}&lt;{2}</expression>\n'
                                '            <recovery_mode>0</recovery_mode>\n'
                                '            <recovery_expression/>\n'
                                '            <name>{3} {4}  {{HOST.NAME}}</name>\n'
                                '            <correlation_mode>0</correlation_mode>\n'
                                '            <correlation_tag/>\n'
                                '            <url/>\n'
                                '            <status>0</status>\n'
                                '            <priority>3</priority>\n'
                                '            <description/>\n'
                                '            <type>0</type>\n'
                                '            <manual_close>0</manual_close>\n'
                                '            <dependencies/>\n'
                                '            <tags/>\n'
                                '        </trigger>'.format(data.default_temp_name,get_zabbix_key(name),alarm_lower1[name],name,data.unit_trigger_lower[units[name]]))

        if name in alarm_lower2:
            trigger_list.append('        <trigger>\n'
                                '            <expression>{{{0}:{1}.last()}}&lt;{2}</expression>\n'
                                '            <recovery_mode>0</recovery_mode>\n'
                                '            <recovery_expression/>\n'
                                '            <name>{3} {4}  {{HOST.NAME}}</name>\n'
                                '            <correlation_mode>0</correlation_mode>\n'
                                '            <correlation_tag/>\n'
                                '            <url/>\n'
                                '            <status>0</status>\n'
                                '            <priority>4</priority>\n'
                                '            <description/>\n'
                                '            <type>0</type>\n'
                                '            <manual_close>0</manual_close>\n'
                                '            <dependencies/>\n'
                                '            <tags/>\n'
                                '        </trigger>'.format(data.default_temp_name,get_zabbix_key(name),alarm_lower2[name],name,data.unit_trigger_lower[units[name]]))

        if name in alarm_lower3:
            trigger_list.append('        <trigger>\n'
                                '            <expression>{{{0}:{1}.last()}}&lt;{2}</expression>\n'
                                '            <recovery_mode>0</recovery_mode>\n'
                                '            <recovery_expression/>\n'
                                '            <name>{3} {4}  {{HOST.NAME}}</name>\n'
                                '            <correlation_mode>0</correlation_mode>\n'
                                '            <correlation_tag/>\n'
                                '            <url/>\n'
                                '            <status>0</status>\n'
                                '            <priority>5</priority>\n'
                                '            <description/>\n'
                                '            <type>0</type>\n'
                                '            <manual_close>0</manual_close>\n'
                                '            <dependencies/>\n'
                                '            <tags/>\n'
                                '        </trigger>'.format(data.default_temp_name, get_zabbix_key(name), alarm_lower3[name], name, data.unit_trigger_lower[units[name]]))

        if name in alarm_higher1:
            trigger_list.append('        <trigger>\n'
                                '            <expression>{{{0}:{1}.last()}}&gt;{2}</expression>\n'
                                '            <recovery_mode>0</recovery_mode>\n'
                                '            <recovery_expression/>\n'
                                '            <name>{3} {4}  {{HOST.NAME}}</name>\n'
                                '            <correlation_mode>0</correlation_mode>\n'
                                '            <correlation_tag/>\n'
                                '            <url/>\n'
                                '            <status>0</status>\n'
                                '            <priority>3</priority>\n'
                                '            <description/>\n'
                                '            <type>0</type>\n'
                                '            <manual_close>0</manual_close>\n'
                                '            <dependencies/>\n'
                                '            <tags/>\n'
                                '        </trigger>'.format(data.default_temp_name,get_zabbix_key(name),alarm_higher1[name],name,data.unit_trigger_higher[units[name]]))

        if name in alarm_higher2:
            trigger_list.append('        <trigger>\n'
                                '            <expression>{{{0}:{1}.last()}}&gt;{2}</expression>\n'
                                '            <recovery_mode>0</recovery_mode>\n'
                                '            <recovery_expression/>\n'
                                '            <name>{3} {4}  {{HOST.NAME}}</name>\n'
                                '            <correlation_mode>0</correlation_mode>\n'
                                '            <correlation_tag/>\n'
                                '            <url/>\n'
                                '            <status>0</status>\n'
                                '            <priority>4</priority>\n'
                                '            <description/>\n'
                                '            <type>0</type>\n'
                                '            <manual_close>0</manual_close>\n'
                                '            <dependencies/>\n'
                                '            <tags/>\n'
                                '        </trigger>'.format(data.default_temp_name,get_zabbix_key(name),alarm_higher2[name],name,data.unit_trigger_higher[units[name]]))

        if name in alarm_higher3:
            trigger_list.append('        <trigger>\n'
                                '            <expression>{{{0}:{1}.last()}}&gt;{2}</expression>\n'
                                '            <recovery_mode>0</recovery_mode>\n'
                                '            <recovery_expression/>\n'
                                '            <name>{3} {4}  {{HOST.NAME}}</name>\n'
                                '            <correlation_mode>0</correlation_mode>\n'
                                '            <correlation_tag/>\n'
                                '            <url/>\n'
                                '            <status>0</status>\n'
                                '            <priority>5</priority>\n'
                                '            <description/>\n'
                                '            <type>0</type>\n'
                                '            <manual_close>0</manual_close>\n'
                                '            <dependencies/>\n'
                                '            <tags/>\n'
                                '        </trigger>'.format(data.default_temp_name,get_zabbix_key(name),alarm_higher3[name],name,data.unit_trigger_higher[units[name]]))
    trigger_list.append('    </triggers>\n'\
                      '</zabbix_export>')
    return '\n'.join(trigger_list)





