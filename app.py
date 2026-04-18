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

# Voices per language
VOICES = {
    "en": "en-US-JennyNeural",
    "es": "es-ES-ElviraNeural",
    "fr": "fr-FR-DeniseNeural",
    "zh": "zh-CN-XiaoxiaoNeural",
    "pt": "pt-BR-FranciscaNeural"
}

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

# ========== LANGUAGE SELECTION ==========
lang = st.sidebar.selectbox(
    "🌐 Language",
    options=["en", "es", "fr", "zh", "pt"],
    format_func=lambda x: {"en": "English", "es": "Español", "fr": "Français", "zh": "中文", "pt": "Português"}[x]
)

# ========== UI TEXT TRANSLATIONS ==========
ui = {
    "en": {
        "select_lesson": "🎯 Select a lesson", "progress": "📚 Your progress", "completed": "of 20 completed",
        "founder": "Founder & Developer:", "price": "💰 Price", "price_value": "**$299 USD** (full book – 20 lessons, source code, certificate)",
        "logout": "🚪 Logout", "lesson": "📖 Lesson", "tab1": "📘 Explanation & Demo", "tab2": "💻 Practice Exercises",
        "tab3": "📝 Notes", "demo_code": "🎬 Demo Code", "hardware_img": "🖼️ Hardware Example",
        "info_text": "Copy this code and run it on your hardware (Raspberry Pi, Arduino, or PC with connected device). Modify to experiment.",
        "practice_title": "🧠 Practice Exercises", "practice_caption": "Complete these exercises to master the hardware interface. Write your code and test it with real hardware.",
        "show_solution": "Show Solution", "notes_title": "📝 Study Notes", "notes_focus": "Lesson focus",
        "notes_concepts": "Key concepts", "notes_next": "Next steps", "notes_remember": "Remember",
        "congrats": "🎓 Congratulations! You have completed the Software & Hardware Course.",
        "contact": "To continue with advanced projects or get support:",
        "footer": "You now know how to connect software with 20 different hardware components. Build your own IoT, robotics, or automation projects!"
    },
    "es": {
        "select_lesson": "🎯 Seleccione una lección", "progress": "📚 Su progreso", "completed": "de 20 completadas",
        "founder": "Fundador y desarrollador:", "price": "💰 Precio", "price_value": "**$299 USD** (libro completo – 20 lecciones, código fuente, certificado)",
        "logout": "🚪 Cerrar sesión", "lesson": "📖 Lección", "tab1": "📘 Explicación y demo", "tab2": "💻 Ejercicios prácticos",
        "tab3": "📝 Notas", "demo_code": "🎬 Código de demostración", "hardware_img": "🖼️ Ejemplo de hardware",
        "info_text": "Copie este código y ejecútelo en su hardware (Raspberry Pi, Arduino o PC con dispositivo conectado). Modifíquelo para experimentar.",
        "practice_title": "🧠 Ejercicios prácticos", "practice_caption": "Complete estos ejercicios para dominar la interfaz de hardware. Escriba su código y pruébelo con hardware real.",
        "show_solution": "Mostrar solución", "notes_title": "📝 Notas de estudio", "notes_focus": "Enfoque de la lección",
        "notes_concepts": "Conceptos clave", "notes_next": "Próximos pasos", "notes_remember": "Recuerde",
        "congrats": "🎓 ¡Felicitaciones! Ha completado el curso de Software y Hardware.",
        "contact": "Para continuar con proyectos avanzados o recibir soporte:",
        "footer": "Ahora sabe cómo conectar software con 20 componentes de hardware diferentes. ¡Construya sus propios proyectos de IoT, robótica o automatización!"
    },
    "fr": {
        "select_lesson": "🎯 Choisissez une leçon", "progress": "📚 Votre progression", "completed": "sur 20 terminées",
        "founder": "Fondateur et développeur :", "price": "💰 Prix", "price_value": "**299 $ USD** (livre complet – 20 leçons, code source, certificat)",
        "logout": "🚪 Déconnexion", "lesson": "📖 Leçon", "tab1": "📘 Explication et démo", "tab2": "💻 Exercices pratiques",
        "tab3": "📝 Notes", "demo_code": "🎬 Code de démonstration", "hardware_img": "🖼️ Exemple de matériel",
        "info_text": "Copiez ce code et exécutez‑le sur votre matériel (Raspberry Pi, Arduino ou PC avec périphérique connecté). Modifiez‑le pour expérimenter.",
        "practice_title": "🧠 Exercices pratiques", "practice_caption": "Complétez ces exercices pour maîtriser l'interface matérielle. Écrivez votre code et testez‑le avec du vrai matériel.",
        "show_solution": "Voir la solution", "notes_title": "📝 Notes d'étude", "notes_focus": "Thème de la leçon",
        "notes_concepts": "Concepts clés", "notes_next": "Prochaines étapes", "notes_remember": "Rappelez‑vous",
        "congrats": "🎓 Félicitations ! Vous avez terminé le cours sur le logiciel et le matériel.",
        "contact": "Pour continuer avec des projets avancés ou obtenir du soutien :",
        "footer": "Vous savez maintenant comment connecter des logiciels avec 20 composants matériels différents. Construisez vos propres projets IoT, robotique ou automatisation !"
    },
    "zh": {
        "select_lesson": "🎯 选择课程", "progress": "📚 您的进度", "completed": "/20 完成",
        "founder": "创始人兼开发者：", "price": "💰 价格", "price_value": "**299 美元**（完整教材 – 20 课，源代码，证书）",
        "logout": "🚪 退出", "lesson": "📖 课程", "tab1": "📘 讲解与演示", "tab2": "💻 编程练习",
        "tab3": "📝 笔记", "demo_code": "🎬 演示代码", "hardware_img": "🖼️ 硬件示例",
        "info_text": "复制此代码并在您的硬件（Raspberry Pi、Arduino 或连接了设备的 PC）上运行。修改代码进行实验。",
        "practice_title": "🧠 编程练习", "practice_caption": "完成这些练习以掌握硬件接口。编写代码并在真实硬件上测试。",
        "show_solution": "显示答案", "notes_title": "📝 学习笔记", "notes_focus": "课程重点",
        "notes_concepts": "关键概念", "notes_next": "下一步", "notes_remember": "请记住",
        "congrats": "🎓 恭喜您完成了软件与硬件课程！",
        "contact": "要继续学习高级项目或获得支持：",
        "footer": "您现在知道如何将软件与 20 种不同的硬件组件连接。构建您自己的物联网、机器人或自动化项目！"
    },
    "pt": {
        "select_lesson": "🎯 Selecione uma lição", "progress": "📚 Seu progresso", "completed": "de 20 concluídas",
        "founder": "Fundador e desenvolvedor:", "price": "💰 Preço", "price_value": "**$299 USD** (livro completo – 20 lições, código fonte, certificado)",
        "logout": "🚪 Sair", "lesson": "📖 Lição", "tab1": "📘 Explicação e demonstração", "tab2": "💻 Exercícios práticos",
        "tab3": "📝 Anotações", "demo_code": "🎬 Código de demonstração", "hardware_img": "🖼️ Exemplo de hardware",
        "info_text": "Copie este código e execute no seu hardware (Raspberry Pi, Arduino ou PC com dispositivo conectado). Modifique para experimentar.",
        "practice_title": "🧠 Exercícios práticos", "practice_caption": "Complete estes exercícios para dominar a interface de hardware. Escreva seu código e teste com hardware real.",
        "show_solution": "Mostrar solução", "notes_title": "📝 Notas de estudo", "notes_focus": "Foco da lição",
        "notes_concepts": "Conceitos principais", "notes_next": "Próximos passos", "notes_remember": "Lembre-se",
        "congrats": "🎓 Parabéns! Você concluiu o curso de Software e Hardware.",
        "contact": "Para continuar com projetos avançados ou obter suporte:",
        "footer": "Agora você sabe como conectar software com 20 componentes de hardware diferentes. Construa seus próprios projetos de IoT, robótica ou automação!"
    }
}

