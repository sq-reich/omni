import RPi.GPIO as gp
from MotorControler import MotorController  # Gemeinsamer Motorcontroller
import sys
import termios
import tty
from time import sleep

class Manuell:
    gp.setmode(gp.BCM)
    gp.setup([24, 25], gp.IN, pull_up_down=gp.PUD_UP)

    def __init__(self):
        self.motor = MotorController()
        print(f"🔄 Letzte Motorposition: {self.motor.pos}")

    def steuerung(self):
        print("\n🎮 **Manuelle Steuerung aktiviert** 🎮")
        print("W = Schritt hoch | S = Schritt runter")
        print("D = Tor auf | A = Tor zu | Q = Beenden\n")

        while True:
            key = self.get_key()
            if key == "w":
                print("⬆️ Schritt hoch")
                self.motor.step_motor(1, direction=1)
            elif key == "s":
                print("⬇️ Schritt runter")
                self.motor.step_motor(1, direction=-1)
            elif key == "d":
                self.motor.tor_auf()
            elif key == "a":
                self.motor.tor_zu()
            elif key == "q":
                print("🚦 Beenden...")
                break

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key.lower()
