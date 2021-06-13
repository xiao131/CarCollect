import requests
from threading import Thread
from wx.lib.pubsub import pub
import wx
import wx.xrc
import wx.grid
# import car58
# import car360
# from updated2wego import PostMain as WegoPost
# from updated2guanjiapo import main as GuanjiapoPost
from bs4 import BeautifulSoup
import re
import base64
from fontTools.ttLib import TTFont
import time
from tqdm import tqdm
import json

def GetFile(name):
    url = "http://demo.xx2018.cn/CarCollect/"+name+".py"
    r = requests.get(url)
    with open(name+".py", "wb") as code:
        code.write(r.content)
    # f = open(name+".py", "wb")
    # f.write(temp_code.text)
    # f.close()

if __name__ == '__main__':
    try:
        code_path = "http://demo.xx2018.cn/CarCollect/CarMain.py"
        code = requests.get(code_path)
        if code.status_code != 200:
            print("请检查您的网路设置")
            time.sleep(600)
        else:
            #下载代码到本地
            GetFile("car58")
            GetFile("car360")
            GetFile("updated2wego")
            GetFile("updated2guanjiapo")
            #运行主程序
            exec(code.content)
    except Exception as e:
        print(e)
        time.sleep(600)