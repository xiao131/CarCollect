from threading import Thread
from wx.lib.pubsub import pub
import requests
import json
import wx
import wx.xrc
import wx.grid
from xlwt import Workbook
import pandas as pd
from os import getcwd
from os import chdir
from re import findall
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
import car58
import car360
from updated2wego import PostMain as WegoPost

#采集数据线程
class CollectThread(Thread):
    def __init__(self,select_num):
        #线程实例化时立即启动
        Thread.__init__(self)
        #主线程关闭
        self.setDaemon(True)

        self.select = select_num
        self.start()

    def run(self):
        #线程执行的代码
        if self.select == 0:
            #采集所有
            car360.Collect()
            car58.Collect()

        elif self.select == 1:
            #采集卡车之家
            car360.Collect()

        elif self.select == 2:
            #采集58同城
            car58.Collect()

        wx.CallAfter(pub.sendMessage, "update", msg="accept_data")

#修改价格线程
class UpdatePriceThread(Thread):
    def __init__(self):
        #线程实例化时立即启动
        Thread.__init__(self)
        #主线程关闭
        self.setDaemon(True)
        self.start()
    def run(self):
        #线程执行的代码
        global Goods_Price
        global Data_List
        data_num = len(Data_List)
        if Goods_Price[-1] == '%':
            bs = float(Goods_Price[0:-1])/100
            for i in range(data_num):
                sku_list = Data_List[i]["sku_list"]
                sku_num = len(sku_list)
                for j in range(sku_num):
                    price_temp = Data_List[i]["sku_list"][j]["goods_price"]
                    price_temp = float(price_temp)
                    price_temp *= bs
                    Data_List[i]["sku_list"][j]["goods_price"] = price_temp
        else:
            bs = float(Goods_Price)
            for i in range(data_num):
                sku_list = Data_List[i]["sku_list"]
                sku_num = len(sku_list)
                for j in range(sku_num):
                    price_temp = Data_List[i]["sku_list"][j]["goods_price"]
                    price_temp = float(price_temp)
                    price_temp += bs
                    Data_List[i]["sku_list"][j]["goods_price"] = price_temp
        wx.CallAfter(pub.sendMessage, "update", msg="accept_price")

#上传数据线程
class UpDataThread(Thread):
    def __init__(self,select_num):
        #线程实例化时立即启动
        Thread.__init__(self)
        #主线程关闭
        self.select = select_num
        self.setDaemon(True)
        self.start()
    def run(self):
        #线程执行的代码
        if self.select == 0:
            #上传所有
            car360.Collect()
            car58.Collect()

        elif self.select == 1:
            #上传卡车之家
            car360.Collect()

        elif self.select == 2:
            #上传58同城
            car58.Collect()
        #上传数据函数
        global Data_List
        global Tag2Id
        global ALL_CAT
        global Wego_Cookie
        global Mc_Account
        global Wego_Account
        global Wego_Password
        f = open("./data/wogo.ini", "r")
        for account in f.readlines():
            account = account.split(" ")
            if len(account) != 2:
                continue
            if account[0] == Wego_Account:
                Wego_Password = account[1]
                break
        f.close()
        Wego_Cookie = FF.WegoLogin(Wego_Account, Wego_Password)

        # GetAllCookie(Mc_Account)
        Tag2Id = FF.CreateTag(ALL_CAT, Wego_Cookie)
        FF.PostToWego(Data_List, Tag2Id,Wego_Cookie)

        wx.CallAfter(pub.sendMessage, "update", msg="accept_up")

#得到有赞的csrf-token
def Get_Csrf_token(Youzan_cookie):
    url = "https://account.youzan.com/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
        , "Cookie": Youzan_cookie}
    res = requests.get(url,headers=headers)
    res = res.text
    csrf_token = findall(r'"csrf_token":"\d+"', res)
    # print(csrf_token)
    csrf_token = csrf_token[0][14:-1]
    print("csrf_token:",csrf_token)
    return csrf_token

