# motor_controller.py
from gpiozero import OutputDevice
from time import sleep
import csv
import os

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

    def set_step(self, values):
        for pin, value in zip(self.motor_pins, values):
            pin.value = value

    def save_position(self):
        with open("last_pos.csv", "w", newline="") as file:
            csv.writer(file).writerow([self.pos])

    def load_position(self):
        if os.path.exists("last_pos.csv"):
            try:
                with open("last_pos.csv", "r") as file:
                    self.pos = int(next(csv.reader(file))[0])
            except:
                self.pos = 0
        else:
            self.pos = 0

    def step_motor(self, steps, direction=1):
        for _ in range(steps):
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
