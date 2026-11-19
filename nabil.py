import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from collections import deque
import time
import threading


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_times = []
        self.end_times = []


class SchedulingSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("النظام المتقدم لمحاكاة خوارزميات الجدولة")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c3e50")

        self.processes = []
        self.current_algorithm = "Round Robin"
        self.quantum = 3
        self.speed = 1.0
        self.is_playing = False

        self.setup_ui()
        self.setup_colors()

    def setup_colors(self):
        self.colors = {
            'P1': '#FF6B6B', 'P2': '#4ECDC4', 'P3': '#45B7D1',
            'P4': '#96CEB4', 'P5': '#FFEAA7', 'P6': '#DDA0DD',
            'P7': '#98D8C8', 'P8': '#F7DC6F', 'P9': '#BB8FCE',
            'P10': '#85C1E9'
        }

    def setup_ui(self):
        # إطار العنوان
        title_frame = tk.Frame(self.root, bg="#34495e", height=80)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="النظام المتقدم لمحاكاة خوارزميات الجدولة",
                               font=("Arial", 20, "bold"), fg="#ecf0f1", bg="#34495e")
        title_label.pack(expand=True)

        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # اللوحة اليسرى (الإدخال والتحكم)
        left_panel = tk.Frame(main_frame, bg="#ecf0f1", width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        # اللوحة اليمنى (النتائج والرسم البياني)
        right_panel = tk.Frame(main_frame, bg="#ecf0f1")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)

    def setup_left_panel(self, parent):
        # إطار خوارزمية الجدولة
        algo_frame = tk.LabelFrame(parent, text="إعدادات الخوارزمية", font=("Arial", 12, "bold"),
                                   bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        algo_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(algo_frame, text="اختر الخوارزمية:", bg="#ecf0f1").pack(anchor=tk.W)
        self.algo_var = tk.StringVar(value="Round Robin")
        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var,
                                  values=["Round Robin", "FCFS", "SJF", "Priority", "SRTF"])
        algo_combo.pack(fill=tk.X, pady=5)
        algo_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        # إطار الكم الزمني (يظهر فقط لـ Round Robin)
        self.quantum_frame = tk.Frame(algo_frame, bg="#ecf0f1")
        self.quantum_frame.pack(fill=tk.X, pady=5)

        tk.Label(self.quantum_frame, text="الكم الزمني:", bg="#ecf0f1").pack(side=tk.LEFT)
        self.quantum_var = tk.StringVar(value="3")
        quantum_entry = tk.Entry(self.quantum_frame, textvariable=self.quantum_var, width=10)
        quantum_entry.pack(side=tk.LEFT, padx=5)

        # إطار إدخال العمليات
        input_frame = tk.LabelFrame(parent, text="إدخال العمليات", font=("Arial", 12, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        input_frame.pack(fill=tk.BOTH, expand=True)

        # إدخال فردي
        single_input_frame = tk.Frame(input_frame, bg="#ecf0f1")
        single_input_frame.pack(fill=tk.X, pady=5)

        tk.Label(single_input_frame, text="PID:", bg="#ecf0f1").grid(row=0, column=0, padx=2)
        tk.Label(single_input_frame, text="وقت الوصول:", bg="#ecf0f1").grid(row=0, column=1, padx=2)
        tk.Label(single_input_frame, text="وقت التنفيذ:", bg="#ecf0f1").grid(row=0, column=2, padx=2)
        tk.Label(single_input_frame, text("الأولوية:"), bg="#ecf0f1").grid(row=0, column=3, padx=2)

        self.pid_var = tk.StringVar()
        self.arrival_var = tk.StringVar()
        self.burst_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="0")

        tk.Entry(single_input_frame, textvariable=self.pid_var, width=8).grid(row=1, column=0, padx=2)
        tk.Entry(single_input_frame, textvariable=self.arrival_var, width=8).grid(row=1, column=1, padx=2)
        tk.Entry(single_input_frame, textvariable=self.burst_var, width=8).grid(row=1, column=2, padx=2)
        tk.Entry(single_input_frame, textvariable=self.priority_var, width=8).grid(row=1, column=3, padx=2)

        add_btn = tk.Button(single_input_frame, text="إضافة عملية", command=self.add_process,
                            bg="#27ae60", fg="white")
        add_btn.grid(row=1, column=4, padx=5)

        # الإدخال الجماعي
        tk.Label(input_frame, text="الإدخال الجماعي (سطر لكل عملية: PID,Arrival,Burst,Priority):",
                 bg="#ecf0f1").pack(anchor=tk.W, pady=(10, 5))

        self.bulk_entry = scrolledtext.ScrolledText(input_frame, height=8, font=("Consolas", 10))
        self.bulk_entry.pack(fill=tk.BOTH, expand=True)
        self.bulk_entry.insert(tk.END, "P1,0,5,1\nP2,1,3,2\nP3,2,8,3\nP4,3,6,4")

        bulk_btn = tk.Button(input_frame, text="إضافة العمليات", command=self.add_bulk_processes,
                             bg="#2980b9", fg="white")
        bulk_btn.pack(pady=5)

        # إطار التحكم
        control_frame = tk.LabelFrame(parent, text="التحكم بالمحاكاة", font=("Arial", 12, "bold"),
                                      bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        control_frame.pack(fill=tk.X, pady=(10, 0))

        control_subframe = tk.Frame(control_frame, bg="#ecf0f1")
        control_subframe.pack(fill=tk.X)

        self.play_btn = tk.Button(control_subframe, text="▶ تشغيل", command=self.toggle_play,
                                  bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
        self.play_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(control_subframe, text="🔄 إعادة تعيين", command=self.reset_simulation,
                              bg="#e74c3c", fg="white")
        reset_btn.pack(side=tk.LEFT, padx=5)

        # سرعة المحاكاة
        speed_frame = tk.Frame(control_frame, bg="#ecf0f1")
        speed_frame.pack(fill=tk.X, pady=5)

        tk.Label(speed_frame, text="سرعة المحاكاة:", bg="#ecf0f1").pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=0.1, to=2.0, resolution=0.1,
                                    orient=tk.HORIZONTAL, length=150, showvalue=True)
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side=tk.LEFT, padx=5)

    def setup_right_panel(self, parent):
        # إطار مخطط جانت
        gantt_frame = tk.LabelFrame(parent, text="مخطط جانت الحي", font=("Arial", 12, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        gantt_frame.pack(fill=tk.BOTH, expand=True)

        self.gantt_canvas = Canvas(gantt_frame, bg="white", height=200)
        self.gantt_canvas.pack(fill=tk.BOTH, expand=True)

        # إطار النتائج
        results_frame = tk.LabelFrame(parent, text="النتائج والإحصائيات", font=("Arial", 12, "bold"),
                                      bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # جدول النتائج
        columns = ("PID", "Arrival", "Burst", "Priority", "Completion", "Turnaround", "Waiting")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=80)

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # الإحصائيات
        stats_frame = tk.Frame(results_frame, bg="#ecf0f1")
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        self.avg_waiting_var = tk.StringVar(value="0.00")
        self.avg_turnaround_var = tk.StringVar(value="0.00")
        self.throughput_var = tk.StringVar(value="0.00")

        tk.Label(stats_frame, text="متوسط وقت الانتظار:", bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W)
        tk.Label(stats_frame, textvariable=self.avg_waiting_var, bg="#ecf0f1").grid(row=0, column=1, sticky=tk.W)

        tk.Label(stats_frame, text="متوسط وقت الاستجابة:", bg="#ecf0f1").grid(row=1, column=0, sticky=tk.W)
        tk.Label(stats_frame, textvariable=self.avg_turnaround_var, bg="#ecf0f1").grid(row=1, column=1, sticky=tk.W)

        tk.Label(stats_frame, text="الإنتاجية:", bg="#ecf0f1").grid(row=2, column=0, sticky=tk.W)
        tk.Label(stats_frame, textvariable=self.throughput_var, bg="#ecf0f1").grid(row=2, column=1, sticky=tk.W)

    def on_algorithm_change(self, event):
        algorithm = self.algo_var.get()
        if algorithm == "Round Robin":
            self.quantum_frame.pack(fill=tk.X, pady=5)
        else:
            self.quantum_frame.pack_forget()

    def add_process(self):
        try:
            pid = self.pid_var.get()
            arrival = int(self.arrival_var.get())
            burst = int(self.burst_var.get())
            priority = int(self.priority_var.get())

            if burst <= 0:
                messagebox.showerror("خطأ", "وقت التنفيذ يجب أن يكون موجباً")
                return

            self.processes.append(Process(pid, arrival, burst, priority))
            messagebox.showinfo("نجاح", f"تمت إضافة العملية {pid}")

            self.clear_input_fields()

        except ValueError:
            messagebox.showerror("خطأ", "يرجى إدخال قيم صحيحة")

    def add_bulk_processes(self):
        try:
            text = self.bulk_entry.get("1.0", tk.END).strip()
            lines = text.split('\n')

            for line in lines:
                if line.strip():
                    parts = line.split(',')
                    if len(parts) >= 3:
                        pid = parts[0].strip()
                        arrival = int(parts[1].strip())
                        burst = int(parts[2].strip())
                        priority = int(parts[3].strip()) if len(parts) > 3 else 0

                        if burst > 0:
                            self.processes.append(Process(pid, arrival, burst, priority))

            messagebox.showinfo("نجاح", f"تمت إضافة {len(lines)} عمليات")

        except ValueError:
            messagebox.showerror("خطأ", "تنسيق البيانات غير صحيح")

    def clear_input_fields(self):
        self.pid_var.set("")
        self.arrival_var.set("")
        self.burst_var.set("")
        self.priority_var.set("0")

    def toggle_play(self):
        if not self.processes:
            messagebox.showerror("خطأ", "يرجى إضافة عمليات أولاً")
            return

        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_btn.config(text="⏸ إيقاف", bg="#e67e22")
            self.run_simulation()
        else:
            self.play_btn.config(text="▶ تشغيل", bg="#27ae60")

    def run_simulation(self):
        # هنا سيتم تنفيذ المحاكاة الفعلية
        # هذه وظيفة افتراضية تحتاج إلى التطبيق الكامل
        algorithm = self.algo_var.get()
        quantum = int(self.quantum_var.get()) if algorithm == "Round Robin" else 0

        # محاكاة بسيطة للعرض
        self.animate_simulation()

    def animate_simulation(self):
        def animation_thread():
            # محاكاة الرسم الحي
            total_time = sum(p.burst_time for p in self.processes)
            current_time = 0

            while current_time <= total_time and self.is_playing:
                self.draw_gantt(current_time)
                current_time += 1
                time.sleep(1.0 / self.speed_scale.get())

            self.is_playing = False
            self.play_btn.config(text="▶ تشغيل", bg="#27ae60")

        thread = threading.Thread(target=animation_thread)
        thread.daemon = True
        thread.start()

    def draw_gantt(self, current_time):
        self.gantt_canvas.delete("all")

        # رسم مخطط جانت مبسط للعرض
        width = self.gantt_canvas.winfo_width()
        height = self.gantt_canvas.winfo_height()

        if width < 10 or height < 10:
            return

        # رسم الخط الزمني
        self.gantt_canvas.create_line(50, height - 30, width - 50, height - 30, width=2)

        # رسم العلامات الزمنية
        for i in range(0, current_time + 5, 5):
            x = 50 + (i * (width - 100) / (current_time + 10))
            self.gantt_canvas.create_line(x, height - 35, x, height - 25, width=1)
            self.gantt_canvas.create_text(x, height - 20, text=str(i))

    def reset_simulation(self):
        self.is_playing = False
        self.processes.clear()
        self.gantt_canvas.delete("all")
        self.clear_results()
        self.play_btn.config(text="▶ تشغيل", bg="#27ae60")

    def clear_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        self.avg_waiting_var.set("0.00")
        self.avg_turnaround_var.set("0.00")
        self.throughput_var.set("0.00")

    def run(self):
        self.root.mainloop()


# تشغيل النظام
if __name__ == "__main__":
    simulator = SchedulingSimulator()
    simulator.run()