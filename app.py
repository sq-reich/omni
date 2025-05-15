from flask import Flask, render_template, redirect, url_for, abort
from classes.mojo import Mojo
from classes.key import Manuell
import subprocess, os, signal
from flask import jsonify

app = Flask(__name__)

# Parkhausmodule
pk = Mojo()
manuell = Manuell()

# Prozess- und Statuskontrolle
process = None
main_running = False

@app.route('/')
def index():
    frei = pk.get_parkp()
    status = "offen" if pk.pos >= pk.max_schritte else "geschlossen"
    return render_template('index.html', frei=frei, status=status, running=main_running)

@app.route('/start')
def start_system():
    global process, main_running
    if not main_running:
        process = subprocess.Popen(['python33', 'main.py'])
        main_running = True
    return redirect(url_for('index'))

@app.route('/stop')
def stop_system():
    global process, main_running
    if main_running and process:
        os.kill(process.pid, signal.SIGTERM)
        process = None
        main_running = False
    return redirect(url_for('index'))

@app.route('/tor-auf')
def tor_auf():
    pk.tor_auf()
    return redirect(url_for('index'))

@app.route('/tor-zu')
def tor_zu():
    pk.tor_zu()
    return redirect(url_for('index'))

# ===== Manuelle Steuerung =====

@app.route('/key')
def key_control():
    if main_running:
        return "⚠️ Parkhaus läuft automatisch – manuelle Steuerung nicht erlaubt!", 403
    return render_template('key.html')

@app.route('/key/up')
def key_up():
    if not main_running:
        manuell.step_motor(1, direction=1)
    return redirect(url_for('key_control'))

@app.route('/key/down')
def key_down():
    if not main_running:
        manuell.step_motor(1, direction=-1)
    return redirect(url_for('key_control'))

@app.route('/key/open')
def key_open():
    if not main_running:
        manuell.tor_auf()
    return redirect(url_for('key_control'))

@app.route('/key/close')
def key_close():
    if not main_running:
        manuell.tor_zu()
    return redirect(url_for('key_control'))

@app.route('/key/reset')
def key_reset():
    if not main_running:
        with open("last_pos.csv", "w") as f:
            f.write("0\n")
    return redirect(url_for('key_control'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.route('/api/status')
def status():
    return jsonify({
        "frei": pk.get_parkp(), 
        "tor_offen": pk.motor.pos > 0  # Annahme: pos > 0 heißt Tor ist offen
    })