import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# --- إعدادات التطبيق والداتا بيس ---
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# !! غيري هذا المفتاح السري عقب !!
app.config['SECRET_KEY'] = 'a7la_secret_key_fedonia_ محد_يعرفه' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cars.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- تعريف شكل الداتا بيس (شو بنخزن؟) ---
class CarLog(db.Model):
    id = db.Column(db.Integer, primary_key=True) # رقم تسلسلي
    username = db.Column(db.String(100), nullable=False) # اسم الشخص
    military_id = db.Column(db.String(50), nullable=False) # الرقم العسكري
    car_type = db.Column(db.String(50), nullable=False) # نوع السيارة
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc)) # الوقت (أوتوماتيك)

    def __repr__(self):
        return f"Log('{self.username}', '{self.car_type}', '{self.timestamp}')"

# --- الصفحة الرئيسية (اللي بيفتحها الموظف) ---
@app.route('/')
def index():
    # بنجيب 'نوع السيارة' من اللينك (عشان الـ QR)
    car_name = request.args.get('car', 'سيارة غير محددة') 
    return render_template('form.html', car_name=car_name)

# --- صفحة استلام البيانات (لما الموظف يضغط 'إرسال') ---
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        military_id = request.form['military_id']
        car_type = request.form['car_type']

        new_log = CarLog(username=username, military_id=military_id, car_type=car_type)

        try:
            db.session.add(new_log)
            db.session.commit()
            flash('تم تسجيل بياناتك بنجاح! شكراً.', 'success')
            return redirect(url_for('index', car=car_type)) # نرجعه لنفس صفحة السيارة
        except:
            flash('صار خطأ! حاول مرة ثانية.', 'danger')
            return redirect(url_for('index', car=car_type))

# --- صفحة الأدمن (Dashboard) - هاي صفحتج أنتي ---
@app.route('/admin')
def admin():
    all_logs = CarLog.query.order_by(CarLog.timestamp.desc()).all()
    return render_template('admin.html', logs=all_logs)

