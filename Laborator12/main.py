from flask import Flask, request, jsonify
import os

app = Flask(__name__)

directoryPath = "senzori/"
os.makedirs(directoryPath, exist_ok=True)

@app.route('/senzori/<ID>', methods=['GET'])
def get_sensor_data(ID):
    file_path = os.path.join(directoryPath, f"{ID}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        return jsonify({"ID": ID, "data": data}), 200
    else:
        return jsonify({"ID": ID, "status": "Error 404, not found"}), 404

@app.route('/senzori/<ID>', methods=['POST'])
def create_sensor_config(ID):
    file_path = os.path.join(directoryPath, f"{ID}_cfg.txt")
    content = request.get_data(as_text=True)

    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"ID": ID, "status": "Cfg created"}), 201
    else:
        return jsonify({"ID": ID, "status": "Cfg exists, cannot recreate"}), 409

@app.route('/senzori/<cfg>', methods=['PUT'])
def update_sensor_config(cfg):
    file_path = os.path.join(directoryPath, f"{cfg}_cfg.txt")
    content = request.get_data(as_text=True)

    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"fileID": cfg, "status": "Cfg updated"}), 200
    else:
        return jsonify({"fileID": cfg, "status": "Error 404, not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