# ========== HARDWARE LISTS (translated) ==========
hardware_lists = {
    "en": [
        "Network Interface Card (NIC)", "Wi‑Fi Adapter", "Bluetooth Module", "Cellular Modem (4G/5G)", "GPS Receiver",
        "USB Controller / Port", "GPIO Pins", "Camera Module", "Microphone & Speaker", "LoRa / Sigfox Module",
        "Accelerometer / Gyroscope", "Temperature & Humidity Sensor", "RFID / NFC Reader", "Relay Module",
        "OLED / LCD Display", "Stepper Motor Driver", "Sound Sensor", "Gas / Smoke Sensor", "Joystick Module",
        "Ethernet Shield (for Arduino)"
    ],
    "es": [
        "Tarjeta de interfaz de red (NIC)", "Adaptador Wi‑Fi", "Módulo Bluetooth", "Módem celular (4G/5G)", "Receptor GPS",
        "Controlador / Puerto USB", "Pines GPIO", "Módulo de cámara", "Micrófono y altavoz", "Módulo LoRa / Sigfox",
        "Acelerómetro / Giroscopio", "Sensor de temperatura y humedad", "Lector RFID / NFC", "Módulo relé",
        "Pantalla OLED / LCD", "Controlador de motor paso a paso", "Sensor de sonido", "Sensor de gas / humo",
        "Módulo joystick", "Escudo Ethernet (para Arduino)"
    ],
    "fr": [
        "Carte d'interface réseau (NIC)", "Adaptateur Wi‑Fi", "Module Bluetooth", "Modem cellulaire (4G/5G)", "Récepteur GPS",
        "Contrôleur / port USB", "Broches GPIO", "Module caméra", "Microphone et haut‑parleur", "Module LoRa / Sigfox",
        "Accéléromètre / Gyroscope", "Capteur de température et d'humidité", "Lecteur RFID / NFC", "Module relais",
        "Écran OLED / LCD", "Pilote de moteur pas à pas", "Capteur sonore", "Capteur de gaz / fumée",
        "Module joystick", "Blindage Ethernet (pour Arduino)"
    ],
    "zh": [
        "网络接口卡 (NIC)", "Wi‑Fi 适配器", "蓝牙模块", "蜂窝调制解调器 (4G/5G)", "GPS 接收器",
        "USB 控制器 / 端口", "GPIO 引脚", "摄像头模块", "麦克风和扬声器", "LoRa / Sigfox 模块",
        "加速度计 / 陀螺仪", "温湿度传感器", "RFID / NFC 读卡器", "继电器模块",
        "OLED / LCD 显示屏", "步进电机驱动器", "声音传感器", "气体 / 烟雾传感器", "摇杆模块",
        "以太网扩展板 (适用于 Arduino)"
    ],
    "pt": [
        "Placa de interface de rede (NIC)", "Adaptador Wi‑Fi", "Módulo Bluetooth", "Modem celular (4G/5G)", "Receptor GPS",
        "Controlador / Porta USB", "Pinos GPIO", "Módulo de câmera", "Microfone e alto‑falante", "Módulo LoRa / Sigfox",
        "Acelerômetro / Giroscópio", "Sensor de temperatura e umidade", "Leitor RFID / NFC", "Módulo relé",
        "Display OLED / LCD", "Driver de motor de passo", "Sensor de som", "Sensor de gás / fumaça", "Módulo joystick",
        "Escudo Ethernet (para Arduino)"
    ]
}

