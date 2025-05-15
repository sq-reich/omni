import RPi.GPIO as gp
import csv
import os
from time import sleep, time
from MotorControler import MotorController  # Neue Importstelle für Motorsteuerung
import random as rnd

gp.setmode(gp.BCM)

class Mojo:
    def __init__(self):
        self.motor = MotorController()

        self.heyMsg = ["Hallo", "Moin", "Willkommen", "Viel Spass!", "Guten Tag"]
        self.beyMsg = ["Tschüss", "Adios", "Auf Wiedersehen", "Schoenen Tag noch"]

        # Sensoren (GPIO 24 = Eingang, GPIO 25 = Ausgang)
        self.irs_enter = 24
        self.irs_exit = 25
        gp.setup([self.irs_enter, self.irs_exit], gp.IN, pull_up_down=gp.PUD_UP)

        # Parkplätze
        self.max_pp = 4
        self.min_pp = 0
        self.parkp = 4
        self.load_parkp()

    def auto_recovery(self):
        self.tor_zu()

    def save_parkp(self):
        with open("last_parkP.csv", "w", newline="") as file:
            csv.writer(file).writerow([self.parkp])
            file.flush()

    def load_parkp(self):
        if os.path.exists("last_parkP.csv"):
            try:
                with open("last_parkP.csv", "r") as file:
                    self.parkp = int(next(csv.reader(file))[0])
                    print(f"🔄 Parkplätze geladen: {self.parkp}")
            except:
                self.parkp = self.max_pp
        else:
            self.parkp = self.max_pp

    def add_parkplatz(self):
        if self.parkp < self.max_pp:
            self.parkp += 1
            self.save_parkp()
            print("➕ Parkplatz freigegeben:", self.parkp)

    def drop_parkplatz(self):
        if self.parkp > self.min_pp:
            self.parkp -= 1
            self.save_parkp()
            print("➖ Parkplatz belegt:", self.parkp)
        else:
            print("🛑 Kein Platz frei!")

    def tor_auf(self):
        self.motor.tor_auf()

    def tor_zu(self):
        self.motor.tor_zu()

    def einfahrt(self):
        if self.parkp > 0:
            print("🚗 Einfahrt erkannt. Schranke öffnet...")
            self.tor_auf()
            timeout = time() + 3

            while time() < timeout:
                if not gp.input(self.irs_exit):
                    self.drop_parkplatz()
                    self.tor_zu()
                    return
                sleep(0.02)

            print("❌ Einfahrt abgebrochen. Schranke schließt...")
            self.tor_zu()

    def ausfahrt(self):
        if self.parkp < self.max_pp:
            print("🚙 Ausfahrt erkannt. Schranke öffnet...")
            self.tor_auf()
            timeout = time() + 3

            while time() < timeout:
                if not gp.input(self.irs_enter):
                    self.add_parkplatz()
                    self.tor_zu()
                    return
                sleep(0.02)

            print("❌ Ausfahrt abgebrochen. Schranke schließt...")
            self.tor_zu()
        else:
            print("🚫 Keine Autos drin. Ausfahrt verweigert.")

    def get_parkp(self):
        return self.parkp

    def is_activeted(self, val):
        val = val.lower()
        if val == "a":
            return not gp.input(self.irs_enter)
        elif val == "b":
            return not gp.input(self.irs_exit)
        else:
            return False
