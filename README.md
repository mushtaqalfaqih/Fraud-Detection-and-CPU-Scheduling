# مشروع كشف الاحتيال في البطاقات الائتمانية (Credit Card Fraud Detection)

مشروع تعلم آلي (Machine Learning) مبني بلغة Python، يهدف إلى تحليل وتصنيف المعاملات المالية للبطاقات الائتمانية إلى معاملات **طبيعية (Normal)** أو **احتيالية (Fraudulent)** باستخدام خوارزميات التصنيف (مثل Random Forest).

---

## 📁 هيكل المشروع (Project Structure)

```text
Classification/
│
├── data/                               # مجلد البيانات
│   ├── creditcard.csv                 # مجموعة البيانات الأصلية
│   └── creditcard_processed.csv       # البيانات بعد المعالجة المسبقة
│
├── models/                             # مجلد حفظ النماذج
│   ├── trained_model.pkl              # نموذج Random Forest المدرب
│   └── scaler.pkl                     # أداة تسوية المقاييس (StandardScaler)
│
├── results/                            # مجلد المخرجات والرسوم البيانية
│   ├── class_distribution.png         # توزيع الفئات (طبيعي مقابل احتيال)
│   ├── amount_time_distribution.png   # توزيع المبالغ والأوقات
│   ├── confusion_matrix.png           # مصفوفة الالتباس
│   ├── roc_curve.png                  # منحنى خصائص التشغيل (ROC Curve)
│   └── precision_recall_curve.png     # منحنى الدقة والاسترجاع (PR Curve)
│
├── src/                                # الأكواد المصدرية لمشروع التعلم الآلي
│   ├── fraud_eda_preprocess.py        # التحليل الاستكشافي للبيانات وحفظ نسخة معالجة
│   ├── fraud_detection_analysis.py    # رسوم إحصائية ومصفوفة الارتباط
│   ├── preprocess.py                  # تحميل، تنظيف، تقسيم وتسوية البيانات
│   ├── train_model.py                 # تدريب نموذج التصنيف وحفظه
│   └── evaluate.py                    # اختبار وتقييم النموذج وتوليد التقارير
│
├── notebooks/                          # مجلد مخصص لدفاتر Jupyter Notebook
│
├── Round Robin/                        # تطبيق محاكاة خوارزمية Round Robin
│   └── round_robin.py                 # واجهة Tkinter لمحاكاة الجدولة
│
├── nabil.py                            # النظام المتقدم لمحاكاة خوارزميات الجدولة (GUI متقدم)
├── .gitignore                          # استثناء الملفات المؤقتة والبيانات الضخمة
└── README.md                           # دليل وتوثيق المشروع
```

---

## ⚙️ متطلبات التشغيل والبيئة (Setup & Installation)

المشروع يحتوي بالفعل على بيئة عمل افتراضية جاهزة في المجلد `.venv`.

لتفعيل البيئة في موجه الأوامر (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

أو عبر Command Prompt (cmd):
```cmd
.\.venv\Scripts\activate.bat
```

> [!NOTE]
> الحزم الرئيسية المستخدمة في المشروع:
> `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `joblib`

---

## 🚀 طريقة تشغيل المشروع (Pipeline Workflow)

يمكن تشغيل مراحل المشروع خطوة بخطوة بالترتيب التالي:

### 1. التحليل الاستكشافي للبيانات (EDA)
عرض إحصائيات البيانات، فحص القيم المفقودة، ورسم التوزيعات:
```powershell
python src/fraud_eda_preprocess.py
```
أو لإنشاء مصفوفة الارتباط والتحليلات الإضافية:
```powershell
python src/fraud_detection_analysis.py
```

### 2. تجهيز ومعالجة البيانات (Preprocessing)
تقسيم البيانات إلى بيانات تدريب واختبار مع موازنة الفئات (`stratify`) وتطبيق `StandardScaler`:
```powershell
python src/preprocess.py
```

### 3. تدريب النموذج (Training)
تدريب نموذج `RandomForestClassifier` وحفظ النموذج المدرب في `models/trained_model.pkl`:
```powershell
python src/train_model.py
```

### 4. تقييم أداء النموذج (Evaluation)
اختبار النموذج على بيانات الاختبار وتوليد تقارير الأداء ومخططات التقييم في مجلد `results/`:
```powershell
python src/evaluate.py
```

---

## 📊 النتائج والتقييم (Evaluation Metrics)

نظراً لعدم توازن فئات الاحتيال (Imbalanced Data) حيث تمثل العمليات الاحتيالية نسبة ضئيلة جداً (~0.17%)، يتم الاعتماد على مقاييس:
* **Precision & Recall** للفئة 1 (الاحتيال).
* **PR Curve (Precision-Recall Curve)**.
* **ROC-AUC Score**.
* **مصفوفة الالتباس (Confusion Matrix)** للتأكد من تقليل الإيجابيات الكاذبة والسلبيات الكاذبة.

جميع المخططات البيانية والتقارير تحفظ تلقائياً داخل المجلد [results/](file:///c:/Users/hp/Classification/results).

---

## 🛠️ أدوات إضافية داخل المشروع

* **محاكي خوارزميات الجدولة (CPU Scheduling Simulator):**
  * [nabil.py](file:///c:/Users/hp/Classification/nabil.py): واجهة رسومية متقدمة (Tkinter) لمحاكاة خوارزميات الجدولة بأنظمة التشغيل (Round Robin, FCFS, SJF, Priority, SRTF) مع مخطط جانت الزمني.
  * [Round Robin/round_robin.py](file:///c:/Users/hp/Classification/Round Robin/round_robin.py): محاكي مخصص لخوارزمية Round Robin.
