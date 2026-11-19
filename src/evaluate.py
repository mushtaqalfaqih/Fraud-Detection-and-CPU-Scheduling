# src/evaluate.py

import os
import sys
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc, precision_recall_curve

# التأكد من تضمين مجلد src في مسار البحث
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# استيراد البيانات المعالجة
from preprocess import X_test, y_test

# 📂 إعداد مسارات الملفات
base_dir = os.path.dirname(current_dir)
model_path = os.path.join(base_dir, 'models', 'trained_model.pkl')
results_dir = os.path.join(base_dir, 'results')

os.makedirs(results_dir, exist_ok=True)

if not os.path.exists(model_path):
    raise FileNotFoundError(f"لم يتم العثور على النموذج في: {model_path}. يرجى تشغيل train_model.py أولاً.")

# 🔹 تحميل النموذج
print("تحميل النموذج المدرب...")
model = joblib.load(model_path)
print("تم تحميل النموذج بنجاح!")

# 🔹 التنبؤ
print("بدء التنبؤ على بيانات الاختبار...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# 🔹 طباعة التقارير
print("\n=== Confusion Matrix ===")
cm = confusion_matrix(y_test, y_pred)
print(cm)

print("\n=== Classification Report ===")
cr = classification_report(y_test, y_pred)
print(cr)

# 🔹 رسم ومصفوفة الالتباس (Confusion Matrix)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['طبيعي (0)', 'احتيال (1)'],
            yticklabels=['طبيعي (0)', 'احتيال (1)'])
plt.title('مصفوفة الالتباس (Confusion Matrix)')
plt.xlabel('المتوقع (Predicted)')
plt.ylabel('الفعلي (Actual)')
plt.tight_layout()
cm_path = os.path.join(results_dir, 'confusion_matrix.png')
plt.savefig(cm_path)
plt.close()
print(f"تم حفظ مصفوفة الالتباس في: {cm_path}")

# 🔹 رسم منحنى ROC
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.title('Receiver Operating Characteristic (ROC)')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.tight_layout()
roc_path = os.path.join(results_dir, 'roc_curve.png')
plt.savefig(roc_path)
plt.close()
print(f"تم حفظ منحنى ROC في: {roc_path}")

# 🔹 رسم منحنى Precision-Recall
precision, recall, pr_thresholds = precision_recall_curve(y_test, y_pred_proba)
pr_auc = auc(recall, precision)

plt.figure(figsize=(6, 5))
plt.plot(recall, precision, color='purple', lw=2, label=f'PR curve (AUC = {pr_auc:.4f})')
plt.title('منحنى الدقة والاسترجاع (Precision-Recall Curve)')
plt.xlabel('الاسترجاع (Recall)')
plt.ylabel('الدقة (Precision)')
plt.legend(loc="lower left")
plt.tight_layout()
pr_path = os.path.join(results_dir, 'precision_recall_curve.png')
plt.savefig(pr_path)
plt.close()
print(f"تم حفظ منحنى الدقة والاسترجاع في: {pr_path}")

print(f"\nاكتمل التقييم بنجاح! تم حفظ كل المخططات في المجلد: {results_dir}")
