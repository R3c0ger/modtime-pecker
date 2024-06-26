#!usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看指定文件夹下所有直接文件夹和文件的最后修改时间，
递归查找所有文件夹的子文件夹中的所有内容，以找出直接子文件夹的最新修改日期"""

import argparse
import json
import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog, messagebox

import pyperclip
from tqdm import tqdm


def get_timestamp(entry):
    timestamp = datetime.fromtimestamp(entry.stat().st_mtime)
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return timestamp

def get_latest_modification_time(path):
    """递归查找指定路径下所有直接的文件和文件夹的最后修改时间，并返回查找结果"""
    rst_path = f"In {path}: {os.linesep}"
    # print(rst_path, end="")
    rst = rst_path

    time_path_list = []
    # 遍历目标文件夹下的所有直接的文件和文件夹
    for entry in os.scandir(path):
        modtime = get_timestamp(entry)
        entry_name = entry.path.split(path)[-1]
        # 如果不是文件夹而是文件，则直接记录文件的修改时间；
        # 如果是文件夹，则递归查找子文件夹中的文件和文件夹的修改时间，
        # 然后记录子子文件（夹）修改时间中最新的一个，与子文件夹的修改时间比较，保留最新值
        if entry.is_dir():
            rst_subdir = get_latest_modification_time(entry.path)
            _, top_latest_modtime_in_subdir = rst_subdir
            # 子文件夹可能为空文件夹，所以需要判断是否为空
            if top_latest_modtime_in_subdir:
                # 比较子文件夹中最新的一个条目的修改时间和子文件夹的修改时间
                if top_latest_modtime_in_subdir > modtime:
                    modtime = top_latest_modtime_in_subdir
        time_path_list.append((modtime, entry_name))

    # 递归结束后，获取到目标文件夹下直接的文件和文件夹的修改时间
    if time_path_list:
        # 将列表按修改时间（列表每一项元组中的第一个元素）排序，得到最终所需结果
        time_path_list.sort(key=lambda x: x[0], reverse=True)
        # print(time_path_list)
        for modtime, entry_name in time_path_list:
            rst_entry = f"{modtime} - {entry_name}{os.linesep}"
            # print(rst_entry, end="")
            rst += rst_entry
        # 获取子文件夹中最新修改的一个条目的修改时间，用于返回给上一级文件夹
        top_latest_modtime = time_path_list[0][0]
        # print(f"{top_latest_modtime}")
    else:
        # 空文件夹，返回空字符串
        top_latest_modtime = ""
    return rst, top_latest_modtime

def multi_check(path_list):
    """检查多个目标路径
    :param path_list: list[str], 目标路径列表
    :return rsts: str, 检查结果
    """
    # 检查所有目标路径是否有效
    for path in path_list:
        if not os.path.exists(path) or not os.path.isdir(path):
            raise FileNotFoundError(f"{path} is not a valid directory")

    # 逐个检查目标路径
    rsts = ""
    try:
        pbar = tqdm(path_list)
    except AttributeError:
        pbar = path_list
    for target_path in pbar:
        if not isinstance(pbar, list):
            desc = f"Checking the latest modification time in {target_path}"
            try:
                pbar.set_description(desc)
            except AttributeError:
                pass
        rsts += get_latest_modification_time(target_path)[0]
        rsts += os.linesep
    return rsts

def save2clipboard(rst):
    """将结果保存到剪贴板"""
    pyperclip.copy(rst)
    msg = "The result has been copied to the clipboard."
    print(msg)
    return msg

def save2txt(rst):
    """将结果以txt形式保存到脚本所在文件夹，使用时间戳作为文件名后缀"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"modtime_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(rst)
    msg = f"The result has been saved as {filename}" \
          " in the folder where the script resides."
    print(msg)
    return msg

