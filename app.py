from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Limite de 16 MB

if not os.path.exists('uploads'):
    os.makedirs('uploads')

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS documentos
                        (id INTEGER PRIMARY KEY, titulo TEXT, conteudo TEXT, filename TEXT)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS fornecedores
                        (id INTEGER PRIMARY KEY, nome TEXT, avaliacao INTEGER,
                         condicoes_pagamento INTEGER, frete_cif INTEGER, possui_iso INTEGER,
                         precos_justos INTEGER, boa_indicacao INTEGER)''')

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/documentos', methods=['GET', 'POST'])
def documentos():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        file = request.files['file']
        filename = None
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO documentos (titulo, conteudo, filename) VALUES (?, ?, ?)', (titulo, conteudo, filename))
            conn.commit()
        return redirect(url_for('documentos'))
    with sqlite3.connect('database.db') as conn:
        docs = conn.execute('SELECT * FROM documentos').fetchall()
    return render_template('documentos.html', documentos=docs)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_documento/<int:id>', methods=['POST'])
def delete_documento(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute('SELECT filename FROM documentos WHERE id = ?', (id,))
        file = cursor.fetchone()
        if file and file[0]:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file[0]))
        conn.execute('DELETE FROM documentos WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('documentos'))

@app.route('/fornecedores', methods=['GET', 'POST'])
def fornecedores():
    if request.method == 'POST':
        nome = request.form['nome']
        condicoes_pagamento = int(request.form['condicoes_pagamento'])
        frete_cif = int(request.form['frete_cif'])
        possui_iso = int(request.form['possui_iso'])
        precos_justos = int(request.form['precos_justos'])
        boa_indicacao = int(request.form['boa_indicacao'])
        avaliacao = (condicoes_pagamento + frete_cif + possui_iso + precos_justos + boa_indicacao) / 5
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO fornecedores (nome, avaliacao, condicoes_pagamento, frete_cif, possui_iso, precos_justos, boa_indicacao) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (nome, avaliacao, condicoes_pagamento, frete_cif, possui_iso, precos_justos, boa_indicacao))
            conn.commit()
        return redirect(url_for('fornecedores'))
    with sqlite3.connect('database.db') as conn:
        fornecedores = conn.execute('SELECT * FROM fornecedores').fetchall()
    return render_template('fornecedores.html', fornecedores=fornecedores)

@app.route('/delete_fornecedor/<int:id>', methods=['POST'])
def delete_fornecedor(id):
    with sqlite3.connect('database.db') as conn:
        conn.execute('DELETE FROM fornecedores WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('fornecedores'))

if __name__ == '__main__':
    app.run(debug=True)
