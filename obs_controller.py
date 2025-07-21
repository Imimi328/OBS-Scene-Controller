import sys
import os
import json
import threading
import time
import subprocess
import re
import keyboard
import pyperclip
from flask import Flask, render_template_string, redirect, jsonify
from obswebsocket import obsws, requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QInputDialog, QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QPalette, QColor, QFont, QIcon

SAVE_FILE = "controller_scenes.json"
TEMPORARY_FILE = "temporary_scenes.json"
PASSWORD_FILE = "saved_password.json"
OBS_PORT = 4455
scene_data = []
temporary_scenes = []
ws = None
active_scene = ""
cloudflare_url = "Starting Cloudflare Tunnel..."

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>OBS Controller</title>
  <style>
    body { background: #111; color: #00FF9C; font-family: Consolas, monospace; padding: 20px; }
    .scene { display: inline-block; margin: 20px; text-align: center; }
    img { width: 320px; height: 180px; border: 2px solid #00FF9C; margin-bottom: 10px; }
    .active-scene img { border: 3px solid red; }
    button { background: #1e1e1e; color: #00FF9C; border: 1px solid #00FF9C; padding: 10px 20px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>OBS Scene Control</h1>
  <p>Software made by Ritesh. All rights reserved to Team Emogi.</p>

  <h2>Normal Scenes</h2>
  <div id="normal-scenes">Loading normal scenes...</div>

  <h2>Temporary Scenes</h2>
  <div id="temporary-scenes">Loading temporary scenes...</div>

  <script>
    async function fetchScenes() {
        try {
            const response = await fetch('/api/scenes');
            const data = await response.json();
            const normalContainer = document.getElementById('normal-scenes');
            const tempContainer = document.getElementById('temporary-scenes');

            normalContainer.innerHTML = '';
            tempContainer.innerHTML = '';

            data.scenes.forEach(scene => {
                const div = document.createElement('div');
                div.className = 'scene';
                if (scene.scene === data.active_scene) {
                    div.classList.add('active-scene');
                }

                div.innerHTML = `
                    <img src="${scene.tunnel_url}" onerror="this.src='https://via.placeholder.com/320x180?text=No+Image';"><br>
                    <strong>${scene.scene}</strong><br>
                    <a href="/switch/${scene.scene}"><button>Switch</button></a>
                `;

                normalContainer.appendChild(div);
            });

            data.temporary.forEach(scene => {
                const div = document.createElement('div');
                div.className = 'scene';

                div.innerHTML = `
                    <img src="${scene.thumbnail}" onerror="this.src='https://via.placeholder.com/320x180?text=No+Image';"><br>
                    <strong>${scene.scene}</strong><br>
                    <a href="/trigger_temp/${scene.scene}"><button>Trigger Temporary</button></a>
                `;

                tempContainer.appendChild(div);
            });
        } catch (err) {
            console.error('Error fetching scenes:', err);
        }
    }

    setInterval(fetchScenes, 1000);
    fetchScenes();
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/switch/<scene>')
def switch_scene_route(scene):
    switch_scene(scene)
    return redirect('/')

@app.route('/trigger_temp/<scene>')
def trigger_temp_scene_route(scene):
    threading.Thread(target=trigger_temporary_scene_by_name, args=(scene,), daemon=True).start()
    return redirect('/')

@app.route('/api/scenes')
def api_scenes():
    return jsonify({
        "scenes": scene_data,
        "temporary": temporary_scenes,
        "active_scene": active_scene
    })

def switch_scene(scene_name):
    global active_scene
    try:
        ws.call(requests.SetCurrentProgramScene(sceneName=scene_name))
    except:
        try:
            ws.call(requests.SetCurrentScene(sceneName=scene_name))
        except Exception as e:
            print("[ERROR]", e)
    active_scene = scene_name

def trigger_temporary_scene_by_name(scene_name):
    for scene in temporary_scenes:
        if scene['scene'] == scene_name:
            trigger_temporary_scene(scene)
            return

def trigger_temporary_scene(scene):
    previous_scene = active_scene
    switch_scene(scene['scene'])
    time.sleep(float(scene['duration']))
    switch_scene(previous_scene)

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def start_cloudflare_tunnel():
    global cloudflare_url
    process = subprocess.Popen(
        ['cloudflared', 'tunnel', '--url', 'http://localhost:5000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    start_time = time.time()
    timeout = 30

    for line in process.stdout:
        print("[CLOUDFLARE]", line.strip())
        match = re.search(r'(https://[a-zA-Z0-9.-]+\.trycloudflare\.com)', line)
        if match:
            cloudflare_url = match.group(1)
            pyperclip.copy(cloudflare_url)
            print(f"[TUNNEL] {cloudflare_url} (Copied to clipboard)")
            break
        if time.time() - start_time > timeout:
            cloudflare_url = "Failed to start Cloudflare Tunnel."
            print("[TUNNEL ERROR] Timeout exceeded.")
            break

def hotkey_worker():
    while True:
        for entry in scene_data:
            if keyboard.is_pressed(entry['hotkey']):
                switch_scene(entry['scene'])
                while keyboard.is_pressed(entry['hotkey']):
                    pass
        for entry in temporary_scenes:
            if keyboard.is_pressed(entry['hotkey']):
                threading.Thread(target=trigger_temporary_scene, args=(entry,), daemon=True).start()
                while keyboard.is_pressed(entry['hotkey']):
                    pass
        time.sleep(0.1)

def load_data():
    global scene_data, temporary_scenes
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                scene_data = json.loads(content)
            else:
                scene_data = []
    else:
        scene_data = []

    if os.path.exists(TEMPORARY_FILE):
        with open(TEMPORARY_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                temporary_scenes = json.loads(content)
            else:
                temporary_scenes = []
    else:
        temporary_scenes = []

def save_data():
    with open(SAVE_FILE, 'w') as f:
        json.dump(scene_data, f, indent=2)
    with open(TEMPORARY_FILE, 'w') as f:
        json.dump(temporary_scenes, f, indent=2)

def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, 'r') as f:
            return json.load(f).get("password", "")
    return ""

def save_password(pw):
    with open(PASSWORD_FILE, 'w') as f:
        json.dump({"password": pw}, f)

class ControllerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OBS Scene Controller - by Ritesh")
        self.setWindowIcon(QIcon("logo.jpg"))  # Place logo.png in same directory
        self.setMinimumSize(700, 700)
        self.setup_theme()

        load_data()

        saved_password = load_password()

        obs_ip, ok_ip = QInputDialog.getText(self, "OBS Connection", "Enter OBS WebSocket IP:", QLineEdit.Normal, "localhost")
        if not ok_ip or not obs_ip:
            QMessageBox.critical(self, "Error", "No IP entered.")
            sys.exit(1)

        pw, ok_pw = QInputDialog.getText(self, "OBS Password", "Enter OBS WebSocket Password:", QLineEdit.Normal, saved_password)
        if not ok_pw:
            QMessageBox.critical(self, "Error", "No password entered.")
            sys.exit(1)

        save_password(pw)

        global ws
        ws = obsws(obs_ip, OBS_PORT, pw)
        try:
            ws.connect()
        except Exception as e:
            QMessageBox.critical(self, "OBS Connection Failed", str(e))
            sys.exit(1)

        threading.Thread(target=run_flask, daemon=True).start()
        threading.Thread(target=start_cloudflare_tunnel, daemon=True).start()
        threading.Thread(target=hotkey_worker, daemon=True).start()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Software made by Ritesh. All rights reserved to Team Emogi."))

        layout.addWidget(QLabel("Add Normal Scene:"))
        self.scene_input = QLineEdit()
        self.scene_input.setPlaceholderText("Scene Name")
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText("e.g. ctrl+f9")
        self.tunnel_url_input = QLineEdit()
        self.tunnel_url_input.setPlaceholderText("Screen Tunnel URL")
        add_button = QPushButton("Add Normal Scene")
        add_button.clicked.connect(self.add_scene)

        layout.addWidget(self.scene_input)
        layout.addWidget(self.hotkey_input)
        layout.addWidget(self.tunnel_url_input)
        layout.addWidget(add_button)

        self.scene_list = QListWidget()
        layout.addWidget(QLabel("Normal Scenes:"))
        layout.addWidget(self.scene_list)

        normal_scene_buttons = QHBoxLayout()
        edit_scene_button = QPushButton("Edit Selected Scene")
        edit_scene_button.clicked.connect(self.edit_scene)
        delete_scene_button = QPushButton("Delete Selected Scene")
        delete_scene_button.clicked.connect(self.delete_scene)
        normal_scene_buttons.addWidget(edit_scene_button)
        normal_scene_buttons.addWidget(delete_scene_button)
        layout.addLayout(normal_scene_buttons)

        layout.addWidget(QLabel("Add Temporary Scene:"))
        self.temp_scene_input = QLineEdit()
        self.temp_scene_input.setPlaceholderText("Temporary Scene Name")
        self.temp_hotkey_input = QLineEdit()
        self.temp_hotkey_input.setPlaceholderText("Hotkey")
        self.temp_thumbnail_input = QLineEdit()
        self.temp_thumbnail_input.setPlaceholderText("Thumbnail Image Path")
        select_thumbnail_button = QPushButton("Browse Thumbnail")
        select_thumbnail_button.clicked.connect(self.browse_thumbnail)
        self.temp_duration_input = QLineEdit()
        self.temp_duration_input.setPlaceholderText("Duration (Seconds)")
        temp_add_button = QPushButton("Add Temporary Scene")
        temp_add_button.clicked.connect(self.add_temporary_scene)

        layout.addWidget(self.temp_scene_input)
        layout.addWidget(self.temp_hotkey_input)
        layout.addWidget(self.temp_thumbnail_input)
        layout.addWidget(select_thumbnail_button)
        layout.addWidget(self.temp_duration_input)
        layout.addWidget(temp_add_button)

        self.temp_scene_list = QListWidget()
        layout.addWidget(QLabel("Temporary Scenes:"))
        layout.addWidget(self.temp_scene_list)

        temp_scene_buttons = QHBoxLayout()
        edit_temp_scene_button = QPushButton("Edit Selected Temporary Scene")
        edit_temp_scene_button.clicked.connect(self.edit_temporary_scene)
        delete_temp_scene_button = QPushButton("Delete Selected Temporary Scene")
        delete_temp_scene_button.clicked.connect(self.delete_temporary_scene)
        temp_scene_buttons.addWidget(edit_temp_scene_button)
        temp_scene_buttons.addWidget(delete_temp_scene_button)
        layout.addLayout(temp_scene_buttons)

        self.tunnel_label = QLabel("Cloudflare Tunnel: Initializing...")
        layout.addWidget(self.tunnel_label)

        self.setLayout(layout)
        self.refresh_scene_list()

        threading.Thread(target=self.update_tunnel_label, daemon=True).start()

    def setup_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, QColor("#00FF9C"))
        palette.setColor(QPalette.Base, QColor("#1E1E1E"))
        palette.setColor(QPalette.Text, QColor("#00FF9C"))
        palette.setColor(QPalette.Button, QColor("#282828"))
        palette.setColor(QPalette.ButtonText, QColor("#00FF9C"))
        self.setPalette(palette)
        self.setFont(QFont("Consolas", 10))

    def browse_thumbnail(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Thumbnail Image")
        if filename:
            self.temp_thumbnail_input.setText(filename)

    def add_scene(self):
        scene = self.scene_input.text().strip()
        hotkey = self.hotkey_input.text().strip().lower()
        tunnel_url = self.tunnel_url_input.text().strip()
        if not scene or not hotkey or not tunnel_url:
            QMessageBox.warning(self, "Invalid Input", "Scene name, hotkey, and tunnel URL are required.")
            return
        scene_data.append({"scene": scene, "hotkey": hotkey, "tunnel_url": tunnel_url})
        save_data()
        self.refresh_scene_list()
        self.scene_input.clear()
        self.hotkey_input.clear()
        self.tunnel_url_input.clear()

    def edit_scene(self):
        selected_items = self.scene_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a scene to edit.")
            return
        selected_text = selected_items[0].text()
        scene_name = selected_text.split(" | ")[0]
        
        for scene in scene_data:
            if scene['scene'] == scene_name:
                new_name, ok_name = QInputDialog.getText(self, "Edit Scene", "Enter new scene name:", QLineEdit.Normal, scene['scene'])
                new_hotkey, ok_hotkey = QInputDialog.getText(self, "Edit Scene", "Enter new hotkey:", QLineEdit.Normal, scene['hotkey'])
                new_tunnel_url, ok_url = QInputDialog.getText(self, "Edit Scene", "Enter new tunnel URL:", QLineEdit.Normal, scene['tunnel_url'])
                if ok_name and ok_hotkey and ok_url and new_name and new_hotkey and new_tunnel_url:
                    scene['scene'] = new_name.strip()
                    scene['hotkey'] = new_hotkey.strip().lower()
                    scene['tunnel_url'] = new_tunnel_url.strip()
                    save_data()
                    self.refresh_scene_list()
                break

    def delete_scene(self):
        selected_items = self.scene_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a scene to delete.")
            return
        selected_text = selected_items[0].text()
        scene_name = selected_text.split(" | ")[0]
        
        if QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete scene '{scene_name}'?") == QMessageBox.Yes:
            global scene_data
            scene_data = [scene for scene in scene_data if scene['scene'] != scene_name]
            save_data()
            self.refresh_scene_list()

    def add_temporary_scene(self):
        scene = self.temp_scene_input.text().strip()
        hotkey = self.temp_hotkey_input.text().strip().lower()
        thumbnail = self.temp_thumbnail_input.text().strip()
        duration = self.temp_duration_input.text().strip()
        if not scene or not hotkey or not thumbnail or not duration:
            QMessageBox.warning(self, "Invalid Input", "All fields are required.")
            return
        try:
            float(duration)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Duration must be a number.")
            return
        temporary_scenes.append({
            "scene": scene,
            "hotkey": hotkey,
            "thumbnail": thumbnail,
            "duration": duration
        })
        save_data()
        self.refresh_scene_list()
        self.temp_scene_input.clear()
        self.temp_hotkey_input.clear()
        self.temp_thumbnail_input.clear()
        self.temp_duration_input.clear()

    def edit_temporary_scene(self):
        selected_items = self.temp_scene_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a temporary scene to edit.")
            return
        selected_text = selected_items[0].text()
        scene_name = selected_text.split(" | ")[0]
        
        for scene in temporary_scenes:
            if scene['scene'] == scene_name:
                new_name, ok_name = QInputDialog.getText(self, "Edit Temporary Scene", "Enter new scene name:", QLineEdit.Normal, scene['scene'])
                new_hotkey, ok_hotkey = QInputDialog.getText(self, "Edit Temporary Scene", "Enter new hotkey:", QLineEdit.Normal, scene['hotkey'])
                new_thumbnail, ok_thumbnail = QInputDialog.getText(self, "Edit Temporary Scene", "Enter new thumbnail path:", QLineEdit.Normal, scene['thumbnail'])
                new_duration, ok_duration = QInputDialog.getText(self, "Edit Temporary Scene", "Enter new duration (seconds):", QLineEdit.Normal, scene['duration'])
                if ok_name and ok_hotkey and ok_thumbnail and ok_duration and new_name and new_hotkey and new_thumbnail and new_duration:
                    try:
                        float(new_duration)
                        scene['scene'] = new_name.strip()
                        scene['hotkey'] = new_hotkey.strip().lower()
                        scene['thumbnail'] = new_thumbnail.strip()
                        scene['duration'] = new_duration.strip()
                        save_data()
                        self.refresh_scene_list()
                    except ValueError:
                        QMessageBox.warning(self, "Invalid Input", "Duration must be a number.")
                break

    def delete_temporary_scene(self):
        selected_items = self.temp_scene_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a temporary scene to delete.")
            return
        selected_text = selected_items[0].text()
        scene_name = selected_text.split(" | ")[0]
        
        if QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete temporary scene '{scene_name}'?") == QMessageBox.Yes:
            global temporary_scenes
            temporary_scenes = [scene for scene in temporary_scenes if scene['scene'] != scene_name]
            save_data()
            self.refresh_scene_list()

    def refresh_scene_list(self):
        self.scene_list.clear()
        for entry in scene_data:
            self.scene_list.addItem(f"{entry['scene']} | {entry['hotkey']} | {entry['tunnel_url']}")

        self.temp_scene_list.clear()
        for entry in temporary_scenes:
            self.temp_scene_list.addItem(f"{entry['scene']} | {entry['hotkey']} | {entry['duration']}s")

    def update_tunnel_label(self):
        while True:
            self.tunnel_label.setText(f"Cloudflare Tunnel URL:\n{cloudflare_url}")
            time.sleep(2)

if __name__ == '__main__':
    app_gui = QApplication(sys.argv)
    window = ControllerGUI()
    window.show()
    sys.exit(app_gui.exec())