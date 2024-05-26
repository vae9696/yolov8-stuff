import os, shutil, random
from alive_progress import alive_bar

#ONLY RUN IN F5 (Cause alive_progress can be read as a module just on F5..wTF???)


def DetleImage(img_path,label_path):
    img_list = os.listdir(img_path)
    label_list = os.listdir(label_path)
    loop_range1 = len(label_list)
    with alive_bar(loop_range1,title="Duing file name") as bar:
        for i in range(loop_range1):
            label_list[i] = label_list[i][:-4] + '.jpg'
            bar()


    diff_itemlist = [i for i in img_list if i not in label_list]
    loop_range2 = len(diff_itemlist)
    print("Find {x} diff img".format(x = loop_range2))
    loopn2 = 0
    with alive_bar(loop_range2,title="Deleting diff img") as bar:
        for i in range(loop_range2):
            try:
                remove_imgpath = img_path + '/'+ diff_itemlist[i]
                os.remove(remove_imgpath)
                loopn2+=1
                bar()
            except:
                print("Delete {x} Fail!????WTF???".format(x = diff_itemlist[i]))
                bar()
    print("Delete {x} diff img".format(x = loopn2))

img_path = r'CodeSavePlace/data/images/all_temp'
label_path = r'CodeSavePlace/data/dataset/p1-t1_obj_train_data'

DetleImage(img_path,label_path)
    