from ultralytics import YOLO


def t_val():
    # Load a model
    model = YOLO('runs/detect/train9/weights/best.pt')  # load a custom model

    # Validate the model
    if __name__ == '__main__':
        metrics = model.val(device = 0)  # no arguments needed, dataset and settings remembered
        print(metrics.box.map)    # map50-95
        print(metrics.box.map50)  # map50
        print(metrics.box.map75)  # map75
        print(metrics.box.maps)  # a list contains map50-95 of each category

# Load a model
def t_train():
    model = YOLO("yolov8s.yaml")  # build a new model from scratch

    if __name__ == '__main__':
        # Use the model
        model.train(data='CodeSavePlace/t1setting.yaml', epochs=50)  # train the model


t_train()