from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from automata.automata import Automata
from pdf_generator import generar_pdf
from csv_generator import  generar_csv
import os
import PyPDF2
import docx
import tempfile

# Configuración de Flask
app = Flask(__name__)

# Carpeta para subir archivos temporalmente
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurarse de que la carpeta de subida exista
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para verificar que el archivo subido es permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def leer_txt(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def leer_pdf(filepath):
    content = ""
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            content += reader.pages[page_num].extract_text()
    return content

def leer_docx(filepath):
    doc = docx.Document(filepath)
    content = "\n".join([para.text for para in doc.paragraphs])
    return content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file-upload' not in request.files:
        return jsonify({'error': 'No se subió ningún archivo'}), 400

    file = request.files['file-upload']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if filename.endswith('.txt'):
            content = leer_txt(filepath)
        elif filename.endswith('.pdf'):
            content = leer_pdf(filepath)
        elif filename.endswith('.docx'):
            content = leer_docx(filepath)
        else:
            return jsonify({'error': 'Formato de archivo no permitido'}), 400

        automata = Automata()
        patrones = automata.extraer_patrones(content)

        if patrones:
            return jsonify({'patrones': patrones, 'pdf': True, 'excel': True})
        else:
            return jsonify({'patrones': [], 'pdf': False, 'excel': False})

    return jsonify({'error': 'Archivo no permitido'}), 400

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    patrones = request.json.get('patrones')
    if patrones:
        pdf_filename = generar_pdf(patrones)
        return send_file(pdf_filename, as_attachment=True)
    return jsonify({'error': 'No se encontraron patrones'}), 400

@app.route('/download_excel', methods=['POST'])
@app.route('/download_csv')
def download_csv():
    patrones = request.args.getlist('patrones')
    if patrones:
        csv_filename = generar_csv(patrones)
        return send_file(csv_filename, as_attachment=True, mimetype='text/csv')
    return jsonify({'error': 'No se encontraron patrones'}), 400


if __name__ == '__main__':
    app.run(debug=True)