def save2json(rst):
    """将结果以json形式保存到脚本所在文件夹，使用时间戳作为文件名后缀"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"modtime_{timestamp}.json"
    paragraphs = rst.split(f'{os.linesep}'*2)
    # 去除空段落
    for paragraph in paragraphs:
        if not paragraph:
            paragraphs.remove(paragraph)
    # 将段落转换为json格式
    json_dict = {}
    for paragraph in paragraphs:
        lines = paragraph.split(os.linesep)
        target_path = lines[0][3:-2]
        json_dict[target_path] = []
        for line in lines[1:]:
            mtime, entry_name = line.split(' - ')
            json_dict[target_path].append({mtime: entry_name})
    # 保存为json文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)
    msg = f"The result has been saved as {filename}" \
          " in the folder where the script resides."
    print(msg)
    return msg

def gui():
    def browse_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, folder_path)

    def check_modification_time():
        target_path = path_entry.get()
        if not target_path:
            messagebox.showerror("Error", "Please select a folder.")
            return

        try:
            rst = get_latest_modification_time(target_path)[0]
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, rst)
            status_label.config(text="Status: Check completed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Status: Error occurred.")

    def check_script_folder_time():
        script_path = os.path.dirname(os.path.realpath(sys.executable))
        try:
            rst = get_latest_modification_time(script_path)[0]
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, rst)
            status_label.config(text="Status: Check completed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            status_label.config(text="Status: Error occurred.")

    def copy_to_clipboard():
        result = result_text.get("1.0", tk.END)
        if result.strip():
            pyperclip.copy(result)
            messagebox.showinfo("Info", "Result copied to clipboard.")
        else:
            messagebox.showwarning("Warning", "Nothing to copy.")

    def save_as_txt():
        result = result_text.get("1.0", tk.END)
        if result.strip():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                messagebox.showinfo("Info", f"Result saved as {filename}.")
        else:
            messagebox.showwarning("Warning", "Nothing to save.")

    def save_as_json():
        result = result_text.get("1.0", tk.END)
        if result.strip():
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            if filename:
                paragraphs = result.split('\n\n')
                # 去除空段落
                for paragraph in paragraphs:
                    if not paragraph:
                        paragraphs.remove(paragraph)
                json_dict = {}
                for paragraph in paragraphs:
                    lines = paragraph.split('\n')
                    target_path = lines[0][3:-3]
                    json_dict[target_path] = []
                    for line in lines[1:]:
                        try:
                            mtime, entry_name = line.strip().split(' - ')
                        except ValueError:
                            # 提醒用户尽量避免修改结果文本之后再保存
                            error_msg = (f"Invalid text: \n'{line}'\n"
                                         f"Please avoid modifying the "
                                         f"result text before saving.")
                            messagebox.showerror("Error", error_msg)
                            return
                        json_dict[target_path].append({mtime: entry_name})
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(json_dict, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Info", f"Result saved as {filename}.")
        else:
            messagebox.showwarning("Warning", "Nothing to save.")

    root = tk.Tk()
    root.title("Modtime Pecker - Latest Modification Time Checker")
    root.geometry('800x600')

    # 文件夹路径
    folder_frame = ttk.Frame(root)
    folder_frame.pack(pady=10)

    ttk.Label(folder_frame, text="Folder Path:").grid(
        row=0, column=0, padx=5, pady=5)
    path_entry = ttk.Entry(folder_frame, width=50)
    path_entry.grid(row=0, column=1, padx=5, pady=5)

    browse_button = ttk.Button(folder_frame,
                               text="Browse",
                               command=browse_folder)
    browse_button.grid(row=0, column=2, padx=5, pady=5)

    # 功能按钮
    action_frame = ttk.Frame(root)
    action_frame.pack(pady=10)

    check_button = ttk.Button(action_frame,
                              text="Check Modification Time",
                              command=check_modification_time)
    check_button.grid(row=0, column=0, padx=5, pady=5)

    check_script_button = ttk.Button(action_frame,
                                     text="Check Script Folder Time",
                                     command=check_script_folder_time)
    check_script_button.grid(row=0, column=1, padx=5, pady=5)

    copy_button = ttk.Button(action_frame,
                             text="Copy Result",
                             command=copy_to_clipboard)
    copy_button.grid(row=0, column=2, padx=5, pady=5)

    save_txt_button = ttk.Button(action_frame,
                                 text="Save as TXT",
                                 command=save_as_txt)
    save_txt_button.grid(row=0, column=3, padx=5, pady=5)

    save_json_button = ttk.Button(action_frame,
                                  text="Save as JSON",
                                  command=save_as_json)
    save_json_button.grid(row=0, column=4, padx=5, pady=5)

    # 结果显示框
    result_frame = ttk.Frame(root)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    ttk.Label(result_frame, text="Result:").pack(anchor=tk.W, padx=5, pady=5)
    result_text = tk.Text(result_frame, wrap=tk.WORD, width=80, height=20)
    result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 状态栏
    status_label = ttk.Label(root, text="Status: Ready")
    status_label.pack(side=tk.BOTTOM, padx=10, pady=5)

    root.mainloop()

def argparser():
    parser = argparse.ArgumentParser(
        description='Check the latest modification time of all '
                    'folders and files in the specified folder')
    # 目标路径，可以提供多条路径，如果没有指定则默认为None
    parser.add_argument('-p', '--path', type=str,
                        default=None, nargs='+',
                        help='Path(s) of the folder(s) to be checked')
    # 从指定的txt文件中读取路径，可以提供多条txt文件路径，如果没有指定则默认为None
    parser.add_argument('-i', '--import_txt', type=str,
                        default=None, nargs='+',
                        help='Read path from the specified txt file')
    # 直接查看当前脚本所在文件夹
    parser.add_argument('-c', '--current', action='store_true',
                        help='Check the modification time of current folder')
    # GUI界面
    parser.add_argument('-g', '--gui', action='store_true',
                        help='Use GUI interface')
    # 是否要复制结果到剪贴板
    parser.add_argument('-sc', '--save_clipboard', action='store_true',
                        help='Save(copy) the result to the clipboard')
    # 是否要将结果保存为txt文件
    parser.add_argument('-st', '--save_txt', action='store_true',
                        help='Save the result as a txt file')
    # 是否要将结果保存为json文件
    parser.add_argument('-sj', '--save_json', action='store_true',
                        help='Save the result as a json file')
    args = parser.parse_args()
    return args

def cli():
    args = argparser()
    if args.gui:
        gui()
        return

    # 获取所有目标路径
    script_path = os.path.dirname(os.path.realpath(sys.executable))
    if args.current or (not args.path and not args.import_txt):
        # 如果提供了-c参数，或者既没有提供路径也没有提供txt文件，
        # 则默认目标路径为脚本所在文件夹
        path_list = [script_path]
    else:
        # 如果提供了路径，则将路径添加到列表中
        path_list = list(args.path) if args.path else []
        # 如果提供了txt文件，则读取文件中的路径
        if args.import_txt:
            import_txt_list = list(args.import_txt)
            # 检查提供的txt文件是否存在
            for txt in import_txt_list:
                if not os.path.exists(txt) or not os.path.isfile(txt):
                    raise FileNotFoundError(f"{txt} is not a valid txt file")
            # 读取txt文件中的路径
            for txt in import_txt_list:
                with open(txt, 'r') as f:
                    path_list.extend(f.read().splitlines())
        path_list = set(path_list)

    # 执行查看任务并记录结果
    rst = multi_check(path_list)
    print(os.linesep, "-" * 10, "Result", "-" * 10, os.linesep)
    print(rst)

    # 保存结果
    if args.save_clipboard:
        save2clipboard(rst)
    if args.save_txt:
        save2txt(rst)
    if args.save_json:
        save2json(rst)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        gui()
    else:
        cli()