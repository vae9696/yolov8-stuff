import fiftyone as fo
import fiftyone.zoo as foz


if __name__ == '__main__':
    dataset_test = foz.load_zoo_dataset(
        "open-images-v7",
        split="test",
        classes=["Food"],
        max_samples=1,
        only_matching=True,  
        label_types=["detections"],  # 指定下载目标检测的类型,detections,
        dataset_dir='CodeSavePlace/v7-dow/dw1',# 保存的路径
    )
