import serial
import time
from .squaresense import SquareSense

if __name__ == "__main__":
    # Configura la porta seriale (modifica la porta e il baudrate secondo necessità)
    SERIAL_PORT = '/dev/ttyUSB0'  # o 'COM3' su Windows
    BAUD_RATE = 230400              # o il valore corretto per il tuo dispositivo

    squaresense = SquareSense()

    print(f"Connesso alla seriale: {SERIAL_PORT} a {BAUD_RATE} baud")

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline()
                line_str = line.decode('ascii', errors='ignore').strip()
                #print(f"Ricevuto: {line_str}")
                if line:
                    squaresense.input(line_str)
    except serial.SerialException as e:
        print(f"Errore nella connessione seriale: {e}")
    except KeyboardInterrupt:
        print("\nInterrotto dall'utente.")