# ========== FULL EXPLANATIONS FOR ALL 5 LANGUAGES (20 lessons each) ==========
explanations = {
    "en": {
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
    },
    "es": {
        1: "**Tarjeta de interfaz de red (NIC)**\nUna NIC permite que su computadora se conecte a una red Ethernet cableada. El software puede enviar y recibir paquetes de datos mediante sockets (TCP/IP). Ejemplo: la biblioteca `socket` de Python.",
        2: "**Adaptador Wi‑Fi**\nPermite la comunicación inalámbrica. El software puede escanear redes, conectarse e intercambiar datos. Use `subprocess` para ejecutar comandos del sistema o bibliotecas como `wifi`.",
        3: "**Módulo Bluetooth**\nSe conecta a dispositivos cercanos (teclados, sensores IoT). Use PyBluez o Bleak en Python para descubrir y comunicarse con dispositivos Bluetooth.",
        4: "**Módem celular (4G/5G)**\nProporciona Internet a través de redes móviles. El software puede usar comandos AT por serial para enviar SMS, hacer llamadas o establecer conexiones de datos.",
        5: "**Receptor GPS**\nRecibe ubicación de satélites. El software lee oraciones NMEA por puerto serie para obtener latitud, longitud, altitud. `pynmea2` de Python analiza datos GPS.",
        6: "**Controlador / Puerto USB**\nInterfaz universal para periféricos. El software puede detectar dispositivos USB con `pyusb` o leer/escribir en dispositivos USB serie (CDC ACM).",
        7: "**Pines GPIO**\nEn Raspberry Pi o Arduino, los pines GPIO leen sensores y controlan LEDs, motores. Bibliotecas `RPi.GPIO` o `gpiozero` de Python.",
        8: "**Módulo de cámara**\nCaptura imágenes/video. Use OpenCV (`cv2`) para acceder al flujo de la cámara, procesar cuadros y ejecutar algoritmos de visión artificial.",
        9: "**Micrófono y altavoz**\nEntrada/salida de audio. Use `pyaudio` o `sounddevice` para grabar desde el micrófono y reproducir sonido. Reconocimiento de voz con `speech_recognition`.",
        10: "**Módulo LoRa / Sigfox**\nRadio de baja potencia y largo alcance para IoT. Comuníquese mediante comandos AT por serie. Úselo para agricultura, seguimiento de activos, ciudades inteligentes.",
        11: "**Acelerómetro / Giroscopio**\nMide aceleración y rotación. Conéctese vía I2C (ej. MPU6050). Bibliotecas `smbus` o `adafruit-circuitpython` de Python.",
        12: "**Sensor de temperatura y humedad**\nSensores DHT11/DHT22. Lea mediante protocolo de un solo cable. Biblioteca `Adafruit_DHT` de Python.",
        13: "**Lector RFID / NFC**\nLee etiquetas RFID. Conéctese por serie o I2C. Use `pyserial` para leer el UID e interactuar con sistemas de control de acceso.",
        14: "**Módulo relé**\nConmuta dispositivos de alta potencia desde GPIO de baja potencia. Controle con `GPIO.output(pin, True/False)`. Se usa en domótica.",
        15: "**Pantalla OLED / LCD**\nMuestra texto y gráficos. Interfaz I2C o SPI. Use las bibliotecas `luma.oled` o `RPLCD`.",
        16: "**Controlador de motor paso a paso**\nControla rotación precisa. Use pulsos GPIO con `RPi.GPIO` o la biblioteca `AccelStepper`.",
        17: "**Sensor de sonido**\nDetecta intensidad de sonido. Sensor analógico leído mediante ADC (MCP3008) o salida digital por umbral.",
        18: "**Sensor de gas / humo**\nDetecta gases (serie MQ). Lea voltaje analógico para estimar concentración.",
        19: "**Módulo joystick**\nDos ejes analógicos y un botón. Lea con ADC y GPIO. Usado en robótica y controladores de juegos.",
        20: "**Escudo Ethernet**\nAgrega Ethernet cableada a Arduino. Use la biblioteca Ethernet de Arduino para comunicación TCP/IP."
    },
    "fr": {
        1: "**Carte d'interface réseau (NIC)**\nUne NIC permet à votre ordinateur de se connecter à un réseau Ethernet filaire. Le logiciel peut envoyer et recevoir des paquets de données via des sockets (TCP/IP). Exemple : la bibliothèque `socket` de Python.",
        2: "**Adaptateur Wi‑Fi**\nPermet la communication réseau sans fil. Le logiciel peut scanner les réseaux, se connecter et échanger des données. Utilisez `subprocess` pour exécuter des commandes système ou des bibliothèques comme `wifi`.",
        3: "**Module Bluetooth**\nSe connecte aux appareils proches (claviers, capteurs IoT). Utilisez PyBluez ou Bleak en Python pour découvrir et communiquer avec des appareils Bluetooth.",
        4: "**Modem cellulaire (4G/5G)**\nFournit Internet via les réseaux mobiles. Le logiciel peut utiliser des commandes AT en série pour envoyer des SMS, passer des appels ou établir des connexions de données.",
        5: "**Récepteur GPS**\nReçoit la position des satellites. Le logiciel lit les phrases NMEA via le port série pour obtenir la latitude, longitude, altitude. `pynmea2` de Python analyse les données GPS.",
        6: "**Contrôleur / port USB**\nInterface universelle pour périphériques. Le logiciel peut détecter des périphériques USB avec `pyusb` ou lire/écrire sur des périphériques USB série (CDC ACM).",
        7: "**Broches GPIO**\nSur Raspberry Pi ou Arduino, les broches GPIO lisent les capteurs et contrôlent les LEDs, moteurs. Bibliothèques `RPi.GPIO` ou `gpiozero` de Python.",
        8: "**Module caméra**\nCapture des images/vidéos. Utilisez OpenCV (`cv2`) pour accéder au flux de la caméra, traiter les images et exécuter des algorithmes de vision par ordinateur.",
        9: "**Microphone et haut‑parleur**\nEntrée/sortie audio. Utilisez `pyaudio` ou `sounddevice` pour enregistrer depuis le micro et lire du son. Reconnaissance vocale avec `speech_recognition`.",
        10: "**Module LoRa / Sigfox**\nRadio basse consommation et longue portée pour l'IoT. Communiquez via des commandes AT en série. Utilisez‑le pour l'agriculture, le suivi d'actifs, les villes intelligentes.",
        11: "**Accéléromètre / Gyroscope**\nMesure l'accélération et la rotation. Connectez‑vous via I2C (ex. MPU6050). Bibliothèques `smbus` ou `adafruit-circuitpython` de Python.",
        12: "**Capteur de température et d'humidité**\nCapteurs DHT11/DHT22. Lisez via le protocole à un fil. Bibliothèque `Adafruit_DHT` de Python.",
        13: "**Lecteur RFID / NFC**\nLit les étiquettes RFID. Connectez‑vous par série ou I2C. Utilisez `pyserial` pour lire l'UID et interagir avec les systèmes de contrôle d'accès.",
        14: "**Module relais**\nCommute des appareils haute puissance depuis des GPIO basse puissance. Contrôlez avec `GPIO.output(pin, True/False)`. Utilisé pour la domotique.",
        15: "**Écran OLED / LCD**\nAffiche du texte et des graphiques. Interface I2C ou SPI. Utilisez les bibliothèques `luma.oled` ou `RPLCD`.",
        16: "**Pilote de moteur pas à pas**\nContrôle une rotation précise. Utilisez des impulsions GPIO avec `RPi.GPIO` ou la bibliothèque `AccelStepper`.",
        17: "**Capteur sonore**\nDétecte l'intensité sonore. Capteur analogique lu via ADC (MCP3008) ou sortie numérique sur seuil.",
        18: "**Capteur de gaz / fumée**\nDétecte les gaz (série MQ). Lisez la tension analogique pour estimer la concentration.",
        19: "**Module joystick**\nDeux axes analogiques et un bouton. Lisez avec ADC et GPIO. Utilisé en robotique et pour les manettes de jeux.",
        20: "**Blindage Ethernet**\nAjoute Ethernet filaire à Arduino. Utilisez la bibliothèque Ethernet d'Arduino pour la communication TCP/IP."
    },
    "zh": {
        1: "**网络接口卡 (NIC)**\nNIC 允许您的计算机连接到有线以太网。软件可以使用套接字 (TCP/IP) 发送和接收数据包。示例：Python 的 `socket` 库。",
        2: "**Wi‑Fi 适配器**\n实现无线网络通信。软件可以扫描网络、连接并交换数据。使用 `subprocess` 运行系统命令或使用 `wifi` 等库。",
        3: "**蓝牙模块**\n连接到附近的设备（键盘、物联网传感器）。使用 Python 的 PyBluez 或 Bleak 库发现蓝牙设备并进行通信。",
        4: "**蜂窝调制解调器 (4G/5G)**\n通过移动网络提供互联网。软件可以通过串口使用 AT 命令发送短信、拨打电话或建立数据连接。",
        5: "**GPS 接收器**\n从卫星接收位置。软件通过串口读取 NMEA 语句以获取纬度、经度、海拔。Python 的 `pynmea2` 解析 GPS 数据。",
        6: "**USB 控制器 / 端口**\n通用外设接口。软件可以使用 `pyusb` 检测 USB 设备，或对串行 USB 设备 (CDC ACM) 进行读写。",
        7: "**GPIO 引脚**\n在 Raspberry Pi 或 Arduino 上，GPIO 引脚读取传感器并控制 LED、电机。使用 Python 的 `RPi.GPIO` 或 `gpiozero` 库。",
        8: "**摄像头模块**\n捕获图像/视频。使用 OpenCV (`cv2`) 访问摄像头流、处理帧并运行计算机视觉算法。",
        9: "**麦克风和扬声器**\n音频输入/输出。使用 `pyaudio` 或 `sounddevice` 从麦克风录音和播放声音。使用 `speech_recognition` 进行语音识别。",
        10: "**LoRa / Sigfox 模块**\n用于物联网的低功耗长距离无线电。通过串口 AT 命令进行通信。用于农业、资产跟踪、智慧城市。",
        11: "**加速度计 / 陀螺仪**\n测量加速度和旋转。通过 I2C 连接（例如 MPU6050）。使用 Python 的 `smbus` 或 `adafruit-circuitpython` 库。",
        12: "**温湿度传感器**\nDHT11/DHT22 传感器。通过单线协议读取。使用 Python 的 `Adafruit_DHT` 库。",
        13: "**RFID / NFC 读卡器**\n读取 RFID 标签。通过串口或 I2C 连接。使用 `pyserial` 读取 UID 并与门禁系统交互。",
        14: "**继电器模块**\n通过低功耗 GPIO 切换高功率设备。使用 `GPIO.output(pin, True/False)` 控制。用于家庭自动化。",
        15: "**OLED / LCD 显示屏**\n显示文本和图形。I2C 或 SPI 接口。使用 `luma.oled` 或 `RPLCD` 库。",
        16: "**步进电机驱动器**\n控制精确旋转。使用 GPIO 脉冲配合 `RPi.GPIO` 或 `AccelStepper` 库。",
        17: "**声音传感器**\n检测声音强度。通过 ADC (MCP3008) 读取模拟传感器，或通过阈值数字输出。",
        18: "**气体 / 烟雾传感器**\n检测气体（MQ 系列）。读取模拟电压以估算浓度。",
        19: "**摇杆模块**\n两个模拟轴和一个按钮。使用 ADC 和 GPIO 读取。用于机器人和游戏控制器。",
        20: "**以太网扩展板**\n为 Arduino 添加有线以太网。使用 Arduino 的 Ethernet 库进行 TCP/IP 通信。"
    },
    "pt": {
        1: "**Placa de interface de rede (NIC)**\nUma NIC permite que seu computador se conecte a uma rede Ethernet com fio. O software pode enviar e receber pacotes de dados usando soquetes (TCP/IP). Exemplo: biblioteca `socket` do Python.",
        2: "**Adaptador Wi‑Fi**\nPermite comunicação sem fio. O software pode escanear redes, conectar e trocar dados. Use `subprocess` para executar comandos do sistema ou bibliotecas como `wifi`.",
        3: "**Módulo Bluetooth**\nConecta-se a dispositivos próximos (teclados, sensores IoT). Use as bibliotecas PyBluez ou Bleak em Python para descobrir e se comunicar com dispositivos Bluetooth.",
        4: "**Modem celular (4G/5G)**\nFornece internet via redes móveis. O software pode usar comandos AT via serial para enviar SMS, fazer chamadas ou estabelecer conexões de dados.",
        5: "**Receptor GPS**\nRecebe localização de satélites. O software lê frases NMEA pela porta serial para obter latitude, longitude, altitude. O `pynmea2` do Python analisa dados GPS.",
        6: "**Controlador / Porta USB**\nInterface universal para periféricos. O software pode detectar dispositivos USB com `pyusb` ou ler/escrever em dispositivos USB seriais (CDC ACM).",
        7: "**Pinos GPIO**\nNo Raspberry Pi ou Arduino, os pinos GPIO leem sensores e controlam LEDs, motores. Bibliotecas `RPi.GPIO` ou `gpiozero` do Python.",
        8: "**Módulo de câmera**\nCaptura imagens/vídeo. Use OpenCV (`cv2`) para acessar o fluxo da câmera, processar quadros e executar algoritmos de visão computacional.",
        9: "**Microfone e alto‑falante**\nEntrada/saída de áudio. Use `pyaudio` ou `sounddevice` para gravar do microfone e reproduzir som. Reconhecimento de fala com `speech_recognition`.",
        10: "**Módulo LoRa / Sigfox**\nRádio de baixa potência e longo alcance para IoT. Comunique-se via comandos AT seriais. Use para agricultura, rastreamento de ativos, cidades inteligentes.",
        11: "**Acelerômetro / Giroscópio**\nMede aceleração e rotação. Conecte via I2C (ex. MPU6050). Bibliotecas `smbus` ou `adafruit-circuitpython` do Python.",
        12: "**Sensor de temperatura e umidade**\nSensores DHT11/DHT22. Leia via protocolo de um fio. Biblioteca `Adafruit_DHT` do Python.",
        13: "**Leitor RFID / NFC**\nLê etiquetas RFID. Conecte via serial ou I2C. Use `pyserial` para ler o UID e interagir com sistemas de controle de acesso.",
        14: "**Módulo relé**\nComuta dispositivos de alta potência a partir de GPIO de baixa potência. Controle com `GPIO.output(pin, True/False)`. Usado em automação residencial.",
        15: "**Display OLED / LCD**\nExibe texto e gráficos. Interface I2C ou SPI. Use as bibliotecas `luma.oled` ou `RPLCD`.",
        16: "**Driver de motor de passo**\nControla rotação precisa. Use pulsos GPIO com `RPi.GPIO` ou a biblioteca `AccelStepper`.",
        17: "**Sensor de som**\nDetecta intensidade sonora. Sensor analógico lido via ADC (MCP3008) ou saída digital por limiar.",
        18: "**Sensor de gás / fumaça**\nDetecta gases (série MQ). Leia a tensão analógica para estimar a concentração.",
        19: "**Módulo joystick**\nDois eixos analógicos e um botão. Leia com ADC e GPIO. Usado em robótica e controles de jogos.",
        20: "**Escudo Ethernet**\nAdiciona Ethernet com fio ao Arduino. Use a biblioteca Ethernet do Arduino para comunicação TCP/IP."
    }
}

