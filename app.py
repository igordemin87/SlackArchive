import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Получаем токен Slack Bot из переменных окружения
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    "Content-Type": "application/json"
}

@app.route('/slack/actions', methods=['POST'])
def handle_slack_actions():
    payload = request.form.get('payload')
    if payload:
        payload_data = json.loads(payload)
        action_id = payload_data['actions'][0]['action_id']
        channel_id = payload_data['channel']['id']
        
        if action_id == 'archive_channel':
            archive_channel(channel_id)
            return jsonify({"text": "Channel successfully archived!"})

    return jsonify({"text": "No action taken."})

def archive_channel(channel_id):
    archive_url = "https://slack.com/api/conversations.archive"
    response = requests.post(archive_url, headers=HEADERS, json={"channel": channel_id})
    if response.ok:
        print(f"Channel {channel_id} archived successfully.")
    else:
        print(f"Failed to archive channel {channel_id}: {response.text}")

if __name__ == "__main__":
    app.run(port=5000)
