# src/train_model.py

import os
import sys
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# التأكد من تضمين مجلد src في مسار البحث
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from preprocess import X_train, X_test, y_train, y_test, scaler

def train():
    base_dir = os.path.dirname(current_dir)
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, 'trained_model.pkl')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')

    print("بدء تدريب نموذج Random Forest Classifier...")
    # استخدام class_weight='balanced' للتعامل مع عدم توازن فئات الاحتيال
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    print("اكتمل تدريب النموذج بنجاح!")

    # حفظ النموذج والمقياس
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"تم حفظ النموذج في: {model_path}")
    print(f"تم حفظ أداة القياس في: {scaler_path}")

    # تقييم سريع على عينة الاختبار
    print("\n=== تقييم أولي على بيانات الاختبار ===")
    y_pred = model.predict(X_test)
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model

if __name__ == "__main__":
    train()
