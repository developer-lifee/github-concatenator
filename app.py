from flask import Flask, render_template, request, send_file
import requests
from urllib.parse import urlparse
from io import BytesIO

app = Flask(__name__)

INVALID_EXTENSIONS = ["png", "jpg", "exe", "dmg", "webp", "gif", "bmp", "mp3", "mp4", "avi", "mov", "wav", "flac", "iso", "zip", "rar", "7z", "tar", "psd", "ai", "pdf"]

def get_github_repo_contents(api_url):
    headers = {'User-Agent': 'GitHubConcatenatorApp'}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def draw_ascii_structure(file_data, output_lines, prefix=''):
    count = len(file_data)
    for index, item in enumerate(file_data):
        connector = '├── ' if index < count - 1 else '└── '
        if item["type"] == "dir":
            output_lines.append(f"{prefix}{connector}{item['name']}/")
            subdir_data = get_github_repo_contents(item["url"])
            draw_ascii_structure(subdir_data, output_lines, prefix + ('│   ' if index < count - 1 else '    '))
        else:
            output_lines.append(f"{prefix}{connector}{item['name']}")

def concatenate_files(file_data, content_list):
    for item in file_data:
        if item["type"] == "file":
            headers = {'User-Agent': 'GitHubConcatenatorApp'}
            response = requests.get(item["download_url"], headers=headers)
            response.raise_for_status()
            if not item['path'].split(".")[-1].lower() in INVALID_EXTENSIONS:
                content_list.append(f"\nArchivo: {item['path']}\n")
                content_list.append(response.text)
        elif item["type"] == "dir":
            subdir_data = get_github_repo_contents(item["url"])
            concatenate_files(subdir_data, content_list)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        repo_url = request.form['repo_url'].strip()
        output_filename = request.form.get('output_filename', 'onefile.txt').strip() or 'onefile.txt'
        try:
            # Parsear la URL del repositorio
            parsed_url = urlparse(repo_url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            if 'tree' not in path_parts:
                error = "La URL debe contener 'tree' para especificar la rama y el path."
                return render_template('index.html', error=error)
            
            # Extraer owner, repo, branch y ruta
            owner = path_parts[0]
            repo = path_parts[1]
            tree_index = path_parts.index('tree')
            branch = path_parts[tree_index + 1]
            path = '/'.join(path_parts[tree_index + 2:])
            
            # Construir la URL de la API
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
            
            # Obtener los archivos y carpetas desde la API
            file_data = get_github_repo_contents(api_url)
            
            # Generar la estructura de directorios en ASCII
            structure_lines = ["Estructura de directorios:"]
            draw_ascii_structure(file_data, structure_lines)
            
            # Concatenar el contenido de los archivos
            content_list = ["\nContenido de archivos:"]
            concatenate_files(file_data, content_list)
            
            # Crear un archivo en memoria
            output = '\n'.join(structure_lines + content_list)
            memory_file = BytesIO()
            memory_file.write(output.encode('utf-8'))
            memory_file.seek(0)
            
            # Enviar el archivo para descarga
            return send_file(memory_file, download_name=output_filename, as_attachment=True)
            
        except Exception as e:
            error = f"Error al procesar la solicitud: {e}"
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
