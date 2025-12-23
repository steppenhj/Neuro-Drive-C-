# 🚗 Neuro-Drive: Raspberry Pi 5 Autonomous RC Car

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python) ![Flask](https://img.shields.io/badge/Flask-Web_Server-green?logo=flask) ![Raspberry Pi](https://img.shields.io/badge/Hardware-Raspberry_Pi_5-C51A4A?logo=raspberrypi) ![C++](https://img.shields.io/badge/Language-C++-00599C?logo=c%2B%2B)

**Raspberry Pi 5**와 **Ackermann Steering Chassis**를 활용한 자율주행 RC카 프로젝트입니다.  
현재 **Web 기반의 실시간 원격 제어(Remote Control)** 시스템이 구축되어 있으며, 향후 C++ 기반의 고성능 자율주행 알고리즘을 탑재할 예정입니다. Reference: end-to-end-dl-using-px (Nvidia, 2016, CNN 관련)

## 🛠 Hardware Specifications

### 1. Core System (Robot Body)
자율주행 RC카의 구동 및 제어를 담당하는 핵심 하드웨어 구성입니다.

| Component | Model / Specs | Role in System |
| :--- | :--- | :--- |
| **Platform** | **Ackermann Steering Chassis (5KG)** | **[Mechanism]** 실제 차량과 동일한 전륜 조향/후륜 구동(RWD) 방식. 차량 동역학 학습 및 제어. |
| **Main Computer** | **Raspberry Pi 5 (8GB RAM)** | **[Brain]** 고해상도 영상 처리 및 자율주행 알고리즘 연산을 위한 고사양 컴퓨팅 유닛. |
| **Cooling** | **Raspberry Pi 5 Active Cooler** | **[Thermal]** 고부하 연산 시 쓰로틀링 방지 및 시스템 안정성 확보. |
| **Motor Driver** | **Waveshare Motor Driver HAT** | **[Control]** PCA9685 칩셋(I2C 인터페이스)을 통한 정밀 PWM 제어 및 모터 구동. |
| **Power Source** | **Li-Po Battery 7.4V 2S1P (35C)** | **[Power]** 고방전율(35C) 배터리를 통한 급격한 부하 변동 대응 및 안정적 전원 공급. |

### 2. Wiring & Connectivity
시스템 전원 및 신호 전달을 위한 배선입니다.

- **Power Connection:** XT60H Connector Cable (10cm) - *배터리와 드라이버 HAT 간의 안전한 고전류 연결*
- **Signal Wiring:** 40-pin Jumper Cables (M-F, F-F) - *GPIO 확장 및 센서 인터페이스 연결*

### 3. Development & Maintenance Tools
개발 효율성 및 하드웨어 유지보수를 위한 장비입니다.

- **Storage:** SanDisk Micro SD Card 128GB - *OS(Linux), 라이브러리 및 대용량 주행 로그(Log) 저장*
- **I/O:** USB Type-C Card Reader - *PC-라즈베리파이 간 데이터 전송*
- **Charging:** IMAX B6 Charger + 12V 5A PSU - *Li-Po 배터리 셀 밸런싱 및 화재 예방/안전 충전*

---
> **💡 System Highlights**
> - **Ackermann Geometry:** 일반적인 로봇(Differential Drive)과 달리, 실제 자동차의 조향 특성을 모사하여 비홀로노믹(Non-holonomic) 제약 조건을 고려한 제어를 수행합니다.
> - **I2C Communication:** GPIO 직접 제어가 아닌 **I2C 프로토콜**을 통해 모터 드라이버와 통신하며, 확장 가능한 임베디드 시스템 구조를 지향합니다.

## 💻 Software Stack
- **Backend:** Python (Flask), C++ (Low-level Motor Control)
- **Frontend:** HTML5, CSS3, JavaScript (Touch Interface)
- **Communication:** HTTP (REST API), WebSocket (Planned)
- **OS:** Raspberry Pi OS (Bookworm 64-bit)

## 🚀 Key Features
1. **Web-based Controller:** 별도 앱 설치 없이 스마트폰 브라우저로 접속하여 제어
2. **Real-time Latency:** 내부망(Wi-Fi) 기준 지연 시간 최소화
3. **Safety Logic:** Dead Man's Switch 적용 (손을 떼면 즉시 정지)
4. **Touch Interface:** 모바일 터치 이벤트 최적화 (확대/메뉴 팝업 방지)

## 🔧 Installation & Run

### 1. Clone Repository
```bash
git clone [https://github.com/steppenhj/Neuro-Drive-C-.git](https://github.com/steppenhj/Neuro-Drive-C-.git)
cd Neuro-Drive-C++