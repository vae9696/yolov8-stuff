import requests
import json
import pandas as pd
import cv2 as cv
import os
import threading

def GetImages(inputurl,category,savefile,
              user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
              saveimagesnumber=100):
    url = inputurl
    headers = {
        'User-Agent': user_agent
    }
    response = requests.get(url, headers=headers)  
    content = response.text
    result = json.loads(content)
    #test2 = result['000151d10b95b4d3']['image_labels']
    loop_number = 0
    for key in result:
        temp1 = result[key]['image_labels']
        for i in range(0,len(temp1)):
            temp2 = temp1[i]
            if temp2['category'] == category and temp2['confidence'] == 1:
                #print(result[key]['image']["url"])
                image_savename = os.path.basename(result[key]['image']["url"])
                #'CodeSavePlace\data\images\getimagesave'
                save_path = savefile
                file_path = os.path.join(save_path, image_savename)
                print(file_path)
                directory = os.path.dirname(file_path)
                if( not os.path.exists(directory)):
                    os.makedirs(directory)
                image_url = result[key]['image']["url"]
                image_headers = {
                    'User-Agent': user_agent,
                    }
                image_response = requests.get(image_url,headers=image_headers)
                try:
                    with open(file_path,"wb") as file:
                        file.write(image_response.content)
                    loop_number = loop_number + 1
                    print(loop_number)
                except:
                    print("Save Wrong,skip one round")
                if(loop_number == saveimagesnumber):
                    quit()

#Python 中有两种实现多线程的方式，分别是 threading 和 multiprocessing 模块。它们的主要区别如下：
"""
1.实现方式不同
threading 是基于线程的多任务处理模块，它使用共享内存来实现多线程，因此所有线程都可以访问相同的变量和数据结构。
multiprocessing 是基于进程的多任务处理模块，它使用子进程来实现多线程，子进程之间独立运行，各自拥有自己的变量和数据结构。

2. 适用场景不同
由于 multiprocessing 使用独立的进程而非线程来运行多个任务，因此它更适合用于 CPU 密集型任务，如数值计算、图像处理等需要大量计算资源的场景。
threading 适用于 I/O 密集型任务，如网络请求、文件读写等需要等待 I/O 操作完成的场景。
"""


#如果需要传递参数的话，args 是固定参数，kwargs 是可变参数,args接收tuple，kwargs接收dict
#Egg-Vegetable-Bakedgoods
#Egg,Vegetable,Bakedgoods
Egg_thread = threading.Thread(target=GetImages,
                             kwargs={
                                 "inputurl" : "https://storage.googleapis.com/openimages/web_v6/visualizer/annotations_detection_train/_m_033cnk.json",
                                 "category" : "Egg (Food)",
                                 "savefile" : 'CodeSavePlace\data\images\Eggs'
                             }
                             )

Vegetable_thread = threading.Thread(target=GetImages,
                                   kwargs={
                                       "inputurl" : "https://storage.googleapis.com/openimages/web_v6/visualizer/annotations_detection_train/_m_0f4s2w.json",
                                       "category" : "Vegetable",
                                       "savefile" : 'CodeSavePlace\data\images\Vegetable'
                                   }
                                   )

Bakedgoods_thread = threading.Thread(target=GetImages,
                                    kwargs={
                                        "inputurl" : "https://storage.googleapis.com/openimages/web_v6/visualizer/annotations_detection_train/_m_052lwg6.json",
                                        "category" : "Baked goods",
                                        "savefile" : 'CodeSavePlace\data\images\Bakedgoods'
                                    }
                                    )

Egg_thread.start()
Vegetable_thread.start()
Bakedgoods_thread.start()

#result_keys = list(result.keys())
#print(test2['000151d10b95b4d3']['image_labels'])