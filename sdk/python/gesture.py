from enum import Enum

class Gesture(str, Enum):
    NONE = "NONE"
    PICK = "PICK"
    LIFT = "LIFT"
    GRAB = "GRAB"
    PUSH = "PUSH"
    DROP = "DROP"
    PLOP = "PLOP"

LDR_DEPTH = 10
BOARD_SIZE = 8
MIN_FRAMES_FOR_CHANGE = 5  # Almeno 3 frame per considerare un cambiamento significativo

class GestureAnalyzer:
    def __init__(self):
        # Crea un array 3D fisso di dimensioni 8x8x10
        self.buffer = [[[0 for _ in range(LDR_DEPTH)] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.sample_count = 0  # Contatore per il numero di frame ricevuti
        # Matrice per mantenere lo stato corrente di ogni casella
        self.current_status = [[Gesture.NONE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # Matrice per contare il numero di frame con un cambiamento significativo
        self.change_history = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def update_board(self, new_frame):
        """
        Aggiorna il buffer 3D con il nuovo frame tramite shift ricorsivo.
        """
        # Incrementa il contatore dei campioni
        self.sample_count += 1

        # Shifta il buffer per fare spazio al nuovo frame
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                for d in range(LDR_DEPTH - 1):
                    self.buffer[i][j][d] = self.buffer[i][j][d + 1]  # Shifta a sinistra
                self.buffer[i][j][LDR_DEPTH - 1] = new_frame[i][j]  # Aggiungi il nuovo valore

    def compute_linear_regression(self, values):
        """
        Calcola slope (angle) e intercept (quote) per i dati della singola casella.
        """
        xSum = 0
        ySum = 0
        x2Sum = 0
        xySum = 0
        for d in range(LDR_DEPTH):
            xSum += d
            ySum += values[d]
            x2Sum += d * d
            xySum += d * values[d]
        denominator = (LDR_DEPTH * x2Sum) - (xSum * xSum)
        if denominator == 0:
            angle = 0
        else:
            angle = ((LDR_DEPTH * xySum) - (xSum * ySum)) / denominator
        quote = (ySum - (angle * xSum)) / LDR_DEPTH
        return angle * 100, quote  # Amplificato per rendere più leggibili le soglie

    def detect_gesture(self, angle, quote):
        """
        Ritorna il gesto in base all'angolo e alla quota.
        """
        if quote > 200:
            if angle < -50:
                return Gesture.PICK
            elif angle < -20:
                return Gesture.LIFT
            else:
                return Gesture.GRAB
        elif quote < 10:
            if angle > 50:
                return Gesture.PUSH
            elif angle > 20:
                return Gesture.DROP
            else:
                return Gesture.PLOP
        return Gesture.NONE

    def analyze(self):
        """
        Analizza tutte le caselle e stampa un evento solo se c'è un cambiamento di stato.
        Solo se il buffer è completamente riempito.
        """
        if self.sample_count < LDR_DEPTH:
            print(f"Buffer non ancora pieno, campioni ricevuti: {self.sample_count}/{LDR_DEPTH}")
            return False  # Indica che l'analisi non è stata completata

        events_detected = False

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                values = self.buffer[i][j]
                angle, quote = self.compute_linear_regression(values)
                current_gesture = self.detect_gesture(angle, quote)

                # Se siamo ancora in fase di riempimento del buffer, aggiorna lo stato
                # ma non emettere eventi
                if self.sample_count == LDR_DEPTH:
                    self.current_status[i][j] = current_gesture
                    continue

                # Verifica se c'è un cambiamento significativo
                if current_gesture != self.current_status[i][j] and current_gesture != Gesture.NONE:
                    # Se il cambiamento è significativo, aumenta il contatore
                    self.change_history[i][j] += 1
                    # Solo se il cambiamento è accumulato per un numero sufficiente di frame, emetti un evento
                    if self.change_history[i][j] >= MIN_FRAMES_FOR_CHANGE:
                        print(f"Evento rilevato: {current_gesture.value} in casa ({i}, {j})  {angle}/{quote}", values)
                        self.current_status[i][j] = current_gesture
                        events_detected = True
                else:
                    # Reset del contatore se il cambiamento non è significativo
                    self.change_history[i][j] = 0

        return events_detected  # Indica se sono stati rilevati eventi

    def is_buffer_ready(self):
        """
        Verifica se il buffer è stato completamente riempito.
        """
        return self.sample_count >= LDR_DEPTH

    def get_status(self):
        """
        Restituisce la matrice 8x8 con gli stati correnti delle caselle
        """
        return self.current_status

# Esempio d'uso
if __name__ == "__main__":
    analyzer = GestureAnalyzer()

    # Simula l'invio dei primi 10 frame (riempimento del buffer)
    print("\n=== FASE DI RIEMPIMENTO DEL BUFFER ===")
    for t in range(LDR_DEPTH):
        frame = [[0 for _ in range(8)] for _ in range(8)]
        if t > 5:  # Un esempio di oggetto che appare in D4 (3,3)
            frame[3][3] = 255
        analyzer.update_board(frame)
        analyzer.analyze()  # Non emetterà eventi finché il buffer non è pieno

    print("\n=== BUFFER RIEMPITO, INIZIO ANALISI REALE ===")

    # Simula nuovi frame con un oggetto che si solleva gradualmente in D4
    print("\n=== TEST SOLLEVAMENTO IN D4 ===")
    for t in range(5):
        frame = [[0 for _ in range(8)] for _ in range(8)]
        frame[3][3] = 255 - t * 40  # Simula sollevamento graduale
        analyzer.update_board(frame)
        analyzer.analyze()  # Ora emetterà eventi solo se c'è un cambiamento di stato significativo

    # Simula un nuovo oggetto in E5 (4,4)
    print("\n=== TEST NUOVO OGGETTO IN E5 ===")
    for t in range(5):
        frame = [[0 for _ in range(8)] for _ in range(8)]
        frame[3][3] = 95  # Mantiene lo stato precedente in D4
        frame[4][4] = 255  # Nuovo oggetto in E5
        analyzer.update_board(frame)
        analyzer.analyze()

    # Simula la rimozione dell'oggetto in E5
    print("\n=== TEST RIMOZIONE OGGETTO IN E5 ===")
    for t in range(5):
        frame = [[0 for _ in range(8)] for _ in range(8)]
        frame[3][3] = 95  # Mantiene lo stato precedente in D4
        frame[4][4] = max(0, 255 - t * 60)  # L'oggetto viene rimosso gradualmente
        analyzer.update_board(frame)
        analyzer.analyze()
