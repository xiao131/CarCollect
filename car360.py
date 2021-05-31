from urllib import request
from urllib import error
from bs4 import BeautifulSoup as BS
from urllib.parse import quote
import pickle
import json
from tqdm import tqdm

def save_obj(obj, name):
    with open('./data/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('./data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# 得到网页源代码
# 参数：网址
# 返回：网页源代码
def GetHtmlCode(url, headers = None):
    # 解析网页
    try:
        # print(url)
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        #     , "Cookie": cookie}
        headers = [("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0")
                   ]
        opener = request.build_opener()
        opener.addheaders = headers
        file = opener.open(url)
        content_html = file.read()
        opener.close()
        # print(content_html)
        # response = urllib.request.urlopen(url)
    except error.URLError as e:
        print("error2: 网络连接超时", e)
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


def get_Ershou_Detail(car_list):
    global all_pingpai_set
    for car in tqdm(car_list, desc="开始爬取二手车具体信息",ncols=100):
        html_content = GetHtmlCode(car['url'])
        soup = BS(html_content, 'html.parser', from_encoding='utf-8')
        parameter_detail = soup.find('div', class_='truck-detail container')
        ui_list = parameter_detail.find('div',class_ = 'slider-content').find('ul',class_='list')
        image_list = []
        for i,ui in enumerate(ui_list.find_all('li')):
            image_list.append(ui.find('img')['data-src'])
            if i >= 8 :
                break
        car['image'] = image_list
        truck_detail = parameter_detail.find('div',class_ = 'truck-info clearfix')
        for detail in truck_detail.find_all('div',class_='list clearfix'):
            title = detail.find('div',class_='title').get_text().replace(' ','').replace('\n','')
            info = detail.find('div',class_='detail').get_text().replace(' ','').replace('\n','')
            if '品牌' in title:
                car['品牌'] = info
                all_pingpai_set.add(car['品牌'])
            else:
                car[title] = info

    print('所有信息爬取完成')
    return car_list


def get_Newcar_Detail(car_list):
    count = 0
    for car in tqdm(car_list,desc="开始爬取新车具体信息",ncols=100):
        count+=1
        html_content = GetHtmlCode(car['url'])
        soup = BS(html_content, 'html.parser', from_encoding='utf-8')
        parameter_detail = soup.find('div',class_ = 'parameter-detail')
        car_detail_dict = {}
        car_names = parameter_detail.find('tr',id='fixed_top').find_all('th')
        for i in range(1,len(car_names)):
            car_detail_dict[i] = car_detail_dict.get(i, {})
            car_detail_dict[i]['name'] = car_names[i].find('a').get_text().replace('\n','').strip()


        param_rows = parameter_detail.find_all('tr',class_ = 'param-row')
        for param in param_rows:
            tds = param.find_all('td')
            name = tds[0].get_text()
            for i in range(1,len(tds)):
                car_detail_dict[i][name] = tds[i].get_text().replace('\n','').strip()

        # print(car_detail_dict)
        car['detail'] = car_detail_dict


    print('所有信息爬取完成')
    return car_list

def get_Ershou_Url(region,page_end = 1,page_strat = 1):
    region_url = 'https://tao.360che.com/'+region+'/{}.html'
    print('当前爬取：' + region_url)
    ershou_car_list = []
    for i in tqdm(range(page_strat,page_end+1),desc="获取所有二手车链接",ncols=100):
        html_content = GetHtmlCode(region_url.format(i))
        soup = BS(html_content, 'html.parser', from_encoding='utf-8')
        try:
            content = soup.find('div', class_='truck-list-list')
        except:
            print('所有车的URL爬取完成')
            break

        this_page_cars = content.find_all('a',class_ = 'truck-truck-content')
        for car in this_page_cars:
            car_detail = {}
            car_detail['url'] = 'https://tao.360che.com' + car['href']
            car_detail['name'] = car.find('div',class_ = 'title').get_text().replace('\n','').strip()
            car_detail['info'] = car.find('div',class_ = 'info').get_text().replace('\n','').strip()
            car_detail['price'] = car.find('div', class_='price').get_text().replace('\n','').strip()
            # car_detail['品牌'] = car_detail['info'].split('/')[0]
            car_detail['datasource'] = '360-二手车'
            ershou_car_list.append(car_detail)

    return ershou_car_list


def get_Newcar_Url(page_end = 1,page_strat = 1):
    URL = ['https://product.360che.com/p51112/{}.html','https://product.360che.com/p51112_s3/{}.html']
    global all_pingpai_set
    car_list = []

    for url in URL:
        print('当前爬取：'+ url)
        for i in tqdm(range(page_strat,page_end+1),desc="获取所有新车链接",ncols=100):
            html_content = GetHtmlCode(url.format(i))
            soup = BS(html_content, 'html.parser', from_encoding='utf-8')
            try:
                content = soup.find('div',class_ = 'content')
            except:
                print('所有车的URL爬取完成')
                break
            this_page_cars = content.find_all('li',class_='modular')
            for car in this_page_cars:
                car_detail = {}
                #
                href_list = car.find('div',class_= 'config').find_all('p')[3].find_all('a')
                need_href = ''
                for href in href_list:
                    if '国六' in href.get_text():
                        need_href = href['href']
                        break
                if need_href == '':
                    continue
                # href = car.find('a',class_ = 'figure')['href']

                # 'price/c1_s64_b8_s6662_p7%E5%9B%BD%E5%85%AD.html'
                # href = href.split('_')[:-1]+['param.html']
                # href = "_".join(href)
                car_detail['url'] = 'https://product.360che.com'+ quote(need_href)


                name = car.find('div',class_= 'price-wrap temporary').find('tbody').find('td').find('a').get_text().replace('\n','').strip()
                # name = car.find('h2').get_text().replace(' ','').replace('\n','')
                car_detail['name'] = name
                car_detail['品牌'] = name.split(' ')[0]
                all_pingpai_set.add(car_detail['品牌'])
                img_path = car.find('img')['src']
                car_detail['image'] = [img_path]
                car_detail['datasource'] = '360-新车'
                car_list.append(car_detail)

    return car_list

def get_City():
    url = 'https://tao.360che.com/'

    ershou_car_list = []

    html_content = GetHtmlCode(url)
    soup = BS(html_content, 'html.parser', from_encoding='utf-8')
    city_list = soup.find('div',class_='city-list')
    city_code = {}
    for city in city_list.find_all('div',class_='city-click text'):
        name = city.find('a').get_text().replace(' ','').replace('\n','')
        code = city.find('a')['data-pinyin']
        city_code[name] = code

    return city_code

def Collect(city):
    # 得到所有城市code  {'成都':code,...}
    city_code = get_City()
    all_pingpai_set = set()
    before_i = 1
    start_page = 1
    end_page = 500
    for i in tqdm(range(1, 500, 10), desc='总页数', ncols=100):
        try:
            all_pingpai_set = load_obj('pingpai_set')
        except:
            pass
        ershouche_list = get_Ershou_Url(city_code[city], page_strat=before_i, page_end=i)
        ershouche_list = get_Ershou_Detail(ershouche_list)

        ershoucar_path = './data/360che_ershoucar.json'
        with open(ershoucar_path, 'a+', encoding='utf-8') as f:
            f.write(json.dumps(ershouche_list, indent=4, ensure_ascii=False))
        print("保存信息至：", ershoucar_path)

        car_list = get_Newcar_Url(page_strat=before_i, page_end=i)
        car_list = get_Newcar_Detail(car_list)

        newcar_path = './data/360che_newcar.json'
        with open(newcar_path, 'a+', encoding='utf-8') as f:
            f.write(json.dumps(car_list, indent=4, ensure_ascii=False))
        print("保存信息至：", newcar_path)

        before_i = i
        save_obj(all_pingpai_set, 'pingpai_set')
        del ershouche_list
        del car_list

if __name__ == '__main__':
    pass
