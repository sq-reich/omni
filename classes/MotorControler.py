# motor_controller.py
from gpiozero import OutputDevice
from time import sleep
import csv
import os
import RPi.GPIO as gp


gp.setmode(gp.BCM)



class MotorController:
    def __init__(self, pins=[14, 15, 18, 23], max_schritte=130):
        self.motor_pins = [OutputDevice(pin) for pin in pins]
        self.step_sequence = [
            [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
            [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
        ]
        self.pos = 0
        self.max_schritte = max_schritte
        self.load_position()

        # Sensoren (GPIO 24 = Eingang, GPIO 25 = Ausgang)
        self.irs_enter = 24
        self.irs_exit = 25
        gp.setup([self.irs_enter, self.irs_exit], gp.IN, pull_up_down=gp.PUD_UP)
    
    def is_obstructed(self):
        return not gp.input(24) or not gp.input(25)  # True = Objekt erkannt


    def set_step(self, values):
        for pin, value in zip(self.motor_pins, values):
            pin.value = value

    def save_position(self):
        try:
            with open("last_pos.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([self.pos])
            # Backup schreiben
            with open("last_pos_backup.csv", "w", newline="") as backup:
                csv.writer(backup).writerow([self.pos])
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Position: {e}")

    def load_position(self):
        if os.path.exists("last_pos.csv"):
            try:
                with open("last_pos.csv", "r") as file:
                    self.pos = int(next(csv.reader(file))[0])
            except Exception as e:
                print(f"⚠️ Position konnte nicht geladen werden: {e}")
                self.pos = 0
        else:
            self.pos = 0

    def step_motor(self, steps, direction=1):
        for _ in range(steps):
            if direction == -1 and self.is_obstructed():
                print("🛑 Sicherheit: Sensor erkennt Hindernis. Tor öffnet wieder.")
                self.tor_auf()
                return

            for step in (self.step_sequence if direction > 0 else reversed(self.step_sequence)):
                self.set_step(step)
                sleep(0.002)
            self.pos += direction
            self.save_position()

    def tor_auf(self):
        print("⬆️ Tor öffnet...")
        self.step_motor(self.max_schritte - self.pos, direction=1)
        print("✅ Tor ist offen.")

    def tor_zu(self):
        print("⬇️ Tor schließt...")
        self.step_motor(self.pos, direction=-1)
        print("✅ Tor ist geschlossen.")
    
    def is_activeted(self, val):
        val = val.lower()
        if val == "a":
            return not gp.input(self.irs_enter)
        elif val == "b":
            return not gp.input(self.irs_exit)
        else:
            return False
    
    def test_motor(self):
        pass
