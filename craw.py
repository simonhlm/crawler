# -*- enconding:utf-8 -*-
import re
import requests
import random

def init(): #the function init is to initilize a list of proxy 
    ip_proxy = []
    html = requests.get("http://haoip.cc/tiqu.htm")
    plistn = re.findall(r'r/>(.*?)<b', html.text, re.S)
    for ip in plistn:
        i = re.sub('\n','',ip)
        ip_proxy.append(i.strip())
    return ip_proxy

class Craw():
    """
    this is a base class for clawers 
    """
    headers = {
    #'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
    #'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    #'Content-Type': 'application/x-www-form-urlencoded',
    #'Host': 'http://bbs.ngacn.cc',
    #'Origin': 'https://passport.csdn.net',
    #'Referer': 'https://passport.csdn.net/account/login',
    #'Upgrade-Insecure-Requests': 1,
    #'Host': 'bbs.ngacn.cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,zh-CN;q=0.8,zh;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    #'Cookie': 'bbsmisccookies=%7B%22insad_refreshid%22%3A%7B0%3A%22/0a001e494662a12b19fdb530e318%22%2C1%3A1493701482%7D%2C%22pv_count_for_insad%22%3A%7B0%3A-43%2C1%3A1493139684%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1493139684%7D%7D; CNZZDATA30039253=cnzz_eid%3D175419729-1469427320-%26ntime%3D1493095966; CNZZDATA30043604=cnzz_eid%3D1770945354-1469428374-%26ntime%3D1493097569; __utma=240585808.2050012559.1469522546.1493026894.1493096691.63; __utmz=240585808.1487312719.51.10.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; CNZZDATA1256638858=8220914-1472989817-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1479979790; CNZZDATA1256638851=1122129359-1475132538-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1492646600; CNZZDATA1256638828=664457739-1482284745-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1491528706; CNZZDATA1256638874=1420002279-1487224733-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1491612097; UM_distinctid=15b465a569ba1-010239ebbab367-41544131-15f900-15b465a569c2d4; CNZZDATA1256638820=434122517-1491530851-http%253A%252F%252Fbbs.ngacn.cc%252F%7C1493093232; ngaPassportUid=guest058fed8e8e6d04; guestJs=1493097431; __utmb=240585808',
    'Connection': 'keep-alive'
    }

    #ip_proxy = init()

    def __init__(self):
        self.s = requests.Session()
        pass

    def login(self, url, ):
        pass

    def get_content(self, url, params='', proxy=None, retries=5 ):
        if proxy==None:
            try:
                return self.s.get(url,params=params,headers=self.headers)
            except Exception as e:
                if retries > 0:
                    print(e)
                    return self.get_content(url, params=params, proxy=None, retries =retries-1)
                else:
                    return self.get_content(url, params=params, proxy=True, retries = 5)
        else: # using proxy
            try:
                ip = random.choice(self.ip_proxy)
                proxy = {'http': ip}
                return self.s.get(url, params=params, headers=self.headers, proxies = proxy)
            except Exception as e:
                if retries > 0:
                    print(e)
                    return self.get_content(url, params=params, proxy=True, retries =retries-1)
                else:
                    print('The retires has end!, the problem is e')
                    return None

