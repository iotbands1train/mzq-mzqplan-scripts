from flask import Flask, request, jsonify
import os
import shutil

app = Flask(__name__)

# Directories where files will be moved
waiting_directory = r"E:\waiting"
denied_directory = r"E:\denied"

# Ensure target directories exist
os.makedirs(waiting_directory, exist_ok=True)
os.makedirs(denied_directory, exist_ok=True)

@app.route('/approve', methods=['GET'])
def approve():
    file_path = request.args.get('file')
    if file_path:
        move_file(file_path, 'approve')
        return jsonify({"status": "success", "message": f"File {file_path} approved and moved to {waiting_directory}"}), 200
    return jsonify({"status": "error", "message": "File path not provided"}), 400

@app.route('/deny', methods=['GET'])
def deny():
    file_path = request.args.get('file')
    if file_path:
        move_file(file_path, 'deny')
        return jsonify({"status": "success", "message": f"File {file_path} denied and moved to {denied_directory}"}), 200
    return jsonify({"status": "error", "message": "File path not provided"}), 400

def move_file(file_path, action):
    if action == 'approve':
        destination_directory = waiting_directory
    elif action == 'deny':
        destination_directory = denied_directory
    else:
        raise ValueError("Invalid action. Use 'approve' or 'deny'.")

    # Move the file to the appropriate directory
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    shutil.move(file_path, os.path.join(destination_directory, os.path.basename(file_path)))
    print(f"File {file_path} moved to {destination_directory}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
