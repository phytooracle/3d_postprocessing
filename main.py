import argparse
import postprocess

def get_args():
    
    parser = argparse.ArgumentParser(
        description='Postprocessing the 3D data. This repo applies estimated transformation on the points.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i',
                        '--input',
                        help='Path to the directory that contains single pass aligned data.',
                        metavar='input',
                        type=str,
                        required=True)
    
    parser.add_argument('-o',
                        '--output',
                        help='Path to the directory that the results for the given single pass will be save. If it does not exist, it will be created. The name of this folder should be the same as the name of the input folder corresponding to the 3d pass.',
                        metavar='output',
                        type=str,
                        required=True)

    parser.add_argument('-t',
                        '--transformation',
                        help='The transformation matrix',
                        metavar='transformation',
                        type=str,
                        required=True)

    parser.add_argument('-p',
                        '--plants',
                        help='Path to the csv that contains the plant detections.',
                        metavar='plants',
                        type=str,
                        required=False)

    return parser.parse_args()

def main():
    args = get_args()
    postprocess.postprocess_single_pass(args.input,args.output,args.plants,args.transformation)

main()