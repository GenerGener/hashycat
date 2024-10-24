# read_wrangling
Read Wrangling

# File Operations Script Tutorial (Version 10)

## Introduction

This tutorial covers the usage of the File Operations Script (version 10; v11 is current as of 2024-10-24), a powerful Python tool for splitting, concatenating, and hashing files with support for multiprocessing. The script provides functionality for:

- Splitting large files into smaller chunks
- Concatenating multiple files
- Calculating MD5 and SHA256 hashes (as a standalone operation or combined with split/concatenate)
- Saving hash metadata
- Utilizing multiprocessing for improved performance

## Installation

1. Ensure you have Python 3.6 or later installed on your system.
2. Save the script as `file_operations.py` in your desired directory.
3. Install the required `tqdm` library by running:
   ```
   pip install tqdm
   ```

## Basic Usage

The script can be run from the command line with various options. Here's the basic structure of a command:

```
python file_operations.py [OPTIONS] FILE1 [FILE2 ...]
```

### Command-line Options

- `--split`: Split the input file(s)
- `--concatenate`: Concatenate the input file(s)
- `--hash`: Calculate MD5 and SHA256 hashes (can be used alone or with --split/--concatenate)
- `--chunk-size SIZE`: Specify the size of each chunk when splitting (in bytes)
- `--num-files N`: Specify the number of files to split into
- `--output FILE`: Specify the output file for concatenation
- `--verbose`: Display detailed progress information
- `--processes N`: Specify the number of processes to use for multiprocessing

## Usage Examples

### 1. Calculating Hashes (Standalone Mode)

To calculate hashes for multiple files using 10 processes:

```
python file_operations.py --hash --processes 10 --verbose file1.dat file2.dat file3.dat
```

This command will:
- Calculate MD5 and SHA256 hashes for each file in parallel
- Create hash metadata files for each file
- Display progress information

### 2. Splitting a File

To split a large file into 3 parts and calculate hashes:

```
python file_operations.py --split --num-files 3 --hash --verbose large_file.dat
```

This command will:
- Split `large_file.dat` into 3 roughly equal parts
- Calculate MD5 and SHA256 hashes for the original file and each part
- Display progress information
- Create hash metadata files for each operation

### 3. Splitting a File by Chunk Size

To split a file into chunks of 1MB each:

```
python file_operations.py --split --chunk-size 1048576 --verbose large_file.dat
```

This command will:
- Split `large_file.dat` into chunks of 1MB each
- Display progress information

### 4. Concatenating Files

To concatenate multiple files and calculate the hash of the result:

```
python file_operations.py --concatenate --output combined.dat --hash file1.dat file2.dat file3.dat
```

This command will:
- Combine `file1.dat`, `file2.dat`, and `file3.dat` into a single file named `combined.dat`
- Calculate MD5 and SHA256 hashes for the resulting file
- Create a hash metadata file for the combined file

### 5. Processing Multiple Files

To calculate hashes for all files in a directory:

```
python file_operations.py --hash --verbose --processes 8 /path/to/directory/*
```

This command will:
- Calculate hashes for all files in the specified directory
- Use 8 processes in parallel for faster processing
- Display progress information for each file

## Understanding the Output

When running the script with the `--verbose` option, you'll see detailed information about the operations being performed:

1. The number of CPU cores being used
2. Progress bars for overall file processing
3. Hash information for original files, split parts, or concatenated files
4. Names of created metadata files

Example output for hash calculation:
```
Using 8 out of 12 available CPU cores
Processing files: 100%|████████████████████| 3/3 [00:02<00:00,  1.23files/s]
File: file1.dat
MD5: 3f6d9eb418a4df71b05257d95cc75e75
SHA256: 82533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
Metadata: hash_table_file1.dat_20241013_012345.txt

File: file2.dat
MD5: 7f6d9eb418a4df71b05257d95cc75e75
SHA256: 92533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
Metadata: hash_table_file2.dat_20241013_012346.txt

File: file3.dat
MD5: 8f6d9eb418a4df71b05257d95cc75e75
SHA256: a2533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
Metadata: hash_table_file3.dat_20241013_012347.txt
```

## Multiprocessing Behavior

The script utilizes multiprocessing in the following ways:

- For hash calculations (standalone or with other operations): Each file is processed in a separate process, allowing for parallel processing of multiple files.
- For file splitting: The chunks of a single file are processed in parallel.
- For concatenation: The operation itself is sequential, but if hashing is enabled, the hash calculation of the result is done in a separate process.

By default, the script uses half of the available CPU cores. You can adjust this using the `--processes` option.

## Tips and Best Practices

1. Use the `--hash` option when data integrity is crucial, either as a standalone operation or combined with split/concatenate.
2. When splitting very large files, use the `--chunk-size` option to control memory usage.
3. Use the `--processes` option to optimize performance based on your system's capabilities.
4. The `--verbose` option is helpful for monitoring progress, especially for large files or batch operations.
5. When concatenating files, ensure you have enough disk space for the combined file.
6. For processing multiple files, use wildcard patterns (e.g., `/path/to/directory/*`) to easily include all files in a directory.

## Troubleshooting

- If you encounter "Out of Memory" errors, try reducing the chunk size or the number of processes.
- Ensure you have write permissions in the directory where you're running the script.
- For very large files or numerous small files, consider adjusting the number of processes to balance speed and system resource usage.
- If processing files on a network drive, be aware that network latency may impact performance.

## Conclusion

This File Operations Script provides a versatile and efficient way to manage large files, split them into manageable chunks, concatenate multiple files, and ensure data integrity through hash calculations. By leveraging multiprocessing, it offers improved performance for handling multiple files or large datasets, making it a valuable tool for various file management and data integrity tasks.
