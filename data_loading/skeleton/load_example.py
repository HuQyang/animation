import pickle
from save_animation import *

with open('./mydata.p', 'rb') as f:
    data = pickle.load(f)

# The filename where data was extracted from
print(data['filename'])

# Name of nodes
print(data['node_names'])

# Node hierarchy (skeleton)
print(data['children'])

# Each node has a sequence of transformations (keyframes)
transform_sequences = data['global_transforms']

# Get sequence of a node
sequence = transform_sequences['newVegas:LeftFoot']

# Get transformation matrix (4x4) at 10th time step
matrix = sequence.get(9)
print(matrix)


