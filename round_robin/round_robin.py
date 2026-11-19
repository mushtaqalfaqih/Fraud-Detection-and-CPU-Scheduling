import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import io
from collections import deque


# ==============================
# تعريف الكلاس Process
# ==============================
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


# ==============================
# خوارزمية Round Robin
# ==============================
def run_round_robin(processes, quantum):
    time = 0
    queue = deque()
    gantt = []

    processes.sort(key=lambda x: x.arrival_time)
    n = len(processes)
    idx = 0
    completed = 0

    while completed < n:
        while idx < n and processes[idx].arrival_time <= time:
            queue.append(processes[idx])
            idx += 1

        if not queue:
            time = processes[idx].arrival_time
            continue

        current = queue.popleft()
        exec_time = min(quantum, current.remaining_time)
        gantt.append((current.pid, time, time + exec_time))
        time += exec_time
        current.remaining_time -= exec_time

        while idx < n and processes[idx].arrival_time <= time:
            queue.append(processes[idx])
            idx += 1

        if current.remaining_time > 0:
            queue.append(current)
        else:
            current.completion_time = time
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time
            completed += 1

    return processes, gantt


# ==============================
# طباعة النتائج
# ==============================
def print_results(processes, gantt):
    output = ""
    output += "╔══════════════════════════════════════════════════════════════╗\n"
    output += "║                      نتائج خوارزمية Round Robin             ║\n"
    output += "╠══════════════════════════════════════════════════════════════╣\n"
    output += "{:<8} {:<12} {:<12} {:<14} {:<14} {:<12}\n".format(
        "PID", "وقت الوصول", "وقت التنفيذ", "وقت الانتهاء", "وقت الاستجابة", "وقت الانتظار"
    )
    output += "╟──────────────────────────────────────────────────────────────╢\n"

    for p in processes:
        output += "{:<8} {:<12} {:<12} {:<14} {:<14} {:<12}\n".format(
            p.pid, p.arrival_time, p.burst_time,
            p.completion_time, p.turnaround_time, p.waiting_time
        )

    avg_wt = sum(p.waiting_time for p in processes) / len(processes)
    avg_tat = sum(p.turnaround_time for p in processes) / len(processes)

    output += "╠══════════════════════════════════════════════════════════════╣\n"
    output += f"متوسط وقت الانتظار: {avg_wt:.2f}\n"
    output += f"متوسط وقت الاستجابة: {avg_tat:.2f}\n"
    output += "╚══════════════════════════════════════════════════════════════╝\n\n"

    output += "╔══════════════════════════════════════════════════════════════╗\n"
    output += "║                         مخطط جانت                           ║\n"
    output += "╠══════════════════════════════════════════════════════════════╣\n"

    timeline = ""
    for pid, start, end in gantt:
        duration = end - start
        bar = "▇" * duration
        timeline += f"{pid}: {start:2d} [{bar}] {end:2d}\n"

    output += timeline
    output += "╚══════════════════════════════════════════════════════════════╝\n"

    return output


# ==============================
# الدالة المرتبطة بالزر
# ==============================
def run_algorithm_and_display_results():
    try:
        quantum = int(quantum_entry.get())
        if quantum <= 0:
            messagebox.showerror("خطأ", "يجب أن يكون الكم الزمني (Quantum) رقمًا موجبًا.")
            return

        processes_data_str = processes_entry.get("1.0", tk.END).strip().split('\n')
        processes_to_run = []
        for line in processes_data_str:
            if line.strip():
                parts = line.split(',')
                if len(parts) != 3:
                    messagebox.showerror("خطأ", "تنسيق البيانات غير صحيح. يجب أن يكون: PID, Arrival Time, Burst Time")
                    return
                pid = parts[0].strip()
                arrival_time = int(parts[1].strip())
                burst_time = int(parts[2].strip())
                processes_to_run.append(Process(pid, arrival_time, burst_time))

        if not processes_to_run:
            messagebox.showerror("خطأ", "يرجى إدخال بيانات العمليات.")
            return

        final_processes, gantt = run_round_robin(processes_to_run, quantum)
        result_text = print_results(final_processes, gantt)

        results_display.config(state=tk.NORMAL)
        results_display.delete("1.0", tk.END)
        results_display.insert(tk.END, result_text)
        results_display.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("خطأ", "البيانات المدخلة يجب أن تكون أرقامًا صحيحة.")
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ غير متوقع: {e}")