# ========== DEMO CODES (same for all languages) ==========
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

# ========== IMAGE URLS (replace with real hardware images) ==========
image_urls = {i: f"https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=300&fit=crop" for i in range(1, 21)}

# ========== PRACTICE EXERCISES (translated) ==========
def get_practice(lang, lesson_num):
    hw = hardware_lists[lang][lesson_num-1]
    base_texts = {
        "en": f"Write a Python script that reads data from or controls the {hw}. Use the demo code as a starting point. Modify it to add new features (e.g., logging, alerts, or a simple GUI).",
        "es": f"Escriba un script de Python que lea datos o controle el {hw}. Use el código de demostración como punto de partida. Modifíquelo para agregar nuevas funciones (por ejemplo, registro, alertas o una interfaz gráfica simple).",
        "fr": f"Écrivez un script Python qui lit des données ou contrôle le {hw}. Utilisez le code de démonstration comme point de départ. Modifiez‑le pour ajouter de nouvelles fonctionnalités (ex. journalisation, alertes, interface graphique simple).",
        "zh": f"编写一个 Python 脚本，从 {hw} 读取数据或控制它。以演示代码为起点。修改它以添加新功能（例如日志记录、警报或简单的图形界面）。",
        "pt": f"Escreva um script Python que leia dados ou controle o {hw}. Use o código de demonstração como ponto de partida. Modifique‑o para adicionar novos recursos (ex. registro, alertas ou uma interface gráfica simples)."
    }
    desc = base_texts.get(lang, base_texts["en"])
    exercises = []
    for i in range(1, 6):
        exercises.append({"desc": f"{desc} (Exercise {i})", "solution": "# Your solution here\n# Hint: Extend the demo code with your own logic.\npass"})
    return exercises

