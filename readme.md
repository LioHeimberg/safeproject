# 🔐 RFID Access Control System with NeoPixels, LCD & Buzzer

This is the code of my safe project.
 
This project implements a simple **RFID-based access control system** using a microcontroller (e.g., Raspberry Pi Pico), an MFRC522 RFID reader, an I2C LCD display, a NeoPixel LED ring, a buzzer, and a relay to control external devices like doors or lights.

It recognizes multiple RFID cards, provides **visual and audio feedback**, and can control a **relay and lighting** based on the card scanned.

---

## 📸 Features

- ✅ RFID Authentication using MFRC522  
- 💡 LCD Display for status messages (I2C)  
- 🌈 NeoPixel LED ring for visual feedback (red = idle, green = granted, blue = lighting control)  
- 🔔 Buzzer for access granted / denied alerts  
- 🔌 Relay Control to unlock doors or trigger devices  
- ✨ Custom light effects (blink, countdown)  
- 🔄 Multiple cards supported for different functions  

---

## 🧰 Hardware Required

| Component            | Description                                      |
|-----------------------|---------------------------------------------------|
| 🧠 Microcontroller    | Raspberry Pi Pico (or similar with MicroPython)   |
| 📡 MFRC522 RFID Reader| For scanning RFID cards or tags                  |
| 🖥️ I2C LCD (16x2)     | To display access messages                       |
| 🌈 NeoPixel ring     | 12 LEDs used for effects                         |
| 🔔 Buzzer            | For feedback sounds                              |
| ⚡ Relay Module      | Controls door lock or lights                     |
| 💡 Light (optional)  | External light controlled by relay               |
| RFID Cards/Tags      | Pre-programmed UIDs for authentication           |

---

## 🪛 Pin Configuration

| Component      | Pico Pin |
|---------------|---------|
| RFID (SCK)    | GP2     |
| RFID (MISO)   | GP4     |
| RFID (MOSI)   | GP3     |
| RFID (CS)     | GP1     |
| RFID (RST)    | GP0     |
| LCD (SDA)     | GP16    |
| LCD (SCL)     | GP17    |
| NeoPixel      | GP13    |
| Buzzer        | GP14    |
| Relay         | GP15    |
| Lights        | GP12    |

---

## 🧠 RFID Card Functions

| Card UID                     | Function                         |
|-------------------------------|-----------------------------------|
| `[0x93, 0x13, 0xF9, 0x02]`    | ✅ Normal Access (grants entry)   |
| `[0x34, 0x83, 0xE9, 0x74]`    | 🔐 Secret Access (special effects) |
| `[0x2C, 0x4E, 0xA8, 0x17]`    | 💡 Toggle Lights Mode            |
| Any other UID                 | ❌ Access Denied                 |

> You can change these UIDs in the code to match your own cards.

---

## 🧭 System Behavior

1. **Idle mode**  
   - LCD shows “Please identify”  
   - NeoPixel ring glows red  

2. **Card Detected**  
   - UID is checked against allowed cards  

3. **Access Granted**  
   - LCD shows success message  
   - Buzzer gives double short beep  
   - LEDs turn green  
   - Relay activates for a short time  

4. **Secret Access**  
   - Additional LED & light effects for special cards  

5. **Access Denied**  
   - LCD shows “Access denied”  
   - Buzzer gives long beep  
   - LEDs blink red  

6. **Light Toggle Card**  
   - Toggles external light and blinks LEDs blue  

---

## 📝 Installation

1. Flash **MicroPython** onto your Raspberry Pi Pico.  
2. Copy the following libraries to the Pico using Thonny:
   - `mfrc522.py` (RFID driver)  
   - `machine_i2c_lcd.py` (LCD driver)  
   - `neopixel.py` (LED ring driver)  
3. Copy the main Python script to the Pico (`main.py`).  
4. Reboot the Pico — the program starts automatically.

---

## 🛠️ Customization

- ✍️ **Change card UIDs** in the code to match your RFID tags.  
- 🎨 Adjust LED colors by editing the `RED`, `GREEN`, `BLUE` tuples.  
- 🕒 Modify the **countdown durations** or blink speeds to fit your needs.  
- 🔊 Change **buzzer frequencies** or patterns for different feedback sounds.

---

## ⚠️ Notes

- Make sure to power the NeoPixel ring with a stable **5V supply**.  
- Use a **level shifter** for NeoPixels if your board is 3.3V.  
- Keep RFID wires short for better reliability.  

---

## 📄 License

This project is released under the **MIT License**.  
Feel free to use, modify, and share it.

---

## 🌟 Acknowledgements

- MFRC522 MicroPython Library by various contributors  
- NeoPixel & LCD drivers from the MicroPython community  
- Inspired by DIY home access control systems