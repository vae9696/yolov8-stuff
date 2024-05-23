from ultralytics import YOLO
# 读取模型，这里传入训练好的模型
model = YOLO("E:/Anacondaa/envs/yv8/CodeSave/yov8/ultralytics-main/runs/detect/train9/weights/best.pt")
 
# 模型预测，save=True 的时候表示直接保存yolov8的预测结果
images = ['CodeSavePlace/data/pred-use/test1.jpg', 
          'CodeSavePlace/data/pred-use/test2.jpg', 
          'CodeSavePlace/data/pred-use/test3.jpg', 
          'CodeSavePlace/data/pred-use/test4.jpg', 
          ]
results = model.predict(images, stream=True, device=0, show=True, save=True)
# 如果想自定义的处理预测结果可以这么操作，遍历每个预测结果分别的去处理
i = 0
for result in results:
    # 获取每个boxes的结果
    box = result.boxes
    # 获取box的位置，
    xywh = box.xywh
    # 获取预测的类别
    cls = box.cls

    i = i+1
    result.show()
    print(box)
    #print(xywh)
    #print(cls)

    # alwasy save to runs/detect/
    #why save 2 files????
    tempname = 'result'+str(i)+'.jpg'
    file_path = 'CodeSavePlace/data/pred-use/res/' + tempname
    result.save(filename=file_path)  # save to disk