from FbxCommon import *
import numpy as np
import pickle
import os
import glob
from argparse import ArgumentParser


def normalize_node_name(name):
    # this will discard the prefix of the node name
    # example: 'newVegas:LeftFoot' becomes 'LeftFoot'
    return name.split(':')[-1]


def fbx_matrix_to_numpy(matrix):
    m = []
    for i in range(4):
        row = [matrix.Get(i, j) for j in range(4)]
        m.append(row)
    return np.array(m)


class TransformSequence:

    def __init__(self):
        self.timecodes = []
        self.fbx_matrices = []
        self.numpy_matrices = []

    def add(self, fbx_matrix, timecode):
        self.timecodes.append(timecode)
        self.fbx_matrices.append(fbx_matrix)
        self.numpy_matrices.append(fbx_matrix_to_numpy(fbx_matrix))

    def get(self, index):
        return self.numpy_matrices[index]

    def get_tensor(self):
        # Returns the tensor of transformation matrices
        a = [np.expand_dims(m, axis=0) for m in self.numpy_matrices]
        return np.concatenate(a, axis=0)

    def __str__(self):
        return str(self.numpy_matrices)


class NodeWalker:

    def __init__(self, evaluator):
        self._evaluator = evaluator
        self.node_names = []
        self.children = dict()
        self.global_transforms = dict()
        self.local_transforms = dict()
        self._keyframes = [0.0]

    @property
    def keyframes(self):
        return self._keyframes

    @keyframes.setter
    def keyframes(self, values):
        self._keyframes = values

    def traverse_nodes(self, node):
        parent_name = normalize_node_name(node.GetName())
        self.node_names.append(parent_name)
        self.children[parent_name] = []
        globals = TransformSequence()
        locals = TransformSequence()

        # get global transform at time t
        for t in self.keyframes:
            time = FbxTime()
            time.SetSecondDouble(t)

            # Global transformation (relative to skeleton origin)
            tf = self._evaluator.GetNodeGlobalTransform(node, time)
            globals.add(tf, t)

            # Local transformation (relative to parent node)
            tf = self._evaluator.GetNodeLocalTransform(node, time)
            locals.add(tf, t)

        self.global_transforms[parent_name] = globals.get_tensor()
        self.local_transforms[parent_name] = locals.get_tensor()

        for i in range(node.GetChildCount()):
            child = node.GetChild(i)
            child_name = normalize_node_name(child.GetName())
            self.children[parent_name].append(child_name)

            self.traverse_nodes(child)


def extract_animation_data(file, fps=30, max_time=10):
    assert fps > 0
    assert max_time > 0

    lSdkManager, lScene = InitializeSdkObjects()
    LoadScene(lSdkManager, lScene, file)

    evaluator = lScene.GetAnimationEvaluator()
    rootNode = lScene.GetRootNode()

    # Walk node hierarchy and collect data at given time intervals
    w = NodeWalker(evaluator)
    w.keyframes = np.arange(0, max_time, 1 / fps)
    w.traverse_nodes(rootNode)

    data = {
        'filename': file,
        'node_names': w.node_names,
        'children': w.children,
        'keyframes': w.keyframes,
        'global_transforms': w.global_transforms,
        'local_transforms': w.local_transforms,
    }
    return data


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--max_time', type=float, default=2)
    parser.add_argument('--output', type=str, default='./anim_data.p')
    args = parser.parse_args()

    # args.file = '/media/adrian/Portable/Datasets/Mixamo/Character and Anim/Shae/Afoxe Samba Reggae Dance.fbx'

    data = extract_animation_data(args.file, args.fps, args.max_time)

    with open(args.output, 'wb') as f:
        pickle.dump(data, f, protocol=2)
