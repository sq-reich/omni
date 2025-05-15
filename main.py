from time import sleep, time
from classes.mojo import Mojo
from classes.key import Manuell
from classes.Traffic import Traffic
import RPi.GPIO as gp

#initiation of LCD 
try:
    from classes.lcd import LCD
    lcd = LCD()
    lcd_detected = True
except Exception as e:
    print(f"⚠️ LCD konnte nicht initialisiert werden: {e}")
    from classes.lcd_safe import NoLCD
    lcd = NoLCD()
    lcd_detected = False


# Startinfo
print("🚀 Parkhaussystem gestartet...")

if lcd: lcd.display_two_lines("Parkhaussystem", f"gestartet...",True)

# Wiederstellensphase 
pk.auto_recovery()


# Start testphase
light.test_buzz()
light.test_leds()

if lcd: lcd.display_two_lines("Parkhaus bereit", f"Frei: {pk.get_parkp()}",True)
sleep(3)




try:
    while True:
        #>>> Tasteneingaben prüfen <<<
        freie_plaetze = pk.get_parkp()
        lcd.display_two_lines("Verfuegbar:", f"{freie_plaetze} Plaetze",True)
        
                
# Einfahrt -> Sensor A aktiviert >> 
        if pk.is_activeted("a"):
            
            if pk.get_parkp() == 0:
                light.red_on(False)
                light.green_on(True,False)
                light.danger()
                if lcd: lcd.display_two_lines("Kein Platz","frei",True)
                sleep(2)
                
            else:
                light.red_on()
                light.green_on(False,False)
                if lcd: lcd.display_two_lines("Einfahrt erkannt",">>>",True)
                pk.einfahrt()
            

# Ausfahrt -> Sensor B aktiviert >> 
        elif pk.is_activeted("b"):
            
            light.red_on()
            light.green_on(False,False)
            if lcd: lcd.display_two_lines("Ausfahrt erkannt","<<<",True)
            pk.ausfahrt()

        
        elif pk.get_parkp() == 0:
            light.red_on(False)
            light.green_on(True,False)

        
        elif pk.get_parkp() == 4:
            light.red_on(True,False)
            light.green_on(False,True)

        
        elif pk.get_parkp() > 0:        
            light.red_on(False,False)
            light.green_on()
                          
        sleep(0.02)

except KeyboardInterrupt:
    print("\n🚦 Programm manuell beendet.")
    if lcd: lcd.display_two_lines("System gestoppt","_x_",True)
    sleep(2)
finally:
    gp.cleanup()
    lcd.clear()
    pk.tor_zu()
