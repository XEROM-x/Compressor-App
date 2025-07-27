import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from patoolib import extract_archive, create_archive

app = Flask(__name__)
app.secret_key = "supersecret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/unzip', methods=['POST'])
def unzip_file():
    """Extract an uploaded archive to a selected folder"""
    if 'zipfile' not in request.files:
        flash("No file uploaded!")
        return redirect(url_for('index'))

    zip_file = request.files['zipfile']
    extract_path = request.form.get('extract_path')

    if not extract_path:
        flash("Please enter a destination folder!")
        return redirect(url_for('index'))

    filename = secure_filename(zip_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    zip_file.save(file_path)

    try:
        if not os.path.exists(extract_path):
            os.makedirs(extract_path, exist_ok=True)

        extract_archive(file_path, outdir=extract_path)
        flash(f"Extracted successfully to: {extract_path}")
    except Exception as e:
        flash(f"Error extracting: {str(e)}")
    finally:
        os.remove(file_path)

    return redirect(url_for('index'))


@app.route('/compress', methods=['POST'])
def compress_files():
    """Compress uploaded files into a selected format"""
    if 'files[]' not in request.files:
        flash("No files uploaded!")
        return redirect(url_for('index'))

    files = request.files.getlist('files[]')
    format_selected = request.form.get('format')
    output_name = request.form.get('output_name')

    if not format_selected or not output_name:
        flash("Please select format and enter output name!")
        return redirect(url_for('index'))

    # Temporary folder to save files
    temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], "temp_files")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

    saved_files = []
    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        saved_files.append(file_path)

    output_file = os.path.join(app.config['UPLOAD_FOLDER'], f"{output_name}.{format_selected}")

    try:
        create_archive(output_file, saved_files)
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        flash(f"Error compressing: {str(e)}")
        return redirect(url_for('index'))
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    app.run(debug=True)
