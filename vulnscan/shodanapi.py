# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:19:39 2019

@author: hycc
"""

import shodan

api = shodan.Shodan("cB9sXwb7l95ZhSJaNgcaO7NQpkzfhQVM")

def FindTarget(keyword):
    try:
        f = open("target.txt", "w+")
        results = api.search(keyword)
        print("Results found: %s" % results['total'])
        for result in results['matches']:
            url = result['ip_str'] + ":" + str(result['port'])
            print(url)
            f.write(url+'\n')
        f.close()
    except shodan.APIError as e:
        print("Error:%s" % e)


if __name__=='__main__':
    FindTarget()