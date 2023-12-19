import argparse, sys

from utils.scapy_utils import *
from protos import *

OUTDIR = "fastas\\"

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
        if isinstance(class_obj, scapy.base_classes.Packet_metaclass):  # actual class
            proto_name = class_obj.__name__
        else:   # already instantiated; assume it is a composed instance
            proto_name = class_name
    except KeyError:
        print(f'Error: Class "{class_name}" not found. Check protos\__init__.py.')
        sys.exit()
    
    return (proto_name,class_obj,num)

def main():
    proto_name, proto, num = p_args()
    
    outfile = f"{OUTDIR}{proto_name}.fasta"
    write_str(outfile, to_fasta(gen_proto(proto, num)))

if __name__ == "__main__":
    main()