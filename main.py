from mfrc522 import MFRC522
from machine import Pin, PWM, I2C
import machine_i2c_lcd
from neopixel import NeoPixel
import utime

# ----- RFID Setup -----
reader = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)  # Initialize RFID reader with SPI pins

# ----- I2C LCD Setup -----
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)              # Initialize I2C bus for LCD
lcd = machine_i2c_lcd.I2cLcd(i2c, 0x27, 2, 16)  # Create LCD object (address might need to be adjusted)

# ----- Color Definitions -----
RED   = (30, 0, 0)
GREEN = (0, 30, 0)
BLACK = (0, 0, 0)
BLUE  = (0, 0, 30)

# ----- Buzzer, Relay, Lights -----
buzzer_pin = 14                        # Pin for buzzer
relay = Pin(15, Pin.OUT)              # Relay output pin
lights = Pin(12, Pin.OUT)            # Lighting control pin

# ----- NeoPixel (LED strip) Setup -----
leds = 12                             # Number of NeoPixel LEDs
np = NeoPixel(Pin(13, Pin.OUT), leds) # Initialize NeoPixel strip
np.fill(RED)                          # Set all LEDs to red initially
np.write()                            # Apply LED color changes

# ----- Buzzer: Access Granted Sound -----
def beep_granted():
    for _ in range(2):
        buzzer = PWM(Pin(buzzer_pin))     # Create PWM signal for buzzer
        buzzer.freq(2000)                # Set frequency
        buzzer.duty_u16(32768)          # Set volume
        utime.sleep(0.1)                # Short beep
        buzzer.deinit()                 # Stop buzzer
        utime.sleep(0.1)                # Pause between beeps

# ----- Buzzer: Access Denied Sound -----
def beep_denied():
    buzzer = PWM(Pin(buzzer_pin))        # Create PWM signal for buzzer
    buzzer.freq(2000)                   # Set frequency
    buzzer.duty_u16(32768)             # Set volume
    utime.sleep(1)                     # Long beep
    buzzer.deinit()                    # Stop buzzer
    utime.sleep(0.1)                   # Short pause

# ----- LED Countdown Effect -----
def countdown(duration):
    for x in range(leds):
        np[x] = RED                      # Turn on LEDs one by one in red
        np.write()
        utime.sleep(duration/leds)      # Spread out over given duration

# ----- LED Blink Effect -----
def blink(color):
    for x in range(2):
        np.fill(BLACK)                   # Turn LEDs off
        np.write()
        utime.sleep(0.5)
        np.fill(color)                  # Turn LEDs on in given color
        np.write()
        utime.sleep(0.5)

# ----- Light Blink (Relay) -----
def inblink(speed, count):
    for x in range(count):
        lights.toggle()                  # Switch light state
        utime.sleep(speed)
        lights.toggle()                  # Switch back
        utime.sleep(speed)

# ----- Initial System Setup -----
PreviousCard = ""                        # Variable to avoid processing same card repeatedly
relay.off()                              # Ensure relay is off
lcd.clear()                              # Clear LCD screen
lcd.putstr("Please identify")       # Display welcome message

# ----- Main Loop -----
while True:
    reader.init()                                         # Initialize RFID reader for next scan
    (stat, tag_type) = reader.request(reader.REQIDL)      # Look for RFID card
    if stat == reader.OK:                                # If card detected
        (stat, uid) = reader.SelectTagSN()               # Get card UID
        if stat == reader.OK:
            card = reader.tohexstring(uid)               # Convert UID to string
            if card == PreviousCard:                     # Ignore same card repeatedly
                continue

            # ----- Access Granted: Card 1 -----
            if card == "[0x93, 0x13, 0xF9, 0x02]":
                print("ACCESS GRANTED")
                beep_granted()                           # Beep success
                lcd.clear()
                lcd.putstr("Access granted")           # Show success on LCD
                relay.on()                              # Activate relay (e.g. door unlock)
                np.fill(GREEN)                          # LEDs green
                np.write()
                utime.sleep(1)
                inblink(0.2, 1)                         # Light blink
                countdown(2)                            # Countdown effect

            # ----- Access Granted: Secret Card -----
            elif card == "[0x34, 0x83, 0xE9, 0x74]":
                print("ACCESS GRANTED")
                beep_granted()
                lcd.clear()
                lcd.putstr("Secret access activated :)") # Special message
                relay.on()
                np.fill(GREEN)
                np.write()
                utime.sleep(1)
                blink(GREEN)                            # Blink LEDs
                inblink(0.2, 4)                         # Blink lights more
                countdown(3)

            # ----- Special Card: Toggle Lights -----
            elif card == "[0x2C, 0x4E, 0xA8, 0x17]":
                print("LEDS TOGGLED")
                beep_denied()                           # Still uses denied sound
                lcd.clear()
                lcd.putstr("Lighting switched")  # Message on LCD
                lights.toggle()                         # Toggle light state
                blink(BLUE)                             # Blue LED blink
                utime.sleep(1)
                np.fill(RED)                            # Return LEDs to red
                np.write()

            # ----- Unknown Card: Access Denied -----
            else:
                print("ACCESS DENIED")
                print(card)
                beep_denied()
                lcd.clear()
                lcd.putstr("Access denied")        # Show denied message
                blink(RED)                             # Blink LEDs red

            relay.off()                                 # Turn off relay after each operation
            lcd.clear()
            lcd.putstr("Please identify")         # Reset LCD message
            PreviousCard = card                         # Store last card to prevent duplicate reads
    else:
        PreviousCard = ""                               # Reset if no card is detected

    utime.sleep_ms(50)                                  # Small delay to avoid busy loop