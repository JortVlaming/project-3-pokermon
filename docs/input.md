# Input

Documentatie over keyboard en mouse input in pokermon.

Om gebruik te maken van keyboard en mouse input moet je een `state` hebben met een `update` functie.
Deze functie ontvangt elke frame een inputManager variabel dat je kan gebruiken om input te krijgen.
Voor een voorbeeld zie [States (Voorbeeld)](states.md#voorbeeld-state)

Elk keyboard key en mouse button heeft een variabele waarde die je kan krijgen van pygame.
```python
from pygame import K_SPACE, BUTTON_LEFT
```

---

## Functies

### is_key_down -> bool

De is_key_down functie kan worden gebruikt om te controleren of een keyboard key voor het eerst deze frame is ingedrukt.

**Parameters**
<br>
key: int: De key representeert het ID van een keyboard key. (Gebruik hiervoor de pygame variabele waarde)

---

### is_key_held -> bool

De is_key_held functie kan worden gebruikt om te controleren of een keyboard key voor meer dan een frame is ingedrukt.

**Parameters**
<br>
key: int: De key representeert het ID van een keyboard key. (Gebruik hiervoor de pygame variabele waarde)

---

### is_button_down -> bool

De is_button_down functie kan worden gebruikt om te controleren of een mouse button voor het eerst deze frame is ingedrukt.

**Parameters**
<br>
button: int: De button representeert het ID van een mouse button. (Gebruik hiervoor de pygame variabele waarde)

---

### is_button_held -> bool

De is_button_held functie kan worden gebruikt om te controleren of een mouse button voor meer dan een frame is ingedrukt.

**Parameters**
<br>
button: int: De button representeert het ID van een mouse button. (Gebruik hiervoor de pygame variabele waarde)