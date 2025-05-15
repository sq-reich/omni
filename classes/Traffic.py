import RPi.GPIO as GPIO
from time import sleep

class Traffic:
    def __init__(self, red_en=7, green_en=8, red_ex=4, green_ex=17, buzzer=27):
        GPIO.setmode(GPIO.BCM)
        self.pins = {
            "red_en": red_en,
            "green_en": green_en,
            "red_ex": red_ex,
            "green_ex": green_ex,
            "buzzer": buzzer
        }
        self.state = {key: False for key in self.pins if key != "buzzer"}

        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)

    def _set_light(self, color, en=True, ex=True, alone=False):
        """Interne Methode zur Lichtsteuerung (rot oder grün)."""
        en_pin = self.pins[f"{color}_en"]
        ex_pin = self.pins[f"{color}_ex"]

        if alone:
            if en:
                GPIO.output(en_pin, 1)
                self.state[f"{color}_en"] = True
            elif ex:
                GPIO.output(ex_pin, 1)
                self.state[f"{color}_ex"] = True
        else:
            GPIO.output(en_pin, int(en))
            GPIO.output(ex_pin, int(ex))
            self.state[f"{color}_en"] = en
            self.state[f"{color}_ex"] = ex

    def red_on(self, en=True, ex=True, alone=False):
        self._set_light("red", en, ex, alone)

    def green_on(self, en=True, ex=True, alone=False):
        self._set_light("green", en, ex, alone)

    def led_off(self, mode="low_all"):
        """Schaltet LEDs selektiv aus."""
        modes = {
            "low_all": ["red_en", "green_en", "red_ex", "green_ex"],
            "low_en": ["red_en", "green_en"],
            "low_ex": ["red_ex", "green_ex"],
            "low_red_en": ["red_en"],
            "low_green_en": ["green_en"],
            "low_red_ex": ["red_ex"],
            "low_green_ex": ["green_ex"]
        }

        if isinstance(mode, int):
            mode = list(modes.keys())[mode] if 0 <= mode < len(modes) else None

        if mode not in modes:
            print(f"[Warnung] Ungültiger Modus für led_off(): {mode}")
            return

        for key in modes[mode]:
            GPIO.output(self.pins[key], 0)
            self.state[key] = False

    def high_buz(self, on=True):
        GPIO.output(self.pins["buzzer"], int(on))

    def beep(self, sleep_high=0.3, sleep_low=0.2, repeat=1):
        for _ in range(repeat):
            self.high_buz(True)
            sleep(sleep_high)
            self.high_buz(False)
            sleep(sleep_low)

    def danger(self):
        self.beep(0.7, 0.2, 3)

    def test_buzz(self):
        self.beep(0.5, 0.2, 2)

    def test_leds(self):
        self.red_on()
        sleep(0.5)
        self.green_on()
        sleep(0.5)
        self.led_off()

    def cleanPi(self):
        GPIO.cleanup()

    def get_state(self):
        return self.state
