import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# مسار مجلد المشروع ومسار البيانات والنتائج
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, 'data', 'creditcard.csv')
results_dir = os.path.join(base_dir, 'results')

os.makedirs(results_dir, exist_ok=True)

print("تحميل البيانات للتحليل...")
df = pd.read_csv(data_path)
print("تم تحميل البيانات بنجاح!\n")

# 1️⃣ معلومات أساسية عن البيانات
print("=== معلومات عن البيانات ===")
print(df.info())

# 2️⃣ إحصاءات وصفية
print("\n=== إحصاءات وصفية ===")
print(df.describe())

# 3️⃣ توزيع العمليات الاحتيالية والطبيعية
plt.figure(figsize=(6, 4))
sns.countplot(x='Class', data=df)
plt.title('توزيع المعاملات الطبيعية والاحتيالية')
plt.xlabel('Class (0: طبيعي, 1: احتيال)')
plt.ylabel('العدد')
plt.tight_layout()
class_dist_path = os.path.join(results_dir, 'class_distribution.png')
plt.savefig(class_dist_path)
plt.close()
print(f"تم حفظ رسم توزيع الفئات في: {class_dist_path}")

# 4️⃣ تحليل المبالغ (Amount)
plt.figure(figsize=(8, 4))
sns.histplot(df['Amount'], bins=50, kde=True)
plt.title('توزيع مبالغ المعاملات')
plt.xlabel('المبلغ (Amount)')
plt.ylabel('التكرار')
plt.tight_layout()
amount_dist_path = os.path.join(results_dir, 'amount_distribution.png')
plt.savefig(amount_dist_path)
plt.close()
print(f"تم حفظ رسم توزيع المبالغ في: {amount_dist_path}")

# 5️⃣ تحليل الوقت (Time)
plt.figure(figsize=(8, 4))
sns.histplot(df['Time'], bins=50, kde=True)
plt.title('توزيع وقت المعاملات')
plt.xlabel('الوقت بالثواني (Time)')
plt.ylabel('التكرار')
plt.tight_layout()
time_dist_path = os.path.join(results_dir, 'time_distribution.png')
plt.savefig(time_dist_path)
plt.close()
print(f"تم حفظ رسم توزيع الوقت في: {time_dist_path}")

# 6️⃣ مصفوفة الارتباط
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), cmap='coolwarm', annot=False)
plt.title('مصفوفة الارتباط بين المتغيرات')
plt.tight_layout()
corr_path = os.path.join(results_dir, 'correlation_matrix.png')
plt.savefig(corr_path)
plt.close()
print(f"تم حفظ مصفوفة الارتباط في: {corr_path}")

print("\nتم إنشاء جميع الرسوم التحليلية بنجاح! تفقد مجلد results/")
