# vulnscan
一个基于exp的框架扫描工具

在 poc 文件夹下增加 exp

Usage: main.py -t target_url

-h --help            - get help

-k --keyword            - Get a list of hosts by referencing Shodan according to keywords

-t --target            - target url

-s --script            - Matching script

Example: python main.py --script=thinkphp* --keyword=thinkphp/5

Example: python main.py --script=thinkphp* -t http://192.168.0.1:8080
