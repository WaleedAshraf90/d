import os
from flask import Flask, render_template, request, flash
import pandas as pd
import plotly.express as px

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "your_secret_key_here"  

file_path = "Finallll.xlsx"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"الملف {file_path} غير موجود في المسار المحدد.")

df = pd.read_excel(file_path)

# تحقق من الأعمدة المطلوبة في البيانات
required_columns = ['Month', 'Day', 'Day_Name', 'DonationAmount', 'ProductName', 'Marketer', 'DonorName', 'PaymentMethodSystemName', 'IsDonationZakat', 'Hour', 'DonationCount', 'TargetAmount']
for col in required_columns:
    if col not in df.columns:
        flash(f"العمود {col} مفقود في الملف!")

# معالجة عمود التاريخ
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Weekday'] = df['Date'].dt.weekday

    # حذف العمود Date بعد المعالجة
    df.drop(columns=['Date'], inplace=True)

@app.route("/")
def dashboard():
    # الحصول على الشهر واليوم وطريقة الدفع وعدد العملاء من الرابط
    selected_month = request.args.get("month", "")
    selected_day = request.args.get("day", "")
    selected_payment_method = request.args.get("payment_method", "")
    selected_num_clients = request.args.get("num_clients", 5)  # إضافة متغير عدد العملاء

    # تحويل عدد العملاء إلى عدد صحيح
    try:
        selected_num_clients = int(selected_num_clients)
    except ValueError:
        selected_num_clients = 5  # القيمة الافتراضية إذا حدث خطأ

    # تطبيق الفلاتر بناءً على المدخلات
    df_filtered = df
    if selected_month:
        try:
            df_filtered = df_filtered[df_filtered["Month"] == int(selected_month)]
        except ValueError:
            df_filtered = df
            flash("خطأ في اختيار الشهر، سيتم عرض البيانات لجميع الأشهر.")

    if selected_day:
        try:
            df_filtered = df_filtered[df_filtered["Day"] == int(selected_day)]
        except ValueError:
            df_filtered = df_filtered
            flash("خطأ في اختيار اليوم، سيتم عرض البيانات لجميع الأيام.")

    if selected_payment_method:
        df_filtered = df_filtered[df_filtered["PaymentMethodSystemName"] == selected_payment_method]

    # تصنيف العملاء بناءً على التبرعات
    clients_donations = df_filtered.groupby("DonorName")["DonationAmount"].sum().sort_values(ascending=False)

    # الحصول على أفضل عدد من العملاء بناءً على الاختيار
    top_clients = clients_donations.head(selected_num_clients)

    # مجموع التبرعات للعملاء المحددين
    total_donations_top_clients = top_clients.sum()

    # تجميع التبرعات حسب يوم الأسبوع و حسب اليوم
    donations_by_day_name = df_filtered.groupby("Day_Name")["DonationAmount"].sum().to_dict()
    donations_by_day = df_filtered.groupby("Day")["DonationAmount"].sum().to_dict()

    # تفاصيل إضافية حول التبرعات
    num_products = df_filtered["ProductName"].nunique()
    num_marketers = df_filtered["Marketer"].nunique()
    num_donors = df_filtered["DonorName"].nunique()
    total_donations = df_filtered["DonationAmount"].sum()
    donations_by_product = df_filtered.groupby("ProductName")["DonationAmount"].sum().to_dict()
    donations_by_marketer = df_filtered.groupby("Marketer")["DonationAmount"].sum().to_dict()
    unique_donors = df_filtered["DonorName"].nunique()
    donations_by_payment = df_filtered.groupby("PaymentMethodSystemName")["DonationAmount"].sum().to_dict()
    donations_by_zakat = df_filtered[df_filtered["IsDonationZakat"] == True]["DonationAmount"].sum()
    peak_hours = df_filtered.groupby("Hour")["DonationAmount"].sum().to_dict()
    donations_by_month = df_filtered.groupby("Month")["DonationAmount"].sum().to_dict()
    donation_counts = df_filtered.groupby("Month")["DonationCount"].sum().to_dict()
    target_vs_actual = df_filtered.groupby("ProductName")[["TargetAmount", "DonationAmount"]].sum().to_dict()

    # أكثر يوم في التبرعات
    most_donations_day = donations_by_day.get(max(donations_by_day, key=donations_by_day.get), 0) if donations_by_day else 0
    most_donations_day_name = max(donations_by_day_name, key=donations_by_day_name.get) if donations_by_day_name else "غير متوفر"

    # رسم بياني بواسطة Plotly
    fig = px.bar(
        x=list(donations_by_payment.keys()),
        y=list(donations_by_payment.values()),
        labels={"x": "طريقة الدفع", "y": "إجمالي التبرعات"},
        title="إجمالي التبرعات حسب طريقة الدفع"
    )
    fig.write_html("static/payment_method_chart.html")

    return render_template(
        "index.html",
        total_donations_top_clients=total_donations_top_clients,
        top_clients=top_clients,
        num_products=num_products,
        num_marketers=num_marketers,
        num_donors=num_donors,
        total_donations=total_donations,
        donations_by_product=donations_by_product,
        donations_by_marketer=donations_by_marketer,
        unique_donors=unique_donors,
        donations_by_payment=donations_by_payment,
        donations_by_zakat=donations_by_zakat,
        peak_hours=peak_hours,
        donations_by_month=donations_by_month,
        donation_counts=donation_counts,
        target_vs_actual=target_vs_actual,
        donations_by_day_name=donations_by_day_name,
        donations_by_day=donations_by_day,
        most_donations_day=most_donations_day,
        most_donations_day_name=most_donations_day_name,
        selected_month=selected_month,
        selected_day=selected_day,
        selected_payment_method=selected_payment_method,
        selected_num_clients=selected_num_clients
    )

if __name__ == "__main__":
    app.run(debug=True)
