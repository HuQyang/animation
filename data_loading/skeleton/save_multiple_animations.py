from save_animation import extract_animation_data
from argparse import ArgumentParser
import glob
import os
import pickle


def get_character_name(animation_file):
    # character name is the parent folder of the animation file
    return os.path.split(animation_file)[0].split(os.sep)[-1]


def get_animation_name(animation_file):
    return os.path.splitext(os.path.basename(animation_file))[0]


def make_skeleton_filename(animation_file):
    character_name = get_character_name(animation_file)
    animation_name = get_animation_name(animation_file)
    home_dir = os.path.join(args.output_dir, character_name, animation_name)
    os.makedirs(home_dir, exist_ok=True)
    output_file = os.path.join(home_dir, 'skeleton.p')
    return output_file


def write_skeleton(file, data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)


if __name__ == '__main__':

    # "folder" is the character name and contains .fbx files with different animation names
    # Will save skeleton to: output_dir/character_name/animation_name/

    parser = ArgumentParser()
    parser.add_argument('folder')
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--max_time', type=float, default=10)
    parser.add_argument('--output_dir', type=str, default='./out/')
    args = parser.parse_args()

    files = []
    search = os.path.join(args.folder, '*.fbx')
    files = glob.glob(search)
    print('Found {} in {}'.format(len(files), args.folder))

    for file in files:
        data = extract_animation_data(file, args.fps, args.max_time)

        output_file = make_skeleton_filename(file)
        write_skeleton(output_file, data)
