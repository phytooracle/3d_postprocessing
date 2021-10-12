import argparse
import postprocess

def get_args():
    
    parser = argparse.ArgumentParser(
        description='Postprocessing the 3D data. This repo applies estimated transformation on the points.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i',
                        '--input',
                        help='Path to the directory that contains all different folders of preprocessing/alignment (west, east, merged, ...)',
                        metavar='input',
                        type=str,
                        required=True)
    
    parser.add_argument('-o',
                        '--output',
                        help='Path to the geocorrection directory where the results for the given single pass will be save. Within the geocorrection directory, 7 sub-directories will be created (if not exist) for east, west, merged and downsampled of them as well as the updated metadata.',
                        metavar='output',
                        type=str,
                        required=True)

    parser.add_argument('-f',
                        '--folder',
                        help='The folder name to be processed. Often called the timestamp.',
                        metavar='folder',
                        type=str,
                        required=True)

    parser.add_argument('-t',
                        '--transformation',
                        help='The transformation json file',
                        metavar='transformation',
                        type=str,
                        required=True)

    parser.add_argument('-p',
                        '--plants',
                        help='Path to the csv that contains the plant detections.',
                        metavar='plants',
                        type=str,
                        required=False)

    parser.add_argument('-s',
                        '--season',
                        help='The season number, i.e. 10, 11, 12. ',
                        metavar='str',
                        type=str,
                        required=True)

    parser.add_argument('-d',
                        '--date',
                        help='The scan date string in format YYYY-MM-DD. ',
                        metavar='str',
                        type=str,
                        required=True)

    parser.add_argument('-l',
                        '--lids',
                        help='The path to the lids file. ',
                        metavar='str',
                        type=str,
                        required=True)

    return parser.parse_args()

def main():
    args = get_args()
    postprocess.postprocess_single_pass(args.input,args.output,args.folder,args.plants,args.transformation,int(args.season),args.date,args.lids)

main()