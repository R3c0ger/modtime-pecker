# Modtime Pecker - 文件夹最新修改时间检查工具

## Description

Modtime Pecker is a Python script designed to check the latest modification time of all folders and files in a specified folder. It recursively searches all subfolders to find the latest modification time of direct subfolders.

Modtime Pecker 是一个Python脚本，旨在帮助用户高效地查看指定文件夹下所有直接子文件夹和文件的最后修改时间。

In general, when using a file explorer to view the modification time of all files and folders in a folder, there is a problem that the modification time of the folder will not be updated with the modification of the files in the folder. This leads to the inability to intuitively view the latest modification time of the folder. This tool aims to solve this problem.

在通常情况下，使用文件资源管理器查看某一文件夹下的所有文件和文件夹的修改时间时，会出现一个问题，即文件夹修改时间不会随着文件夹内文件的修改而更新。这就导致了无法直观地查看文件夹的最新修改时间。本工具旨在解决这一问题。

## Features

- Recursively search all subfolders to find the latest modification time of direct subfolders.
  递归搜索所有子文件夹，找到直接子文件夹的最新修改时间。
- Support multiple target folders.
  支持一次性查看多个目标文件夹。
- Support custom output format including JSON and TXT.
  支持自定义输出格式，包括JSON和TXT。
- 支持将结果复制到剪切板中。 
  Support copying the result to the clipboard.

## Environment

- Only support Windows currently. 目前仅支持Windows。
- Python 3.6 or higher
- pyperclip~=1.8.2
- tqdm~=4.66.2

## Usage

```bash
python modtime_pecker.py [-h] [-p PATH [PATH ...]] [-i IMPORT_TXT [IMPORT_TXT ...]] [-c] [-g] [-sc] [-st] [-sj]
```
### Arguments

- `-p, --path`: Path(s) of the folder(s) to be checked. 
  指定要检查的文件夹路径，可指定多个。
- `-i, --import_txt`: Read path from the specified txt file(s).
  从TXT文件导入路径列表。
- `-c, --current`: Check the modification time of the current folder.
  检查脚本所在当前文件夹。
- `-g, --gui`: Use GUI interface (not available in modtime_pecker_nogui.py).
  启动图形用户界面（modtime_pecker_nogui.py中无此功能）。
- `-sc, --save_clipboard`: Save (copy) the result to the clipboard.
  将结果复制到剪贴板。
- `-st, --save_txt`: Save the result as a txt file.
  将结果保存为TXT文件。
- `-sj, --save_json`: Save the result as a json file.
  将结果保存为JSON文件。

In `modtime_pecker_nogui.py`: 

Default behavior: If no arguments are specified, the script will check the current folder and save the result as a TXT file.
默认行为：如果未指定任何参数，脚本将检查当前文件夹并保存结果为TXT文件。

In `modtime_pecker.py`: 

Default behavior: If no arguments are specified, the script will start the GUI.
默认行为：如果未指定任何参数，脚本将启动图形用户界面。

### Examples

1. Check the modification time of the current folder and save the result as a text file:

```bash
python modtime_pecker.py -c -st
```

2. Check the modification time of specified folders and save the result as a json file:

```bash
python modtime_pecker.py -p /path/to/folder1 /path/to/folder2 -sj
```

3. Check the modification time of folders listed in a text file and copy the result to clipboard:

```bash
python modtime_pecker.py -i folders.txt -sc
```

### Output

The script will output the latest modification time of each folder and file in the specified folder(s) in the following format:

```
In /path/to/folder1:
2023-12-31 18:30:00 - file1.txt
2023-12-30 12:00:00 - subdir1

In /path/to/folder2:
2024-01-01 08:00:00 - file2.txt
2023-12-28 09:45:00 - subdir2

```

JSON output example:

```json
{
    "/path/to/folder1": [
        {
            "2023-12-31 18:30:00": "file1.txt"
        },
        {
            "2023-12-30 12:00:00": "subdir1"
        }
    ],
    "/path/to/folder2": [
        {
            "2024-01-01 08:00:00": "file2.txt"
        },
        {
            "2023-12-28 09:45:00": "subdir2"
        }
    ]
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
