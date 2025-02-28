from flask import Flask, request, jsonify
from telethon import TelegramClient

app = Flask(__name__)

@app.route("/send_messages", methods=["POST"])
def send_messages():
    data = request.json
    api_id = data["api_id"]
    api_hash = data["api_hash"]
    chat_ids = data["chatIds"]
    message = data["message"]

    client = TelegramClient("session", api_id, api_hash)
    
    async def send_dm():
        await client.start()
        for chat_id in chat_ids:
            try:
                await client.send_message(chat_id, message)
            except Exception as e:
                print(f"Failed to send message to {chat_id}: {str(e)}")
        await client.disconnect()

    with client:
        client.loop.run_until_complete(send_dm())

    return jsonify({"message": "Messages sent successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
