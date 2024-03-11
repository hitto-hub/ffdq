from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # セッション情報を暗号化するための秘密鍵

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    question = request.form['question']
    response = requests.post('http://192.168.10.2/api', json={'question': question})
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            return render_template('success.html', data=data['data'])
        else:
            flash('質問の送信に失敗しました。', 'error')
    else:
        flash('サーバーに接続できませんでした。', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
