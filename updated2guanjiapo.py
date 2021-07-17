from urllib import request
from urllib import error
# from time import time
# from time import sleep
# import datetime
# from xlwt import Workbook
# from pathlib import Path
# from os import makedirs
import ijson
# from urllib.parse import quote,unquote
import time
import datetime
from PIL import Image
import pickle
import json
from requests import post,get
import requests
from excel2img import GetDetailImage

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



def PostImage(image_list,token = None,esn = None):

    post_image_url = 'https://ishoptemp.oss-cn-hangzhou.aliyuncs.com/'
    header = {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'client-src':'pcweb',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
              'token':token,
              'esn':esn
              }

    # key: pctest / 4613912105293ce12732f0b541f9be0b6bbaa0204372.png
    # policy: eyJleHBpcmF0aW9uIjoiMjAyMS0wNS0yOVQwNjoxNTo1Mi44OTBaIiwiY29uZGl0aW9ucyI6W1siY29udGVudC1sZW5ndGgtcmFuZ2UiLDAsMTA0ODU3NjAwMF0sWyJzdGFydHMtd2l0aCIsIiRrZXkiLCJwY3Rlc3QvIl1dfQ ==
    # OSSAccessKeyId: LTAIdNY3vgfU4JmB
    # success_action_status: 200
    # signature: z26H3iygsJZUF0IfR4RxN0YDW1I =
    # file: (binary)

    # [{
    #     "ImgName": "461391210529a62df3f128d34d35a0ac9eb55489deaa.png",
    #     "type": "0"
    # }, {
    #     "ImgName": "461391210529b5ba1f12e31c48079af3b7106653ed9c.png",
    #     "type": "0"
    # }, {
    #     "ImgName": "461391210529074580c29b044da2ba7ccc96ca61ec21.png",
    #     "type": "1"
    # }, {
    #     "ImgName": "461391210529cc892a8240e649fba610934957cba67a.png",
    #     "type": "1"
    # }],
    header1 = [('User-Agent',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'),
               ('token',token),
               ('esn', esn),
               ('Accept', '*/*'),
               ('Accept-Encoding', 'gzip, deflate, br'),
               ('Accept-Language', 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'),
               ('Connection', 'keep-alive'),
               ('Content-Length', '143713'),
               ('client-src', 'pcweb'),
               ('Content-Type', 'application/json')
               ]
    image_name_list = []
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    for img in image_list:
        file_name = img.split('/')[-1]  # 文件名
        file_path = img#.replace('https','http')  # 文件路径
        if '.jpg' in img:
            img_type = 'jpg'
        else:
            img_type = 'png'


        # content = GetHtmlCode('https://v600api-pc.graspishop.com/apc/sys/about/generaterandomstring?count=1',header1)
        # print(header)
        rand_cont = s.get('https://v600api-pc.graspishop.com/apc/sys/about/generaterandomstring?count=1',headers = header).text
        # print(rand_cont)
        img_name = json.loads(rand_cont)['RetObject'][0]
        img_name =  "{}.{}".format(img_name, img_type)
        need_key = 'pctest/{}'.format(img_name)

        if 'http' in img:
            # try:

            # 读取在线图片并且裁剪保存本地
            Hostreferer = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }

            html = s.get(img, headers=Hostreferer)
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
            img_2 = img_2.convert('RGB')
            img_2.save(temp_path)
        else:
            temp_path = img
        files = {'file': (file_name, open(temp_path, 'rb'), 'image/' + img_type)}

        # try:
        #     files = {'file': (img_name, request.urlopen(file_path).read(), 'image/' + img_type)}
        # except:
        #     files = {'file': (img_name, request.urlopen(quote(file_path)).read(), 'image/' + img_type)}


        Img_dict0 = {}
        Img_dict0['ImgName'] = img_name
        Img_dict0['type'] = '0'
        image_name_list.append(Img_dict0)
        Img_dict1 = {}
        Img_dict1['ImgName'] = img_name
        Img_dict1['type'] = '1'
        image_name_list.append(Img_dict1)


        get_oss_policy = json.loads(s.get('https://v600api-pc.graspishop.com/apc/BaseInfo/Goods/GetOssPolicy',headers = header).text)
        need_policy = get_oss_policy['RetObject']['Policy']
        need_OSSAccessKeyId = get_oss_policy['RetObject']['AccessID']
        need_signature = get_oss_policy['RetObject']['Signature']
        post_data = {'key':need_key,
                     'policy':need_policy,
                     'OSSAccessKeyId':need_OSSAccessKeyId,
                     'success_action_status':200,
                     'signature':need_signature

                     }
        # post_data = 'key={}&policy={}&OSSAccessKeyId={}&success_action_status=200&signature={}'.format(need_key,need_policy,need_OSSAccessKeyId,need_signature)
        res = s.request("POST", post_image_url, data=post_data, files=files,headers = header)
        # print(res.text)
    return image_name_list
# 上传数据
def PostToGuanjiapo(goods,token = None,esn = None):
    # esn = 'randomHiR3gLtoFRPGqsEa1622279027206'
    # token = 'mTXqrWKiKGuPIr08ynVR8opM/8pV752wkBNEabLEjQ7G0UBEHXFSF9/YPYMnik0Xn+oAMD4UXZvnWmB2dkGqZwdsWpV1uyhRdfeY3ZfafBWCTI2IU0ry5j/iCO0iEvWTeR/uSuhby3/0dVBng1edCsdYkkFjh2ocrbQvffM7iqc='
    post_goods_url = 'https://v600api-pc.graspishop.com/apc/BaseInfo/Goods/Create?CheckName=false'
    header = {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'client-src':'pcweb',
              'Content-Type': 'application/json',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
              'token':token,
              'esn':esn
              }
    # for goods in goods_data:
    if 'info' not in goods.keys():
        goods['info'] = goods['name']
    t = time.time()
    now_t = int(round(t * 1000))
    info = goods['info']+quote(' ' + str(now_t))+' 参考价：'
    if 'price' not in goods.keys():
        info += '价格私聊'
    else:
        info += str(str2value(goods['price']))

    post_goods_data = {"GoodsID": 0,
	"OldStockList": None,
	"StockList": None,
	"GoodsCode": "SP00006",
	"GoodsName": goods['name'],
	"BarCode": "",
	"MemCode": "",
	"SupID": "",
	"SupName": "",
	"ClassID": goods['classid'],
	"GoodsUnit": "辆",
	"UnitID": 0,
	"BaseSID": 0,
	"LDate": "",
	"Remarks": info,
	"BarPlanID": "0",
	"GoodsSelectSku": {
		"ColorList": [],
		"SizeList": [],
		"CupList": [],
		"SKU1List": [],
		"SKU2List": []
	},
	"ChangedStockList": [],
	"ChangedBarCode": [],
	"GoodsAttrSimpleList": [],
	"BoundPriceSimpleList": [{
		"SKUIDStr": "0_0_0_0_0",
		"GoodsBoundSimpleList": [{
			"StoreID": 0,
			"LowerQty": -1,
			"UpperQty": -1
		}],
		"GoodsPriceSimpleList": []
	}],
	"IsStop": 0}

    post_goods_data['GoodsImgSimpleList'] = PostImage(goods['image'],token,esn)


    r = post(post_goods_url, data=json.dumps(post_goods_data), headers=header)
    format_dict = json.loads(r.text)
    print(format_dict['RetMessage'])
    if format_dict['RetCode'] == -1:
        return
    # print(r.text)
    # print(r.text)
    print('上传商品成功：',goods['name'])
    with open('./data/url.txt','a+',encoding = 'utf-8') as f:
        f.write("{} {}\n".format(now_t,goods['url']))
    return format_dict['RetObject']['ID']

def login(username):
    header = {'accept': '*/*',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
              'client-src':'pcweb',
              'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
              }
    login_url = 'https://api.graspishop.com:50000/apc/login/login/login'
    esn = 'randombMto4mtG1MtZrfcE1622280169460'
    login_data = 'ESN={}&TenantMobile={}&UserCode=kispolo&PassWord=F78C36F4B33580EC50670D30C9B2A471'.format(esn,username)
    r = post(login_url, data=login_data, headers=header)
    format_dict = json.loads(r.text)
    print(format_dict['RetMessage'])
    if format_dict['RetCode'] == 0:
        token = format_dict['RetObject']['JWTModelToken']
        return token,esn

    else:
        return None,esn

def DeleteAllGoods():
    token, esn = login('18620241959')
    check_url = 'https://v610api-pc.graspishop.com/apc/BaseInfo/Goods/CanRemoves?goodsids='
    delete_url = 'https://v610api-pc.graspishop.com/APC/BaseInfo/Goods/BatchRemove'
    header = {'Accept': '*/*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
              'Connection': 'keep-alive',
              'client-src':'pcweb',
              'Content-Type': 'application/json',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
              'token':token,
              'esn':esn
              }
    goods_id = load_obj('guanjiapo_goods_id')
    goods_id = [str(i) for i in goods_id]
    id_str = ",".join(goods_id)
    r = get(check_url+id_str, headers=header)
    format_dict = json.loads(r.text)
    suc_id = format_dict['RetObject']['suc']
    suc_id = [str(i) for i in suc_id]
    r = post(delete_url, data='{"goodsid":"'+",".join(suc_id)+'"}', headers=header)
    print(r.text)


def main(json_path_list = ['./data/360che_ershoucar.json','./data/360che_newcar.json','./data/13che_ershoucar.json']):
    token, esn = login('18620241959')
    if token == None:
        return
    # 流式分块取JSON 防止爆内存

    try:
        have_updated = load_obj('guanjiapo_have_updated')
        guanjiapo_goods_id = load_obj('guanjiapo_goods_id')
    except:
        have_updated = set()
        guanjiapo_goods_id = []
    count = 1
    for json_path in json_path_list:
        with open(json_path, 'r', encoding='utf-8') as f:
            objects = ijson.items(f, 'item',multiple_values=True)
            # 这个objects在这里就是相当于一个生成器，可以调用next函数取它的下一个值
            while True:
                try:
                    car = objects.__next__()
                    # 生成配置图
                    GetDetailImage(car['image'][0], car)
                    car['image'].insert(0, "./data/bg.jpg")

                    if car['url'] in have_updated:
                        continue
                    print(car['name'])
                    if '360che_ershoucar' in json_path:
                        car['datasource'] = '360-二手车'
                        car['classid'] = '1017'
                    elif '360che_newcar' in json_path:
                        car['datasource'] = '360-新车'
                        car['classid'] = '1016'
                    elif '13che_newcar' in json_path:
                        car['datasource'] = '13-新车'
                        car['classid'] = '1018'
                    elif '13che_ershoucar' in json_path:
                        car['datasource'] = '13-二手车'
                        car['classid'] = '1019'
                    # print(car)
                    if 'ershou' in json_path:
                        try:
                            car['label'] = car['datasource']+'-' + car['city']
                        except:
                            continue
                    else:
                        try:
                            car['label'] = car['datasource']+'-'+car['品牌']
                        except:
                            continue
                    try:
                        post_ID = PostToGuanjiapo(car,token, esn )
                        guanjiapo_goods_id.append(str(post_ID))
                        have_updated.add(car['url'])
                        if count%50 == 0:
                            save_obj(have_updated,'guanjiapo_have_updated')
                            save_obj(guanjiapo_goods_id,'guanjiapo_goods_id')
                    except:
                        continue
                    count += 1
                except StopIteration as e:
                    print("数据读取完成")
                    break
                except Exception as e:
                    print(car['url'])
                    print(e)
                    continue
    save_obj(have_updated, 'guanjiapo_have_updated')

if __name__ == "__main__":
    # main()
    # token, esn = login('18620241959')
    # DeleteAllGoods(token, esn)
    pass
