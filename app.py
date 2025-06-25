from flask import Flask, render_template, request
import threading, json
from bot import start_bot, stop_bot

app = Flask(__name__)
bot_thread = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global bot_thread
    if not is_bot_running():
        set_bot_state(True)
        bot_thread = threading.Thread(target=start_bot, daemon=True)
        bot_thread.start()
    return ('', 204)

@app.route('/stop', methods=['POST'])
def stop():
    stop_bot()
    set_bot_state(False)
    return ('', 204)

def set_bot_state(state: bool):
    with open('control_state.json', 'w') as f:
        json.dump({'running': state}, f)

def is_bot_running() -> bool:
    try:
        with open('control_state.json') as f:
            return json.load(f).get('running', False)
    except:
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
