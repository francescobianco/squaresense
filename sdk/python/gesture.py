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

class GestureAnalyzer:
    def __init__(self):
        # Crea un array 3D fisso di dimensioni 8x8x10
        self.buffer = [[[0 for _ in range(LDR_DEPTH)] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.sample_count = 0  # Contatore per il numero di frame ricevuti
        self.first_update = True

    def update_board(self, new_frame):
        """
        Aggiorna il buffer 3D con il nuovo frame.
        Se il buffer non è ancora pieno (prima che raggiunga LDR_DEPTH), lo riempiamo.
        """
        # Incrementa il contatore dei campioni
        self.sample_count += 1

        # Riempie il buffer solo con i primi frame fino a raggiungere LDR_DEPTH
        if self.sample_count <= LDR_DEPTH:
            # Aggiungi i nuovi frame nel buffer e mantieni la profondità
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    for d in range(LDR_DEPTH - 1):
                        self.buffer[i][j][d] = self.buffer[i][j][d + 1]  # Shift a sinistra
                    self.buffer[i][j][LDR_DEPTH - 1] = new_frame[i][j]  # Aggiungi il nuovo frame
            return  # Non emettere eventi finché non abbiamo abbastanza campioni
        else:
            # Shiftare il buffer per fare spazio al nuovo frame
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
        Analizza tutte le caselle e stampa un evento se viene rilevato un gesto.
        """
        if self.sample_count < LDR_DEPTH:
            print(f"Buffer non ancora pieno, campioni ricevuti: {self.sample_count}/{LDR_DEPTH}")
            return

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                values = self.buffer[i][j]
                angle, quote = self.compute_linear_regression(values)
                gesture = self.detect_gesture(angle, quote)

                if gesture != Gesture.NONE:
                    print(f"Evento rilevato: {gesture.value} in casa ({i}, {j})")

    def get_status(self):
        """
        Restituisce la matrice 8x8 con i gesti rilevati (non è più necessario per questa versione).
        """
        return None  # Non serve più mantenere uno stato permanente