# ========== SIDEBAR ==========
with st.sidebar:
    show_logo()
    st.markdown(f"## {ui[lang]['select_lesson']}")
    lesson_number = st.selectbox("", list(range(1, 21)), index=0, label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f"### {ui[lang]['progress']}")
    st.progress(lesson_number / 20)
    st.markdown(f"✅ {ui[lang]['lesson']} {lesson_number} {ui[lang]['completed']}")
    st.markdown("---")
    st.markdown(f"**{ui[lang]['founder']}**")
    st.markdown("Gesner Deslandes")
    st.markdown("📞 WhatsApp: (509) 4738-5663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.markdown(f"### {ui[lang]['price']}")
    st.markdown(ui[lang]['price_value'])
    st.markdown("---")
    st.markdown("### © 2025 GlobalInternet.py")
    st.markdown("All rights reserved")
    st.markdown("---")
    if st.button(ui[lang]['logout'], use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ========== AUDIO FUNCTION ==========
def play_audio(text, key):
    if not EDGE_TTS_AVAILABLE:
        st.info("🔇 Audio disabled. Please install edge-tts.")
        return
    if st.button(f"🔊", key=key):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            try:
                generate_audio(text, tmp.name, VOICES[lang])
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
hw_name = hardware_lists[lang][lesson_number-1]
exp_text = explanations[lang][lesson_number]
demo = demo_codes[lesson_number]
exercises = get_practice(lang, lesson_number)

st.markdown(f"## {ui[lang]['lesson']} {lesson_number}: {hw_name}")

tab1, tab2, tab3 = st.tabs([ui[lang]['tab1'], ui[lang]['tab2'], ui[lang]['tab3']])

with tab1:
    st.markdown(exp_text)
    play_audio(exp_text, f"exp_{lesson_number}")
    st.markdown("---")
    st.subheader(ui[lang]['hardware_img'])
    img_url = image_urls.get(lesson_number, "https://via.placeholder.com/400x300?text=Hardware+Image")
    st.image(img_url, caption=f"{hw_name} (example image)", use_container_width=True)
    st.markdown("---")
    st.subheader(ui[lang]['demo_code'])
    st.code(demo, language="python")
    play_audio(demo, f"demo_audio_{lesson_number}")
    st.info(ui[lang]['info_text'])

with tab2:
    st.markdown(f"### {ui[lang]['practice_title']}")
    st.caption(ui[lang]['practice_caption'])
    for i, ex in enumerate(exercises, 1):
        st.markdown(f"**Exercise {i}:** {ex['desc']}")
        play_audio(ex['desc'], f"ex_desc_{lesson_number}_{i}")
        if st.button(f"{ui[lang]['show_solution']} {i}", key=f"sol_{lesson_number}_{i}"):
            st.code(ex['solution'], language="python")
        st.markdown("---")

with tab3:
    notes_text = f"{ui[lang]['notes_focus']}: {hw_name}\n\n{ui[lang]['notes_concepts']}: Communication protocols (UART, I2C, SPI, GPIO, etc.)\n\n{ui[lang]['notes_next']}: {ui[lang]['info_text']}\n\n{ui[lang]['notes_remember']}: Always check voltage levels and use proper wiring."
    st.markdown(f"### {ui[lang]['notes_title']}")
    st.markdown(notes_text)
    play_audio(notes_text, f"notes_audio_{lesson_number}")

if lesson_number == 20:
    st.markdown("---")
    st.markdown(f"## {ui[lang]['congrats']}")
    st.markdown(f"""
    ### 📞 {ui[lang]['contact']}
    - **Gesner Deslandes** – Founder
    - 📱 WhatsApp: (509) 4738-5663
    - 📧 Email: deslandes78@gmail.com
    - 🌐 [Main website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)
    
    {ui[lang]['footer']}
    """)
