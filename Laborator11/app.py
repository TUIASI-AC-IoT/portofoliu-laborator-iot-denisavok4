from flask import Flask, jsonify, request
import os, random, string
from pathlib import Path

app = Flask(__name__)

files_dir = Path("C:/Users/Denisa/PycharmProjects/files")
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/files', methods=['GET'])
def get_file_list():
    list_of_files=os.listdir(files_dir)
    return jsonify(list_of_files)

@app.route('/files/<filename>', methods=['GET'])
def get_file_by_name(filename):
    file_path = os.path.join(files_dir, filename)

    if os.path.isfile(file_path):
        file = open(file_path, 'r')
        return jsonify({'content': file.read()})
    return jsonify({'error': 'File not found'}), 404

@app.route('/files', methods=['POST'])
def create_file_by_name_and_content():
    data = request.get_json()
    filename = data.get('filename')
    content = data.get('content', '')

    if filename and content is not None:
        file_path = os.path.join(files_dir, filename)
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({'message': 'File created', 'filename': filename}), 201

    return jsonify({'error': 'Filename and content are required'}), 400

@app.route('/files/content', methods=['POST'])
def create_file_by_content():
    data = request.get_json()
    content = data.get('content', '')

    if content is not None:
        random_digits = ''.join(random.choices(string.digits, k=5))
        filename = f'file{random_digits}.txt'
        file_path = os.path.join(files_dir, filename)
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({'message': 'File created', 'filename': filename}), 201

    return jsonify({'error': 'Content are required'}), 400

@app.route('/files/<filename>', methods=['DELETE'])
def delete_file_by_name(filename):
    file_path = os.path.join(files_dir, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File was deleted successfully.'}), 200
    return jsonify({'error': 'File not found.'}), 404

@app.route('/files/<filename>', methods=['PUT'])
def update_file_by_name(filename):
    data = request.get_json()
    new_content = data.get('content', '')

    file_path = os.path.join(files_dir, filename)
    if os.path.isfile(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        return jsonify({'message': 'File was updated successfully.'}), 200
    return jsonify({'error': 'File not found.'}), 404

if __name__ == '__main__':
    app.run()