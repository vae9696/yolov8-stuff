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
        #print(request.data)
        img_bdata = request.data
        file_path  = r"CodeSavePlace/data/pred-use/tempsave/comtest1.jpg"
        with open(file_path, "wb") as f: 
            f.write(img_bdata)
            print("image save success!") 
        print(type(request.data))
        #result = str(request.data,encoding="utf-8")
        #print("result is:{r}".format(r = result))
        try:
            total_result = predict(file_path,True)
            print(total_result)
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
            #print(send_result['image0'].keys())
            #print(send_result['image0'][0].keys())
            temp_list = list(send_result['image0'][0].keys())
            #print(temp_list[0])
            #print(send_result['image0'][0][temp_list[0]])
            send_food_name = temp_list[0]
            print("send_food_name is :{n}".format(send_food_name))
            return send_food_name
        except Exception as e:
            print(e)
            return "wtffff"
    else:
        return "method wrong!!, it should be POST!!!!" #methods不为post



app.run(host = '0.0.0.0')
