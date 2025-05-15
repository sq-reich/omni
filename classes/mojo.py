import RPi.GPIO as gp
import csv
import os
from time import sleep, time
from MotorControler import MotorController  # Neue Importstelle für Motorsteuerung




class Mojo:
    def __init__(self):
        self.motor = MotorController()

        

        
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
                    if not (0 <= self.parkp <= self.max_pp):  # Plausibilitätsprüfung
                        raise ValueError("Unplausibler Parkplatzwert")
            except Exception as e:
                print(f"⚠️ Parkplätze konnten nicht geladen werden: {e}")
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
                if self.motor.is_activeted("b"):
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
                if self.motor.is_activeted("a"):
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

    