# ==============================
# تشغيل واجهة المستخدم
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("محاكي خوارزمية Round Robin - مخطط جدولة العمليات")
    root.geometry("1000x700")
    root.configure(bg="#2c3e50")

    # إطار العنوان
    title_frame = tk.Frame(root, bg="#34495e", height=80)
    title_frame.pack(fill=tk.X, pady=(0, 10))
    title_frame.pack_propagate(False)

    title_label = tk.Label(title_frame, text="محاكي خوارزمية Round Robin",
                           font=("Arial", 20, "bold"), fg="#ecf0f1", bg="#34495e")
    title_label.pack(expand=True)

    # إطار الإدخال الرئيسي
    main_frame = tk.Frame(root, bg="#ecf0f1", padx=15, pady=15, relief=tk.RIDGE, bd=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # إطار إدخال البيانات
    input_frame = tk.LabelFrame(main_frame, text="إدخال البيانات", font=("Arial", 12, "bold"),
                                bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
    input_frame.pack(fill=tk.X, pady=(0, 10))

    # إدخال الكم الزمني
    quantum_frame = tk.Frame(input_frame, bg="#ecf0f1")
    quantum_frame.pack(fill=tk.X, pady=5)

    tk.Label(quantum_frame, text="الكم الزمني (Quantum):", font=("Arial", 12),
             bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=5)
    quantum_entry = tk.Entry(quantum_frame, width=10, font=("Arial", 12),
                             bg="#ffffff", fg="#2c3e50", relief=tk.SUNKEN, bd=2)
    quantum_entry.pack(side=tk.LEFT, padx=5)
    quantum_entry.insert(0, "3")

    # إدخال العمليات
    processes_frame = tk.Frame(input_frame, bg="#ecf0f1")
    processes_frame.pack(fill=tk.X, pady=10)

    tk.Label(processes_frame, text="بيانات العمليات (PID, وقت الوصول, وقت التنفيذ):",
             font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50").pack(anchor=tk.W, padx=5)

    processes_entry = scrolledtext.ScrolledText(processes_frame, height=5, width=50,
                                                font=("Consolas", 10), wrap=tk.WORD,
                                                bg="#ffffff", fg="#2c3e50",
                                                relief=tk.SUNKEN, bd=2)
    processes_entry.pack(fill=tk.X, padx=5, pady=5)
    processes_entry.insert(tk.END, "P1, 0, 5\nP2, 1, 3\nP3, 2, 8\nP4, 3, 6")

    # زر التشغيل
    button_frame = tk.Frame(main_frame, bg="#ecf0f1")
    button_frame.pack(fill=tk.X, pady=10)

    run_button = tk.Button(button_frame, text="تشغيل الخوارزمية",
                           command=run_algorithm_and_display_results,
                           font=("Arial", 14, "bold"),
                           bg="#27ae60", fg="white",
                           activebackground="#2ecc71",
                           relief=tk.RAISED, bd=3,
                           padx=20, pady=10)
    run_button.pack(pady=10)

    # إطار النتائج
    results_frame = tk.LabelFrame(main_frame, text="النتائج", font=("Arial", 12, "bold"),
                                  bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
    results_frame.pack(fill=tk.BOTH, expand=True)

    results_display = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD,
                                                bg="#f8f9fa", fg="#2c3e50",
                                                font=("Consolas", 10),
                                                relief=tk.SUNKEN, bd=2,
                                                state=tk.DISABLED)
    results_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # تذييل الصفحة
    footer_frame = tk.Frame(root, bg="#34495e", height=30)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    footer_frame.pack_propagate(False)

    footer_label = tk.Label(footer_frame, text="تم التطوير باستخدام Python و Tkinter",
                            font=("Arial", 10), fg="#bdc3c7", bg="#34495e")
    footer_label.pack(expand=True)

    # تشغيل التطبيق
    root.mainloop()
