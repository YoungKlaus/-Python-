# Author: Klaus
# Date: 2020/11/29 17:52
# 本脚本仅供学习，还有待改进
import requests
from lxml import etree

if __name__ == "__main__":
    headers = {
        "uer-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"

    }
    url1 = "https://kgbook.com/list/index_{}.html"

    for page_number in range(24, 84):# 2-84是全站
        url = url1.format(page_number)

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

                    # print(index)
                    if '3' in index:
                        extensions = ".azw3"
                    elif 'i' or 'I' in index:
                        extensions = ".mobi"
                    elif 'b' or 'B' in index:
                        extensions = ".epub"
                    elif 'F' or 'f' in index:
                        extensions = ".pdf"
                    else:
                        extensions = ".txt"
                    item_data = requests.get(url=link, headers=headers).content
                    item_path = "E:/onedrive-youngklaus/OneDrive - iklaus/Books/" + item_name + extensions
                    # print(item_path)

                    with open(item_path, "wb") as fp:
                        fp.write(item_data)
                        print(item_name + "success!")
            except:
                print("error")
                continue

