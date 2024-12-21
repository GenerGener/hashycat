# Read Wrangling with hashycat.py :3

# Tutorial (Version 12)

## Introduction

This tutorial covers the usage of the file operations "hashycat.py" script (current as of 2024-11-12), a powerful Python tool for splitting, concatenating, and hashing files with support for multiprocessing. The script provides functionality for:

- Splitting large files into smaller chunks
- Concatenating multiple files
- Calculating MD5 and SHA256 hashes (as a standalone operation or combined with split/concatenate)
- Saving results in CSV format
- Optional individual metadata file generation
- Utilizing multiprocessing for improved performance

## Installation

1. Ensure you have Python 3.6 or later installed on your system.
2. Save the script as `hashycat.py` in your desired directory.
3. Install the required `tqdm` library by running:
   ```
   pip install tqdm
   ```

## Basic Usage

The script can be run from the command line with various options. Here's the basic structure of a command:

```
python hashycat.py [OPTIONS] FILE1 [FILE2 ...]
```

### Command-line Options

- `--split`: Split the input file(s)
- `--concatenate`: Concatenate the input file(s)
- `--hash`: Calculate MD5 and SHA256 hashes (can be used alone or with --split/--concatenate)
- `--metadata`: Generate individual metadata files for each processed file
- `--chunk-size SIZE`: Specify the size of each chunk when splitting (in bytes)
- `--num-files N`: Specify the number of files to split into
- `--output FILE`: Specify the output file for concatenation
- `--verbose`: Display detailed progress information and CSV-formatted results in console
- `--processes N`: Specify the number of processes to use for multiprocessing

## Usage Examples

### 1. Basic Hash Calculation

To calculate hashes for multiple files with CSV output only:

```
python hashycat.py --hash --verbose file1.dat file2.dat file3.dat
```

This command will:
- Calculate MD5 and SHA256 hashes for each file in parallel
- Generate a consolidated CSV file with all results (`hash_results_TIMESTAMP.csv`)
- Display progress information and results if verbose is enabled

### 2. Hash Calculation with Individual Metadata Files

To calculate hashes and generate individual metadata files:

```
python hashycat.py --hash --metadata --processes 10 file1.dat file2.dat file3.dat
```

This command will:
- Calculate hashes for all files
- Generate a consolidated CSV file
- Create individual metadata files for each processed file
- Use 10 processes in parallel for faster processing

### 3. Splitting a File with Hashes

To split a large file into 3 parts and calculate hashes:

```
python hashycat.py --split --num-files 3 --hash --verbose large_file.dat
```

This command will:
- Split `large_file.dat` into 3 roughly equal parts
- Calculate MD5 and SHA256 hashes for the original file and each part
- Generate a consolidated CSV file with results
- Display progress information and results if verbose is enabled

To also generate individual metadata files for each part:

```
python hashycat.py --split --num-files 3 --hash --metadata large_file.dat
```

### 4. Concatenating Files

To concatenate multiple files and calculate the hash of the result:

```
python hashycat.py --concatenate --output combined.dat --hash file1.dat file2.dat file3.dat
```

This command will:
- Combine the input files into `combined.dat`
- Calculate MD5 and SHA256 hashes for the resulting file
- Include results in the CSV file

Add `--metadata` to generate an individual metadata file for the combined file:

```
python hashycat.py --concatenate --output combined.dat --hash --metadata file1.dat file2.dat file3.dat
```

## Understanding the Output

The script provides two types of output:

1. CSV File Output (Always generated when using --hash):
   - A file named `hash_results_TIMESTAMP.csv` containing all results
   - CSV columns: File, Timestamp, MD5, SHA256

2. Individual Metadata Files (Optional with --metadata flag):
   - Separate .txt files for each processed file
   - Format: `hash_table_FILENAME_TIMESTAMP.txt`

Example CSV file content:
```csv
File,Timestamp,MD5,SHA256
file1.dat,20241112_134038,3f6d9eb418a4df71b05257d95cc75e75,82533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
file2.dat,20241112_134039,7f6d9eb418a4df71b05257d95cc75e75,92533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
file3.dat,20241112_134040,8f6d9eb418a4df71b05257d95cc75e75,a2533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
```

Example individual metadata file content (when using --metadata):
```
File: file1.dat
Timestamp: 20241112_134038
MD5: 3f6d9eb418a4df71b05257d95cc75e75
SHA256: 82533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
```

## Console Output (with --verbose):
```
Using 8 out of 12 available CPU cores
Processing files: 100%|████████████████████| 3/3 [00:02<00:00,  1.23files/s]
Results saved to: hash_results_20241112_134038.csv

File,MD5,SHA256
file1.dat,3f6d9eb418a4df71b05257d95cc75e75,82533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
file2.dat,7f6d9eb418a4df71b05257d95cc75e75,92533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
file3.dat,8f6d9eb418a4df71b05257d95cc75e75,a2533214d86d8ad8118996b4187060481264e9ef8a7938612c92c8dbcb6e1ee1
```

## Tips and Best Practices

1. Use CSV output (default with --hash) for easy importing into spreadsheets or databases
2. Use `--metadata` only when individual file records are needed
3. For batch processing, CSV output is more manageable than individual metadata files
4. Use `--verbose` to monitor progress and verify results in real-time
5. When splitting large files, consider using `--chunk-size` to control memory usage
6. Adjust `--processes` based on your system's capabilities
7. Use wildcard patterns (e.g., `/path/to/directory/*`) for processing multiple files

## Troubleshooting

- If you encounter "Out of Memory" errors, try reducing the chunk size or number of processes
- Ensure write permissions in the output directory for both CSV and metadata files
- For large file sets, consider using CSV output without individual metadata files
- If processing files on a network drive, be aware that network latency may impact performance

## Conclusion

This file operations "hashycat.py" script provides a streamlined approach to file management tasks with flexible output options. The CSV-first approach with optional metadata files makes it suitable for both interactive use and automated workflows. The multiprocessing capabilities ensure efficient handling of large datasets, while the modular output options allow users to balance between detailed individual records and consolidated reporting.
