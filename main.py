from flask import Flask, redirect, render_template, request
app = Flask(__name__)

from config import config

api = config



@app.route('/')
def hello_world():
    data = api.getResource('belajar')
    return render_template('index.html', title='Home', data=data, content='Hello World!')

@app.route('/create', methods=['POST'])
def create():
    nama = request.form['nama']
    umur = request.form['umur']
    api.postResource('belajar', {'nama': nama, 'umur': int(umur)})
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    api.deleteResource('belajar', {'id': id})
    return redirect('/')

@app.route('/update/<id>', methods=['POST'])
def update(id):
    nama = request.form['nama']
    umur = request.form['umur']
    api.putResource('belajar', {'nama': nama, 'umur': int(umur)}, {'id': id})
    return redirect('/')

if __name__ == '__app__':
    app.run(debug=True)
