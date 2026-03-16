import pandas as pd
import os
import matplotlib.pyplot as plt

def load_data(filepath):
    """تحميل البيانات من ملف CSV."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} records from {filepath}")
    return df

def clean_data(df):
    """تنظيف البيانات ومعالجة القيم المفقودة والتواريخ."""
    df = df.copy()
    # تعبئة القيم المفقودة بالوسيط
    df['quantity'] = df['quantity'].fillna(df['quantity'].median())
    df['unit_price'] = df['unit_price'].fillna(df['unit_price'].median())
    
    # تحويل التاريخ ومعالجة الصيغ الخاطئة
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    # حذف الصفوف التي لا تزال تحتوي على قيم مفقودة في الأعمدة الأساسية
    df = df.dropna(subset=['quantity', 'unit_price'])
    
    print(f"Cleaned data: {len(df)} records")
    return df

def add_features(df):
    """إضافة أعمدة جديدة (الإيرادات واليوم)."""
    df['revenue'] = df['quantity'] * df['unit_price']
    df['day_of_week'] = df['date'].dt.day_name()
    return df

def generate_summary(df):
    """حساب الإحصائيات الملخصة."""
    summary = {
        'total_revenue': df['revenue'].sum(),
        'avg_order_value': df['revenue'].mean(),
        'top_category': df.groupby('product_category')['revenue'].sum().idxmax(),
        'record_count': len(df)
    }
    return summary

def create_visualizations(df, output_dir='output'):
    """إنشاء 3 رسومات بيانية وحفظها كصور PNG."""
    os.makedirs(output_dir, exist_ok=True)
    
    # الرسم 1: الإيرادات حسب الفئة
    fig, ax = plt.subplots()
    df.groupby('product_category')['revenue'].sum().plot(kind='bar', ax=ax)
    ax.set_title('Total Revenue by Category')
    fig.savefig(f'{output_dir}/revenue_by_category.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # الرسم 2: اتجاه الإيرادات اليومي
    fig, ax = plt.subplots()
    df.groupby('date')['revenue'].sum().plot(kind='line', ax=ax)
    ax.set_title('Daily Revenue Trend')
    fig.savefig(f'{output_dir}/daily_revenue_trend.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

    # الرسم 3: متوسط الطلب حسب طريقة الدفع
    fig, ax = plt.subplots()
    df.groupby('payment_method')['revenue'].mean().plot(kind='barh', ax=ax)
    ax.set_title('Average Order Value by Payment Method')
    fig.savefig(f'{output_dir}/avg_order_by_payment.png', dpi=150, bbox_inches='tight')
    plt.close(fig)

def main():
    """تشغيل الـ Pipeline بالكامل."""
    # 1. تحميل
    raw_df = load_data('data/sales_records.csv')
    # 2. تنظيف
    cleaned_df = clean_data(raw_df)
    # 3. إضافة ميزات
    enriched_df = add_features(cleaned_df)
    # 4. ملخص
    summary = generate_summary(enriched_df)
    print("\n=== Summary Statistics ===")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # 5. رسومات
    create_visualizations(enriched_df)
    print("\nPipeline complete.")

if __name__ == "__main__":
    main()