import os
import sys
import hashlib
import argparse
from tqdm import tqdm
import multiprocessing
import math
import datetime
import csv

def calculate_hash(file_path, hash_type):
    hash_func = hashlib.md5() if hash_type == 'md5' else hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def save_hash_metadata_csv(results, timestamp):
    csv_filename = f"hash_results_{timestamp}.csv"
    fieldnames = ['File', 'Timestamp', 'MD5', 'SHA256', 'Metadata_File']
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow({
                'File': result['file'],
                'Timestamp': result['timestamp'],
                'MD5': result['md5'],
                'SHA256': result['sha256'],
                'Metadata_File': result['metadata_file']
            })
    return csv_filename

def save_hash_metadata(file_path, md5_hash, sha256_hash):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(file_path)
    metadata_file = f"hash_table_{base_name}_{timestamp}.txt"
    with open(metadata_file, 'w') as f:
        f.write(f"File: {file_path}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"MD5: {md5_hash}\n")
        f.write(f"SHA256: {sha256_hash}\n")
    return metadata_file, timestamp

def process_file_hash(file):
    md5_hash = calculate_hash(file, 'md5')
    sha256_hash = calculate_hash(file, 'sha256')
    metadata_file, timestamp = save_hash_metadata(file, md5_hash, sha256_hash)
    return {
        'file': file,
        'timestamp': timestamp,
        'md5': md5_hash,
        'sha256': sha256_hash,
        'metadata_file': metadata_file
    }

def split_file_chunk(args):
    input_file, start, chunk_size, chunk_num, output_dir, hash_flag = args
    base_name = os.path.basename(input_file)
    output_file = os.path.join(output_dir, f"{base_name}.{chunk_num:03d}")
    
    with open(input_file, 'rb') as in_f, open(output_file, 'wb') as out_f:
        in_f.seek(start)
        out_f.write(in_f.read(chunk_size))
    
    if hash_flag:
        result = process_file_hash(output_file)
        return f"Chunk {chunk_num}: {result['file']},{result['md5']},{result['sha256']},{result['metadata_file']}"
    return f"Chunk {chunk_num} created"

def split_file(input_file, chunk_size=None, num_files=None, output_dir=None, hash_flag=False, pool=None):
    if output_dir is None:
        output_dir = os.path.dirname(input_file) or '.'
    
    file_size = os.path.getsize(input_file)
    
    if num_files is not None:
        chunk_size = math.ceil(file_size / num_files)
    elif chunk_size is None:
        raise ValueError("Either chunk_size or num_files must be specified")
    
    num_chunks = math.ceil(file_size / chunk_size)
    
    chunk_args = [(input_file, i * chunk_size, min(chunk_size, file_size - i * chunk_size), i, output_dir, hash_flag) 
                  for i in range(num_chunks)]
    
    if pool:
        results = list(pool.imap(split_file_chunk, chunk_args))
        for result in results:
            print(result)
    else:
        for args in chunk_args:
            result = split_file_chunk(args)
            print(result)
    
    return num_chunks

def concatenate_files(input_files, output_file):
    with open(output_file, 'wb') as out_f:
        for file in input_files:
            with open(file, 'rb') as in_f:
                out_f.write(in_f.read())

def process_files(args, files, pool):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if args.split:
        for file in files:
            print(f"Splitting file: {file}")
            if args.hash:
                result = process_file_hash(file)
                print(f"Original file: {result['file']},{result['md5']},{result['sha256']},{result['metadata_file']}")
            
            output_dir = os.path.dirname(file) or '.'
            chunk_count = split_file(file, chunk_size=args.chunk_size, num_files=args.num_files, 
                                   output_dir=output_dir, hash_flag=args.hash, pool=pool)
            print(f"Split into {chunk_count} chunks")
    
    elif args.concatenate:
        output_file = args.output or "concatenated_output"
        print(f"Concatenating files to: {output_file}")
        concatenate_files(files, output_file)
        if args.hash:
            result = process_file_hash(output_file)
            print(f"Concatenated file: {result['file']},{result['md5']},{result['sha256']},{result['metadata_file']}")
    
    elif args.hash:
        results = list(tqdm(pool.imap(process_file_hash, files), total=len(files), desc="Processing files"))
        csv_file = save_hash_metadata_csv(results, timestamp)
        print(f"Results saved to: {csv_file}")
        if args.verbose:
            print("\nFile,MD5,SHA256,Metadata_File")
            for result in results:
                print(f"{result['file']},{result['md5']},{result['sha256']},{result['metadata_file']}")

def main():
    parser = argparse.ArgumentParser(description="File split, concatenate, and hash tool with multiprocessing")
    parser.add_argument('files', nargs='+', help="Input files or directories")
    parser.add_argument('--split', action='store_true', help="Split files")
    parser.add_argument('--concatenate', action='store_true', help="Concatenate files")
    parser.add_argument('--hash', action='store_true', help="Calculate MD5 and SHA256 hashes")
    parser.add_argument('--chunk-size', type=int, help="Chunk size for splitting")
    parser.add_argument('--num-files', type=int, help="Number of files to split into")
    parser.add_argument('--output', help="Output file for concatenation")
    parser.add_argument('--verbose', action='store_true', help="Verbose output")
    parser.add_argument('--processes', type=int, default=None, help="Number of processes to use (default: number of CPU cores / 2)")
    args = parser.parse_args()

    if sum([args.split, args.concatenate, args.hash]) == 0:
        print("Error: You must choose at least one operation: --split, --concatenate, or --hash")
        sys.exit(1)

    if args.split and args.concatenate:
        print("Error: You cannot use both --split and --concatenate at the same time")
        sys.exit(1)

    if args.split and args.chunk_size is None and args.num_files is None:
        print("Error: When splitting, you must specify either --chunk-size or --num-files")
        sys.exit(1)

    if args.split and args.chunk_size is not None and args.num_files is not None:
        print("Error: You can specify either --chunk-size or --num-files, but not both")
        sys.exit(1)

    input_files = []
    for path in args.files:
        if os.path.isdir(path):
            input_files.extend([os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        elif os.path.isfile(path):
            input_files.append(path)
        else:
            print(f"Warning: {path} is not a valid file or directory. Skipping.")

    args.files = input_files

    num_cpus = multiprocessing.cpu_count()
    if args.processes is None:
        num_processes = max(1, num_cpus // 2)  # Use half of available CPUs by default
    else:
        num_processes = min(args.processes, num_cpus)  # Use specified number, but no more than available CPUs
    
    print(f"Using {num_processes} out of {num_cpus} available CPU cores")

    with multiprocessing.Pool(num_processes) as pool:
        process_files(args, args.files, pool)

if __name__ == "__main__":
    main()
