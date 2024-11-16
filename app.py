from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Payment System')

@app.route('/create_wallet')
def create_wallet(create_wallet):
    return render_template('create_wallet.html')

@app.route('/recover_wallet')
def recover_wallet(recover_wallet):
    return render_template('recover_wallet.html')

if __name__ == '__main__':
    app.run(debug=True)
