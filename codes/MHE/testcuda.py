import torch

print(torch.cuda.nccl.version())
print(torch.cuda.is_available())
print(torch.version.cuda)
print(torch.cuda.get_device_name(0))


# nvcc --version
# nvcc version in cmd