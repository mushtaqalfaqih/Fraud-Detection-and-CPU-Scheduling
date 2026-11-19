# مشروع كشف الاحتيال في البطاقات الائتمانية (Credit Card Fraud Detection)

مشروع تعلم آلي (Machine Learning) مبني بلغة Python، يهدف إلى تحليل وتصنيف المعاملات المالية للبطاقات الائتمانية إلى معاملات **طبيعية (Normal)** أو **احتيالية (Fraudulent)** باستخدام خوارزمية **Random Forest Classifier**، ومزوّد بـ **واجهة رسومية تفاعلية (GUI)** كاملة للفحص والتحليل.

---

## 🖥️ تشغيل الواجهة الرسومية (GUI Dashboard)

أسهل وأفضل طريقة لتشغيل المشروع هي عبر تشغيل الواجهة الرسومية الرئيسية:

```powershell
python main.py
```

### ✨ ميزات الواجهة الرسومية:
1. **💳 فحص المعاملات الحية:**
   * زر لاختبار **معاملة احتيالية حقيقية** بنقرة واحدة.
   * زر لاختبار **معاملة طبيعية آمنة** بنقرة واحدة.
   * إدخال مخصص لجميع ميزات المعاملة (Time, Amount, V1-V28).
   * عرض نتيجة الفحص الفورية مع نسبة الخطر واحتمالية الاحتيال.
2. **📊 استعراض التقارير والمخططات:**
   * عرض بطاقات مؤشرات الأداء (Accuracy: 99.95%, Precision: 94%, Recall: 81%).
   * استعراض الرسوم البيانية المحفوظة (Confusion Matrix, ROC Curve, PR Curve, إلخ) داخل النافذة مباشرة.
3. **⚙️ إدارة وتدريب النموذج:**
   * إعادة تدريب نموذج Random Forest على كامل البيانات بنقرة زر في خيط خلفي (Background Thread) دون تجميد الواجهة.

---

## 📁 هيكل المشروع (Project Structure)

```text
Classification/
│
├── main.py                             # الواجهة الرسومية الرئيسية لمشروع كشف الاحتيال (GUI Dashboard)
│
├── data/                               # مجلد البيانات
│   ├── creditcard.csv                 # مجموعة البيانات الأصلية
│   ├── creditcard_processed.csv       # البيانات بعد المعالجة المسبقة
│   └── samples_for_gui.csv            # عينات حقيقية سريعة لاختبار الواجهة
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
├── round_robin/                        # تطبيق محاكاة خوارزمية Round Robin
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
> `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `joblib`, `Pillow`

---

## 🚀 التشغيل عبر سطر الأوامر (Command Line Pipeline)

يمكن أيضاً تشغيل مراحل المشروع عبر السكربتات المستقلة بالترتيب التالي:

```powershell
# 1. التحليل الاستكشافي للبيانات (EDA)
python src/fraud_eda_preprocess.py

# 2. مصفوفة الارتباط والتحليلات الإضافية
python src/fraud_detection_analysis.py

# 3. تدريب النموذج وحفظه
python src/train_model.py

# 4. تقييم أداء النموذج وتوليد المخططات
python src/evaluate.py
```

---

## 📊 النتائج والتقييم (Evaluation Metrics)

* **الدقة (Precision) لكشف الاحتيال:** 94.05%
* **الاسترجاع (Recall) لكشف الاحتيال:** 80.61%
* **F1-Score:** 0.87
* **مساحة منحنى ROC (AUC):** 0.97
* **الدقة العامة (Accuracy):** 99.95%

جميع المخططات البيانية والتقارير تحفظ تلقائياً داخل المجلد [results/](file:///c:/Users/hp/Classification/results).

---

## 🛠️ أدوات إضافية داخل المشروع

* **محاكي خوارزميات الجدولة في أنظمة التشغيل (CPU Scheduling Simulator):**
  * [nabil.py](file:///c:/Users/hp/Classification/nabil.py): واجهة رسومية متقدمة (Tkinter) لمحاكاة خوارزميات الجدولة (Round Robin, FCFS, SJF, Priority, SRTF) مع مخطط جانت الزمني.
    ```powershell
    python nabil.py
    ```
  * [round_robin/round_robin.py](file:///c:/Users/hp/Classification/round_robin/round_robin.py): محاكي مخصص لخوارزمية Round Robin.
