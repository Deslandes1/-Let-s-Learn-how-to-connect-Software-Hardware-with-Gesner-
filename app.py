import streamlit as st
import asyncio
import tempfile
import base64
import os

# ----- Audio setup with edge-tts -----
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    EDGE_TTS_AVAILABLE = False

def run_async_with_timeout(coro, timeout=30):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(asyncio.wait_for(coro, timeout=timeout))
    finally:
        loop.close()

async def save_speech(text, file_path, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_path)

def generate_audio(text, output_path, voice):
    if not EDGE_TTS_AVAILABLE:
        raise Exception("edge-tts not installed")
    run_async_with_timeout(save_speech(text, output_path, voice))

VOICE = "en-US-JennyNeural"

st.set_page_config(page_title="Let's Learn Software & Hardware with Gesner", layout="wide")

# ========== STYLING ==========
def set_style():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
        .main-header { background: linear-gradient(135deg, #00c9a7, #00a8c5, #005f6b); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1rem; }
        .main-header h1 { color: white; text-shadow: 2px 2px 4px #000000; font-size: 2.5rem; margin: 0; }
        .main-header p { color: #fff5cc; font-size: 1.2rem; margin: 0; }
        html, body, .stApp, .stMarkdown, .stText, .stRadio label, .stSelectbox label, .stTextInput label, .stButton button, .stTitle, .stSubheader, .stHeader, .stCaption, .stAlert, .stException, .stCodeBlock, .stDataFrame, .stTable, .stTabs [role="tab"], .stTabs [role="tablist"] button, .stExpander, .stProgress > div, .stMetric label, .stMetric value, div, p, span, .element-container, .stTextArea label, .stText p, .stText div, .stText span, .stText code { color: white !important; }
        .stTabs [role="tab"] { color: white !important; background: rgba(0,200,160,0.2); border-radius: 10px; margin: 0 2px; }
        .stTabs [role="tab"][aria-selected="true"] { background: #00c9a7; color: black !important; }
        .stRadio [role="radiogroup"] label { background: rgba(255,255,255,0.15); border-radius: 10px; padding: 0.3rem; margin: 0.2rem 0; color: white !important; }
        .stButton button { background-color: #00c9a7; color: white; border-radius: 30px; font-weight: bold; }
        .stButton button:hover { background-color: #00a8c5; color: black; }
        section[data-testid="stSidebar"] { background: linear-gradient(135deg, #0f2027, #203a43); }
        section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] .stText, section[data-testid="stSidebar"] label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox label { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] { background-color: #203a43; border: 1px solid #00c9a7; border-radius: 10px; }
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div { color: white !important; }
        section[data-testid="stSidebar"] .stSelectbox svg { fill: white; }
        div[data-baseweb="popover"] ul { background-color: #203a43; border: 1px solid #00c9a7; }
        div[data-baseweb="popover"] li { color: white !important; background-color: #203a43; }
        div[data-baseweb="popover"] li:hover { background-color: #00c9a7; }
        .image-placeholder {
            background-color: #2c5364;
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def show_logo():
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <svg width="100" height="100" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="45" fill="url(#gradLogo)" stroke="#00c9a7" stroke-width="3"/>
                <defs><linearGradient id="gradLogo" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00c9a7"/>
                    <stop offset="100%" stop-color="#005f6b"/>
                </linearGradient></defs>
                <text x="50" y="70" font-size="45" text-anchor="middle" fill="white" font-weight="bold">🔌</text>
            </svg>
        </div>
    """, unsafe_allow_html=True)

# ========== AUTHENTICATION ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    set_style()
    st.title("🔐 Access Required")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_logo()
        st.markdown("<h2 style='text-align: center;'>Let's Learn how to connect Software & Hardware with Gesner</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #00c9a7;'>20 lessons – from network cards to sensors and actuators</p>", unsafe_allow_html=True)
        password_input = st.text_input("Enter password to access", type="password")
        if st.button("Login"):
            if password_input == "20082010":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Access denied.")
    st.stop()

set_style()
st.markdown("""
<div class="main-header">
    <h1>🔌 Let's Learn how to connect Software & Hardware with Gesner</h1>
    <p>20 interactive lessons | Hardware communication | Audio support | Coding practice</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    show_logo()
    st.markdown("## 🎯 Select a lesson")
    lesson_number = st.selectbox("Lesson", list(range(1, 21)), index=0)
    st.markdown("---")
    st.markdown("### 📚 Your progress")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ Lesson {lesson_number} of 20 completed")
    st.markdown("---")
    st.markdown("**Founder & Developer:**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown("### 💰 Price")
    st.markdown("**$299 USD** (full book – 20 lessons, source code, certificate)")
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ========== HARDWARE LESSONS DATA ==========
hardware_list = [
    "Network Interface Card (NIC)", "Wi‑Fi Adapter", "Bluetooth Module", "Cellular Modem (4G/5G)", "GPS Receiver",
    "USB Controller / Port", "GPIO Pins", "Camera Module", "Microphone & Speaker", "LoRa / Sigfox Module",
    "Accelerometer / Gyroscope", "Temperature & Humidity Sensor", "RFID / NFC Reader", "Relay Module",
    "OLED / LCD Display", "Stepper Motor Driver", "Sound Sensor", "Gas / Smoke Sensor", "Joystick Module",
    "Ethernet Shield (for Arduino)"
]

explanations = {
    1: "**Network Interface Card (NIC)**\nA NIC allows your computer to connect to a wired Ethernet network. Software can send and receive data packets using sockets (TCP/IP). Example: Python's `socket` library.",
    2: "**Wi‑Fi Adapter**\nEnables wireless network communication. Software can scan networks, connect, and exchange data. Use `subprocess` to run system commands or libraries like `wifi`.",
    3: "**Bluetooth Module**\nConnects to nearby devices (keyboards, IoT sensors). Use PyBluez or Bleak libraries in Python to discover and communicate with Bluetooth devices.",
    4: "**Cellular Modem (4G/5G)**\nProvides internet via mobile networks. Software can use AT commands over serial to send SMS, make calls, or establish data connections.",
    5: "**GPS Receiver**\nReceives location from satellites. Software reads NMEA sentences via serial port to get latitude, longitude, altitude. Python's `pynmea2` parses GPS data.",
    6: "**USB Controller / Port**\nUniversal interface for peripherals. Software can detect USB devices using `pyusb` or read/write to serial USB devices (CDC ACM).",
    7: "**GPIO Pins**\nOn Raspberry Pi or Arduino, GPIO pins read sensors and control LEDs, motors. Python's `RPi.GPIO` or `gpiozero` libraries.",
    8: "**Camera Module**\nCaptures images/video. Use OpenCV (`cv2`) to access camera stream, process frames, and run computer vision algorithms.",
    9: "**Microphone & Speaker**\nAudio input/output. Use `pyaudio` or `sounddevice` to record from mic and play sound. Speech recognition with `speech_recognition`.",
    10: "**LoRa / Sigfox Module**\nLow‑power, long‑range radio for IoT. Communicate via serial AT commands. Use for agriculture, asset tracking, smart cities.",
    11: "**Accelerometer / Gyroscope**\nMeasures acceleration and rotation. Connect via I2C (e.g., MPU6050). Python's `smbus` or `adafruit-circuitpython` libraries.",
    12: "**Temperature & Humidity Sensor**\nDHT11/DHT22 sensors. Read via single‑wire protocol. Python's `Adafruit_DHT` library.",
    13: "**RFID / NFC Reader**\nRead RFID tags. Connect via serial or I2C. Use `pyserial` to read UID and interact with access control systems.",
    14: "**Relay Module**\nSwitch high‑power devices from low‑power GPIO. Control with `GPIO.output(pin, True/False)`. Used for home automation.",
    15: "**OLED / LCD Display**\nShow text and graphics. I2C or SPI interface. Use `luma.oled` or `RPLCD` libraries.",
    16: "**Stepper Motor Driver**\nControl precise rotation. Use GPIO pulses with `RPi.GPIO` or `AccelStepper` library.",
    17: "**Sound Sensor**\nDetects sound intensity. Analog sensor read via ADC (MCP3008) or digital output on threshold.",
    18: "**Gas / Smoke Sensor**\nDetect gases (MQ series). Read analog voltage to estimate concentration.",
    19: "**Joystick Module**\nTwo analog axes and a button. Read with ADC and GPIO. Used for robotics and game controllers.",
    20: "**Ethernet Shield**\nAdds wired Ethernet to Arduino. Use Arduino's Ethernet library for TCP/IP communication."
}

# Demo code snippets (simplified Python or Arduino examples)
demo_codes = {
    1: "import socket\ns = socket.socket()\ns.connect(('google.com', 80))\ns.send(b'GET / HTTP/1.1\\r\\n\\r\\n')\nprint(s.recv(1024))",
    2: "import subprocess\nsubprocess.run(['nmcli', 'dev', 'wifi', 'list'])",
    3: "import asyncio\nfrom bleak import BleakScanner\nasync def scan():\n    devices = await BleakScanner.discover()\n    for d in devices:\n        print(d.name)\nasyncio.run(scan())",
    4: "import serial\nser = serial.Serial('/dev/ttyUSB0', 9600)\nser.write(b'AT\\r\\n')\nprint(ser.readline())",
    5: "import serial\nimport pynmea2\nser = serial.Serial('/dev/ttyACM0', 9600)\nline = ser.readline()\nmsg = pynmea2.parse(line.decode())\nprint(msg.latitude, msg.longitude)",
    6: "import usb.core\ndev = usb.core.find(idVendor=0x1234)\nprint(dev)",
    7: "import RPi.GPIO as GPIO\nGPIO.setmode(GPIO.BCM)\nGPIO.setup(18, GPIO.OUT)\nGPIO.output(18, GPIO.HIGH)",
    8: "import cv2\ncap = cv2.VideoCapture(0)\nret, frame = cap.read()\ncv2.imshow('Camera', frame)\ncv2.waitKey(0)",
    9: "import pyaudio\np = pyaudio.PyAudio()\nstream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)\ndata = stream.read(1024)\nprint('Audio captured')",
    10: "import serial\nser = serial.Serial('/dev/ttyUSB0', 9600)\nser.write(b'AT+SEND=1:1234567890\\r\\n')",
    11: "import board\nimport adafruit_mpu6050\nimport busio\ni2c = busio.I2C(board.SCL, board.SDA)\nmpu = adafruit_mpu6050.MPU6050(i2c)\nprint(mpu.acceleration)",
    12: "import Adafruit_DHT\nsensor = Adafruit_DHT.DHT11\npin = 4\nhumidity, temp = Adafruit_DHT.read_retry(sensor, pin)\nprint(f'Temp: {temp}°C, Humidity: {humidity}%')",
    13: "import serial\nser = serial.Serial('/dev/ttyUSB0', 9600)\nuid = ser.readline().strip()\nprint(f'Tag UID: {uid}')",
    14: "import RPi.GPIO as GPIO\nGPIO.setmode(GPIO.BCM)\nGPIO.setup(17, GPIO.OUT)\nGPIO.output(17, True)  # Turn relay on",
    15: "from luma.core.interface.serial import i2c\nfrom luma.oled.device import ssd1306\nserial = i2c(port=1, address=0x3C)\ndevice = ssd1306(serial)\nfrom PIL import ImageDraw\ndraw = ImageDraw.Draw(device)\ndraw.rectangle((0,0,128,32), outline=1, fill=0)",
    16: "import RPi.GPIO as GPIO\nimport time\nGPIO.setmode(GPIO.BCM)\ncoil_pins = [18,23,24,25]\nfor pin in coil_pins:\n    GPIO.setup(pin, GPIO.OUT)\nsequence = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]\nwhile True:\n    for step in sequence:\n        for i, pin in enumerate(coil_pins):\n            GPIO.output(pin, step[i])\n        time.sleep(0.01)",
    17: "import RPi.GPIO as GPIO\nGPIO.setmode(GPIO.BCM)\nGPIO.setup(25, GPIO.IN)\nif GPIO.input(25):\n    print('Sound detected!')",
    18: "import spidev\nspi = spidev.SpiDev()\nspi.open(0,0)\nadc = spi.xfer2([1, (8+0)<<4, 0])\nvalue = ((adc[1]&3) << 8) + adc[2]\nprint(f'Gas sensor reading: {value}')",
    19: "import RPi.GPIO as GPIO\nimport spidev\nGPIO.setmode(GPIO.BCM)\nGPIO.setup(22, GPIO.IN)  # button\nspi = spidev.SpiDev()\nspi.open(0,0)\nx = spi.xfer2([1, (8+0)<<4, 0])\nx_val = ((x[1]&3) << 8) + x[2]\nprint(f'X axis: {x_val}, Button: {GPIO.input(22)}')",
    20: "// Arduino code\n#include <SPI.h>\n#include <Ethernet.h>\nbyte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};\nEthernetServer server(80);\nvoid setup() { Ethernet.begin(mac); server.begin(); }\nvoid loop() { EthernetClient client = server.available(); if (client) { client.println(\"HTTP/1.1 200 OK\"); client.println(); client.println(\"Hello from Arduino\"); delay(1); } }"
}

# Image URLs (free placeholder images – replace with actual hardware photos)
image_urls = {
    1: "https://images.unsplash.com/photo-1563770660941-20978e870e26?w=400&h=300&fit=crop",
    2: "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400&h=300&fit=crop",
    3: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    4: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    5: "https://images.unsplash.com/photo-1573804633927-b8a8b3d6f1c0?w=400&h=300&fit=crop",
    6: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    7: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=300&fit=crop",
    8: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    9: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=300&fit=crop",
    10: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    11: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    12: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    13: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    14: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    15: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    16: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    17: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    18: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    19: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop",
    20: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop"
}

# Practice exercises per lesson (5 exercises each, different from one another)
def get_practice(lesson_num):
    exercises = []
    for i in range(1, 6):
        desc = f"Practice {i}: Write a Python script that interacts with {hardware_list[lesson_num-1]} – for example, read data, send a command, or control an output. Use the demo code as reference."
        sol = "# Your solution here\n# Hint: Use the appropriate library and connection method.\n# Example: " + demo_codes.get(lesson_num, "print('Hello')")
        exercises.append({"desc": desc, "solution": sol})
    return exercises

def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled. Please install edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                generate_audio(text, tmp.name, VOICE)
                with open(tmp.name, "rb") as f:
                    audio_bytes = f.read()
                    b64 = base64.b64encode(audio_bytes).decode()
                    st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width: 100%;"></audio>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Audio error: {e}")
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

# ========== DISPLAY LESSON ==========
st.markdown(f"## 📖 Lesson {lesson_number}: {hardware_list[lesson_number-1]}")
exp_text = explanations[lesson_number]
demo = demo_codes.get(lesson_number, "print('Demo code not available')")
exercises = get_practice(lesson_number)

tab1, tab2, tab3 = st.tabs(["📘 Explanation & Demo", "💻 Practice Exercises", "📝 Notes"])

with tab1:
    st.markdown(exp_text)
    play_audio(exp_text, f"exp_{lesson_number}")
    st.markdown("---")
    st.subheader("🖼️ Hardware Example")
    # Image placeholder (replace with actual image URL)
    img_url = image_urls.get(lesson_number, "https://via.placeholder.com/400x300?text=Hardware+Image")
    st.image(img_url, caption=f"{hardware_list[lesson_number-1]} (example image)", use_container_width=True)
    st.markdown("---")
    st.subheader("🎬 Demo Code")
    st.code(demo, language="python")
    play_audio(demo, f"demo_audio_{lesson_number}")
    st.info("Copy this code and run it on your hardware (Raspberry Pi, Arduino, or PC with connected device). Modify to experiment.")

with tab2:
    st.markdown("### 🧠 Practice Exercises")
    st.caption("Complete these exercises to master the hardware interface. Write your code and test it with real hardware.")
    for i, ex in enumerate(exercises, 1):
        st.markdown(f"**Exercise {i}:** {ex['desc']}")
        play_audio(ex['desc'], f"ex_desc_{lesson_number}_{i}")
        if st.button(f"Show Solution {i}", key=f"sol_{lesson_number}_{i}"):
            st.code(ex['solution'], language="python")
        st.markdown("---")

with tab3:
    notes = f"""
    **Lesson focus:** {hardware_list[lesson_number-1]}  
    **Key concepts:** Communication protocols (UART, I2C, SPI, GPIO, Wi-Fi, Bluetooth, etc.)  
    **Next steps:** Connect the actual hardware, run the demo code, then modify it to add new features.  
    **Remember:** Always check voltage levels and use proper wiring to avoid damaging components.
    """
    st.markdown("### 📝 Study Notes")
    st.markdown(notes)
    play_audio(notes, f"notes_audio_{lesson_number}")

if lesson_number == 20:
    st.markdown("---")
    st.markdown("## 🎓 Congratulations! You have completed the Software & Hardware Course.")
    st.markdown("""
    ### 📞 To continue with advanced projects or get support:
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    You now know how to connect software with 20 different hardware components. Build your own IoT, robotics, or automation projects!
    """)
