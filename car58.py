import requests
from bs4 import BeautifulSoup
import re
import base64
from fontTools.ttLib import TTFont
import time
from tqdm import tqdm
import json

#获取Html
def GetHtmlCode(url,Cookie,try_num=0):
    headers = {
        "user-agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
        "Cookie": Cookie,}
        #"Content-Type": "application/x-www-form-urlencoded"}
    try:
        req = requests.get(url, headers=headers)
    except Exception as e:
        print("error2: 网络连接超时",e)
        return None
    if req.status_code != 200:

        print("error1: 打开网页失败，请检查您的网络！")
        if try_num < 3: #如果网络错误，重试3次
            return GetHtmlCode(url, Cookie, try_num + 1)
        return None
    content_html = req.text
    return content_html

#解码 58同城 数字显示
def Get58Num(num = "&#x9a4b;&#x9ea3;"):
    # base_fonts = ['uni9FA4', 'uni9F92', 'uni9A4B', 'uni9EA3', 'uni993C', 'uni958F', 'uni9FA5', 'uni9476', 'uni9F64',
    #               'uni9E3A']
    # base_fonts2 = ['&#x' + x[3:].lower() + ';' for x in base_fonts]  # 构造成 &#x9e3a; 的形式
    base_font = ['&#x9fa4;', '&#x9f92;', '&#x9a4b;', '&#x9ea3;', '&#x993c;', '&#x958f;', '&#x9fa5;', '&#x9476;', '&#x9f64;', '&#x9e3a;']
    base_font = ['','','','','','','','','','','']
    num = num.replace(";","; ")
    num = num.split(" ")
    print(num)
    result = 0
    for n in num:
        for i in range(10):
            if n == base_font[i]:
                result = result*10 + i
                break
    return result

