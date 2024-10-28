from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# 假设有一个用户存储（在实际应用中应使用数据库）
users = {}

class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

@login_manager.user_loader
def load_user(email):
    return users.get(email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users:
            flash('用户已存在！')
        else:
            users[email] = User(email, password)
            flash('注册成功，请登录！')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = load_user(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('登录失败，请检查您的电子邮件和密码。')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f'欢迎，{current_user.email}！这是您的个人仪表盘。'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
