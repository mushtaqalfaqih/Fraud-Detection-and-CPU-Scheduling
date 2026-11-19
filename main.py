"""
نظام كشف الاحتيال في المعاملات المالية | Credit Card Fraud Detection System
واجهة مستخدم رسومية متقدمة (GUI) مدعومة بنموذج Random Forest
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import numpy as np
import pandas as pd
from PIL import Image, ImageTk

# ضبط المسارات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
MODEL_PATH = os.path.join(MODELS_DIR, 'trained_model.pkl')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')
SAMPLES_PATH = os.path.join(DATA_DIR, 'samples_for_gui.csv')


class FraudDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام كشف الاحتيال المالي الذكي | Fraud Detection System")
        self.root.geometry("1100x780")
        self.root.minsize(950, 680)
        self.root.configure(bg="#f1f5f9")

        # المتغيرات الأساسية
        self.model = None
        self.scaler = None
        self.samples_df = None
        self.current_sample_actual_class = None
        self.feature_entries = {}
        self.current_image_obj = None

        # أسماء الميزات بالترتيب
        self.feature_names = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']

        # تجهيز الثيم والواجهة
        self.setup_styles()
        self.create_header()
        self.create_tabs()
        self.create_footer()

        # تحميل النموذج والعينات في خيط خلفي حتى تفتح الواجهة فوراً
        self.root.after(100, self.async_load_resources)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # ألوان النظام
        self.PRIMARY = "#1e3a8a"    # كحلي داكن
        self.SECONDARY = "#3b82f6"  # أزرق ساطع
        self.SUCCESS = "#10b981"    # أخضر
        self.DANGER = "#ef4444"     # أحمر
        self.BG_LIGHT = "#f8fafc"   # رمادي فاتح
        self.CARD_BG = "#ffffff"    # أبيض
        self.TEXT_DARK = "#0f172a"  # نص داكن
        self.TEXT_MUTED = "#64748b" # نص رمادي

        # تخصيص Notebook (التبويبات)
        style.configure("TNotebook", background="#f1f5f9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[18, 10],
                        background="#e2e8f0", foreground=self.TEXT_DARK)
        style.map("TNotebook.Tab",
                  background=[("selected", "#ffffff")],
                  foreground=[("selected", self.PRIMARY)])

        # أزرار مخصصة
        style.configure("Primary.TButton", font=("Arial", 10, "bold"), background=self.PRIMARY, foreground="white")
        style.configure("Success.TButton", font=("Arial", 10, "bold"), background=self.SUCCESS, foreground="white")
        style.configure("Danger.TButton", font=("Arial", 10, "bold"), background=self.DANGER, foreground="white")

    def create_header(self):
        header_frame = tk.Frame(self.root, bg=self.PRIMARY, height=75)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🛡️ نظام كشف الاحتيال في المعاملات المالية (Fraud Detection System)",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg=self.PRIMARY
        )
        title_label.pack(pady=(12, 2))

        subtitle_label = tk.Label(
            header_frame,
            text="لوحة تحكم ذكية مدعومة بنموذج Random Forest Classifier",
            font=("Arial", 10),
            fg="#bfdbfe",
            bg=self.PRIMARY
        )
        subtitle_label.pack()

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 0))

        # إنشاء التبويبات
        self.tab_predict = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_analytics = tk.Frame(self.notebook, bg="#f8fafc")
        self.tab_model_info = tk.Frame(self.notebook, bg="#f8fafc")

        self.notebook.add(self.tab_predict, text="  💳 فحص المعاملات الحية  ")
        self.notebook.add(self.tab_analytics, text="  📊 التقارير والمخططات  ")
        self.notebook.add(self.tab_model_info, text="  ⚙️ إدارة النموذج والبيانات  ")

        self.setup_predict_tab()
        self.setup_analytics_tab()
        self.setup_model_info_tab()

    # =========================================================================
    # التبويب الأول: فحص المعاملات
    # =========================================================================
    def setup_predict_tab(self):
        container = tk.Frame(self.tab_predict, bg="#f8fafc")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # اللوحة اليسرى: بطاقة النتيجة والإجراءات السريعة
        left_panel = tk.Frame(container, bg="#ffffff", bd=1, relief=tk.SOLID, width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)

        # عنوان الإجراءات السريعة
        tk.Label(left_panel, text="⚡ نماذج جاهزة للاختبار", font=("Arial", 12, "bold"),
                 bg="#ffffff", fg=self.PRIMARY).pack(pady=(15, 8))

        btn_normal = tk.Button(
            left_panel, text="🟢 تحميل معاملة طبيعية آمنة", font=("Arial", 10, "bold"),
            bg="#ecfdf5", fg="#047857", activebackground="#a7f3d0", bd=1, relief=tk.RIDGE,
            padx=10, pady=8, cursor="hand2", command=lambda: self.load_sample(label_filter=0)
        )
        btn_normal.pack(fill=tk.X, padx=20, pady=4)

        btn_fraud = tk.Button(
            left_panel, text="🚨 تحميل معاملة احتيالية حقيقية", font=("Arial", 10, "bold"),
            bg="#fef2f2", fg="#b91c1c", activebackground="#fecaca", bd=1, relief=tk.RIDGE,
            padx=10, pady=8, cursor="hand2", command=lambda: self.load_sample(label_filter=1)
        )
        btn_fraud.pack(fill=tk.X, padx=20, pady=4)

        btn_random = tk.Button(
            left_panel, text="🎲 تحميل عينة عشوائية", font=("Arial", 10),
            bg="#f1f5f9", fg=self.TEXT_DARK, bd=1, relief=tk.RIDGE,
            padx=10, pady=6, cursor="hand2", command=lambda: self.load_sample(label_filter=None)
        )
        btn_random.pack(fill=tk.X, padx=20, pady=4)

        tk.Frame(left_panel, height=1, bg="#e2e8f0").pack(fill=tk.X, padx=20, pady=15)

        # زر الفحص الرئيسي
        btn_predict = tk.Button(
            left_panel, text="🔍 فحص وتحليل المعاملة الآن", font=("Arial", 12, "bold"),
            bg=self.PRIMARY, fg="#ffffff", activebackground="#1e40af", activeforeground="#ffffff",
            bd=0, padx=12, pady=12, cursor="hand2", command=self.predict_transaction
        )
        btn_predict.pack(fill=tk.X, padx=20, pady=8)

        # كرت عرض النتيجة
        self.result_card = tk.Frame(left_panel, bg="#f8fafc", bd=1, relief=tk.RIDGE)
        self.result_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 15))

        self.result_icon_label = tk.Label(self.result_card, text="💳", font=("Arial", 36), bg="#f8fafc")
        self.result_icon_label.pack(pady=(15, 5))

        self.result_title_label = tk.Label(
            self.result_card, text="جاهز للفحص", font=("Arial", 13, "bold"),
            bg="#f8fafc", fg=self.TEXT_MUTED
        )
        self.result_title_label.pack(pady=3)

        self.result_prob_label = tk.Label(
            self.result_card, text="اضغط على زر الفحص للبدء", font=("Arial", 10),
            bg="#f8fafc", fg=self.TEXT_MUTED
        )
        self.result_prob_label.pack(pady=3)

        self.result_actual_label = tk.Label(
            self.result_card, text="", font=("Arial", 9, "italic"),
            bg="#f8fafc", fg=self.TEXT_MUTED
        )
        self.result_actual_label.pack(pady=(5, 10))

        # اللوحة اليمنى: جدول إدخال الميزات
        right_panel = tk.Frame(container, bg="#ffffff", bd=1, relief=tk.SOLID)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        header_inputs = tk.Frame(right_panel, bg="#f1f5f9", height=40)
        header_inputs.pack(fill=tk.X)
        tk.Label(
            header_inputs, text="📋 قيم متغيرات المعاملة المالية (30 ميزة)",
            font=("Arial", 11, "bold"), bg="#f1f5f9", fg=self.PRIMARY
        ).pack(side=tk.LEFT, padx=15, pady=8)

        # حاوية سكرول لقيم المتغيرات
        canvas = tk.Canvas(right_panel, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # وضع الحقول في شبكة أعمدة أنيقة (3 أعمدة)
        for i, feat in enumerate(self.feature_names):
            row = i // 3
            col = (i % 3) * 2

            lbl_color = self.PRIMARY if feat in ['Amount', 'Time'] else "#334155"
            lbl = tk.Label(
                scrollable_frame, text=f"{feat}:", font=("Consolas", 10, "bold"),
                bg="#ffffff", fg=lbl_color, width=8, anchor="e"
            )
            lbl.grid(row=row, column=col, padx=(8, 4), pady=5, sticky="e")

            entry = ttk.Entry(scrollable_frame, width=14, font=("Consolas", 10))
            entry.grid(row=row, column=col + 1, padx=(0, 15), pady=5, sticky="w")
            entry.insert(0, "0.00")
            self.feature_entries[feat] = entry

    # =========================================================================
    # التبويب الثاني: التقارير والرسوم البيانية
    # =========================================================================
    def setup_analytics_tab(self):
        container = tk.Frame(self.tab_analytics, bg="#f8fafc")
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # كروت الأرقام والإحصائيات العلوية
        kpi_frame = tk.Frame(container, bg="#f8fafc")
        kpi_frame.pack(fill=tk.X, pady=(0, 10))

        kpis = [
            ("الدقة الإجمالية (Accuracy)", "99.95%", self.PRIMARY),
            ("دقة كشف الاحتيال (Precision)", "94.05%", self.SUCCESS),
            ("الاسترجاع (Recall)", "80.61%", "#d97706"),
            ("مقياس F1-Score", "0.87", self.SECONDARY),
            ("مساحة منحنى ROC (AUC)", "0.97", "#7c3aed")
        ]

        for i, (title, val, color) in enumerate(kpis):
            card = tk.Frame(kpi_frame, bg="#ffffff", bd=1, relief=tk.RIDGE)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

            tk.Label(card, text=val, font=("Arial", 16, "bold"), fg=color, bg="#ffffff").pack(pady=(8, 2))
            tk.Label(card, text=title, font=("Arial", 8), fg=self.TEXT_MUTED, bg="#ffffff").pack(pady=(0, 8))

        # شريط اختيار المخطط
        control_bar = tk.Frame(container, bg="#ffffff", bd=1, relief=tk.RIDGE)
        control_bar.pack(fill=tk.X, pady=(0, 10))

        tk.Label(control_bar, text="اختر المخطط البياني للعرض:", font=("Arial", 11, "bold"),
                 bg="#ffffff", fg=self.TEXT_DARK).pack(side=tk.LEFT, padx=15, pady=10)

        self.chart_options = {
            "مصفوفة الالتباس (Confusion Matrix)": "confusion_matrix.png",
            "منحنى ROC (Receiver Operating Characteristic)": "roc_curve.png",
            "منحنى الدقة والاسترجاع (Precision-Recall Curve)": "precision_recall_curve.png",
            "توزيع الفئات (Class Distribution)": "class_distribution.png",
            "توزيع المبالغ والوقت (Amount & Time Distribution)": "amount_time_distribution.png"
        }

        self.chart_var = tk.StringVar(value=list(self.chart_options.keys())[0])
        self.chart_combo = ttk.Combobox(
            control_bar, textvariable=self.chart_var,
            values=list(self.chart_options.keys()), state="readonly", width=45, font=("Arial", 10)
        )
        self.chart_combo.pack(side=tk.LEFT, padx=10, pady=10)
        self.chart_combo.bind("<<ComboboxSelected>>", self.on_chart_selected)

        btn_reload = tk.Button(
            control_bar, text="🔄 تحديث الصورة", font=("Arial", 9),
            bg="#f1f5f9", fg=self.TEXT_DARK, bd=1, relief=tk.RIDGE,
            padx=10, pady=4, cursor="hand2", command=self.on_chart_selected
        )
        btn_reload.pack(side=tk.LEFT, padx=10)

        # مساحة عرض الصورة
        self.image_container = tk.Frame(container, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.image_container.pack(fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(self.image_container, bg="#ffffff", text="جاري تحميل الرسم...")
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def on_chart_selected(self, event=None):
        chart_name = self.chart_var.get()
        filename = self.chart_options.get(chart_name)
        if not filename:
            return

        file_path = os.path.join(RESULTS_DIR, filename)
        if not os.path.exists(file_path):
            self.image_label.config(
                image="",
                text=f"لم يتم العثور على المخطط: {filename}\nيرجى تشغيل التقييم لتوليد الصور."
            )
            return

        try:
            pil_img = Image.open(file_path)
            # تغيير حجم الصورة بما يناسب المساحة المتاحة (حد أقصى 700x450)
            pil_img.thumbnail((750, 420), Image.Resampling.LANCZOS)
            self.current_image_obj = ImageTk.PhotoImage(pil_img)
            self.image_label.config(image=self.current_image_obj, text="")
        except Exception as e:
            self.image_label.config(image="", text=f"خطأ في عرض الصورة: {e}")

    # =========================================================================
    # التبويب الثالث: إدارة النموذج والبيانات
    # =========================================================================
    def setup_model_info_tab(self):
        container = tk.Frame(self.tab_model_info, bg="#f8fafc")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # صندوق معلومات البيانات
        info_frame = tk.LabelFrame(
            container, text="📊 ملخص مجموعة البيانات (Credit Card Fraud Dataset)",
            font=("Arial", 11, "bold"), bg="#ffffff", fg=self.PRIMARY, padx=15, pady=12
        )
        info_frame.pack(fill=tk.X, pady=(0, 15))

        details = [
            "• إجمالي عدد المعاملات: 284,807 معاملة",
            "• المعاملات الطبيعية (Class 0): 284,315 معاملة (99.83%)",
            "• المعاملات الاحتيالية (Class 1): 492 معاملة (0.17%)",
            "• عدد الميزات: 30 ميزة (Time, Amount بالإضافة إلى V1 إلى V28 المشفرة بـ PCA)",
            "• خوارزمية النموذج: Random Forest Classifier (100 الأشجار)",
            "• معالجة عدم التوازن: تم التدريب بنمط Balanced Class Weights"
        ]
        for d in details:
            tk.Label(info_frame, text=d, font=("Arial", 10), bg="#ffffff", fg=self.TEXT_DARK, anchor="w").pack(fill=tk.X, pady=2)

        # صندوق التدريب
        train_frame = tk.LabelFrame(
            container, text="⚙️ تدريب النموذج", font=("Arial", 11, "bold"),
            bg="#ffffff", fg=self.PRIMARY, padx=15, pady=12
        )
        train_frame.pack(fill=tk.BOTH, expand=True)

        desc_lbl = tk.Label(
            train_frame,
            text="يمكنك إعادة تدريب النموذج على البيانات بالكامل بنقرة زر واحدة. يتم التدريب في خيط خلفي لتجنب تعليق الواجهة.",
            font=("Arial", 10), bg="#ffffff", fg=self.TEXT_MUTED, wraplength=700, justify="left"
        )
        desc_lbl.pack(anchor="w", pady=(0, 10))

        self.btn_train = tk.Button(
            train_frame, text="⚡ بدء إعادة تدريب النموذج بالكامل", font=("Arial", 11, "bold"),
            bg=self.PRIMARY, fg="#ffffff", activebackground="#1e40af", activeforeground="#ffffff",
            bd=0, padx=16, pady=10, cursor="hand2", command=self.start_retraining
        )
        self.btn_train.pack(anchor="w", pady=5)

        self.train_status_label = tk.Label(
            train_frame, text="", font=("Arial", 10, "italic"),
            bg="#ffffff", fg=self.PRIMARY
        )
        self.train_status_label.pack(anchor="w", pady=5)

        self.progress_bar = ttk.Progressbar(train_frame, mode="indeterminate", length=400)

    def start_retraining(self):
        confirm = messagebox.askyesno(
            "تأكيد إعادة التدريب",
            "هل أنت متأكد من إعادة تدريب النموذج؟ قد يستغرق التدريب من 1 إلى 3 دقائق نظراً لحجم البيانات (284 ألف سجل)."
        )
        if not confirm:
            return

        self.btn_train.config(state=tk.DISABLED, text="جاري التدريب...")
        self.train_status_label.config(text="جاري معالجة البيانات وتدريب Random Forest Classifier، يرجى الانتظار...", fg=self.PRIMARY)
        self.progress_bar.pack(anchor="w", pady=8)
        self.progress_bar.start(10)

        def train_worker():
            try:
                # استدعاء دالة التدريب من src
                sys.path.append(os.path.join(BASE_DIR, 'src'))
                from train_model import train
                train()
                # إعادة تحميل النموذج
                self.model = joblib.load(MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)

                self.safe_after(0, lambda: self.finish_training(success=True))
            except Exception as e:
                self.safe_after(0, lambda: self.finish_training(success=False, error_msg=str(e)))

        threading.Thread(target=train_worker, daemon=True).start()

    def finish_training(self, success, error_msg=None):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.btn_train.config(state=tk.NORMAL, text="⚡ بدء إعادة تدريب النموذج بالكامل")

        if success:
            self.train_status_label.config(text="✅ اكتمل التدريب وتم حفظ النموذج والمقياس بنجاح!", fg=self.SUCCESS)
            messagebox.showinfo("تم بنجاح", "تم تدريب نموذج Random Forest بنجاح وتحديث الملفات!")
            self.on_chart_selected()
        else:
            self.train_status_label.config(text=f"❌ فشل التدريب: {error_msg}", fg=self.DANGER)
            messagebox.showerror("خطأ في التدريب", f"حدث خطأ أثناء تدريب النموذج:\n{error_msg}")

    # =========================================================================
    # الشريط السفلي (Footer)
    # =========================================================================
    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#e2e8f0", height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        self.footer_status = tk.Label(
            footer_frame, text="جاري تهيئة النظام...",
            font=("Arial", 9), bg="#e2e8f0", fg=self.TEXT_MUTED
        )
        self.footer_status.pack(side=tk.LEFT, padx=15)

        footer_author = tk.Label(
            footer_frame, text="Classification & Fraud Detection Project",
            font=("Arial", 9), bg="#e2e8f0", fg=self.TEXT_MUTED
        )
        footer_author.pack(side=tk.RIGHT, padx=15)

    def safe_after(self, delay, callback):
        """استدعاء آمن لـ root.after يتجنب الأخطاء عند إغلاق النافذة"""
        try:
            if self.root.winfo_exists():
                self.root.after(delay, callback)
        except (tk.TclError, RuntimeError):
            pass

    # =========================================================================
    # العمليات والتحميل
    # =========================================================================
    def async_load_resources(self):
        """تحميل النموذج والمقياس والعينات في خيط خلفي"""
        def loader():
            model_loaded = False
            try:
                if os.path.exists(MODEL_PATH):
                    self.model = joblib.load(MODEL_PATH)
                    model_loaded = True

                if os.path.exists(SCALER_PATH):
                    self.scaler = joblib.load(SCALER_PATH)

                if os.path.exists(SAMPLES_PATH):
                    self.samples_df = pd.read_csv(SAMPLES_PATH)

                self.safe_after(0, lambda: self.on_resources_ready(model_loaded))
            except Exception as e:
                self.safe_after(0, lambda: self.footer_status.config(text=f"تنبيه: {e}"))

        threading.Thread(target=loader, daemon=True).start()

    def on_resources_ready(self, model_loaded):
        if model_loaded:
            self.footer_status.config(text="✅ النموذج جاهز للعمل | تم التحميل من models/trained_model.pkl")
            # تحميل أول عينة تلقائياً
            self.load_sample(label_filter=0)
            # عرض الرسم البياني الافتراضي
            self.on_chart_selected()
        else:
            self.footer_status.config(text="⚠️ لم يتم العثور على نموذج مدرب في models/trained_model.pkl")

    def load_sample(self, label_filter=None):
        """تحميل عينة حقيقية من البيانات في الحقول"""
        if self.samples_df is None or len(self.samples_df) == 0:
            messagebox.showwarning("تنبيه", "ملف العينات غير متوفر.")
            return

        df_filtered = self.samples_df
        if label_filter is not None:
            df_filtered = self.samples_df[self.samples_df['Class'] == label_filter]

        if len(df_filtered) == 0:
            df_filtered = self.samples_df

        sample = df_filtered.sample(1).iloc[0]
        self.current_sample_actual_class = int(sample['Class'])

        for feat in self.feature_names:
            if feat in sample:
                val = sample[feat]
                entry = self.feature_entries.get(feat)
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, f"{val:.5f}")

        # إعادة ضبط بطاقة النتيجة
        actual_text = "المعاملة في البيانات الأصلية: " + ("🚨 احتيالية (Fraud)" if self.current_sample_actual_class == 1 else "🟢 طبيعية (Normal)")
        self.result_card.config(bg="#f8fafc")
        self.result_icon_label.config(text="💳", bg="#f8fafc")
        self.result_title_label.config(text="تم تحميل العينة", fg=self.PRIMARY, bg="#f8fafc")
        self.result_prob_label.config(text="اضغط على 'فحص وتحليل المعاملة الآن'", fg=self.TEXT_MUTED, bg="#f8fafc")
        self.result_actual_label.config(text=actual_text, bg="#f8fafc", fg=self.TEXT_DARK)

    def predict_transaction(self):
        """قراءة الحقول، وتطبيق المقياس، والتنبؤ بواسطة النموذج"""
        if self.model is None:
            messagebox.showerror("خطأ", "النموذج غير محمل! تأكد من وجود ملف models/trained_model.pkl")
            return

        try:
            values = []
            for feat in self.feature_names:
                entry = self.feature_entries.get(feat)
                val_str = entry.get().strip() if entry else "0"
                values.append(float(val_str))

            # إنشاء DataFrame بالأسماء المحددة لتفادي تحذيرات الميزات
            X_df = pd.DataFrame([values], columns=self.feature_names)

            # تطبيق StandardScaler إذا كان متوفراً
            if self.scaler is not None:
                X_scaled = self.scaler.transform(X_df)
            else:
                X_scaled = X_df

            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]

            fraud_prob = probabilities[1] * 100
            normal_prob = probabilities[0] * 100

            # تحديث بطاقة النتيجة
            if prediction == 1:
                # احتيال
                self.result_card.config(bg="#fef2f2")
                self.result_icon_label.config(text="🚨", bg="#fef2f2")
                self.result_title_label.config(
                    text="تحذير: معاملة احتيالية!",
                    fg="#dc2626",
                    bg="#fef2f2"
                )
                self.result_prob_label.config(
                    text=f"احتمالية الاحتيال: {fraud_prob:.2f}%\nدرجة الخطورة: مرتفعة جداً",
                    fg="#991b1b",
                    bg="#fef2f2"
                )
            else:
                # طبيعي
                self.result_card.config(bg="#f0fdf4")
                self.result_icon_label.config(text="✅", bg="#f0fdf4")
                self.result_title_label.config(
                    text="معاملة آمنة وطبيعية",
                    fg="#16a34a",
                    bg="#f0fdf4"
                )
                self.result_prob_label.config(
                    text=f"نسبة الأمان: {normal_prob:.2f}%\nاحتمالية الاحتيال: {fraud_prob:.2f}%",
                    fg="#166534",
                    bg="#f0fdf4"
                )

            if self.current_sample_actual_class is not None:
                actual_str = "احتيال (1)" if self.current_sample_actual_class == 1 else "طبيعي (0)"
                match_text = "✔️ التوقع مطابق للفئة الفعلية" if prediction == self.current_sample_actual_class else "⚠️ النتيجة تختلف عن الفئة الفعلية"
                self.result_actual_label.config(
                    text=f"الفئة الفعلية: {actual_str} | {match_text}",
                    bg="#fef2f2" if prediction == 1 else "#f0fdf4"
                )

        except ValueError:
            messagebox.showerror("خطأ في البيانات", "يرجى التأكد من أن جميع الحقول تحتوي على أرقام صحيحة أو عشرية صالحة.")
        except Exception as e:
            messagebox.showerror("خطأ غير متوقع", f"حدث خطأ أثناء الفحص: {e}")


def main():
    root = tk.Tk()
    app = FraudDetectorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