def convertNumber(html_page):
    base_fonts = ['uni9FA4', 'uni9F92', 'uni9A4B', 'uni9EA3', 'uni993C', 'uni958F', 'uni9FA5', 'uni9476', 'uni9F64',
                  'uni9E3A']
    base_fonts2 = ['&#x' + x[3:].lower() + ';' for x in base_fonts]  # 构造成 &#x9e3a; 的形式
    pattern = '(' + '|'.join(base_fonts2) + ')'  #拼接上面十个字体编码

    font_base64 = re.findall("base64,(AA.*AAAA)", html_page)[0]  # 找到base64编码的字体格式文件
    font = base64.b64decode(font_base64)
    with open('58font2.ttf', 'wb') as tf:
        tf.write(font)
    onlinefont = TTFont('58font2.ttf')
    convert_dict = onlinefont['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap  # convert_dict数据如下：{40611: 'glyph00004', 40804: 'glyph00009', 40869: 'glyph00010', 39499: 'glyph00003'
    new_page = re.sub(pattern, lambda x: getNumber(x.group(),convert_dict), html_page)
    return new_page

def getNumber(g,convert_dict):
    key = int(g[3:7], 16)  # '&#x9ea3',截取后四位十六进制数字，转换为十进制数，即为上面字典convert_dict中的键
    number = int(convert_dict[key][-2:]) - 1  # glyph00009代表数字8， glyph00008代表数字7，依次类推
    return str(number)

def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''

def getPinyin(string):
    if string == None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        charLst.append(single_get_first(l))
    return ''.join(charLst)

def CollectSingle(car_link,Cookie):
    try:
        # 单条车信息
        car_single = {}

        car_link = car_link.find("a", target="_blank")
        #print(car_link["href"])
        url_info = car_link["href"]

        data_html = GetHtmlCode(url_info, Cookie)
        if "请输入验证码" in data_html:
            return "访问频繁",None
        if data_html == None:
            return False,None
        # print(data_html)

        data_html = convertNumber(data_html)
        data_html = BeautifulSoup(data_html, "html.parser")

        title = data_html.find("h1", class_="info-title").text
        print("名称：", title)
        brand = title.split(" ")
        if len(brand) == 1:
            brand = "其他"
        else:
            brand = brand[0]
        #print("品牌：", brand)
        # price
        pattern = re.compile(r'____json4fe = {.*}')  # 查找数字
        result = pattern.findall(str(data_html))
        if len(result) > 0:
            result = result[0][14:]
            # print(result)
            result = result.replace("null", "None")
            result = result.replace("true", "True")
            result = result.replace("false", "False")
            result = eval(result)

        # print("车类型：", car_type)
        area = result["locallist"][0]["name"]
        print("地区：", area)
        seller_name = result["linkman"]
        print("卖家信息：", seller_name)
        phone = None
        # phone_url = "https://chephone.58.com/api/detail/phone/get/"+str(result["infoid"])+\
        #         "?clientType="+str(result["rootcatentry"]["dispid"])+"&action=getVC&callback=jQuery18009104542058383776_1621689580910&_=1621690800162"
        # print(phone_url)
        # 车辆信息

        price = None
        price_num = data_html.find("em", class_="info-price_usedcar strongbox").text
        price_unit = data_html.find("b", class_="info-price_unit").text
        price_num = price_num.replace("\n", "")
        price = price_num + price_unit
        print("价格：", price)

        desc = data_html.find("dd", class_="info-usr-desc_cont").text
        desc = desc.replace("\n", "")
        desc = desc.replace(" ", "")
        #print("描述：", desc)

        # 图片列表
        img_list = []
        imgs = data_html.find("div", class_="info-pics h-clearfix")
        imgs = imgs.find_all("img")
        for img in imgs:
            img_url = img["data-original"]
            img_url = img_url.split("?")[0]
            img_list.append(img_url)
        #print("图片列表：", img_list)

        car_single["url"] = url_info
        car_single["name"] = title
        car_single["info"] = desc
        car_single["price"] = price
        car_single["image"] = img_list
        car_single["品牌"] = brand

        car_info = {}
        car_info_html = data_html.find("dl", class_="info-conf")
        car_info_html = car_info_html.find_all("dd")
        for c in car_info_html:
            label = c.find("span", class_="info-conf_label").text
            value = c.find("span", class_="info-conf_value").text
            car_info[label] = value
            car_single[label] = value
        #print("车信息：", car_info)

        return True, car_single

    except Exception as e:
        print(e)
        return "error", car_single

def CollectPage(url_car,Cookie):
    content_html = GetHtmlCode(url_car, Cookie)
    if "请输入验证码" in content_html:
        return False,None

    # print(content_html)
    soup = BeautifulSoup(content_html, "html.parser")

    car_links = soup.find_all("div", class_="info--wrap")
    # print(len(car_links))
    return True,car_links

def Collect(city):
    # 58同城 二手车
    Cookie1 = 'f=n; commontopbar_new_city_info=8728%7C%E5%85%A8%E5%9B%BD%7Cquanguo; f=n; commontopbar_new_city_info=8728%7C%E5%85%A8%E5%9B%BD%7Cquanguo; commontopbar_ipcity=wx%7C%E6%97%A0%E9%94%A1%7C0; time_create=1624258576157; userid360_xml=1C6F7C345E3BF67FEACA7781B6403670; fzq_h=b7ce8b1d7996bf6f4ba538769e61c338_1621665244296_42fc8daac9b34a4b9d86962a5c4e44bc_826441976; sessionid=60893154-450a-4238-8c3c-7a8a96ac35df; id58=c5/nfGCopdwHv6MSL2U7Ag==; 58tj_uuid=d86b5da3-47de-44cf-8d2c-35bacd80a043; wmda_uuid=63d09f4faf599c46f69f7f4dda571ac2; wmda_new_uuid=1; als=0; f=n; gr_user_id=0bfe92c5-5988-4a62-8f77-27a732c42e83; wmda_visited_projects=%3B1732038237441%3B11187958619315; xxzl_deviceid=jpM3DraNrxoxJPMSRi9Qr%2B6wCtJrxpcGj4%2BJ0AqLZqbw%2BTOHPaWowsG%2FVjOIscz6; wmda_session_id_1732038237441=1621687253811-8fe8cedb-763f-d82a; new_uv=4; utm_source=; spm=; init_refer=https%253A%252F%252Fquanguo.58.com%252Fershouche%252F; new_session=0; 58home=wx; city=wx; xxzl_cid=4aa405d2705148d48f0768b73ade5fb4; xzuid=16995c85-c03e-4e53-acd8-4bfdebf62ce4; wmda_session_id_11187958619315=1621688608289-d998f213-aace-b2be; ppStore_fingerprint=82074AF4EFA67B19FB0FBF0CED178E5795345BA0728E59B3%EF%BC%BF1621688673015; gr_session_id_b26c1cbc59d303d8=d99c07d1-8719-4232-80a2-69b378288d65; gr_session_id_b26c1cbc59d303d8_d99c07d1-8719-4232-80a2-69b378288d65=true; xxzl_token="qReyCkomHGAWHQOXB+IJGQElnVs3BOtXRHmBFcqxp15HJihMMVtvKyCh4a6wxnTNin35brBb//eSODvMgkQULA=="; xxzl_sid="undefined"; fzq_js_usdt_infolist_car=61cece06e5616a992826979d319a9ba8_1621688936195_6'
    Cookie2 = 'f=n; commontopbar_new_city_info=93%7C%E6%97%A0%E9%94%A1%7Cwx; time_create=1626428454121; userid360_xml=3FACE3B0EA7304D01AFBE1587FBB82C5; myLat=""; myLon=""; id58=wVPluWDJxxZ7iyYrYDH7eQ==; spm=u-LlFBrx8a1luDwQM.sgppzq_zbt; mcity=wx; f=n; commontopbar_new_city_info=93%7C%E6%97%A0%E9%94%A1%7Cwx; 58home=wx; city=wx; commontopbar_ipcity=wx%7C%E6%97%A0%E9%94%A1%7C0; 58tj_uuid=d38ec230-eeea-42ea-a63d-c91dbd8fb4fc; utm_source=market; new_uv=1; als=0; xxzl_cid=77898cd3892b4935bc775a298f9a97f1; xzuid=2324d1fd-1875-46a0-950c-ec3b4b71e517; wmda_new_uuid=1; wmda_uuid=12fb69a02e57815c0e2761ed91363f43; wmda_session_id_11187958619315=1623836441164-fc199436-b237-a941; fzq_h=cc1f5afe2bba47015723d188e6678205_1623836442670_326c444736164ae6ac0ef84aae683f87_987139655; sessionid=daca027c-413e-498d-b55b-7655d6fe4151; wmda_session_id_1732038237441=1623836443110-bb65b132-eed4-9421; wmda_visited_projects=%3B11187958619315%3B1732038237441; new_session=0; init_refer=; gr_user_id=b9e65bf5-521d-4d52-8ccd-80ffa2bfe5a0; gr_session_id_b26c1cbc59d303d8=a30e1ef2-a90b-4399-807b-383ba31842a2; gr_session_id_b26c1cbc59d303d8_a30e1ef2-a90b-4399-807b-383ba31842a2=true; ppStore_fingerprint=0148FF5E7C9F5FDC67AFBA6A0B0EB34C2E48909511B980AE%EF%BC%BF1623836472666; fzq_js_usdt_infolist_car=0716a44472d98c18e1f8a85a46e2e7e1_1623836479484_7'
    Cookie = Cookie1
    # 1、工程车
    url_engineer_car = "https://quanguo.58.com/cheliangmaimai/pn1/?PGTID=0d30001d-0221-8a2d-e3c0-00094d974a53&ClickID=62&template=new"
    url_truck = "https://quanguo.58.com/huochec/pn1/?PGTID=0d30001d-0221-8a2d-e3c0-00094d974a53&ClickID=54&template=new"
    url_trailer = "https://quanguo.58.com/guache/pn1/?PGTID=0d30001d-0221-8a2d-e3c0-00094d974a53&ClickID=71"

    if city == "全国":
        city = "quanguo"
    elif city == "重庆市":
        city = "cq"
    elif city == "深圳市":
        city = "sz"
    elif "市" in city:
        city = city[:-1]
        city = getPinyin(city)
    else:
        city = getPinyin(city)
    print(city)

    car_list = []
    car_path = './data/13che_ershoucar.json'
    save_num = 0 #保存计数
    for url_num in range(3):
        # 判断是否爬完
        sta_page =1
        # if url_num == 0:
        #     sta_page = 71
        # elif url_num == sta_page:
        #     sta_page = 7

        is_end = False #是否是最后一页
        for page in tqdm(range(1, 100)):
            print("页数：", page)
            save_num += 1

            # 请求数据
            # url_engineer_car = "https://"+city+".58.com/cheliangmaimai/pn" + str(
            #     page) + "/?PGTID=0d30001d-0221-8a2d-e3c0-00094d974a53&ClickID=62&template=new"
            # url_truck = "https://"+city+".58.com/huochec/pn" + str(
            #     page) + "/?PGTID=0d30001d-0221-8a2d-e3c0-00094d974a53&ClickID=54&template=new"
            # url_trailer = "https://"+city+".58.com/guache/pn" + str(
            #     page) + "/?PGTID=0d30001d-0221-8a2d-e3c0-00094d974a53&ClickID=71"
            url_engineer_car = "https://" + city + ".58.com/cheliangmaimai/pn" + str(
                page) + "/"
            url_truck = "https://" + city + ".58.com/huochec/pn" + str(
                page) + "/"
            url_trailer = "https://" + city + ".58.com/guache/pn" + str(
                page) + "/"

            if url_num == 0:
                url_car = url_engineer_car
                car_type = "工程车"
            elif url_num == 1:
                url_car = url_truck
                car_type = "货车"
            else:
                url_car = url_trailer
                car_type = "挂车"
            print(car_type, url_car)

            # 解析数据
            if page % 2 == 1:
                Cookie = Cookie1
            else:
                Cookie = Cookie2
            try:
                try_page_num = 5
                while(1):
                    #获取每一页的详情链接
                    is_success,car_links = CollectPage(url_car, Cookie)
                    # print(len(car_links))
                    if is_success:
                        if len(car_links) == 0:
                            is_end = True
                            print("当前页面无数据")
                        break
                    if car_links == None:
                        print("访问频繁,暂停2分钟,请进行验证,剩余重试次数：",try_page_num)
                        time.sleep(120)

                        break
                    try_page_num -= 1
                    if try_page_num <= 0:
                        break
                cookie_num = 0
                for car_link in car_links:
                    # 进入链接详情页，获取数据
                    try_num = 0 #重试次数\
                    is_continue = False
                    while(1):
                        cookie_num += 1
                        if cookie_num % 2 == 1:
                            Cookie = Cookie1
                        else:
                            Cookie = Cookie2
                        tip, car_single = CollectSingle(car_link,Cookie)
                        # time.sleep(10)

                        if tip == True:
                            car_list.append(car_single)
                            break
                        elif tip == False:
                            print("网络错误,暂停1分钟,请检查您的网络")
                            time.sleep(60)
                        elif tip == "error":
                            print("error001")
                        elif "访问频繁" in tip:
                            print("访问频繁,暂停3分钟,请访问58同城进行验证，或者切换网络，已重试：",try_num)
                            time.sleep(180)

                        try_num += 1
                        if try_num > 5:
                            print("重试5次后未获取数据")
                            break

            except Exception as e:
                print(e)
            if is_end == True:
                break
            #每页保存一次
            # if save_num % 2 == 0:
            with open(car_path, 'a+', encoding='utf-8') as f:
                f.write(json.dumps(car_list, indent=4, ensure_ascii=False))
            print("保存信息至：", car_path)
            car_list = []
            save_num = 0

            # time.sleep(20)

    # if save_num != 0:
    #     with open(car_path, 'a+', encoding='utf-8') as f:
    #         f.write(json.dumps(car_list, indent=4, ensure_ascii=False))
    #     print("保存信息至：", car_path)
    #     del car_list

if __name__ == '__main__':
    # Collect()
    pass
