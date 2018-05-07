from save_animation import extract_animation_data
from argparse import ArgumentParser
import glob
import os
import pickle

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--max_time', type=float, default=10)
    parser.add_argument('--output_dir', type=str, default='./out/')
    args = parser.parse_args()

    files = []
    search = os.path.join(args.file, '*.fbx')
    files = glob.glob(search)
    print('Found {} in {}'.format(len(files), args.file))

    os.mkdir(args.output_dir)

    for file in files:
        basename = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(args.output_dir, basename + '.p')

        data = extract_animation_data(args.file, args.fps, args.max_time)

        with open(output_file, 'wb') as f:
            pickle.dump(data, f)
