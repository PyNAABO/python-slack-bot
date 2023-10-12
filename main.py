"""
https://github.com/techwithtim/Slack-Bot/blob/main/bot.py
"""
import os
import slack
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

# os.system("pip install slackclient")
SLACK_TOKEN = os.environ['SLACK_TOKEN']
SIGNING_SECRET = os.environ['SIGNING_SECRET']
os.system("clear")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)


@app.route('/')
def home():
	return "I'm alive"


client = slack.WebClient(token=SLACK_TOKEN)
BOT_ID = client.api_call("auth.test")['user_id']

# #Send Message
# client.chat_postMessage(channel="#random", text="Hello World!!")

# #Update Sent Message
# response = client.chat_postMessage(channel=channel_id,text=f"You Sent: {text}")
# client.chat_update(channel=channel_id, ts=response['ts'], text="Updated!!")

# #Send DM
# client.chat_postMessage(channel=f"@{user_id}", text="Hello World!!")

message_counts = {}


##Checking for new Message
@slack_event_adapter.on('message')
def message(payload):
	event = payload.get('event', {})
	channel_id = event.get('channel')
	user_id = event.get('user')
	text = event.get('text')

	if user_id != None and BOT_ID != user_id:
		if user_id in message_counts:
			message_counts[user_id] += 1
		else:
			message_counts[user_id] = 1
		client.chat_postMessage(channel=channel_id, text=f"You Sent: {text}")


##Slash Commands
@app.route('/message-count', methods=['POST'])
def message_count():
	data = request.form
	user_id = data.get('user_id')
	# text = data.get('text')
	channel_id = data.get('channel_id')
	message_count = message_counts.get(user_id, 0)

	client.chat_postMessage(channel=channel_id, text=f"Message: {message_count}")
	return Response(), 200


app.run(host='0.0.0.0', port=38355)
