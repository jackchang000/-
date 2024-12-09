from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinking_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # 用來保護 session

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 定義資料庫模型
class DrinkRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<DrinkRecord {self.name}, {self.time}>'

# 初始化資料庫表格
def create_tables():
    # 使用應用上下文來執行資料庫創建
    with app.app_context():
        db.create_all()

# 設定首頁路由
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 取得使用者輸入的體重
        weight = float(request.form['weight'])
        
        # 計算每日所需水量
        required_water = weight * 30  # 每公斤30cc
        
        # 顯示計算結果
        return render_template('index.html', required_water=required_water)

    # 顯示所有紀錄
    records = DrinkRecord.query.all()  # 查詢所有紀錄
    return render_template('index.html', records=records, required_water=None)

# 新增紀錄頁面
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        location = request.form['location']
        reason = request.form['reason']
        amount = request.form['amount']

        # 新增資料到資料庫
        new_record = DrinkRecord(name=name, time=time, location=location, reason=reason, amount=amount)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add.html')

# 編輯紀錄頁面
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    record = DrinkRecord.query.get_or_404(id)

    if request.method == 'POST':
        record.name = request.form['name']
        record.time = request.form['time']
        record.location = request.form['location']
        record.reason = request.form['reason']
        record.amount = request.form['amount']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', record=record)

# 刪除紀錄
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    record = DrinkRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 在啟動應用程式之前創建資料表
    create_tables()
    app.run(debug=True)
