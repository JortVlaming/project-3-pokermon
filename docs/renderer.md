# Renderer
Documentatie voor de renderer van Pokermon.

Om gebruik te maken van de renderer moet je een `state` hebben met een `draw` functie.
Deze functie ontvangt elke frame een renderer variabel dat je kan gebruiken om te renderen.
Voor een voorbeeld zie [States (Voorbeeld)](states.md#voorbeeld-state)

---

## Functies

### set_font
De set_font functie kan worden gebruikt om de tekstfont van de renderer aan te passen.
De fontwijziging vindt plaats voor alle tekst die wordt gerenderd vanaf dat deze functie is aangeroepen

**Parameters**
<br>
font: str | None: De naam van de nieuwe font. Bij None is het de standaard font
<br>
size: int: De grootte van de font.

---

### set_text_color
De set_text_color functie kan worden gebruikt om de tekstkleur van de renderer aan te passen.
De kleurwijziging vindt plaats voor alle tekst die wordt gerenderd vanaf dat deze functie is aangeroepen

**Parameters**
<br>
color: str | Tuple[int, int, int]: De nieuwe kleur van de tekst

---

### get_font_of_size -> pygame.font.Font
De get_font_of_size functie kan worden gebruikt om de standaardfont te krijgen met een specifieke grootte.

**Parameters**
<br>
size: int: De grootte van de font

---

### draw_text
De draw_text functie kan worden gebruikt om tekst te renderen.

**Parameters**
<br>
text: str: De tekst om te renderen
<br>
x: int: De X positie van de tekst
<br>
y: int: De Y positie van de tekst
<br>
size: int = 64: De grootte van de font om te gebruiken
<br>
antialias: bool = True: Of de renderer antialiasing moet gebruiken tijdens het renderen
<br>
color: str | Tuple[int, int, int] = huidige renderer kleur: Kleur om te gebruiken bij renderen
<br>
centered: bool = True: Of de tekst moet worden gecentreerd op de coordinaten

---

### draw_text_x_centered
De draw_text_x_centered functie kan worden gebruikt om tekst in het midden van het scherm te renderen

**Parameters**
<br>
text: str: De tekst om te renderen
<br>
y: int: De Y positie van de tekst
<br>
Deze functie accepteert alle parameters van de `draw_text` functie. Alleen de X parameter heeft geen functie

---

### draw_text_centered
De draw_text_centered functie kan worden gebruikt om tekst in het midden van een rect of het scherm te tekenen.
<br>
Je kan een rect maken met behulp van de `draw_rect` functie
<br>
Tekst wordt automatisch resized om te passen

**Parameters**
<br>
text: str: De tekst om te renderen
<br>
rect: pygame.Rect = None: Rect om de tekst in te renderen
<br>
font: pygame.font.Font = None: De font om te gebruiken bij renderen
<br>
start: int = 72: De begin font grootte om mee te testen
<br>
color: str | Tuple[int, int, int] = huidige renderer kleur: Kleur om te gebruiken bij renderen
<br>
y_offset: int = 0: Een Y offset om toe te voegen aan de tekst Y positie
<br>
alignment: "left" | "right" | "center" = "center": Aan welke kant van de rect de tekst moet worden gerenderd

---

### get_text_width -> int
De get_text_width functie kan worden gebruikt om te berekenen hoelang de tekst op het scherm is bij renderen.

**Parameters**
<br>
text: str: De tekst om de lengte van te berekenen

---

### draw_rect -> pygame.Surface
De draw_rect functie kan worden gebruikt om een vierkant op het scherm te renderen.

**Parameters**
<br>
color: str | Tuple[int, int, int] | Tuple[int, int, int, int]: Kleur van het vierkant om te renderen
<br>
x: int: De X positie van het vierkant
<br>
y: int: De Y positie van het vierkant
<br>
width: int: De breedte van het vierkant
<br>
height: int: De hoogte van het vierkant
<br>
border_radius: int = 0: Hoe rond de hoeken van het vierkant moet zijn

---

### draw_image
De draw_image functie kan worden gebruikt om een image op het scherm te tekenen

**Parameters**
<br>
image: str | pygame.Surface: Het pad naar de afbeelding of een al ingeladen afbeelding
<br>
x: int: De X positie van de afbeelding
<br>
y: int: De Y positie van de afbeelding
<br>
image_scale: int = 1: Een schaal voor de afbeelding om de afbeelding te vergroten