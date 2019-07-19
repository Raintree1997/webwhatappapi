import requests
from bs4 import BeautifulSoup
import threading
import re
import random

lock = threading.local()

class commodity2(object):
    def __init__(self,URL_Folder):
        self.URL_List=[]
        with open(URL_Folder) as a:
            while True:
                if a.readline()=='':
                    break
                else:
                    self.URL_List.append(a.readline())

ip=[]
port=[]
def get_ip(i):
    with lock:
        respon=requests.get('https://www.kuaidaili.com/free/inha/'+str(i)+'/')
        rsp=respon.text
        ip.append(re.findall('<td data-title="IP">(.*?)</td>',rsp,re.S))
        port.append(re.findall('<td data-title="PORT">(.*?)</td>',rsp,re.S))
        return ip,port

def check_ip(ip,port):
    while True:
        i=random.randint(0,len(ip)-1)
        proxies={
            "http": "http://"+ip[i]+':'+port[i],
            "https": "http://"+ip[i]+':'+port[i],
        }
        try:
            c=requests.get('https://detail.1688.com/offer/45357626946.html?spm=a2615.12330364.autotrace-bestOffer.2.66275de0ibqXpx',proxies=proxies,timeout=1)
            with open('./ip.txt','w') as a :
                a.write(ip[i]+':'+port[i])
        except:
            ip.remove(ip[i])
            port.remove(port[i])

def main():

    for i in range(1,100):
        getip=threading.Thread(target=get_ip,args=(i,))
        checkip=threading.Thread(target=check_ip,args=(ip,port))