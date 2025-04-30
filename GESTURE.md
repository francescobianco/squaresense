# GESTURE.md

## 🎯 Obiettivo

Questo documento descrive il meccanismo di riconoscimento dei gesti sulla scacchiera elettronica basata su sensori LDR (Light Dependent Resistor), in particolare l'algoritmo che consente di rilevare e distinguere eventi come sollevamento e rilascio dei pezzi in modo dettagliato e contestuale.

---

## 📦 Meccanismo di acquisizione dati

- La scacchiera contiene **64 sensori LDR**, uno per ogni casella.
- Ogni LDR produce un valore analogico da 0 a 255 in base alla quantità di luce incidente.
- I valori vengono campionati in modo regolare e **memorizzati in un buffer temporale** per ogni casella.
- Il buffer ha una profondità definita (es. `ldrDepth = 10`), quindi **ogni casella ha a disposizione gli ultimi 10 valori letti**.

Esempio struttura dati:
```
board[8][8][ldrDepth]  // board[i][j][t]
```

---

## 🧠 Analisi temporale: squareAngle e squareQuote

Per ogni casella `(i, j)`, viene applicata una **regressione lineare** sui 10 valori temporali più recenti per determinare:

- **`squareAngle[i][j]`** → la **pendenza** della curva nel tempo, ovvero quanto velocemente varia la luce.
- **`squareQuote[i][j]`** → il **valore medio** (offset) della curva.

Formula per la pendenza (`angle`):
```
angle = ((n * Σ(xy)) - (Σx * Σy)) / ((n * Σ(x²)) - (Σx)²)
```

Formula per l’intercetta (`quote`):
```
quote = (Σy - (angle * Σx)) / n
```

---

## 🧭 Classificazione eventi

Usando i valori di `squareAngle` e `squareQuote`, è possibile classificare in modo raffinato gli eventi dinamici:

| Evento   | Condizione `squareAngle`     | Condizione `squareQuote` | Descrizione                        |
|----------|------------------------------|---------------------------|-------------------------------------|
| `PICK`   | angle < -50                  | quote > 200               | Sollevamento molto rapido           |
| `LIFT`   | -50 < angle < -20            | quote > 200               | Sollevamento normale                |
| `GRAB`   | angle > -20                  | quote > 200               | Sollevamento lento o esitante       |
| `PUSH`   | angle > 50                   | quote < 10                | Rilascio molto rapido               |
| `DROP`   | 20 < angle < 50              | quote < 10                | Rilascio normale                    |
| `PLOP`   | angle < 20                   | quote < 10                | Rilascio lento, quasi appoggiato    |

---

## 🔁 Logica ciclica di aggiornamento

La funzione `liftDropAnalisys()` viene eseguita periodicamente e:

1. Calcola `squareAngle` e `squareQuote` per ogni casella `(i,j)`.
2. Classifica l’evento attuale.
3. Aggiorna lo stato della casella (`currentSquareStatus[i][j]`) con l’evento rilevato.

Esempio codice logico:
```cpp
if (quote > 200) {
  if (angle < -50) status = PICK;
  else if (angle < -20) status = LIFT;
  else status = GRAB;
} else if (quote < 10) {
  if (angle > 50) status = PUSH;
  else if (angle > 20) status = DROP;
  else status = PLOP;
}
```

---

## 📊 Esempi d’uso

- **PICK**: un utente afferra rapidamente un pezzo → evento registrato.
- **PLOP**: il pezzo viene rilasciato lentamente e con cura → evento distinto.
- Questo meccanismo permette di ottenere una **timeline dei gesti** sulla scacchiera, utile per:
    - Ricostruzione fedele della partita
    - Replay dinamici
    - Riconoscimento intenzioni del giocatore (esitazioni, tocchi falsi)

---

## 💡 Possibili miglioramenti futuri

- Aggiunta di **isteresi** per evitare fluttuazioni tra eventi.
- **Normalizzazione dei dati** per compensare variazioni di luce ambientale.
- Implementazione di **filtri digitali** per pulizia del segnale.
- Salvataggio degli eventi in formato **PGN arricchito** con timestamp e tipo gesto.

---

## 📁 Estensione del protocollo

Nel protocollo `OpenSquareSense`, questi eventi possono essere codificati come:

```
E4: PICK → E5: PLOP
```

O in formato JSON:

```json
{
  "from": "E4",
  "to": "E5",
  "lift": "PICK",
  "drop": "PLOP",
  "timestamp": 1714517264
}
```

---

## 🧪 Debug e testing

- Può essere utile registrare il valore di `squareAngle` in tempo reale per tarare meglio le soglie.
- Si consiglia di **loggare eventi per casella** e verificare che i gesti siano rilevati solo quando reali.

---

## 🛠️ Note implementative

- Assicurarsi che il sampling dei dati sia regolare e a frequenza costante.
- Le soglie sono **parametri tarabili** e possono essere adattate a seconda del tipo di pezzo e di luce ambientale.

---

## 📎 Conclusione

Il sistema di riconoscimento gesti basato su `squareAngle` e `squareQuote` è semplice, efficiente e molto potente. Permette di trasformare una scacchiera fisica in un’interfaccia reattiva e precisa, in grado di comprendere non solo **cosa** accade, ma anche **come** avviene.

