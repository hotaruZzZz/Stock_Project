import torch
import numpy as np

x = torch.Tensor([1, 2, 3])
print(f'x: {x}')

y = torch.Tensor([10, 20, 30])
print(f'y: {y}')

z = x + y
print(f'z = x + y: {z}')

z = x.add(y)
print(f'z = x.add(y): {z}')

zz = x.sub(y)
print(zz)