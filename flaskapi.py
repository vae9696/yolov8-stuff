import sys
import os
sys.path.append(os.getcwd())
import json
from flask import Flask,request,jsonify
from Predict.predict import predict

UPLOAD_FOLDER = r"CodeSavePlace\data\pred-use\tempsave" #上传文件储存目录
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} #允许上传的文件扩展名的集合。

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
Content-type = multipart/form-data
"""

def allowed_file(filename): #检查文件扩展名是否合法
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""
API接口要求:
Headers = {
    "Content-Type" : "multipart/form-data",
}

for-data:{
    numbers: 图片数量
    imagex(x由1~numbers) : xxxxjpg/png/jpeg(文件,not str)
}
"""

@app.route("/CallPredic",methods = ["POST"]) #API接口
def CallPredict():
    if request.method == 'POST':
        if request.values.get("numbers"): #判断是否有numbers字段
            print("User send {x} images.".format(x = request.values.get("numbers")))
            numbers = int(request.values.get("numbers"))
            images = []
            for i in range(1,numbers+1): 
                tempstr = "image" + str(i)
                if request.files.get(tempstr): #判断是否有imagex字段
                    result = request.files.get(tempstr)
                    if(allowed_file(result.filename)): #检查文件扩展名是否合法
                        result.save(os.path.join(app.config['UPLOAD_FOLDER'], result.filename))  #暂存图片
                        print("Save image: {x}".format(x = result.filename))
                        images.append(r'CodeSavePlace/data/pred-use/tempsave/' + result.filename) #暂存图片路由
                    else:
                        print("{x} is not corrrect in ALLOWED_EXTENSIONS".format(x = result.filename))
                        return jsonify(Error_msg = "{x} is not corrrect in ALLOWED_EXTENSIONS".format(x = result.filename)) #文件扩展名不合法
                else:
                    temp_delete = os.listdir(r'CodeSavePlace/data/pred-use/tempsave') #暂存刪除图片路由
                    for res_file_name in temp_delete:
                        os.remove(r'CodeSavePlace/data/pred-use/tempsave/'+res_file_name) #刪除暂存图片
                    print("Cant get key {x} data".format(x = tempstr))
                    return jsonify(Error_msg = "Cant get key {x} data".format(x = tempstr)) #没有这个imagex字段, 取值失败
            try:
               total_result = predict(images,True)
               send_result = {} #返回结果容器
               for i in range(0,len(total_result)): #构建结果容器(dict)字段
                    send_result.setdefault("image"+str(i),{})
                    res = json.loads(total_result[i])
                    j = 0
                    for r in res:
                        print("{i} -- {name} : {confidence}".format(i = i, name = r["name"], confidence = r["confidence"]))
                        send_result["image"+str(i)].setdefault(j,{r["name"] : r["confidence"]})
                        j = j + 1
               print("Find result is:")
               print(send_result)
               send_result = json.dumps(send_result) #转化为json数据(dict -> json)
               for i in range(len(images)): #刪除暂存图片
                   os.remove(images[i])
               return send_result  #返回结果
            except Exception as e: #检测Error
                print("Predict function error!!!")
                print(e)
                return jsonify(Error_msg = "Predict function error!!!")

        else:
            print("Don't know user send how much images") #没有numbers字段
            return jsonify(Error_msg = "You need to send numbers of how many images.")
    else:
        return jsonify(msg = "method wrong!!, it should be POST!!!!") #methods不为post



app.run(host = '0.0.0.0')
