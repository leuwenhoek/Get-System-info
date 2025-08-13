import fetch
import plot
import show_data
import tkinter as tk
import os
from tkinter import ttk
import threading
import time
import webbrowser

def run_diagnose(progress_var, percent_label, start_btn, done_frame):
    start_btn.config(state='disabled')
    for i in range(34):
        time.sleep(0.03)
        progress_var.set(i)
        percent_label.config(text=f"{i}%")
    fetch.main()  # Call fetch.py
    for i in range(34, 67):
        time.sleep(0.03)
        progress_var.set(i)
        percent_label.config(text=f"{i}%")
    plot.main()   # Call plot.py
    for i in range(67, 101):
        time.sleep(0.03)
        progress_var.set(i)
        percent_label.config(text=f"{i}%")
    show_data.main()  # Call show_data.py
    done_frame.pack(fill='both', expand=True)
    percent_label.config(text="100%")
    start_btn.config(state='normal')

def open_report():
    webbrowser.open_new(os.path.join("main","Scripts","content","index.html"))

def main():
    root = tk.Tk()
    root.title("Get-System-Info Diagnose")
    root.geometry("400x250")
    root.resizable(False, False)

    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    start_btn = tk.Button(main_frame, text="Start Diagnose", font=("Segoe UI", 12, "bold"))
    start_btn.pack(pady=10)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate", variable=progress_var, maximum=100)
    percent_label = tk.Label(main_frame, text="0%", font=("Segoe UI", 10))
    progress_bar.pack(pady=10)
    percent_label.pack()

    done_frame = tk.Frame(root)
    done_label = tk.Label(done_frame, text="Done!", font=("Segoe UI", 14, "bold"), fg="#21a1c4")
    done_label.pack(pady=10)
    download_btn = tk.Button(done_frame, text="View Report", font=("Segoe UI", 12), command=open_report)
    download_btn.pack(pady=5)

    def start_process():
        done_frame.pack_forget()
        threading.Thread(target=run_diagnose, args=(progress_var, percent_label, start_btn, done_frame), daemon=True).start()

    start_btn.config(command=start_process)

    root.mainloop()

if __name__ == "__main__":
    main()