from PIL import Image,ImageDraw,ImageFont
from requests import get

#生成配置图
def GetDetailImage(img_url,car_info,save_path="./data/bg.jpg"):
    # 解决 画图中文 方块问题
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    title = car_info["name"]
    try:
        desc = car_info["info"]
    except:
        desc = car_info["name"]

    # 创建一张空白图片
    img = Image.new('RGB', (800, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("SimHei.ttf", 30, encoding="utf-8")
    title_font = ImageFont.truetype("SimHei.ttf", 40, encoding="utf-8")
    desc_font = ImageFont.truetype("SimHei.ttf", 16, encoding="utf-8")

    # # 获取一张没有水印的图,贴展示图片
    # car_img = Image.open("1.jpg")
    # 读取在线图片并且裁剪保存本地
    Hostreferer = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    html = get(img_url, headers=Hostreferer)
    img_type = img_url.split('.')[-1]
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
    # temp_path = './data/temp.' + img_type
    # img_2.save(temp_path)
    car_img = img_2

    h_limit = 400
    # 缩小或放大图片
    if car_img.size[1] > h_limit:
        new_h = h_limit
        new_w = int(car_img.size[0] * new_h / car_img.size[1])
        car_img = car_img.resize((new_w, new_h))
    img.paste(car_img, (320, 60))

    # 写标题
    draw.text((10, 10), title, (0, 0, 0), font=title_font)
    # 写描述
    temp_desc = desc
    row = 1
    while True:
        if row == 1:
            draw.text((360, 480), temp_desc[:27], (0, 0, 0), font=desc_font)
            temp_desc = temp_desc[27:]
        else:
            draw.text((330, 480 + (row - 1) * 20), temp_desc[:29], (0, 0, 0), font=desc_font)
            temp_desc = temp_desc[29:]
        row += 1

        if len(temp_desc) <= 28:
            break

    #判断新车还是二手车
    try:
        temp = car_info["detail"]
        car_info = car_info["detail"]["1"]
    except:
        pass
    # 写配置
    setting_path = './data/配置图.txt'
    f = open(setting_path, 'r',encoding="utf8")
    setting_item = f.read()
    f.close()
    # print(setting_item)
    setting_item = setting_item.split('\n')
    # print(setting_item)

    row = 1
    for key in car_info:
        if key == "url" or key == "name" or key == "info" or key == "price" or key == "image":
            continue
        value = car_info[key]
        if "：" in key:
            key = key.replace("：","")
        #如果没有设置配置图，则跳过
        if key not in setting_item:
            continue
        draw.text((30, 80 + (row - 1) * 40), key + ":" + value, (0, 0, 0), font=font)
        row += 1

    img.save(save_path)

if __name__ == '__main__':
    car_info = {
        "url": "https://tao.360che.com/m423047_index.html",
        "name": "上汽通用五菱 五菱荣光 105马力",
        "info": "五菱柳机/2.7m/20年4月/成都市",
        "price": "4.28万",
        "image": [
            "https://img7.kcimg.cn/uploads/2021/427//6b473d1090d34269897c503cf97fd96c.jpg_750x500.jpg",
            "https://img7.kcimg.cn/uploads/2021/427//e6b476371ada42c39937cc22bbe02c4c.jpg_750x500.jpg",
            "https://img7.kcimg.cn/uploads/2021/427//3bcd5428d18b4de7b053b341cf6cae83.jpg_750x500.jpg",
            "https://img7.kcimg.cn/uploads/2021/427//46978e5be0af4550933edf2df6978a0b.jpg_750x500.jpg",
            "https://img7.kcimg.cn/uploads/2021/427//c4f9f237c38b4cc6a768eab234fe73d3.jpg_750x500.jpg",
            "https://img7.kcimg.cn/uploads/2021/427//ab550068346a42caa519eff6ece51c47.jpg_750x500.jpg"
        ],
        "品牌": "五菱柳机",
        "品牌：": "上汽五菱",
        "上牌时间：": "2020年04月",
        "车系：": "五菱荣光",
        "吨位级别：": "微卡",
        "货箱长度：": "2.7",
        "货箱形式：": "栏板式",
        "变速箱挡位：": "5挡",
        "发动机品牌：": "五菱柳机",
        "驱动形式：": "4X2",
        "排放标准：": "国五",
        "马力：": "105马力"
    }

    GetDetailImage(img_url="https://img7.kcimg.cn/uploads/2021/427//6b473d1090d34269897c503cf97fd96c.jpg_750x500.jpg",
                   car_info=car_info,save_path="./data/bg.jpg")


