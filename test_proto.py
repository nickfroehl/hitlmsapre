import argparse, sys

from utils.scapy_utils import *
from protos import *

def p_args() -> tuple[Packet,int]:
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='A script to create an instance of a class.')

    # Add arguments
    parser.add_argument('proto_name', type=str, help='Protocol class name')
    parser.add_argument('num', type=int, help='Number of samples to generate')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the arguments
    class_name = args.proto_name
    num = args.num

    try:
        # Get the class object by name
        class_obj = globals()[class_name]
    except KeyError:
        print(f'Error: Class "{class_name}" not found. Check protos\__init__.py.')
        sys.exit()
    
    return (class_obj,num)

def main():
    proto, num = p_args()
    show_proto(proto, num)

if __name__ == "__main__":
    main()