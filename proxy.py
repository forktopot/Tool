import requests
from lxml import etree
import re
import threading
from multiprocessing import Pool
import random


global proxys
global user_agent_list

user_agent_list = [ \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

def getxiciproxy():
    UserAgent = random.choice(user_agent_list)
    header = {'User-Agent': UserAgent}
    for i in range(1,5):
        try:
            html = requests.session()
            temp = html.get('https://www.xicidaili.com/nn/'+str(i), headers = header)
            temp.decoding = 'utf-8'
            text = re.findall('<td>(.*?)</td>', temp.text, re.I|re.M)
            for x in range(len(text)):
                if x%5==0:
                    proxys.append(text[x]+':'+text[x+1])
        except:
            continue


def getqydaliliproxy():
    UserAgent = random.choice(user_agent_list)
    header = {'User-Agent': UserAgent}
    for i in range(1,50):
        try:
            html = requests.session()
            temp = html.get('http://www.qydaili.com/free/?action=china&page='+str(i), headers = header)
            temp.decoding = 'utf-8'
            IP = re.findall('<td data-title="IP">(.*?)</td>', temp.text, re.I|re.M)
            PORT = re.findall('<td data-title="PORT">(.*?)</td>', temp.text, re.I|re.M)
            for x in range(len(IP)):
                proxys.append(IP[x]+':'+PORT[x])
        except:
            continue


def dealproxy(proxy):
    proxies = {
        'http':'http://' + proxy,
        'https':'https://' + proxy,
    }

    try:
        response = requests.get('http://httpbin.org/get', proxies=proxies, timeout = 5)
        if response.status_code==200:
            with open('proxy.txt', 'a') as f:
                f.write(proxy+'\n')
    except requests.exceptions.ConnectionError as e:
        return

if __name__ == "__main__":
    proxys = []
    getxiciproxy()
    getqydaliliproxy()
    print(proxys)
    print(len(proxys))
    p = Pool(8)
    for proxy in proxys:
        p.apply_async(dealproxy, args=(proxy,))
    p.close()
    p.join()


