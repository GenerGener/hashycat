# read_wrangling
Read Wrangling

# File Operations Script Tutorial

## Introduction

This tutorial covers the usage of the File Operations Script (version 11; formerly v8), a powerful Python tool for splitting and concatenating files with support for multiprocessing and hash calculations. The script provides functionality for:

- Splitting large files into smaller chunks
- Concatenating multiple files
- Calculating MD5 and SHA256 hashes
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
- `--chunk-size SIZE`: Specify the size of each chunk when splitting (in bytes)
- `--num-files N`: Specify the number of files to split into
- `--output FILE`: Specify the output file for concatenation
- `--hash`: Calculate MD5 and SHA256 hashes
- `--verbose`: Display detailed progress information
- `--processes N`: Specify the number of processes to use for multiprocessing

## Usage Examples

### 1. Splitting a File

To split a large file into 3 parts and calculate hashes:

```
python file_operations.py --split --num-files 3 --hash --verbose large_file.dat
```

This command will:
- Split `large_file.dat` into 3 roughly equal parts
- Calculate MD5 and SHA256 hashes for the original file and each part
- Display progress information
- Create hash metadata files for each operation

### 2. Splitting a File by Chunk Size

To split a file into chunks of 1MB each:

```
python file_operations.py --split --chunk-size 1048576 --verbose large_file.dat
```

This command will:
- Split `large_file.dat` into chunks of 1MB each
- Display progress information

### 3. Concatenating Files

To concatenate multiple files:

```
python file_operations.py --concatenate --output combined.dat --hash file1.dat file2.dat file3.dat
```

This command will:
- Combine `file1.dat`, `file2.dat`, and `file3.dat` into a single file named `combined.dat`
- Calculate MD5 and SHA256 hashes for the resulting file
- Create a hash metadata file for the combined file

### 4. Processing Multiple Files

To split multiple files in a directory:

```
python file_operations.py --split --num-files 2 --hash --verbose /path/to/directory/*
```

This command will:
- Split each file in the specified directory into 2 parts
- Calculate hashes for all original files and their parts
- Display progress information for each file

### 5. Controlling CPU Usage

To limit the script to use only 4 CPU cores:

```
python file_operations.py --split --num-files 3 --hash --verbose --processes 4 large_file.dat
```

This command will:
- Use only 4 CPU cores for processing
- Split `large_file.dat` into 3 parts
- Calculate hashes
- Display progress information

## Understanding the Output

When running the script with the `--verbose` option, you'll see detailed information about the operations being performed:

1. The number of CPU cores being used
2. Progress bars for overall file processing
3. Hash information for original files and split parts
4. Names of created metadata files

Example output:
```
Using 4 out of 8 available CPU cores
Splitting file: large_file.dat
Original file: MD5=3f6d9eb418a4df71b05257d95cc75e75, SHA256=82533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1, Metadata=hash_table_large_file.dat_20241013_012345.txt
Chunk 0: MD5=7f6d9eb418a4df71b05257d95cc75e75, SHA256=92533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1, Metadata=hash_table_large_file.dat.000_20241013_012346.txt
Chunk 1: MD5=8f6d9eb418a4df71b05257d95cc75e75, SHA256=a2533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1, Metadata=hash_table_large_file.dat.001_20241013_012347.txt
Chunk 2: MD5=9f6d9eb418a4df71b05257d95cc75e75, SHA256=b2533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1, Metadata=hash_table_large_file.dat.002_20241013_012348.txt
Split into 3 chunks
Processing files: 100%|████████████████████████████████████████| 1/1 [00:05<00:00,  5.43s/it]
```

## Tips and Best Practices

1. When splitting very large files, use the `--chunk-size` option to control memory usage.
2. Use the `--processes` option to optimize performance based on your system's capabilities.
3. Always use the `--hash` option when data integrity is crucial.
4. The `--verbose` option is helpful for monitoring progress, especially for large files or batch operations.
5. When concatenating files, ensure you have enough disk space for the combined file.

## Troubleshooting

- If you encounter "Out of Memory" errors, try reducing the chunk size or the number of processes.
- Ensure you have write permissions in the directory where you're running the script.
- For very large files, consider running the script on a machine with more RAM and CPU cores.

## Conclusion

This File Operations Script provides a versatile and efficient way to manage large files, split them into manageable chunks, and ensure data integrity through hash calculations. By leveraging multiprocessing, it offers improved performance for handling multiple files or large datasets.
