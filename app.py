from flask import Flask, render_template, redirect, url_for
from classes.mojo import Mojo  # dein bestehendes Modul
import subprocess
import os
import signal
from classes.key import Manuell

manuell = Manuell()

pk = Mojo()


app = Flask(__name__)

@app.route('/')
def index():
    frei = pk.get_parkp()
    return render_template('index.html', frei=frei)

@app.route('/tor-auf')
def tor_auf():
    pk.tor_auf()
    return redirect(url_for('index'))

@app.route('/tor-zu')
def tor_zu():
    pk.tor_zu()
    return redirect(url_for('index'))

@app.route('/start')
def start_system():
    global process
    if process is None:
        process = subprocess.Popen(['python3', 'main.py'])
    return redirect(url_for('index'))

@app.route('/stop')
def stop_system():
    global process
    if process:
        os.kill(process.pid, signal.SIGTERM)
        process = None
    return redirect(url_for('index'))

@app.route('/key')
def key_control():
    return render_template('key.html')

@app.route('/key/up')
def key_up():
    manuell.step_motor(1, direction=1)
    return redirect(url_for('key_control'))

@app.route('/key/down')
def key_down():
    manuell.step_motor(1, direction=-1)
    return redirect(url_for('key_control'))

@app.route('/key/open')
def key_open():
    manuell.tor_auf()
    return redirect(url_for('key_control'))

@app.route('/key/close')
def key_close():
    manuell.tor_zu()
    return redirect(url_for('key_control'))

@app.route('/key/reset')
def key_reset():
    with open("last_pos.csv", "w") as f:
        f.write("0\n")
    return redirect(url_for('key_control'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)