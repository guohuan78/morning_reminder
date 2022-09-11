# -*- coding: utf-8 -*-
import http.client, urllib
import json
import random
from requests import get, post
import datetime
import sys
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import logging

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def get_holiday(date):
    conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    params = urllib.parse.urlencode({'key':'e6f96b565c8e0265b4b9d3042c965558','date':date})
    conn.request('POST','/jiejiari/index',params,headers)
    return json.loads(conn.getresponse().read().decode('utf-8'))["newslist"][0]

def get_response(func):
    dic = {
        'saylove': {
            'args':{'key':'e6f96b565c8e0265b4b9d3042c965558'},
            'url':'/saylove/index'
        },
        'one': {
            'args':{'key':'e6f96b565c8e0265b4b9d3042c965558','rand':'1'},
            'url':'/one/index'
        },
        'copywriting': {
            'args':{'key':'e6f96b565c8e0265b4b9d3042c965558'},
            'url':'/pyqwenan/index'
        },
        'rainbow_fart': {
            'args':{'key':'e6f96b565c8e0265b4b9d3042c965558'},
            'url':'/caihongpi/index'
        }
    }
    conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
    headers = {'Content-type':'application/x-www-form-urlencoded'}
    params = urllib.parse.urlencode(dic[func]['args'])
    conn.request('POST',dic[func]['url'],params,headers)
    return json.loads(conn.getresponse().read().decode('utf-8'))["newslist"][0]

def one():
    data = get_response('one')
    return data['word']

def copywriting():
    data = get_response('copywriting')
    return data['content']

def rainbow_fart():
    data = get_response('rainbow_fart')
    return data['content']

def saylove():
    data = get_response('saylove')
    return data['content']

def date():
    today = datetime.date.today()
    data = get_holiday(today)
    date = "{} {} 农历{}{} ".format(today,data["cnweekday"],data["lunarmonth"],data["lunarday"])
    if(data["name"] != ''):
        date = date + '\n' + data["name"] + "假期快乐！"
    else:
        for i in range(1,51):
            days_after = datetime.date.today() + datetime.timedelta(days=i)
            data = get_holiday(days_after)
            if(data["name"] != ''):
                date = date + '\n' + "距离" + data["name"] + "假期还有" + str(i) + "天"
                break
    return date

def send_message(data, access_token):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)

def run(username: str, password: str):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    username_element = driver.find_element(By.ID, 'username')
    username_element.send_keys(username)
    password_element = driver.find_element(By.ID, 'password')
    password_element.send_keys(password)
    driver.find_element(By.NAME, 'submit').click()
    js = 'go_sub();go_subfx();document.querySelector("label.weui-cell.weui-cell_active.weui-check__label").click();save();savefx()'
    driver.execute_script(js)
    fail = None
    driver.close()
    if fail:
        return False
    else:
        return True

def yqtb(students: list):
    logger.info('开始执行填报...')
    all_num = len(students)
    cur_num = 0
    suc_num = 0
    for username, password in students:
        cur_num += 1
        if run(username, password):
            suc_num += 1
            logger.info(
                f'{username} 填报成功 √; ({all_num}个任务中的第{cur_num}个,共成功{suc_num}个)')
        else:
            logger.info(
                f'{username} 填报失败 x; ({all_num}个任务中的第{cur_num}个,共成功{suc_num}个)')
    logger.info('填报执行完毕')
    if suc_num < all_num:
        raise Exception("填报过程出现异常")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    env_dist = os.environ
    config = eval(env_dist.get("config"))
    # with open("config.txt", encoding="utf-8") as f:
    #     config = eval(f.read())


    url = r'https://yqtb.nwpu.edu.cn/wx/ry/jrsb.jsp'
    driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    service = Service(driver_path)
 
    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = eval(env_dist.get("user"))
    # users = config['user']

    # 构建推送数据 不包含推送对象
    data = {
        "template_id": config["template_id_1"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": date(),
                "color": get_color()
            },
            "saylove": {
                "value": saylove(),
                "color": get_color()
            },
            "rainbow_fart":{
                "value": rainbow_fart(),
                "color": get_color()
            },
            "copywriting":{
                "value": copywriting(),
                "color": get_color()
            },
            "one":{
                "value": one(),
                "color": get_color()
            }
        }
    }

    # 遍历推送对象 公众号推送消息
    for user in users:
        data["touser"] = user
        send_message(data, accessToken)

    try:
        data["touser"] = users[0]
        data["template_id"] = config["template_id_2"]
        # students = json.loads(str(config))
        students = config["account"]
        logger.info(f'加载的用户列表: {[username for username, _ in students]}')
        yqtb(students)
    except Exception as e:
        logger.info('发送错误消息')
        data["data"] = {
            "msg": {
                "value": str(e),
                "color": get_color()
            }
        }
        send_message(data, accessToken)
        raise e
    data["data"] = {
        "msg": {
             "value": "今日填报成功！",
            "color": get_color()
        }
    }
    send_message(data, accessToken)