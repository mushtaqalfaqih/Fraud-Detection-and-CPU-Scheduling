# src/preprocess.py

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_preprocess(data_path=None, test_size=0.2, random_state=42):
    """
    تحميل بيانات المعاملات المالية ومعالجتها وتقسيمها إلى بيانات تدريب واختبار.
    """
    if data_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, 'data', 'creditcard.csv')

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"لم يتم العثور على ملف البيانات في المسار: {data_path}")

    print(f"تحميل البيانات من: {data_path} ...")
    df = pd.read_csv(data_path)

    # فصل الميزات عن المتغير المستهدف
    X = df.drop('Class', axis=1)
    y = df['Class']

    # تقسيم البيانات مع الحفاظ على نسبة الفئات (stratify) نظراً لعدم توازن البيانات
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # توحيد مقاييس الميزات
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("تم تجهيز البيانات وتقسيمها بنجاح!")
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler

# تصدير المتغيرات على مستوى الوحدة لدعم التوافق مع نصوص الاستيراد المباشرة
X_train, X_test, y_train, y_test, scaler = load_and_preprocess()

if __name__ == "__main__":
    print(f"حجم بيانات التدريب: {X_train.shape}, حجم بيانات الاختبار: {X_test.shape}")
