# Author: Klaus
# Date: 2020/11/30 20:32
# 本脚本仅供学习，还有待改进
import requests
from lxml import etree
from multiprocessing.dummy import Pool


def get_data(dic):
    lin = dic["lin"]
    item_nam = dic["item_nam"]
    extension = dic["extension"]

    item_data = requests.get(url=lin, headers=headers).content
    item_path = "E:/onedrive-youngklaus/OneDrive - iklaus/Books/" + item_nam + extension
    # print(item_path)

    with open(item_path, "wb") as fp:
        fp.write(item_data)
        print(item_nam + "success!")


if __name__ == "__main__":
    headers = {
        "uer-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

    }
    url1 = "https://kgbook.com/list/index_{}.html"

    for page_number in range(24, 25):#自己改页数
        url = url1.format(page_number)
        params = []
        page = requests.get(url=url, headers=headers)
        page.encoding = "utf-8"
        page_text = page.text
        tree = etree.HTML(page_text)
        div_list = tree.xpath('//div[@class="channel-item"]')
        for div in div_list:

            try:
                item_src = div.xpath('./div[@class="bd"]/h3/a/@href')[0]
                if "http" not in item_src:
                    item_src = "https://kgbook.com" + item_src

                print(item_src)
                # time.sleep(3)
                item = requests.get(url=item_src, headers=headers)
                item.encoding = "utf-8"
                item_text = item.text
                # print(item_text)
                item_tree = etree.HTML(item_text)
                item_name = item_tree.xpath('//h1[@class="news_title"]/text()')[0]
                item_list = item_tree.xpath('//div[@id="introduction"]/a[@class="button"]')

                # link_list = item_tree.xpath('//div[@id="introduction"]/a[@class="button"]/@href')
                # print(link_list)
                # print(item_name)

                for item in item_list:
                    index = item.xpath('./text()')[0]
                    link = item.xpath('./@href')[0]

                    print(index)
                    if '3' in index:
                        extensions = ".azw3"
                    elif ('b' in index) or ('B'in index):
                        extensions = ".epub"
                    elif ('F' in index) or ('f' in index):
                        extensions = ".pdf"
                    elif ("i" in index) or ("I" in index):
                        extensions = ".mobi"
                    else:
                        extensions = ".txt"

                    dic = {
                        "lin": link,
                        "item_nam": item_name,
                        "extension": extensions,
                    }

                    params.append(dic)

            except:
                print("error")
                continue

        print(params)
        pool = Pool()
        pool.map(get_data, params)