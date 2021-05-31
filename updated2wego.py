from urllib import request
from urllib import error
from time import time
from time import sleep
import datetime
from xlwt import Workbook
from pathlib import Path
from os import makedirs
from PIL import Image

import ijson
from urllib.parse import quote,unquote
import pickle
import json
from requests import post,get
import requests


def save_obj(obj, name ):
    with open('./data/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('./data/'+name + '.pkl', 'rb') as f:
        return pickle.load(f)
#得到网页源代码
#参数：网址
#返回：网页源代码
def GetHtmlCode(url,headers):
    # 解析网页
    try:
        # print(url)
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        #     , "Cookie": cookie}
        # headers = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
        #            ,("Cookie",cookie)]
        opener = request.build_opener()
        opener.addheaders = headers
        file = opener.open(url)
        content_html = file.read()
        opener.close()
        # print(content_html)
        # response = urllib.request.urlopen(url)
    except error.URLError as e:
        print("error2: 网络连接超时",e)
        return None
    # except Exception as e:
    #     print(e)
    #     return None
    # if response.getcode() != 200:
    #     print("error1: 打开网页失败，请检查您的网络！")
    #     return None
    # content_html = file.read()
    # print(content_html.decode('utf8'))  # 解码
    return content_html


# 创建标签
def CreateTag(car):
    tag_url = 'https://www.szwego.com/service/album/album_theme_tag_operation.jsp?act=edit_tag'
    theme_url = 'https://www.szwego.com/service/album/album_theme_tag_operation.jsp?act=edit_group'
    header = {'Accept': 'application/json, text/javascript, */*;q=0.01',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'Content-Length': '26',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'Cookie':'UM_distinctid=173d742468b495-09573fb05fb77a-5d492f12-1fa400-173d742468c579; token=MjAyOTI2RUVDMEZGODc1NDU5NzE1OUY2NTFEMEI2NUY0RjZDNEM4NzcxRENCMkFDMkI2NDBBRTQxNDkwNDRCODgyMEYxRjhBODUyQUU4Njk4RTNERTNEQkIyRDdBQzcy; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22A2017072620535302484%22%2C%22first_id%22%3A%22173d74246d418b-075c01c8978eb3-5d492f12-2073600-173d74246d592a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22173d74246d418b-075c01c8978eb3-5d492f12-2073600-173d74246d592a%22%7D; CNZZDATA1275056938=1097037509-1597040283-https%253A%252F%252Fwww.wegooooo.com%252F%7C1597979109; client_type=net; JSESSIONID=6BDDACF146849B02B2B8C477A3D01E82',
              'Host': 'www.szwego.com',
              'Origin': 'https://www.szwego.com',
              'Referer': 'https://www.szwego.com/static/index.html',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}
    header_get = [('Cookie','UM_distinctid=173d742468b495-09573fb05fb77a-5d492f12-1fa400-173d742468c579; token=MjAyOTI2RUVDMEZGODc1NDU5NzE1OUY2NTFEMEI2NUY0RjZDNEM4NzcxRENCMkFDMkI2NDBBRTQxNDkwNDRCODgyMEYxRjhBODUyQUU4Njk4RTNERTNEQkIyRDdBQzcy; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22A2017072620535302484%22%2C%22first_id%22%3A%22173d74246d418b-075c01c8978eb3-5d492f12-2073600-173d74246d592a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22173d74246d418b-075c01c8978eb3-5d492f12-2073600-173d74246d592a%22%7D; CNZZDATA1275056938=1097037509-1597040283-https%253A%252F%252Fwww.wegooooo.com%252F%7C1597979109; client_type=net; JSESSIONID=6BDDACF146849B02B2B8C477A3D01E82'),
                  ('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36')]
    tag2id = {}
    label = car['label']
    try:
        tag2id = load_obj('tag2id')
    except:
        pass
    if label in tag2id.keys():
        return tag2id
    tagid_str = ''
    theme_detail_url = 'https://www.szwego.com/service/album/album_theme_tag_operation.jsp?act=get_tags'

    # theme_detail = get(url=theme_detail_url, headers=header)
    theme_detail = GetHtmlCode(theme_detail_url,header_get)
    theme_detail = json.loads(theme_detail)
    # for data_from,cat_set in all_cat.items():
        # 先找是否存在该目录获取ID
    exist_groups =  theme_detail['result']['groups']
    groupId = -3
    for groups in exist_groups:
        if car['datasource'] == groups['groupName']:
            groupId = groups['groupId']
            # break
    # 获得所有标签的ID
    for tags in theme_detail['result']['allTags']:
        tag2id[tags['tagName']] = tags['tagId']

    # for cat in cat_set:
    if label not in tag2id.keys(): # 标签没有在现有标签中
        tag_data = 'tag_id=&tag_name='+quote(label)
        # tag_data = tag_data.encode('utf-8')
        r_tag = post(tag_url, data=tag_data, headers=header)
        tag_dict = json.loads(r_tag.text)
        if tag_dict['errcode'] == 0:
            print('添加标签成功：',label)
            tag2id[label] = tag_dict['result']['tagId']

        tagid_str+=str(tag2id[label])+'%2C'


    if groupId == -3: # 没有找到对应目录则新建
        theme_data = 'group_id=&group_name='+quote(car['datasource'] )+'&ids=%5B'+tagid_str[:-3]+'%5D'
    else:
        theme_data = 'group_id='+str(groupId)+'&group_name=' + quote(car['datasource'] ) + '&ids=%5B' + tagid_str[:-3] + '%5D'
    # theme_data = theme_data.encode('utf-8')
    r_theme = post(theme_url, data=theme_data, headers=header)
    theme_dict = json.loads(r_theme.text)
    print(theme_dict)
    if theme_dict['errcode'] == 0 and groupId == -3:
        print('添加目录成功：',car['datasource'] )

    save_obj(tag2id,'tag2id')
    return tag2id

# 单位转换
def str2value(valueStr):
    valueStr = str(valueStr)
    idxOfYi = valueStr.find('亿')
    idxOfWan = valueStr.find('万')
    if idxOfYi != -1 and idxOfWan != -1:
        return int(float(valueStr[:idxOfYi])*1e8 + float(valueStr[idxOfYi+1:idxOfWan])*1e4)
    elif idxOfYi != -1 and idxOfWan == -1:
        return int(float(valueStr[:idxOfYi])*1e8)
    elif idxOfYi == -1 and idxOfWan != -1:
        return int(float(valueStr[idxOfYi+1:idxOfWan])*1e4)
    elif idxOfYi == -1 and idxOfWan == -1:
        return float(valueStr)


# 创建规格获得规格ID
def CreateFormat(name):
    format_url = 'https://www.szwego.com/service/album/album_theme_format_operation.jsp?act=save_format_list'
    header = {'Accept': 'application/json, text/javascript, */*;q=0.01',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'Content-Length': '26',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'Cookie': 'UM_distinctid=173d742468b495-09573fb05fb77a-5d492f12-1fa400-173d742468c579; token=MjAyOTI2RUVDMEZGODc1NDU5NzE1OUY2NTFEMEI2NUY0RjZDNEM4NzcxRENCMkFDMkI2NDBBRTQxNDkwNDRCODgyMEYxRjhBODUyQUU4Njk4RTNERTNEQkIyRDdBQzcy; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22A2017072620535302484%22%2C%22first_id%22%3A%22173d74246d418b-075c01c8978eb3-5d492f12-2073600-173d74246d592a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22173d74246d418b-075c01c8978eb3-5d492f12-2073600-173d74246d592a%22%7D; CNZZDATA1275056938=1097037509-1597040283-https%253A%252F%252Fwww.wegooooo.com%252F%7C1597979109; client_type=net; JSESSIONID=6BDDACF146849B02B2B8C477A3D01E82',
              'Host': 'www.szwego.com',
              'Origin': 'https://www.szwego.com',
              'Referer': 'https://www.szwego.com/static/index.html',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}
    format_data = 'formats=%5B%7B%22formatName%22%3A%22'+quote(name)+'%22%7D%5D'
    r_theme = post(format_url, data=format_data, headers=header)
    format_dict = json.loads(r_theme.text)
    if format_dict['errcode'] == 0:
        return format_dict['result']['formats'][0]['formatId']

    return 0

# 上传数据
def PostToWego(goods,tag2id):
    post_goods_url = 'https://www.szwego.com/service/album/album_theme_operation.jsp?act=save_theme'
    header = {'Accept': 'application/json, text/javascript, */*;q=0.01',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'Content-Length': '333',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'Cookie': 'UM_distinctid=17993bbae6f4bc-04767713025c5f-5771031-1fa400-17993bbae70d03; token=MjAyOTI2RUVDMEZGODc1NDU5NzE1OUY2NTFEMEI2NUY0RjZDNEM4NzcxRENCMkFDMkI2NDBBRTQxNDkwNDRCODgyMEYxRjhBODUyQUU4Njk4RTNERTNEQkIyRDdBQzcy; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22A2017072620535302484%22%2C%22first_id%22%3A%2217993bbb062580-0b2bb8ebf95e4b-5771031-2073600-17993bbb063b6c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217993bbb062580-0b2bb8ebf95e4b-5771031-2073600-17993bbb063b6c%22%7D; CNZZDATA1275056938=2000595176-1621678674-%7C1622361743; JSESSIONID=0A02CE71EE28EBE920669067C011FDEF',
              'Host': 'www.szwego.com',
              'Origin': 'https://www.szwego.com',
              'Referer': 'https://www.szwego.com/static/index.html',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin',
              'wego-channel':'net',
              'wego-staging':'0',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}
    # for goods in goods_data:
    id = 'id='
    title = '&title='+quote(goods['name'])+quote(' 参考价：')
    if 'price' not in goods.keys():
        title += quote('价格私聊')
    else:
        title += str(str2value(goods['price']))

    main_imgs = '&main_imgs=['
    for img in goods['image']:
        # import requests
        url = "https://upload.qiniup.com/"
        file_name = img.split('/')[-1]  # 文件名
        file_path = img#.replace('https','http')  # 文件路径
        img_type = img.split('.')[-1]

        if 'http' in img:
            # try:

            # 读取在线图片并且裁剪保存本地
            Hostreferer = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            html = requests.get(img, headers=Hostreferer)
            temp_path = './data/temp.' + img_type
            f = open(temp_path, 'wb')
            f.write(html.content)
            f.close()
            # 读取图片
            img_1 = Image.open(temp_path)
            size = img_1.size
            # 设置裁剪的位置
            crop_box = (0, 0, size[0], int(size[1] * 0.9))
            # 裁剪图片
            img_2 = img_1.crop(crop_box)
            # img_2.show()
            temp_path = './data/temp1.' + img_type
            img_2.save(temp_path)
        else:
            temp_path = img
        files = {'file': (file_name, open(temp_path, 'rb'), 'image/' + img_type)}


        # try:
        #     # res = request.urlopen(file_path).read()
        #     files = {'file': (file_name, request.urlopen(file_path).read(), 'image/'+img_type)}
        # except:
        #     # res = request.urlopen(quote(file_path)).read()
        #     files = {'file': (file_name, request.urlopen(quote(file_path)).read(), 'image/' + img_type)}



        # update token
        uptoken = json.loads(get('https://www.szwego.com/service/get_qiuniu_token.jsp').text)['uptoken']
        data = {
            "token": uptoken}
        res = requests.request("POST", url, data=data, files=files)
        # print(res.status_code)
        # print(res.text)
        xcimg_url = 'https://xcimg.szwego.com/'
        main_imgs+=quote('"'+xcimg_url+json.loads(res.text)['key']+'",')
    main_imgs = main_imgs[:-3]+']'
        # pass
    tags = '&tags=[{"tagId":'+quote(str(tag2id[goods['label']]))+',"tagName":'+quote('"'+goods['label'])+'"}]'
    groups = '&groups=[]'
    personal = '&personal=0'
    personalTagIds = '&personalTagIds=[]'
    sources = '&sources=[]'
    digital_watermark = '&digital_watermark='
    subTitle = '&subTitle='+quote(goods['name'])
    goodsNum = '&goodsNum='
    formats = '&formats='
    colors = '&colors=[]'

    priceArr = '&priceArr=[]'
    noteArr = '&noteArr=[]'
    skuPriceType = '&skuPriceType='
    # skus = '&skus=['
    # for sku in goods['sku_list']:
    #     # 创建规格获得规格ID
    #     formatid = CreateFormat(sku['goods_title']+' '+sku['unit_price'])
    #     formats += '{"formatId":'+str(formatid)+',"formatName":"'+quote(sku['goods_title'])+'"},'
    #     skus += '{"id":'+str(formatid)+',"name":"'+quote(sku['goods_title'])+'","cname":"'+quote(sku['goods_title'])+'","quantity":0,"price":"'+str(sku['goods_price'])+'","stock":'+sku['goods_stock']+',"formatNum":""},'
    # formats = formats[:-1]+']'
    # skus = skus[:-1]+']'
    totalStock = '&totalStock='
    post_goods_data = id+title+main_imgs+tags+groups+personal+personalTagIds+sources+digital_watermark+subTitle+goodsNum+formats+colors+priceArr+noteArr+skuPriceType+totalStock
    # post_goods_data = urllib.parse.unquote(post_goods_data)

    r = post(post_goods_url, data=post_goods_data, headers=header)
    # format_dict = json.loads(r.text)
    # print(r.text)
    # print(r.text)
    print('上传商品成功：',goods['name'])


if __name__ == "__main__":
    # 流式分块取JSON 防止爆内存
    json_path_list = ['./data/360che_ershoucar.json']
    for json_path in json_path_list:
        with open(json_path, 'r', encoding='utf-8') as f:
            objects = ijson.items(f, 'item')
            # 这个objects在这里就是相当于一个生成器，可以调用next函数取它的下一个值
            while True:
                try:
                    car = objects.__next__()
                    if '360che_ershoucar' in json_path:
                        car['datasource'] = '360-二手车'
                    elif '360che_newcar' in json_path:
                        car['datasource'] = '360-新车'
                    car['image'].insert('./',0)
                    print(car)
                    try:
                        car['label'] = car['datasource']+'-'+car['品牌']
                    except:
                        continue
                    tag2id = CreateTag(car)
                    PostToWego(car, tag2id)
                except StopIteration as e:
                    print("数据读取完成")
                    break
