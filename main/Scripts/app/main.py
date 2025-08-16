import fetch
import plot
import show_data
import tkinter as tk
from tkinter import messagebox
import os
from tkinter import ttk
import threading
import time
import webbrowser
import traceback
import sys
import matplotlib.pyplot as plt

def show_error(error_type, error_msg, traceback_info):
    error_window = tk.Toplevel()
    error_window.title("Error Occurred")
    error_window.geometry("500x400")
    error_window.configure(bg="#0f1419")
    
    # Error frame
    error_frame = tk.Frame(error_window, bg="#0f1419", padx=20, pady=20)
    error_frame.pack(fill='both', expand=True)
    
    # Error type
    tk.Label(error_frame, 
            text=f"Error Type: {error_type}",
            fg="#ff4d4d",
            bg="#0f1419",
            font=("Segoe UI", 12, "bold")).pack(pady=(0,10))
    
    # Error message
    tk.Label(error_frame,
            text="Error Message:",
            fg="#61dafb",
            bg="#0f1419",
            font=("Segoe UI", 10, "bold")).pack(anchor='w')
    
    error_text = tk.Text(error_frame, 
                        height=4,
                        bg="#1a2332",
                        fg="#e8eaed",
                        font=("Consolas", 10))
    error_text.insert('1.0', error_msg)
    error_text.config(state='disabled')
    error_text.pack(fill='x', pady=(0,10))
    
    # Traceback
    tk.Label(error_frame,
            text="Traceback:",
            fg="#61dafb",
            bg="#0f1419",
            font=("Segoe UI", 10, "bold")).pack(anchor='w')
    
    trace_text = tk.Text(error_frame,
                        height=8,
                        bg="#1a2332",
                        fg="#e8eaed",
                        font=("Consolas", 10))
    trace_text.insert('1.0', traceback_info)
    trace_text.config(state='disabled')
    trace_text.pack(fill='x', pady=(0,10))
    
    # Help link
    help_link = tk.Label(error_frame,
                        text="Get help at: Get-System-Info Support",
                        fg="#61dafb",
                        bg="#0f1419",
                        cursor="hand2",
                        font=("Segoe UI", 10, "underline"))
    help_link.pack(pady=10)
    help_link.bind("<Button-1>", lambda e: webbrowser.open("http://localhost:5000/help"))

def run_diagnose(progress_var, percent_label, start_btn, done_frame):
    start_btn.config(state='disabled')
    try:
        # Fetch data (34%)
        for i in range(34):
            time.sleep(0.03)
            progress_var.set(i)
            percent_label.config(text=f"{i}%")
        fetch.main()

        # Plot data (33%)
        for i in range(34, 67):
            time.sleep(0.03)
            progress_var.set(i)
            percent_label.config(text=f"{i}%")
        # Run plot in main thread
        root.after(0, plot.main)
        
        # Generate report (33%)
        for i in range(67, 101):
            time.sleep(0.03)
            progress_var.set(i)
            percent_label.config(text=f"{i}%")
        show_data.main()
        
        done_frame.pack(fill='both', expand=True)
        percent_label.config(text="100%")
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        traceback_info = traceback.format_exc()
        root.after(0, lambda: show_error(error_type, error_msg, traceback_info))
    finally:
        # Cleanup matplotlib
        plt.close('all')
        start_btn.config(state='normal')

def open_report():
    webbrowser.open_new(os.path.join("main","Scripts","content","index.html"))

def main():
    global root  # Make root accessible to run_diagnose
    root = tk.Tk()
    root.title("Get-System-Info Diagnose")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(bg="#0f233a")

    # Report Issue Link Frame
    report_frame = tk.Frame(root, bg="#0f233a", pady=5)
    report_frame.pack(fill='x')
    
    # Website Link
    report_link = tk.Label(
        report_frame,
        text="Report Issues → get-system-info.web.app/report",
        font=("Segoe UI", 9),
        fg="#61dafb",
        bg="#0f233a",
        cursor="hand2"
    )
    report_link.pack()
    report_link.bind("<Button-1>", lambda e: webbrowser.open("http://localhost:5000/report"))
    
    # Separator
    tk.Frame(root, height=1, bg="#21a1c4").pack(fill='x', padx=10)

    # Main content frame
    main_frame = tk.Frame(root, bg="#0f233a")
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)

    start_btn = tk.Button(
        main_frame, 
        text="Start Diagnose", 
        font=("Segoe UI", 12, "bold"),
        bg="#21a1c4",
        fg="white",
        activebackground="#61dafb"
    )
    start_btn.pack(pady=10)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(
        main_frame, 
        orient="horizontal", 
        length=300, 
        mode="determinate", 
        variable=progress_var, 
        maximum=100
    )
    percent_label = tk.Label(
        main_frame, 
        text="0%", 
        font=("Segoe UI", 10), 
        bg="#0f233a", 
        fg="#61dafb"
    )
    progress_bar.pack(pady=10)
    percent_label.pack()

    done_frame = tk.Frame(root, bg="#0f233a")
    done_label = tk.Label(
        done_frame, 
        text="Done!", 
        font=("Segoe UI", 14, "bold"), 
        fg="#21a1c4",
        bg="#0f233a"
    )
    done_label.pack(pady=10)
    download_btn = tk.Button(
        done_frame, 
        text="View Report", 
        font=("Segoe UI", 12), 
        command=open_report,
        bg="#21a1c4",
        fg="white",
        activebackground="#61dafb"
    )
    download_btn.pack(pady=5)

    def start_process():
        done_frame.pack_forget()
        threading.Thread(
            target=run_diagnose, 
            args=(progress_var, percent_label, start_btn, done_frame), 
            daemon=True
        ).start()

    start_btn.config(command=start_process)

    root.mainloop()

if __name__ == "__main__":
    main()