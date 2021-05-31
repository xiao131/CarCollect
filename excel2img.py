import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from PIL import Image,ImageDraw,ImageFont

if __name__ == '__main__':
    # 解决 画图中文 方块问题
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    title = "挖掘机小松2小松200进口原版工地车二手"
    desc = "小松200-8原装进口报关车手续齐全合肥本地看车实车实拍非诚勿扰中介勿扰，小松200-8原装进口报关车手续齐全合肥本地看车实车实拍非诚勿扰中介勿扰，小松200-8原装进口报关车手续齐全合肥本地看车实车实拍非诚勿扰中介勿扰，"

    #创建一张空白图片
    img = Image.new('RGB', (800, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("SimHei.ttf", 30, encoding="utf-8")
    title_font = ImageFont.truetype("SimHei.ttf", 40, encoding="utf-8")
    desc_font = ImageFont.truetype("SimHei.ttf", 16, encoding="utf-8")
    #写标题
    draw.text((10, 10), title, (0, 0, 0), font=title_font)
    #写描述
    temp_desc = desc
    row = 1
    while len(temp_desc) > 28:
        if row == 1:
            draw.text((360, 480), temp_desc[:27], (0, 0, 0), font=desc_font)
            temp_desc = temp_desc[27:]
        else:
            draw.text((330, 480+(row-1)*20), temp_desc[:29], (0, 0, 0), font=desc_font)
            temp_desc = temp_desc[29:]
        row += 1
    #写配置
    '''名称： 挖掘机小松2小松200进口原版工地车二手
品牌： 其他
车类型： 工程车
地区： 合肥
卖家信息： 吴先生
价格： 25万
描述： 小松200-8原装进口报关车手续齐全合肥本地看车实车实拍非诚勿扰中介勿扰
车信息： {'出厂年限': '2016年', '小时数': '6580小时', '吨位': '20吨'}'''
    car_info = {"品牌": "其他",
                "车类型": "工程车",
                "价格": "25万",
                "出厂年限": "2016年",
                "吨位": "20吨",
                "小时数": "6580小时",
                "发动机":"YCS04 国六"}
    row = 1
    for key in car_info:
        value = car_info[key]
        draw.text((30, 80+(row-1)*40), key+":"+value, (0, 0, 0), font=font)
        row += 1

    #贴展示图片
    car_img = Image.open("1.jpg")
    h_limit = 400
    #缩小或放大图片
    if car_img.size[1] > h_limit:
        new_h = h_limit
        new_w = int(car_img.size[0] * new_h / car_img.size[1])
        car_img = car_img.resize((new_w,new_h))
    img.paste(car_img,(320,60))

    img.save('bg.jpg')

    exit(0)


    # figsize 指定figure的宽和高，单位为英寸；
    # dpi参数指定绘图对象的分辨率，即每英寸多少个像素，缺省值为80      1英寸等于2.5cm,A4纸是 21*30cm的纸张
    fig = plt.figure(figsize=(3, 3), dpi=350)
    # frameon:是否显示边框
    ax = fig.add_subplot(111, frame_on=False,)
    # 隐藏x轴 y轴
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    # 读取excel
    datas = pd.read_excel('测试.xls')
    datas = datas.iloc[:16, 0:2]
    print(datas)

    # 生成图片
    table(ax, datas,rowLabels=None, colLabels=None, loc='upper center',colWidths=[0.5, 0.5])  # where df is your data frame
    #1、生成表格图片
    plt.savefig('photo.jpg')

    #2、裁剪表格图片


    #3、将表格图片、展示图片、车辆描述、名称 放到一个底图上面。


