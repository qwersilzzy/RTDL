# import torch
# print(torch.cuda.is_available())
# print(torch.version.cuda)
# print(torch.cuda.get_device_name(0))
# print(torch.cuda.nccl.version())

# nvcc --version
# nvcc version in cmd


import torch
import torch.nn as nn

# Assuming you have a model architecture defined as 'YourModelClass'
class YourModelClass(nn.Module):
    # Your model definition here...
    pass

model = YourModelClass()
checkpoint = torch.load('path_to_your_model.th')
model.load_state_dict(checkpoint)

# Create dummy input data that matches the input shape of your model.
# This is needed for tracing the model architecture.
dummy_input = torch.randn(1, C, H, W)  # Modify the shape based on your model's input

# Convert and save the model to ONNX format
torch.onnx.export(model, dummy_input, 'path_to_output_model.onnx')
