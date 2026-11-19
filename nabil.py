import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas
import numpy as np
from collections import deque
import copy


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = str(pid)
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)
        self.remaining_time = int(burst_time)
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.start_times = []
        self.end_times = []


class SchedulingSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("النظام المتقدم لمحاكاة خوارزميات الجدولة")
        self.root.geometry("1300x850")
        self.root.minsize(1050, 700)
        self.root.configure(bg="#2c3e50")

        self.processes = []
        self.current_algorithm = "Round Robin"
        self.quantum = 3
        self.is_playing = False

        self.setup_colors()
        self.setup_ui()

    def setup_colors(self):
        self.colors = {
            'P1': '#FF6B6B', 'P2': '#4ECDC4', 'P3': '#45B7D1',
            'P4': '#96CEB4', 'P5': '#FFEAA7', 'P6': '#DDA0DD',
            'P7': '#98D8C8', 'P8': '#F7DC6F', 'P9': '#BB8FCE',
            'P10': '#85C1E9', 'P11': '#F1948A', 'P12': '#82E0AA'
        }

    def setup_ui(self):
        # إطار العنوان
        title_frame = tk.Frame(self.root, bg="#34495e", height=75)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame, text="النظام المتقدم لمحاكاة خوارزميات الجدولة (CPU Scheduling)",
            font=("Arial", 18, "bold"), fg="#ecf0f1", bg="#34495e"
        )
        title_label.pack(expand=True)

        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=5)

        # اللوحة اليسرى (الإدخال والتحكم)
        left_panel = tk.Frame(main_frame, bg="#ecf0f1", width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # اللوحة اليمنى (النتائج ورسم جانت)
        right_panel = tk.Frame(main_frame, bg="#ecf0f1")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)

    def setup_left_panel(self, parent):
        # إطار خوارزمية الجدولة
        algo_frame = tk.LabelFrame(parent, text="إعدادات الخوارزمية", font=("Arial", 11, "bold"),
                                   bg="#ecf0f1", fg="#2c3e50", padx=10, pady=8)
        algo_frame.pack(fill=tk.X, pady=(0, 8))

        tk.Label(algo_frame, text="اختر الخوارزمية:", font=("Arial", 10), bg="#ecf0f1").pack(anchor=tk.W)
        self.algo_var = tk.StringVar(value="Round Robin")
        algo_combo = ttk.Combobox(
            algo_frame, textvariable=self.algo_var, state="readonly",
            values=["Round Robin", "FCFS", "SJF (Non-Preemptive)", "Priority (Non-Preemptive)", "SRTF (Preemptive SJF)"],
            font=("Arial", 10)
        )
        algo_combo.pack(fill=tk.X, pady=5)
        algo_combo.bind("<<ComboboxSelected>>", self.on_algorithm_change)

        # إطار الكم الزمني (يظهر فقط لـ Round Robin)
        self.quantum_frame = tk.Frame(algo_frame, bg="#ecf0f1")
        self.quantum_frame.pack(fill=tk.X, pady=4)

        tk.Label(self.quantum_frame, text="الكم الزمني (Quantum):", font=("Arial", 10), bg="#ecf0f1").pack(side=tk.LEFT)
        self.quantum_var = tk.StringVar(value="3")
        quantum_entry = tk.Entry(self.quantum_frame, textvariable=self.quantum_var, width=8, font=("Arial", 10))
        quantum_entry.pack(side=tk.LEFT, padx=6)

        # إطار إدخال العمليات
        input_frame = tk.LabelFrame(parent, text="إدخال العمليات", font=("Arial", 11, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50", padx=10, pady=8)
        input_frame.pack(fill=tk.BOTH, expand=True)

        # إدخال فردي
        single_input_frame = tk.Frame(input_frame, bg="#ecf0f1")
        single_input_frame.pack(fill=tk.X, pady=5)

        tk.Label(single_input_frame, text="PID:", bg="#ecf0f1", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=2)
        tk.Label(single_input_frame, text="الوصول:", bg="#ecf0f1", font=("Arial", 9, "bold")).grid(row=0, column=1, padx=2)
        tk.Label(single_input_frame, text="التنفيذ:", bg="#ecf0f1", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=2)
        tk.Label(single_input_frame, text="الأولوية:", bg="#ecf0f1", font=("Arial", 9, "bold")).grid(row=0, column=3, padx=2)

        self.pid_var = tk.StringVar()
        self.arrival_var = tk.StringVar()
        self.burst_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="0")

        tk.Entry(single_input_frame, textvariable=self.pid_var, width=6, font=("Arial", 9)).grid(row=1, column=0, padx=2)
        tk.Entry(single_input_frame, textvariable=self.arrival_var, width=6, font=("Arial", 9)).grid(row=1, column=1, padx=2)
        tk.Entry(single_input_frame, textvariable=self.burst_var, width=6, font=("Arial", 9)).grid(row=1, column=2, padx=2)
        tk.Entry(single_input_frame, textvariable=self.priority_var, width=6, font=("Arial", 9)).grid(row=1, column=3, padx=2)

        add_btn = tk.Button(single_input_frame, text="إضافة", command=self.add_process,
                            bg="#27ae60", fg="white", font=("Arial", 9, "bold"), cursor="hand2")
        add_btn.grid(row=1, column=4, padx=5)

        # الإدخال الجماعي
        tk.Label(input_frame, text="الإدخال الجماعي (PID, وقت الوصول, وقت التنفيذ, الأولوية):",
                 bg="#ecf0f1", font=("Arial", 9)).pack(anchor=tk.W, pady=(8, 3))

        self.bulk_entry = scrolledtext.ScrolledText(input_frame, height=5, font=("Consolas", 10))
        self.bulk_entry.pack(fill=tk.BOTH, expand=True)
        self.bulk_entry.insert(tk.END, "P1,0,5,1\nP2,1,3,2\nP3,2,8,3\nP4,3,6,4")

        bulk_btn = tk.Button(input_frame, text="📥 تحميل العمليات من النص الجماعي", command=self.add_bulk_processes,
                             bg="#2980b9", fg="white", font=("Arial", 10, "bold"), cursor="hand2")
        bulk_btn.pack(fill=tk.X, pady=6)

        # إطار أزرار التحكم
        control_frame = tk.LabelFrame(parent, text="التحكم بالمحاكاة", font=("Arial", 11, "bold"),
                                      bg="#ecf0f1", fg="#2c3e50", padx=10, pady=8)
        control_frame.pack(fill=tk.X, pady=(6, 0))

        self.play_btn = tk.Button(control_frame, text="▶ تشغيل المحاكاة", command=self.run_simulation,
                                  bg="#27ae60", fg="white", font=("Arial", 12, "bold"), cursor="hand2")
        self.play_btn.pack(fill=tk.X, pady=4)

        reset_btn = tk.Button(control_frame, text="🔄 إعادة تعيين", command=self.reset_simulation,
                              bg="#e74c3c", fg="white", font=("Arial", 10), cursor="hand2")
        reset_btn.pack(fill=tk.X, pady=4)

    def setup_right_panel(self, parent):
        # إطار مخطط جانت
        gantt_frame = tk.LabelFrame(parent, text="مخطط جانت (Gantt Chart)", font=("Arial", 11, "bold"),
                                    bg="#ecf0f1", fg="#2c3e50", padx=10, pady=8)
        gantt_frame.pack(fill=tk.X, pady=(0, 8))

        self.gantt_canvas = Canvas(gantt_frame, bg="#ffffff", height=140, bd=1, relief=tk.SUNKEN)
        self.gantt_canvas.pack(fill=tk.BOTH, expand=True)

        # إطار النتائج
        results_frame = tk.LabelFrame(parent, text="النتائج وجدول العمليات", font=("Arial", 11, "bold"),
                                      bg="#ecf0f1", fg="#2c3e50", padx=10, pady=8)
        results_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("PID", "Arrival", "Burst", "Priority", "Completion", "Turnaround", "Waiting")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)

        headers = {
            "PID": "معرف العملية (PID)",
            "Arrival": "وقت الوصول",
            "Burst": "وقت التنفيذ",
            "Priority": "الأولوية",
            "Completion": "وقت الانتهاء",
            "Turnaround": "وقت الاستجابة (TAT)",
            "Waiting": "وقت الانتظار (WT)"
        }

        for col in columns:
            self.results_tree.heading(col, text=headers.get(col, col))
            self.results_tree.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)

        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # إطار الإحصائيات العامة
        stats_frame = tk.Frame(parent, bg="#ffffff", bd=1, relief=tk.RIDGE)
        stats_frame.pack(fill=tk.X, pady=(8, 0), padx=2)

        self.avg_waiting_var = tk.StringVar(value="0.00")
        self.avg_turnaround_var = tk.StringVar(value="0.00")
        self.throughput_var = tk.StringVar(value="0.00")

        tk.Label(stats_frame, text="متوسط وقت الانتظار (Average WT):", font=("Arial", 10, "bold"),
                 bg="#ffffff", fg="#2c3e50").grid(row=0, column=0, padx=10, pady=6, sticky=tk.W)
        tk.Label(stats_frame, textvariable=self.avg_waiting_var, font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="#e67e22").grid(row=0, column=1, padx=5, sticky=tk.W)

        tk.Label(stats_frame, text="متوسط وقت الاستجابة (Average TAT):", font=("Arial", 10, "bold"),
                 bg="#ffffff", fg="#2c3e50").grid(row=0, column=2, padx=15, pady=6, sticky=tk.W)
        tk.Label(stats_frame, textvariable=self.avg_turnaround_var, font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="#2980b9").grid(row=0, column=3, padx=5, sticky=tk.W)

        tk.Label(stats_frame, text="الإنتاجية (Throughput):", font=("Arial", 10, "bold"),
                 bg="#ffffff", fg="#2c3e50").grid(row=0, column=4, padx=15, pady=6, sticky=tk.W)
        tk.Label(stats_frame, textvariable=self.throughput_var, font=("Arial", 11, "bold"),
                 bg="#ffffff", fg="#27ae60").grid(row=0, column=5, padx=5, sticky=tk.W)

    def on_algorithm_change(self, event=None):
        algorithm = self.algo_var.get()
        if algorithm == "Round Robin":
            self.quantum_frame.pack(fill=tk.X, pady=4)
        else:
            self.quantum_frame.pack_forget()

    def add_process(self):
        try:
            pid = self.pid_var.get().strip()
            if not pid:
                messagebox.showerror("خطأ", "يرجى إدخال معرف العملية (PID)")
                return
            arrival = int(self.arrival_var.get().strip())
            burst = int(self.burst_var.get().strip())
            priority = int(self.priority_var.get().strip()) if self.priority_var.get().strip() else 0

            if burst <= 0:
                messagebox.showerror("خطأ", "وقت التنفيذ (Burst Time) يجب أن يكون موجباً")
                return

            self.processes.append(Process(pid, arrival, burst, priority))
            messagebox.showinfo("نجاح", f"تمت إضافة العملية {pid} بنجاح!")
            self.clear_input_fields()

        except ValueError:
            messagebox.showerror("خطأ", "يرجى التأكد من إدخال أرقام صحيحة لوقت الوصول والتنفيذ والأولوية.")

    def add_bulk_processes(self):
        try:
            text = self.bulk_entry.get("1.0", tk.END).strip()
            lines = text.split('\n')
            new_processes = []

            for line in lines:
                line = line.strip()
                if line:
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 3:
                        pid = parts[0]
                        arrival = int(parts[1])
                        burst = int(parts[2])
                        priority = int(parts[3]) if len(parts) > 3 else 0

                        if burst > 0:
                            new_processes.append(Process(pid, arrival, burst, priority))

            if new_processes:
                self.processes = new_processes
                messagebox.showinfo("نجاح", f"تم تحميل {len(new_processes)} عمليات بنجاح! جاهز للتشغيل.")
            else:
                messagebox.showwarning("تنبيه", "لم يتم العثور على أسطر صالحة. التنسيق: PID, Arrival, Burst, Priority")

        except ValueError:
            messagebox.showerror("خطأ", "تنسيق البيانات غير صحيح. تأكد من أن الأوقات والأولويات أرقام صحيحة.")

    def clear_input_fields(self):
        self.pid_var.set("")
        self.arrival_var.set("")
        self.burst_var.set("")
        self.priority_var.set("0")

    def run_simulation(self):
        if not self.processes:
            # محاولة تحميل من النص الجماعي إذا لم تكن هناك عمليات مضافة
            self.add_bulk_processes()
            if not self.processes:
                messagebox.showerror("خطأ", "يرجى إدخال أو تحميل العمليات أولاً.")
                return

        algorithm = self.algo_var.get()
        proc_list = [copy.deepcopy(p) for p in self.processes]

        gantt = []
        if algorithm == "Round Robin":
            try:
                quantum = int(self.quantum_var.get())
                if quantum <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("خطأ", "يجب أن يكون الكم الزمني (Quantum) رقماً صحيحاً موجباً.")
                return
            proc_list, gantt = self.simulate_round_robin(proc_list, quantum)

        elif "FCFS" in algorithm:
            proc_list, gantt = self.simulate_fcfs(proc_list)

        elif "SJF" in algorithm:
            proc_list, gantt = self.simulate_sjf(proc_list)

        elif "Priority" in algorithm:
            proc_list, gantt = self.simulate_priority(proc_list)

        elif "SRTF" in algorithm:
            proc_list, gantt = self.simulate_srtf(proc_list)

        # عرض النتائج في الجدول
        self.display_results(proc_list, gantt)

    def simulate_fcfs(self, processes):
        processes.sort(key=lambda x: (x.arrival_time, x.pid))
        time = 0
        gantt = []

        for p in processes:
            if time < p.arrival_time:
                time = p.arrival_time
            start = time
            time += p.burst_time
            end = time
            gantt.append((p.pid, start, end))

            p.completion_time = end
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

        return processes, gantt

    def simulate_sjf(self, processes):
        n = len(processes)
        time = 0
        completed = 0
        gantt = []
        visited = set()

        while completed < n:
            available = [p for p in processes if p.arrival_time <= time and p.pid not in visited]
            if not available:
                remaining = [p for p in processes if p.pid not in visited]
                time = min(p.arrival_time for p in remaining)
                continue

            # اختيار الأقصر تنفيذاً
            current = min(available, key=lambda x: (x.burst_time, x.arrival_time))
            start = time
            time += current.burst_time
            end = time
            gantt.append((current.pid, start, end))

            current.completion_time = end
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time

            visited.add(current.pid)
            completed += 1

        return processes, gantt

    def simulate_priority(self, processes):
        n = len(processes)
        time = 0
        completed = 0
        gantt = []
        visited = set()

        while completed < n:
            available = [p for p in processes if p.arrival_time <= time and p.pid not in visited]
            if not available:
                remaining = [p for p in processes if p.pid not in visited]
                time = min(p.arrival_time for p in remaining)
                continue

            # اختيار الأقل رقماً (أعلى أولوية)
            current = min(available, key=lambda x: (x.priority, x.arrival_time))
            start = time
            time += current.burst_time
            end = time
            gantt.append((current.pid, start, end))

            current.completion_time = end
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time

            visited.add(current.pid)
            completed += 1

        return processes, gantt

    def simulate_round_robin(self, processes, quantum):
        time = 0
        queue = deque()
        gantt = []

        processes.sort(key=lambda x: (x.arrival_time, x.pid))
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
            start = time
            time += exec_time
            end = time
            gantt.append((current.pid, start, end))
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

    def simulate_srtf(self, processes):
        n = len(processes)
        time = 0
        completed = 0
        raw_slices = []

        max_limit = sum(p.burst_time for p in processes) + max(p.arrival_time for p in processes) + 10

        while completed < n and time < max_limit:
            available = [p for p in processes if p.arrival_time <= time and p.remaining_time > 0]
            if not available:
                time += 1
                continue

            current = min(available, key=lambda x: (x.remaining_time, x.arrival_time))
            current.remaining_time -= 1
            raw_slices.append((current.pid, time, time + 1))
            time += 1

            if current.remaining_time == 0:
                current.completion_time = time
                current.turnaround_time = current.completion_time - current.arrival_time
                current.waiting_time = current.turnaround_time - current.burst_time
                completed += 1

        # دمج الشرائح الزمنية المتتالية لنفس العملية
        compressed_gantt = []
        for pid, s, e in raw_slices:
            if compressed_gantt and compressed_gantt[-1][0] == pid and compressed_gantt[-1][2] == s:
                compressed_gantt[-1] = (pid, compressed_gantt[-1][1], e)
            else:
                compressed_gantt.append((pid, s, e))

        return processes, compressed_gantt

    def display_results(self, processes, gantt):
        self.clear_results()

        processes.sort(key=lambda x: x.pid)
        for p in processes:
            self.results_tree.insert(
                "", tk.END,
                values=(p.pid, p.arrival_time, p.burst_time, p.priority,
                        p.completion_time, p.turnaround_time, p.waiting_time)
            )

        if processes:
            avg_wt = sum(p.waiting_time for p in processes) / len(processes)
            avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
            max_time = max(end for _, _, end in gantt) if gantt else 1
            throughput = len(processes) / max_time if max_time > 0 else 0

            self.avg_waiting_var.set(f"{avg_wt:.2f}")
            self.avg_turnaround_var.set(f"{avg_tat:.2f}")
            self.throughput_var.set(f"{throughput:.3f} عمل/وحدة زمن")

        self.draw_gantt(gantt)

    def draw_gantt(self, gantt):
        self.gantt_canvas.delete("all")
        if not gantt:
            return

        canvas_width = self.gantt_canvas.winfo_width()
        canvas_height = self.gantt_canvas.winfo_height()

        if canvas_width < 100:
            canvas_width = 800
        if canvas_height < 50:
            canvas_height = 140

        max_time = max(end for _, _, end in gantt)
        margin_left = 40
        margin_right = 40
        usable_width = canvas_width - margin_left - margin_right
        scale = usable_width / max(1, max_time)

        y_top = 30
        y_bottom = 85

        for pid, start, end in gantt:
            x1 = margin_left + start * scale
            x2 = margin_left + end * scale
            color = self.colors.get(pid, '#3498db')

            # رسم مستطيل العملية
            self.gantt_canvas.create_rectangle(x1, y_top, x2, y_bottom, fill=color, outline="#2c3e50", width=2)
            # اسم العملية
            mid_x = (x1 + x2) / 2
            self.gantt_canvas.create_text(mid_x, (y_top + y_bottom) / 2, text=pid, font=("Arial", 10, "bold"), fill="#2c3e50")

            # العلامات الزمنية للبداية والنهاية
            self.gantt_canvas.create_text(x1, y_bottom + 14, text=str(start), font=("Arial", 8))
            self.gantt_canvas.create_text(x2, y_bottom + 14, text=str(end), font=("Arial", 8))

        # خط الأساس الزمني
        self.gantt_canvas.create_line(margin_left, y_bottom + 5, margin_left + max_time * scale, y_bottom + 5,
                                      width=2, fill="#7f8c8d")

    def reset_simulation(self):
        self.processes.clear()
        self.gantt_canvas.delete("all")
        self.clear_results()

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
