# Buttons
Documentatie over buttons in de game UI


- [Basis informatie](#basis)
- [Soorten buttons](#types)
- [Buttons maken](#gebruikt)
  - [Voorbeeld](#voorbeeld)

---

## <a name="basis"></a>Basis informatie

Buttons kunnen worden gebruikt om functies aan te roepen wanneer op de buttons wordt ge-clicked.
Een voorbeeld hiervan is de `Play` button in de main menu.

---

## <a name="types"></a>Soorten buttons

In pokermon zijn er 2 soorten buttons: `TextButton` en `ImageButton`, allebei erven ze van de `Button` class.
Het enige verschil tussen deze 2 soorten buttons is dat de `TextButton` een vierkant met tekst is en de `ImageButton` is een image.

---

## <a name="gebruik"></a>Buttons maken

Buttons maken is een 3 stappen process:
- De button declareren (maken als variabel)
- De on_click functie declareren
- De button toevoegen aan de huidige_state

De on_click functie kan je op 2 manieren declareren: direct en indirecte declaratie.
Bijde soorten hebben hun betere punten.

Directe declaratie kan je gebruiken als je geen parameters (behalve de geclickte knop) nodig hebt in je on_click functie.
<br>
Indirecte declaratie kan je gebruiken als je je eigen parameters wil meegeven aan je on_click functie.

Hieronder zijn voorbeelden van allebei de methodes met 2 `TextButton`
<a name="voorbeeld"></a>
```python
from src.engine.ui.textButton import TextButton
from src.engine.state.state import State


# voorbeeld functie met enkel de button als parameter
def direct_voorbeeld(btn):
    print("Dit is een directe knop!")

# voorbeeld functie met een parameter dat niet de knop is
def indirect_voorbeeld(bericht):
    print("Dit is een indirecte knop!")
    print(f"Bericht van de knop: {bericht}")

class ButtonExample(State):
    def __init__(self):
        super().__init__()

        # Voorbeeld declaratie van een TextButton
        # Alle parameters voor een TextButton zijn aanwezig (inclusief optionele parameters)
        directeButton = TextButton(
            x=100,
            y=100,
            width=100,
            height=100,
            color="Black",
            text="Direct voorbeeld",
            text_color="White"
        )
        
        # Voorbeeld van een directe on_click
        directeButton.set_on_click(direct_voorbeeld)
        
        
        # Voorbeeld declaratie van een TextButton
        # Alle parameters voor een TextButton zijn aanwezig (inclusief optionele parameters)
        indirecteButton = TextButton(
            x=250,
            y=100,
            width=100,
            height=100,
            color="Black",
            text="Indirect voorbeeld",
            text_color="White"
        )

        # Voorbeeld van een indirecte on_click door middel van een anonieme lambda functie
        # https://www.w3schools.com/python/python_lambda.asp
        indirecteButton.set_on_click(lambda btn: print("Hello Button!"))
        
        # Voorbeeld van een indirecte on_click door middel van een lambda en functie
        indirecteButton.set_on_click(lambda btn: indirect_voorbeeld("Hello Buttons!"))
        
        # buttons toevoegen aan de huidige staat
        # als je deze stap overslaat worden de buttons niet getekend of ge-checked voor clicks
        self.buttons = [directeButton, indirecteButton]
```

Als je in plaats van een `TextButton` een `ImageButton` wilt gebruiken kan je deze constructor gebruiken:
```python
from src.engine.ui.imageButton import ImageButton
btn = ImageButton(x=0, y=0, image="", image_scale=1)
```