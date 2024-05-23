import requests
import json
import io
import os
import sys
import threading
import urllib
from urllib import parse
from re import sub


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')  #改变标准输出的默认编码


def decode_url(url):
    """
    对百度加密后的地址进行解码
    :param url:百度加密的url
    :return:解码后的url
    """
    table = {'w': "a", 'k': "b", 'v': "c", '1': "d", 'j': "e", 'u': "f", '2': "g", 'i': "h",
             't': "i", '3': "j", 'h': "k", 's': "l", '4': "m", 'g': "n", '5': "o", 'r': "p",
             'q': "q", '6': "r", 'f': "s", 'p': "t", '7': "u", 'e': "v", 'o': "w", '8': "1",
             'd': "2", 'n': "3", '9': "4", 'c': "5", 'm': "6", '0': "7",
             'b': "8", 'l': "9", 'a': "0", '_z2C$q': ":", "_z&e3B": ".", 'AzdH3F': "/"}
    url = sub(r'(?P<value>_z2C\$q|_z\&e3B|AzdH3F+)', lambda matched: table.get(matched.group('value')), url)
    return sub(r'(?P<value>[0-9a-w])', lambda matched: table.get(matched.group('value')), url)


def SaveImages(inputurl,user_agent,save_path,save_name):
    requests.packages.urllib3.disable_warnings()
    requests.Session().keep_alive = False
    url = inputurl
    user_agent = user_agent
    headers = {
        "User-Agent":user_agent,
        'Connection':'close'
    }
    try:
        response = requests.get(url, headers=headers)
        file_path = os.path.join(save_path, save_name)
        directory = os.path.dirname(file_path)
        if( not os.path.exists(directory)):
            os.makedirs(directory)
        with open(file_path,"wb") as file:
                file.write(response.content)
        #print("{i} Success download:".format(i = save_name))
        #print(url)
        response.close()
    except:
        print("Conntect WRONG!!!:{i} ".format(i = url))

def Get_baidu_images_url(keyword,pages_number,save_path):
    temp_key = keyword
    keyword = urllib.parse.quote(keyword) #在转换成URL编码后，密文的字母都为大写
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    host = "image.baidu.com"
    referer = "https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDEsMiw2LDQsNSw3LDgsOQ%3D%3D&word=%E5%B7%A7%E5%85%8B%E5%8A%9B"
    headers = {
        "Host":host,
        "User-Agent":user_agent,
        "Referer":referer,
    }
    #print(result['data'][0]['objURL'])
    #print(decode_url(result['data'][0]['objURL']))
    # result['data'][30] always is empty
    if pages_number >= 2:
        loop_number = 1
        for i in range(1,pages_number+1):
            pages = 30 + i * 30
            url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=9702419668007270257&ipn=rj&ct=201326592&is=&fp=result&fr=&word={word}&queryWord={queryword}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn={pages}&rn=30&gsm=3c&1716458353246=".format(word = keyword, queryword = keyword, pages = pages)
            #print(url)
            response = requests.get(url, headers=headers)  
            response.encoding = "uft-8"
            content = response.text
            try:
                cj = response.json()
            except:
                print("response.json() is error")
            #print(cj)
            try:
                result = json.loads(content.replace('\\','\\\\'), strict=False)
            except:
                result = cj
            for j in range(0,len(result['data'])-1):
                save_name = str(loop_number) + '.jpg'
                loop_number+=1
                SaveImages(result['data'][j]['thumbURL'],user_agent,save_path,save_name)
            print("{name} dow {x}/{y}".format(name = temp_key, x = i, y = pages_number))
            response.close()
    else:
        pages = 60
        url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=9702419668007270257&ipn=rj&ct=201326592&is=&fp=result&fr=&word={word}&queryWord={queryword}&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn={pages}&rn=30&gsm=3c&1716458353246=".format(word = keyword, queryword = keyword, pages = pages)
        response = requests.get(url, headers=headers)  
        response.encoding = "uft-8"
        content = response.text
        try:
            cj = response.json()
        except:
            print("response.json() is error")
        #print(cj)
        try:
            result = json.loads(content.replace('\\','\\\\'), strict=False)
        except:
            result = cj
        #print(url)
        #print(len(result['data']))
        for i in range(0,len(result['data'])-1):
            save_name = str(i+1) + '.jpg'
            SaveImages(result['data'][i]['thumbURL'],user_agent,save_path,save_name)
        response.close()

    

#Get_baidu_images_url("薯片",1,'CodeSavePlace\data\images\Chocolate')
    
Thread1 = threading.Thread(target=Get_baidu_images_url,
                           kwargs={
                                 "keyword" : "巧克力",
                                 "pages_number" : 7,
                                 "save_path" : 'CodeSavePlace\data\images\Chocolate'
                             }
                           )
                           
Thread2 = threading.Thread(target=Get_baidu_images_url,
                           kwargs={
                                 "keyword" : "薯片",
                                 "pages_number" : 7,
                                 "save_path" : 'CodeSavePlace\data\images\Pot_chip'
                             }
                           )

Thread3 = threading.Thread(target=Get_baidu_images_url,
                           kwargs={
                                 "keyword" : "米饭",
                                 "pages_number" : 7,
                                 "save_path" : r'CodeSavePlace\data\images\Rice'
                             }
                           )

Thread4 = threading.Thread(target=Get_baidu_images_url,
                           kwargs={
                                 "keyword" : "小泡芙食物",
                                 "pages_number" : 7,
                                 "save_path" : r'CodeSavePlace\data\images\Popfu'
                             }
                           )    

Thread5 = threading.Thread(target=Get_baidu_images_url,
                           kwargs={
                                 "keyword" : "香蕉",
                                 "pages_number" : 7,
                                 "save_path" : r'CodeSavePlace\data\images\Banana'
                             }
                           )

Thread6 = threading.Thread(target=Get_baidu_images_url,
                           kwargs={
                                 "keyword" : "蛋糕",
                                 "pages_number" : 7,
                                 "save_path" : r'CodeSavePlace\data\images\Cake'
                             }
                           )

#Thread1.start()
#Thread2.start()
#Thread3.start()
#Thread4.start()
#Thread5.start()
#Thread6.start()

