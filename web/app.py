import sys
import time
import serial
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# ==========================================
# 1. 설정 (Configuration)
# ==========================================
SERIAL_PORT = '/dev/ttyACM0'  
BAUD_RATE = 115200

# [수정됨] 조향 튜닝 (좌회전이 약하면 값을 키우세요!)
# 기존 500 -> 600으로 변경 (범위가 900~2100으로 넓어짐)
STEERING_FACTOR = 500 
CENTER_PWM = 1500    # 만약 직진이 안 맞으면 이 값을 1450 or 1550으로 조절

app = Flask(__name__, static_folder='static', template_folder='templates')
socketio = SocketIO(app, cors_allowed_origins="*")

stm32_serial = None
engine_running = False # [수정됨] 엔진 상태 관리 변수

# ==========================================
# 2. 시스템 기능
# ==========================================
def sys_log(msg, type="INFO"):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    print(f"[{type}] {formatted_msg}")
    socketio.emit('system_log', {'type': type, 'log': formatted_msg})

def connect_serial():
    global stm32_serial
    try:
        stm32_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        sys_log(f"Connected to STM32 on {SERIAL_PORT}", "SUCCESS")
        return True
    except Exception as e:
        sys_log(f"Serial Connection Failed: {e}", "ERROR")
        return False

def send_to_stm32(speed, angle):
    """STM32로 패킷 전송하는 헬퍼 함수"""
    if stm32_serial and stm32_serial.is_open:
        command = f"{speed},{angle}\n"
        stm32_serial.write(command.encode())

# ==========================================
# 3. 라우팅 & 소켓 핸들러
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    sys_log("Client Connected", "SUCCESS")
    # 접속 시 현재 엔진 상태 알려줌
    emit('engine_update', {'running': engine_running})
    if stm32_serial is None or not stm32_serial.is_open:
        connect_serial()

@socketio.on('ping_event')
def handle_ping(data):
    socketio.emit('pong_event', data)

# [수정됨] 엔진 토글 로직 완벽 구현
@socketio.on('toggle_engine')
def handle_engine():
    global engine_running
    engine_running = not engine_running # 상태 반전 (On <-> Off)
    
    if engine_running:
        sys_log("Engine STARTED", "SUCCESS")
        emit('engine_update', {'running': True})
    else:
        sys_log("Engine STOPPED", "WARN")
        emit('engine_update', {'running': False})
        # 엔진 끄면 즉시 정지 & 바퀴 정렬
        send_to_stm32(0, CENTER_PWM)

# [수정됨] 조향 범위 확대 및 엔진 상태 체크
@socketio.on('control_command')
def handle_control_command(data):
    # 엔진이 꺼져있으면 명령 무시
    if not engine_running:
        return

    try:
        throttle = float(data.get('throttle', 0))
        steering = float(data.get('steering', 0))
        
        # 1. 속도 계산
        pwm_speed = int(throttle * 999)
        
        # 2. 조향 계산 (튜닝 변수 적용)
        # steering(-1.0 ~ 1.0) * 600 = -600 ~ 600
        # 1500 + (-600) = 900 (더 많이 꺾임)
        # 1500 + (600) = 2100 (더 많이 꺾임)
        pwm_angle = int(CENTER_PWM + (steering * STEERING_FACTOR))
        
        # 3. 안전 범위 제한 (하드웨어 보호)
        # 서보가 씹히는 소리가 나면 이 범위를 800~2200 정도로 줄이세요.
        pwm_angle = max(700, min(2300, pwm_angle))

        # 4. 전송
        send_to_stm32(pwm_speed, pwm_angle)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    print("Starting Neuro-Driver Bridge Server...")
    connect_serial()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)