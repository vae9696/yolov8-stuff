import os
from ultralytics import YOLO
# 读取模型，这里传入训练好的模型
model = YOLO("runs/detect/train/weights/best.pt")


def predict(images,is_save): # 模型预测，save=True 的时候表示直接保存yolov8的预测结果
    results = model.predict(images, stream=True, device=0, show=True, save=False)
    # 如果想自定义的处理预测结果可以这么操作，遍历每个预测结果分别的去处理
    i = 0
    sum_result = []
    for result in results:
        # 获取每个boxes的结果
        box = result.boxes
        # 获取box的位置，
        #xywh = box.xywh
        # 获取预测的类别
        cls = box.cls
        #result.show()
        #print(box)
        #print(xywh)
        #print(cls)
        # alwasy save to runs/detect/
        if isinstance(images,list):
            tempname = os.path.basename(images[i])
        if isinstance(images,str):
            tempname = os.path.basename(images)
        print("tempameis: {x}".format(x = tempname))
        i = i + 1
        file_path = 'CodeSavePlace/data/pred-use/res/' + tempname
        if is_save:
            result.save(filename=file_path)  # save to disk
        sum_result.append(result.tojson())
    return sum_result
