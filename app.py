from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os
import datetime

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max size

messages = []

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    username = request.form['username']
    message = request.form.get('message', '')

    image_url = None
    if 'image' in request.files:
        image_file = request.files['image']
        if image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            image_url = url_for('static', filename=f'uploads/{image_filename}')

    new_message = {
        'id': len(messages) + 1,
        'username': username,
        'message': message if message else "[Image]",  # If there's no text, assume it's an image message
        'image_url': image_url,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(new_message)

    return '', 204

@app.route('/send_voice_message', methods=['POST'])
def send_voice_message():
    if 'voiceMessage' not in request.files:
        return jsonify({'error': 'No voice message uploaded'}), 400
    
    voice_file = request.files['voiceMessage']
    if voice_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if voice_file:
        filename = secure_filename(voice_file.filename)
        voice_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        voice_file.save(voice_path)

        voice_message_data = {
            'id': len(messages) + 1,
            'username': request.form['username'],
            'message': '[Voice Message]',
            'image_url': url_for('static', filename=f'uploads/{filename}'),
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        messages.append(voice_message_data)
        return '', 204

    return jsonify({'error': 'File upload failed'}), 500

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

@app.route('/delete_message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    username = request.form['username']
    message_to_delete = next((msg for msg in messages if msg['id'] == message_id), None)

    if message_to_delete and message_to_delete['username'] == username:
        messages.remove(message_to_delete)
        return '', 204
    else:
        return jsonify({'error': 'Message not found or unauthorized'}), 403

if __name__ == '__main__':
    app.run(debug=True)
