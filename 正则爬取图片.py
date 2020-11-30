# Author: Klaus
# Date: 2020/11/28 16:14


import requests
import os
import re
import ssl

if __name__ == "__main__":


    url = "https://www.flaticon.com/search"
    headers = {
        "uer-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
    kw = input("请输入关键字：")
    params = {
        "word": kw
    }
    if not os.path.exists("./Data/icon/"+kw):
        os.mkdir("./Data/icon/"+kw)

    '''
    proxy = {
        "http": "http://127.0.0.1:7890",
        "https": "https://127.0.0.1:7890"
    }
    '''
    page_text = requests.get(url=url, params=params, headers=headers).text
    # ex = '<a class="shot-thumbnail-link dribbble-link js-shot-thumbnail-link" href="(.*?)">.*?</a>'
    # print(page_text)
    ex = '<div class="icon--holder.*?data-src="(.*?)".*?</div>'
    img_src_list = re.findall(ex, page_text, re.S)
    # print(img_src_list)

    for src in img_src_list:
        # src="https://dribbble.com"+src
        get_data = requests.get(url=src, headers=headers).content
        data_name = src.split("/")[-1]
        data_path = "./Data/icon/" + kw + "/" + data_name
        with open(data_path, "wb", ) as fp:
            fp.write(get_data)
            print(data_name + " success!")
