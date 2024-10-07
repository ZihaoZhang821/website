from flask import Flask, send_from_directory, request, redirect, url_for,render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 配置连接到 MySQL 的数据库URL，使用 pymysql 驱动
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mypassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db = SQLAlchemy(app)


# 定义 SQLAlchemy 模型
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)


# 创建数据库表（如果不存在）
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


# 处理表单提交，将数据插入数据库
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']

        # 创建 Booking 实例并添加到数据库
        new_booking = Booking(name=name, email=email, phone=phone, date=date, time=time)

        try:
            db.session.add(new_booking)
            db.session.commit()
            return redirect(url_for('index', success='true'))
        except Exception as e:
            return f'There was an issue submitting your booking: {str(e)}'


if __name__ == "__main__":
    app.run(debug=True)