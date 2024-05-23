import torch

#check torch-version
print(torch.__version__)

#check can we use gpu
print(torch.cuda.is_available())

#this will reture how much gpus can we use
print(torch.cuda.device_count())

#Check cuda-version
print(torch.backends.cudnn.version())
print(torch.version.cuda)

quit()
