import pickle
from save_animation import *


file = './out/test_data/Air Squat Workout/skeleton.p'

with open(file, 'rb') as f:
    data = pickle.load(f)

# Contents of dictionary
print('\n', data.keys(), '\n')


# The filename where data was extracted from
print(data['filename'])

# Name of nodes
# You can access the transformations using these names (see below)
print(data['node_names'])

# Node hierarchy (skeleton)
print(data['children'])

# Each node has a sequence of transformations (keyframes)
transform_sequences = data['global_transforms']

# Get sequence of a node
sequence = transform_sequences['LeftFoot']

# Get transformation matrix (4x4) at 10th time step
matrix = sequence.get(9)
print(matrix)
