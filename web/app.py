from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    action = request.form['direction']

    if action == 'FORWARD':
        print("[동작] 전진!")
    elif action == 'BACKWARD':
        print("[동작] 후진!")
    elif action == 'LEFT':
        print("[조향] 좌회전")
    elif action == 'RIGHT':
        print("[조향] 우회전")
    elif action == 'STOP':
        print("[정지] 모터 전원 차단")

    return "received"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)