import importlib
import threading
import sys
import getopt
import shodanapi
import os

version = '1.0'
logo = '''
  _____             __      __    _       
 / ____|            \ \    / /   | |      
| (___   ___ __ _ _ _\ \  / /   _| |_ __  
 \___ \ / __/ _` | '_ \ \/ / | | | | '_ \ 
 ____) | (_| (_| | | | \  /| |_| | | | | |
|_____/ \___\__,_|_| |_|\/  \__,_|_|_| |_|
                                          
                        by hycc | V {}
'''.format(version)
print(logo)


def usage():
    print("\n")
    print("Usage: main.py -t target_url")
    print("-h --help            - get help")
    print("-k --keyword            - Get a list of hosts by referencing Shodan according to keywords")
    print("-t --target            - target url")
    print("-s --script            - Matching script")
    print("Example: python main.py --script=thinkphp* --keyword=thinkphp/5")
    print("Example: python main.py --script=thinkphp* -t http://192.168.0.1:8080")


def getnamescript():
    global poclist
    poclist = []
    dirlist = os.listdir("./poc")
    for i in dirlist:
        if ".py" in i:
            poclist.append(i[:-3])
    poclist.pop()
    

def deal(script):
    global poclist
    dirlist = os.listdir("./poc")
    poclist=[]
    if "*" in script:
        script = script.strip("*")
    for i in range(len(dirlist)):
        if script in dirlist[i]:
            poclist.append(dirlist[i].strip(".py"))


def exp(url):
    #[*] 正在测试 thinkphp 5.x remote command execution 测试命令(phpinfo())
    #poc.thinkphp5023.test(url)
    #[*] 正在测试 thinkphp 5022_5129  remote command execution 测试命令(phpinfo())
    #poc.thinkphp5022_5129.test(url)
    for name in poclist:
        poc = importlib.import_module("."+name,"poc")
        poc.test(url)


def run(keyword):
    shodanapi.FindTarget(keyword)
    with open("target.txt","r") as f:
        url = f.readlines()
    for i in range(len(url)):
        k = 'http://'+url[i].strip()
        t = threading.Thread(target=exp, args=(k,))
        t.start()
        t.join()


def main():
    global keyword
    global target
    
    keyword = ''
    target = ''
    script = ''
    
    getnamescript()
    
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hk:t:s:",["help","keyword=","target=","script="])
    except getopt.GetoptError as err:
        print(str(err))
        #usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        if o in ("-s", "--script"):
            script = a
        if o in ("-k", "--keyword"):
            keyword = a
        if o in ("-t", "--target"):
            target = a
    
    if script:
        deal(script)
    if keyword:
        run(keyword)
    if target:
        exp(target)

if __name__ == "__main__":
    main()