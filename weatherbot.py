# python3
# 和风天气

from typing import ValuesView
import requests
import json
import time
import os
import hashlib
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
# 配置各种key
# 机器人的 webhook，支持钉钉、server酱等服务
webhook = ''
#和风天气API key
hfapi = ''
#灾害天气API key
warningapi = ''
#工作日查询接口
workdayapi = ''
#定义年份
CUR_YEAR = '2021'
global contents
contents = ''
#-------------------------------------------------------------------------------------------------
#                          测试机器人
#-------------------------------------------------------------------------------------------------
 
 
#输出方式
def output(content):
    global contents
    content += '  '
    # 整合输出内容
    contents += content + '\n'
    content += '  '
    print(content)
 
 

#KIM消息推送
def KIM():
    webhook_url = webhook
    dd_header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    global contents
    dd_message = {
        "msgtype": "markdown",
        "markdown": {
            "content": f'【温❤提示】\n{contents}'
        }
    }
    r = requests.post(url=webhook_url,
                      headers=dd_header,
                      data=json.dumps(dd_message))
    if r.status_code == 200:
        print('[+]KIM消息已推送，请查收  ')



# 上海
#和风天气开发文档
def sign_sh():
    yburl = 'https://free-api.heweather.com/s6/weather/forecast'
    value = {
        #天气地址
        'location': '上海',
        #和风天气API
        'key': hfapi,
        #语言
        'lang': 'zh'
    }
    ybreq = requests.get(yburl, params=value)
    ybjs = ybreq.json()
    # print(ybjs)
    for i in range(1):
        yb = ybjs['HeWeather6'][0]['daily_forecast']
        d1 = '今日天气' + '：'  + yb[i]['cond_txt_d'] + '\n' + '温度' + '：'  + yb[i]['tmp_max'] + '℃/'  + yb[i]['tmp_min'] + '℃' + '\n' + '风力：' + yb[i]['wind_dir']  + yb[i]['wind_sc'] + '级'
        output(d1)
        
#获取生活小提示
def sign_gx():
    yburl = 'https://free-api.heweather.com/s6/weather/lifestyle'
    value = {
        #天气地址
        'location': '上海',
        #和风天气API
        'key': hfapi,
        #语言
        'lang': 'zh'
    }
    ybreq = requests.get(yburl, params=value)
    ybjs = ybreq.json()
    # print(ybjs)
    for i in range(1):
        yb = ybjs['HeWeather6'][0]['lifestyle']
        d1 = yb[datetype]['txt']
        output(d1)

def warning_sh():
    yburl = 'https://api.qweather.com/v7/warning/now'
    value = {
        #天气地址上海：101020100
        'location': '101020100',
        #和风天气API
        'key': warningapi,
        #语言
        'lang': 'zh'
    }
    ybreq = requests.get(yburl, params=value)
    ybjs = ybreq.json()
    # print(ybjs)
    for i in range(1):
        yb = ybjs['warning']
        if not ybjs['warning']:
            print("无灾害预警")
        else:
            if '蓝色' == yb[0]['level'] or '黄色' == yb[0]['level'] or '橙色' == yb[0]['level'] or '红色' == yb[0]['level']:
                d1 = '————————————\n' + yb[0]['text']
                output(d1)
            else:
                print("灾害预警等级较低")

#检查是否是工作日
def check_if_is_work_day():
    #获取当前日期
    day_info = time.strftime("%m%d",time.localtime(time.time()))
    print(day_info)
    global holiday_info
    #这里判断工作日是通过开源项目实现搭建在服务器内部的
    #项目地址：https://gitee.com/web/holidays_api
    rep = requests.get(workdayapi + CUR_YEAR + day_info)
    info_txt = rep.content.decode()
    holiday_info = json.loads(info_txt)
    global datetype
    if 0 != holiday_info['info']:
        datetype = 3
        print('判断为非工作日')
    else:
        datetype = 2
        sign_sh()
        sign_gx()
        warning_sh()
        try:
            KIM()
        except Exception:
            print('[+]请检查KIM配置是否正确')

    return False

def main():
    print("--------------------------------------------------")
    check_if_is_work_day()
 
def main_handler(event, context):
    return main()
 
 
if __name__ == '__main__':
    main()
