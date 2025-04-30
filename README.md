# SquareSense (v1)

Il protocollo legge dei log generati dagli LDR (es. [e2e4](https://github.com/francescobianco/squaresense/blob/main/fixtures/dataset/synthetic/e2e4.log)) e li invia ad'un interprete che è in grado di decifrare l'evento avvenuto sopra la scacchiera
ad esempio

- PICK e2 # Sollevato il pezzo sulla casa e2
- DROP e4 # Posato un pezzo sulla casa e4

Da questi eventi poi genera sulla base delle regole degli scacchi un evento di tipo MOVE

- MOVE e2e4


Leggere il seguente file per capire come funziona il protocollo e come implementarlo in un progetto.

- [GESTURE.md](GESTURE.md)

## Related Links

- Graphic Design: https://github.com/fulminati/gravitboard
- Circuit Design: https://github.com/fulminati/tutorboard
- Arduino Engine: https://github.com/fulminati/freeboard/blob/main/src/board.cpp
