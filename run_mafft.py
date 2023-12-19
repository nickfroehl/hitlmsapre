import argparse
import subprocess
import os

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Run a shell command with input file and redirect output.')

    # Add arguments
    parser.add_argument('filename_prefix', type=str, help='Filename prefix for input file')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the arguments
    filename_prefix = args.filename_prefix

    # Construct input and output file paths
    input_file_path = f'fastas/{filename_prefix}.fasta'
    output_file_path = f'aligned/{filename_prefix}.aligned_linsi'
    output_info_file_path = f'aligned/run_info/{filename_prefix}.info'

    # Ensure the input file exists
    if not os.path.exists(input_file_path):
        print(f'Error: Input file "{input_file_path}" not found.')
        return

    # Construct the shell command
    mafft_command = f'mafft --localpair --maxiterate 1000 {input_file_path} > {output_file_path} 2> {output_info_file_path}'
    awk_command = f'awk -i inplace -f utils/nobreak.awk {output_file_path}'
    term_newline_command = f"echo >> {output_file_path}"

    try:
        # Run the shell commands
        subprocess.run(mafft_command, shell=True, check=True)
        # print("Mafft terminated; now just awk to clean up")
        subprocess.run(awk_command, shell=True, check=True)
        subprocess.run(term_newline_command, shell=True, check=True)
        print(f'Success: Output written to "{output_file_path}"')
    except subprocess.CalledProcessError as e:
        print(f'Error running the shell command: {e}')

if __name__ == '__main__':
    main()
