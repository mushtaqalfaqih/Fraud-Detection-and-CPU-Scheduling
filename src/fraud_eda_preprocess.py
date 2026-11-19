# src/fraud_eda_preprocess.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'data', 'creditcard.csv')
results_dir = os.path.join(base_dir, 'results')
os.makedirs(results_dir, exist_ok=True)

print("تحميل البيانات...")
df = pd.read_csv(data_path)

print("تم تحميل البيانات!")
print(df.head())

# فحص القيم المفقودة
print("\nفحص القيم المفقودة:")
print(df.isnull().sum())

# وصف إحصائي سريع
print("\nالوصف الإحصائي للبيانات:")
print(df.describe())

# توزيع الفئة المستهدفة (Class)
print("\nتوزيع الفئات:")
print(df['Class'].value_counts())

# رسم توزيع الفئات
plt.figure(figsize=(6, 4))
sns.countplot(x='Class', data=df)
plt.title('توزيع معاملات الاحتيال مقابل الطبيعية')
class_dist_path = os.path.join(results_dir, 'class_distribution.png')
plt.tight_layout()
plt.savefig(class_dist_path)
plt.close()
print(f"تم حفظ رسم توزيع الفئات في: {class_dist_path}")

# رسم التوزيع الزمني Amount و Time
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.histplot(df['Amount'], bins=50, kde=True)
plt.title('توزيع مبلغ المعاملات')

plt.subplot(1, 2, 2)
sns.histplot(df['Time'], bins=50, kde=True)
plt.title('توزيع الوقت للمعاملات')
plt.tight_layout()
amount_time_path = os.path.join(results_dir, 'amount_time_distribution.png')
plt.savefig(amount_time_path)
plt.close()
print(f"تم حفظ رسم توزيع المبالغ والوقت في: {amount_time_path}")

# حفظ نسخة معالجة
processed_path = os.path.join(base_dir, 'data', 'creditcard_processed.csv')
if not os.path.exists(processed_path):
    df.to_csv(processed_path, index=False)
    print(f"\nتم حفظ نسخة معالجة من البيانات في: {processed_path}")
