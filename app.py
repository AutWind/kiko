from flask import Flask,render_template,request,session,redirect,url_for
import config
app = Flask(__name__)
app.config.from_object(config)



# 默认初始路径，跳转到登陆页面
@app.route('/base')
def index():
    return render_template('index1.html')

@app.route('/crawler')
def crawler():
    return render_template('index2.html')

@app.route('/usernet')
def usernet():
    return render_template('index3.html')

@app.route('/recommend')
def recommend():
    return render_template('index4.html')
@app.route('/commodity')
def commodity():
    return render_template('index5.html')
# 登陆功能
@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        if email == '123@qq.com' and password == '123':
            return render_template('index1.html')
        else:
            return '用户名或密码错误'








if __name__ == '__main__':
    app.run()


