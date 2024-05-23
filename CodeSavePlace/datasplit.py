import os, shutil, random
from tqdm import tqdm

"""
标注文件是yolo格式（txt文件）
训练集：验证集：测试集 （7：2：1） 
"""


def split_img(img_path, label_path, split_list):
    try:
        Data = 'CodeSavePlace/data/dataset'
        # Data是你要将要创建的文件夹路径
        # os.mkdir(Data)

        train_img_dir = Data + '/images/train'
        val_img_dir = Data + '/images/val'
        test_img_dir = Data + '/images/test'

        train_label_dir = Data + '/labels/train'
        val_label_dir = Data + '/labels/val'
        test_label_dir = Data + '/labels/test'

        # 创建文件夹
        os.makedirs(train_img_dir)
        os.makedirs(train_label_dir)
        os.makedirs(val_img_dir)
        os.makedirs(val_label_dir)
        os.makedirs(test_img_dir)
        os.makedirs(test_label_dir)

    except:
        print('file dir already exist')

    train, val, test = split_list
    all_img = os.listdir(img_path) 

    #os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。
    #img_path+img in all_img list
    all_img_path = [img_path + '/'+ img for img in all_img]
    
    #all_label = os.listdir(label_path)
    #all_label_path = [os.path.join(label_path, label) for label in all_label]

    #sample(list, k)返回一个长度为k新列表，新列表存放list所产生k个随机唯一的元素
    train_img = random.sample(all_img_path, int(train * len(all_img_path)))

    #train_img_copy = [os.path.join(train_img_dir, img.split('\\')[-1]) for img in train_img]
    #train_label = random.sample(all_label_path, int(train * len(all_label_path)))

    train_label = [toLabelPath(img, label_path) for img in train_img]
    #train_label_copy = [os.path.join(train_label_dir, label.split('\\')[-1]) for label in train_label]


    for i in tqdm(range(len(train_img)), desc='train ', ncols=80, unit='img'): #ncols-固定总长度, unit='x'表示进度条的单位是x
        _copy(train_img[i], train_img_dir)
        _copy(train_label[i], train_label_dir)
        all_img_path.remove(train_img[i])
    
    val_img = random.sample(all_img_path, int(val / (val + test) * len(all_img_path))) #cause all_img_path remove some imgs,so number will change
    val_label = [toLabelPath(img, label_path) for img in val_img]
    for i in tqdm(range(len(val_img)), desc='val ', ncols=80, unit='img'):
        _copy(val_img[i], val_img_dir)
        _copy(val_label[i], val_label_dir)
        all_img_path.remove(val_img[i])
    
    test_img = all_img_path
    test_label = [toLabelPath(img, label_path) for img in test_img]
    for i in tqdm(range(len(test_img)), desc='test ', ncols=80, unit='img'):
        _copy(test_img[i], test_img_dir)
        _copy(test_label[i], test_label_dir)


def _copy(from_path, to_path):
    shutil.copy(from_path, to_path)


def toLabelPath(img_path, label_path):
    img = img_path.split('/')[-1]
    #['CodeSavePlace', 'data', 'images', 'Eggs', '137077659_ca70ad7c0c_z.jpg'] [-1] = '137077659_ca70ad7c0c_z.jpg'
    label = img.split('.jpg')[0] + '.txt'
    #['137077659_ca70ad7c0c_z', ''] [0] = '137077659_ca70ad7c0c_z'
    result = label_path + '/' + label
    return result



img_path = 'CodeSavePlace/data/images/all_temp'  # 你的图片存放的路径
label_path = 'CodeSavePlace/cavtdata/Egg-Vegetable-Bakedgoods/obj_train_data'  # 你的txt文件存放的路径
split_list = [0.7, 0.2, 0.1]  # 数据集划分比例[train:val:test]
split_img(img_path, label_path, split_list)



"""
首先定义了一个split_img函数，它接受三个参数：img_path表示图片文件夹的路径，label_path表示Yolo格式标注文件的路径，split_list是一个包含三个数值的列表，
表示训练集、验证集和测试集所占比例。这个函数的功能包括创建用于存放训练集、验证集和测试集图片和标签的文件夹，然后进行文件的复制和移动操作。

在split_img函数内部，首先创建了用于存放训练集、验证集和测试集图片和标签的文件夹，然后通过随机抽样的方式，将所有的图片分配到训练集、验证集和测试集，
并将它们复制到对应的文件夹中。在这个过程中，使用了os模块来进行文件夹的创建和文件的复制，使用了random模块来进行随机抽样，
还用到了tqdm模块来展示进度条，使得在处理大量文件时可以清晰地看到进度。

在代码中还定义了_copy函数和toLabelPath函数，_copy函数用于将文件从一个路径复制到另一个路径，toLabelPath函数用于根据图片路径生成对应的标注文件路径。
最后，在if __name__ == '__main__':部分，指定了图片文件夹的路径、Yolo格式标注文件的路径和数据集划分比例，然后调用split_img函数进行数据集划分。
"""
