from tkinter.constants import *
import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
import os
import shutil

source_directory = ""  
file_extension = ""  
destination_directory = ""  
file_size_limit_kb = 0
moved_files = []
all_extensions = []

def select_source_directory():
    global source_directory
    source_directory = filedialog.askdirectory()
    
    if source_directory:
        source_directory_label_display.config(text=f"原資料夾: <{source_directory}>")
    else:
        source_directory_label_display.config(text="請選擇有效資料夾")
    extention_menu_scan_update(source_directory)

def select_destination_directory():
    global destination_directory
    destination_directory = filedialog.askdirectory()
    
    if destination_directory:
        destination_directory_label_display.config(text=f"目標資料夾: <{destination_directory}>")
    else:
        destination_directory_label_display.config(text="請選擇有效資料夾")
        
def extention_menu_scan_update(directory):
    global all_extensions
    
    available_extensions = set()
    for root, _, files in os.walk(directory):
        for file in files:
            available_extensions.add(os.path.splitext(file)[1])
    sorted_ext = sorted(all_extensions)
    
    file_extension_menu["menu"].delete(0, "end")
    for extensions in available_extensions:
        file_extension_menu["menu"].add_command(label=extensions, command = tk._setit(extension_var, extensions))
    if sorted_ext:
        extension_var.set(sorted_ext[0])
    else:
        extension_var.set("--請選擇資料夾以選擇類型--")

def move_files():
    global source_directory, destination_directory, file_extension, file_size_limit_kb, moved_files
    
    file_extension = extension_var.get()
    
    try:
        file_size_limit_kb = int(size_var.get())
    except ValueError:
        debugger_display.config(text="執行錯誤: 請輸入有效整數於大小限制內")
        
    for root, _, files in os.walk(source_directory):
        for file in files:
            if not file.endswith(file_extension):
                continue
            source_file_path = os.path.join(root, file)
            file_size_kb = os.path.getsize(source_file_path) / 1024
            
            if file_size_kb < file_size_limit_kb:
                debugger_display.config(text=f"執行錯誤: 文件 <{file}> 太小")
                file_size_kb = 0
                continue
            try:
                shutil.move(source_file_path, destination_directory)
                moved_files.append((source_file_path, os.path.join(destination_directory, file)))
                debugger_display.config(text=f"執行成功: 文件 <{file}> 成功移動至 <{destination_directory}>")
            except Exception as e:
                debugger_display.config(text=f"執行錯誤: 移動文件 <{file}> 時出錯 <{e}>")

def undo_last_move():
    global moved_files
    
    for original_path, moved_path in moved_files:
        try:
            shutil.move(moved_path, original_path)
            debugger_display.config(text=f"執行成功: 文件 <{original_path}> 成功復原至 <{moved_path}>")
        except Exception as e:
            debugger_display.config(text=f"執行錯誤: 復原文件 <{original_path}> 時出錯 <{e}>")
    moved_files.clear()

# WINDOWS #
window = tk.Tk()
window.title('文件移動工具 Version : 1.2')
window.geometry('420x420')
window.resizable(True, False)

# FONT #
font = tkFont.Font(family="Verdana", size=12)

# SOURCE DIRECTORY #
source_directory_label = tk.Label(text=" 1.原檔案所屬資料夾 ", bg="white", fg="black", height=2, font=font)
source_directory_label.place(x=20, y=20)

source_directory_button = tk.Button(window, text=" 請選擇資料夾 ", command=select_source_directory, font=font)
source_directory_button.place(x=200, y=25)

source_directory_label_display = tk.Label(window, text="原資料夾 : ", font=font)
source_directory_label_display.place(x=20, y=70)

# FILE EXTENSION #
extension_var = tk.StringVar(value="-請選擇資料夾以選擇類型-")

extension_label = tk.Label(text=" 2.檔案類型 ", bg="white", fg="black", height=2, font=font)
extension_label.place(x=20, y=105)

file_extension_menu = tk.OptionMenu(window, extension_var,"-請選擇資料夾以選擇類型-")
file_extension_menu.config(font=font)
file_extension_menu.place(x=130, y=110)

# FILE SIZE LIMIT #
size_var = tk.StringVar(value="0")

size_limit_label = tk.Label(text=" 3.檔案大小下限 ( KB ) ", bg="white", fg="black", height=2, font=font)
size_limit_label.place(x=20, y=170)

file_size_limit_input = tk.Entry(window, textvariable=size_var )
file_size_limit_input.place(x=220, y=175, width=50, height= 30)

# DESTINATION DIRECTORY #
destination_directory_label = tk.Label(text=" 4.請選擇目標資料夾 ", bg="white", fg="black", height=2, font=font)
destination_directory_label.place(x=20, y=235)

destination_directory_button = tk.Button(window, text="請選擇資料夾", command=select_destination_directory, font=font)
destination_directory_button.place(x=200, y=240)

destination_directory_label_display = tk.Label(window, text="目標資料夾 : ", font=font)
destination_directory_label_display.place(x=20, y=290)

# ACTIVATE #
activate_button = tk.Button(window, text="執行", command=move_files, font=font)
activate_button.place(x=20, y=330)

# UNDO BUTTON #
undo_last_move_button = tk.Button(window, text="返回上一步移動", command=undo_last_move, font=font)
undo_last_move_button.place(x=100, y=330)

# DEBUGGER #
debugger_display = tk.Label(window, text="執行狀態 : 待命中", font=font)
debugger_display.place(x=20, y=390)

window.mainloop()