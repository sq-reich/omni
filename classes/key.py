import RPi.GPIO as gp
from gpiozero import OutputDevice
import csv
import os  # Für Datei-Existenzprüfung
from time import sleep, time
import sys
import termios
import tty

 

class Manuell:
    
    #GPIO Setup
    gp.setmode(gp.BCM)  
    gp.setup([24, 25], gp.IN, pull_up_down=gp.PUD_UP) 
    def __init__(self):
        # Motorsteuerung (Stepmotor)
        self.motor_pins = [OutputDevice(pin, initial_value=False) for pin in [14, 15, 18, 23]]
        self.step_sequence = [
            [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0],
            [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [1, 0, 0, 1]
        ]
        
        self.max_schritte = 130  
        self.pos = 0  
        self.load_position()  # Letzte gespeicherte Position laden

    # Setzt die Motor-Pins
    def set_step(self, values):
        for pin, value in zip(self.motor_pins, values):
            pin.value = value

    # Speichert die aktuelle Position
    def save_position(self):
        with open("last_pos.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.pos])
            file.flush()  # Sofort speichern

   
    # Liest die gespeicherte Position
    def load_position(self):
        if os.path.exists("last_pos.csv"):
            with open("last_pos.csv", "r") as file:
                reader = csv.reader(file)
                try:
                    self.pos = int(next(reader)[0])
                    print(f"🔄 Letzte Position geladen: {self.pos}")
                except (StopIteration, ValueError):
                    self.pos = 0  
        else:
            self.pos = 0  

    # Motor-Schrittweise bewegen
    def step_motor(self, steps, direction=1):
        for _ in range(steps): 
            # if (direction == 1 and self.pos >= self.max_schritte) or (direction == -1 and self.pos <= 0):
            #     break
            for step in (self.step_sequence if direction > 0 else reversed(self.step_sequence)):  
                self.set_step(step) 
                sleep(0.002)
            self.pos += direction
            self.save_position()  # Speichert nach jedem Schritt

    # Tor komplett öffnen
    def tor_auf(self):
        print("⬆️ Tor öffnet...")
        self.step_motor(130, direction=1)
        print("✅ Tor ist offen.")

    # Tor komplett schließen
    def tor_zu(self):
        print("⬇️ Tor schließt...")
        self.step_motor(130, direction=-1)
        print("✅ Tor ist geschlossen.")

    # Manuelle Steuerung mit Tastatur
    def steuerung(self):
        print("\n🎮 **Manuelle Steuerung aktiviert** 🎮")
        print("W = Schritt hoch | S = Schritt runter")
        print("D = Tor auf | A = Tor zu | Q = Beenden\n")

        while True:
            key = self.get_key()
            if key == "w":
                print("⬆️ Schritt hoch")
                self.step_motor(1, direction=1)
            elif key == "s":
                print("⬇️ Schritt runter")
                self.step_motor(1, direction=-1)
            elif key == "d":
                print ("tor auf")
                self.tor_auf()
            elif key == "a":
                print("tor zu")
                self.tor_zu()
            elif key == "q":
                print("🚦 Beenden...")
                break

    # Liest eine Tasteneingabe (ohne Enter)
    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key.lower()

    