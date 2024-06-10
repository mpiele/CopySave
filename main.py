import pyperclip
from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("1280x720")

root.title("CopySave")

clipboard_list = []
previous_content = None

pyperclip.copy("")

def remove_item(index):
    if index < len(clipboard_list):
        del clipboard_list[index]
        update_display()

def copy_to_clipboard(index):
    if index < len(clipboard_list):
        pyperclip.copy(clipboard_list[index])

def update_display():
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    for i, text in enumerate(clipboard_list):
        frame = ttk.Frame(canvas_frame, padding=(5, 5, 5, 5))
        frame.grid(row=i, column=0, sticky="ew", pady=2)

        text_widget = Text(frame, wrap=WORD, height=2, padx=5, pady=5, bg="#f0f0f0", font=("Helvetica", 10))
        text_widget.insert(1.0, text)
        text_widget.config(state=DISABLED)
        text_widget.grid(row=0, column=0, sticky="ew")

        copy_button = ttk.Button(frame, text="Copy", command=lambda i=i: copy_to_clipboard(i))
        copy_button.grid(row=0, column=1, padx=5)

        remove_button = ttk.Button(frame, text="X", command=lambda i=i: remove_item(i))
        remove_button.grid(row=0, column=2, padx=5)

        frame.columnconfigure(0, weight=1)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def addToList():
    global previous_content

    current_content = pyperclip.paste()

    if current_content != previous_content:
        if current_content:
            clipboard_list.append(current_content)
            update_display()

    previous_content = current_content
    root.after(500, addToList)

def startMonitoring():
    addToList()

style = ttk.Style()
style.configure("TFrame", background="#dfe3ee")
style.configure("TLabel", background="#dfe3ee", font=("Helvetica", 12))
style.configure("TButton", background="#4267B2", foreground="black", font=("Helvetica", 10, "bold"))
style.configure("TScrollbar", background="#f0f0f0")

main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.pack(fill=BOTH, expand=YES)

title_label = ttk.Label(main_frame, text="CopySave", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

items_frame = ttk.Labelframe(main_frame, text="Clipboard Items", padding=(10, 10, 10, 10))
items_frame.pack(fill=BOTH, expand=YES, pady=10)

canvas = Canvas(items_frame, bg="#ffffff")
canvas.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)

scrollbar = ttk.Scrollbar(items_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)

canvas_frame = Frame(canvas, bg="#ffffff")
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

root.after(0, startMonitoring)
root.mainloop()