#上传有赞数据线程
class UpDataYouzanThread(Thread):
    def __init__(self):
        #线程实例化时立即启动
        Thread.__init__(self)
        #主线程关闭
        self.setDaemon(True)
        self.start()
    def run(self):
        #线程执行的代码
        #上传数据函数
        global Data_List
        global Tag2Id
        global ALL_CAT
        global Youzan_Cookie
        global Mc_Account
        GetAllCookie(Mc_Account)
        # Tag2Id = FF.CreateTag(ALL_CAT, Wego_Cookie)
        # FF.PostToWego(Data_List, Tag2Id,Wego_Cookie)
        # print(Data_List)
        # print(Get_Csrf_token())
        # print(Youzan_Cookie)
        FF.PostToYouZan(Data_List,csrf_token=Get_Csrf_token(Youzan_Cookie),cookie=Youzan_Cookie)

        wx.CallAfter(pub.sendMessage, "update", msg="accept_up")

class Car(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title = u"二手车采集 V1.0.0", pos=wx.DefaultPosition,
                          size=wx.Size(540, 170), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        m_choice1Choices = ["采集全部", "卡车之家","58同城"]
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(80, -1), m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        bSizer2.Add(self.m_choice1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u" 价格", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, u"100%", wx.DefaultPosition, wx.Size(65, -1), 0)
        bSizer2.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u" ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # self.m_button1 = wx.Button(self, wx.ID_ANY, u"修改价格", wx.DefaultPosition, wx.Size(140, -1), 0)
        # bSizer2.Add(self.m_button1, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.SHAPED, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button3 = wx.Button(self, wx.ID_ANY, u"采集数据", wx.DefaultPosition, wx.Size(170, -1), 0)
        bSizer3.Add(self.m_button3, 0, wx.ALL, 5)

        self.m_button4 = wx.Button(self, wx.ID_ANY, u"修改价格", wx.DefaultPosition, wx.Size(170, -1), 0)
        bSizer3.Add(self.m_button4, 0, wx.ALL, 5)

        self.m_button5 = wx.Button(self, wx.ID_ANY, u"生成配置图", wx.DefaultPosition, wx.Size(170, -1), 0)
        bSizer3.Add(self.m_button5, 0, wx.ALL, 5)

        bSizer1.Add(bSizer3, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.SHAPED, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        #获取微商相册账号列表
        f = open("./data/wogo.ini","r")
        m_choice1Choices3 = []
        for account in f.readlines():
            account = account.split(" ")
            if len(account) != 2:
                continue
            m_choice1Choices3.append("微商相册："+account[0])
        f.close()
        # m_choice1Choices3 = ["微商13717330034", "微商13378465583"]
        self.m_choice3 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(170, -1), m_choice1Choices3, 0)
        self.m_choice3.SetSelection(0)
        bSizer5.Add(self.m_choice3, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_button6 = wx.Button(self, wx.ID_ANY, u"上传微商相册", wx.DefaultPosition, wx.Size(170, -1), 0)
        bSizer5.Add(self.m_button6, 0, wx.ALL, 5)

        self.m_button7 = wx.Button(self, wx.ID_ANY, u"上传管家婆", wx.DefaultPosition, wx.Size(170, -1), 0)
        bSizer5.Add(self.m_button7, 0, wx.ALL, 5)

        bSizer1.Add(bSizer5, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.SHAPED, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_button3.Bind(wx.EVT_BUTTON, self.Collect)
        self.m_button4.Bind(wx.EVT_BUTTON, self.UpdatePrice)
        self.m_button5.Bind(wx.EVT_BUTTON, self.GetImage)
        self.m_button6.Bind(wx.EVT_BUTTON, self.UpData)
        self.m_button7.Bind(wx.EVT_BUTTON, self.UpData_Guanjiapo)

        pub.subscribe(self.updateDisplay, "update")

        html_info = requests.get(URL_MMP)
        if html_info.status_code != 200:
            wx.MessageBox("登录失败，请检查您的网络，或者联系开发人员", "you are wrong", wx.OK | wx.YES_DEFAULT)
            self.Destroy()

        #在 采集 和上传 之前获取Cookie
        #获取Cookie和更新Cookie

    def __del__(self):
        pass

    #启动所有按钮
    def EnableAllButton(self):
        self.m_button3.Enable()
        self.m_button4.Enable()
        self.m_button5.Enable()
        self.m_button6.Enable()
        self.m_button7.Enable()

    #关闭所有按钮
    def ColseAllButton(self):
        self.m_button3.Enable(False)
        self.m_button4.Enable(False)
        self.m_button5.Enable(False)
        self.m_button6.Enable(False)
        self.m_button7.Enable(False)

    # 进程完成后更新显示信息
    def updateDisplay(self, msg):
        t = msg
        if t == "accept_data":
            self.updateData()
            wx.MessageBox("采集数据已经成功完成！", "完成消息", wx.OK | wx.YES_DEFAULT)
            # 将按钮重新开启
            self.EnableAllButton()
        elif t == "accept_price":
            #更新数据
            self.updateData()
            wx.MessageBox("修改价格已经成功完成！", "完成消息", wx.OK | wx.YES_DEFAULT)
            # 将按钮重新开启
            self.EnableAllButton()
        elif t == "accept_up":
            wx.MessageBox("上传商品已经成功完成！", "完成消息", wx.OK | wx.YES_DEFAULT)
            # 将按钮重新开启
            self.EnableAllButton()

    def Collect(self,event):
        #多线程
        select_str = self.m_choice1.GetStringSelection()
        select_num = 0
        if select_str == "采集全部":
            select_num = 0
        elif select_str == "卡车之家":
            select_num = 1
        elif select_str == "58同城":
            select_num = 2

        # 采集函数
        CollectThread(select_num)
        # 将按钮设置为禁用
        self.ColseAllButton()

    def UpdatePrice(self,event):
        wx.MessageBox("当前功能正在测试中", "提示消息", wx.OK | wx.YES_DEFAULT)
        return
        #获取价格，判断是否为空
        global Goods_Price
        Goods_Price = self.m_textCtrl1.GetValue()
        if Goods_Price == "":
            wx.MessageBox("请先输入价格的倍数", "提示消息", wx.OK | wx.YES_DEFAULT)
            return
        print("修改价格倍数：", Goods_Price)

        UpdatePriceThread()
        # 将按钮设置为禁用
        self.ColseAllButton()

    def GetImage(self,event):
        wx.MessageBox("生成配置图，当前功能正在测试中", "提示消息", wx.OK | wx.YES_DEFAULT)
        return
        #生成配置图线程

        # 将按钮设置为禁用
        self.ColseAllButton()

    #上传数据，到微商相册
    def UpData(self,event):
        # 多线程
        #获取上传数据的类别
        select_str = self.m_choice1.GetStringSelection()
        select_num = 0
        if select_str == "采集全部":
            select_num = 0
        elif select_str == "卡车之家":
            select_num = 1
        elif select_str == "58同城":
            select_num = 2

        global Wego_Account
        wogo_select = self.m_choice3.GetStringSelection()
        Wego_Account = wogo_select[5:]

        #上传
        UpDataThread(select_num)
        # 将按钮设置为禁用
        self.ColseAllButton()

    # 上传数据，到管家婆
    def UpData_Guanjiapo(self, event):

        # wx.MessageBox("上传Cookie未更新", "提示消息", wx.OK | wx.YES_DEFAULT)
        # return
        global Mc_Account
        mc_select = self.m_choice2.GetStringSelection()

        # 获取价格，判断是否为空
        UpDataYouzanThread()
        # 将按钮设置为禁用
        self.ColseAllButton()

if __name__ == '__main__':
    Goods_Price = "" #商品价格修改
    Goods_Stock = "" #商品库存修改
    Open_File_Path = "" #导入文件的路径
    Save_File_Path = "" #保存文件的路径
    Data_List = [] #采集得到的数据列表

    Dpy_Cookie = ""
    Mc_Cookie = ""
    Jn_Cookie = ""
    Wego_Cookie = ""
    Youzan_Cookie = ""
    Mc_Account = ""
    Wego_Account = ""
    Wego_Password = ""

    Tag2Id = {} #标签对应的上传ID
    ALL_CAT = {}
    URL_MMP = "http://demo.xx2018.cn/210524二手车采集.txt"
    app = wx.App(False)
    frame = Car(None)
    # 根据自己的类名来生成实例
    frame.Show(True)
    # start the applications
    app.MainLoop()