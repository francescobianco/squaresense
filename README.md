# squaresense

Il protocollo legge dei log generati dagli LDR e li invia ad'un interprete che è in grado di decifrazione l'evento avvenuto sopra la scacchiera
ad esempio

- PICK e2 # Sollevato il pezzo sulla casa e2
- DROP e4 # Posato un pezzo sulla casa e4

Da questi eventi poi genera sulla base delle regole degli scacchi un evento di tipo MOVE

- MOVE e2e4

## Related Links

- Graphic Design: https://github.com/fulminati/gravitboard
- Circuit Design: https://github.com/fulminati/tutorboard
- Arduino Engine: https://github.com/fulminati/freeboard/blob/main/src/board.cpp
