from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')  # Получаем токен из переменной окружения

@app.route('/archive', methods=['POST'])
def archive_channel():
    data = request.json
    channel_id = data['channel_id']  # Получаем ID канала из запроса

    try:
        response = requests.post(
            'https://slack.com/api/conversations.archive',
            headers={
                'Authorization': f'Bearer {SLACK_TOKEN}',
                'Content-Type': 'application/json',
            },
            json={'channel': channel_id}
        )

        if response.json().get('ok'):
            return jsonify({'status': 'success', 'message': 'Channel archived successfully.'}), 200
        else:
            return jsonify({'status': 'error', 'message': response.json().get('error')}), 400

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
