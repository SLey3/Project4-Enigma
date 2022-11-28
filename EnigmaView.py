# File: EnigmaView.py

"""
This module implements the class EnigmaView, which manages the
graphics for the Enigma simulator.
"""

from EnigmaConstants import N_ROTORS, ALPHABET
from pgl import GWindow, GCompound, GOval, GLabel, GRect, GImage

class EnigmaView(GWindow):
    """This class creates the Enigma view, which maintains the display."""

    def __init__(self, model):
        """Creates the Enigma window."""

        def add_background():
            self.add(GImage("images/EnigmaTopView.png"))

        def add_keys():
            self._keys = { }
            for letter in ALPHABET:
                x,y = KEY_LOCATIONS[letter]
                key = EnigmaKey(letter)
                self.add(key, x, y)
                self._keys[letter] = key

        def add_lamps():
            self._lamps = { }
            for letter in ALPHABET:
                x,y = LAMP_LOCATIONS[letter]
                lamp = EnigmaLamp(letter)
                self.add(lamp, x, y)
                self._lamps[letter] = lamp

        def add_rotors():
            self._rotors = [ ]
            for index in range(N_ROTORS):
                x,y = ROTOR_LOCATIONS[index]
                rotor = EnigmaRotor()
                self.add(rotor, x, y)
                self._rotors.append(rotor)

        def mousedown_action(e):
            letter = find_key(e)
            if letter is not None:
                self._model.key_pressed(letter)
            else:
                index = find_rotor(e)
                if index is not None:
                    self._model.rotor_clicked(index)

        def mouseup_action(e):
            letter = find_key(e)
            if letter is not None:
                self._model.key_released(letter)

        def find_key(e):
            rsq = KEY_RADIUS ** 2
            for letter in ALPHABET:
                x,y = KEY_LOCATIONS[letter]
                if (x - e.get_x()) ** 2 + (y - e.get_y()) ** 2 <= rsq:
                    return letter
            return None

        def find_rotor(e):
            w2 = ROTOR_FRAME_WIDTH / 2
            h2 = ROTOR_FRAME_HEIGHT / 2
            for index in range(N_ROTORS):
                x,y = ROTOR_LOCATIONS[index]
                if x - w2 < e.get_x() < x + w2 and y - h2 < e.get_y() < y + h2:
                    return index
            return None

        GWindow.__init__(self, GWINDOW_WIDTH, GWINDOW_HEIGHT)
        self._model = model
        add_background()
        add_keys()
        add_lamps()
        add_rotors()
        self.add_event_listener("mousedown", mousedown_action)
        self.add_event_listener("mouseup", mouseup_action)

    def update(self):
        """Updates the view on the window to reflect the current state."""
        for letter in ALPHABET:
            self._keys[letter].set_state(self._model.is_key_down(letter))
            self._lamps[letter].set_state(self._model.is_lamp_on(letter))
        for index in range(N_ROTORS):
            self._rotors[index].set_letter(self._model.get_rotor_letter(index))

class EnigmaKey(GCompound):
    """This class defines the graphical representation of an Enigma key."""

    def __init__(self, letter):
        GCompound.__init__(self)
        base = GOval(2 * KEY_RADIUS, 2 * KEY_RADIUS)
        base.set_filled(True)
        base.set_color(KEY_BORDER_COLOR)
        base.set_fill_color(KEY_BGCOLOR)
        base.set_line_width(KEY_BORDER)
        self.add(base, -KEY_RADIUS, -KEY_RADIUS)
        label = GLabel(letter)
        label.set_font(KEY_FONT)
        label.set_color(KEY_UP_COLOR)
        self.add(label, -label.get_width() / 2, KEY_LABEL_DY)
        self._letter = letter
        self._label = label

    def set_state(self, state):
        if state:
            color = KEY_DOWN_COLOR
        else:
            color = KEY_UP_COLOR
        self._label.set_color(color)


class EnigmaLamp(GCompound):
    """This class defines the graphical form of an Enigma lamp."""

    def __init__(self, letter):
        GCompound.__init__(self)
        base = GOval(2 * LAMP_RADIUS, 2 * LAMP_RADIUS)
        base.set_filled(True)
        base.set_color(LAMP_BORDER_COLOR)
        base.set_fill_color(LAMP_BGCOLOR)
        self.add(base, -LAMP_RADIUS, -LAMP_RADIUS)
        label = GLabel(letter)
        label.set_font(LAMP_FONT)
        label.set_color(LAMP_OFF_COLOR)
        self.add(label, -label.get_width() / 2, LAMP_LABEL_DY)
        self._letter = letter
        self._label = label

    def set_state(self, state):
        if state:
            color = LAMP_ON_COLOR
        else:
            color = LAMP_OFF_COLOR
        self._label.set_color(color)


class EnigmaRotor(GCompound):
    """This class defines the graphical representation of an Enigma rotor."""

    def __init__(self):
        GCompound.__init__(self)
        rect = GRect(ROTOR_WIDTH, ROTOR_HEIGHT)
        rect.set_filled(True)
        rect.set_color(ROTOR_BGCOLOR)
        self.add(rect, -ROTOR_WIDTH / 2, -ROTOR_HEIGHT / 2)
        label = GLabel("")
        label.set_font(ROTOR_FONT)
        label.set_color(ROTOR_COLOR)
        self.add(label)
        self._label = label
        self.set_letter("A")

    def set_letter(self, letter):
        self._label.set_label(letter)
        self._label.set_location(-self._label.get_width() / 2, ROTOR_LABEL_DY)
        
# Constants

GWINDOW_WIDTH = 818             # Width of the GWindow
GWINDOW_HEIGHT = 694            # Height of the GWindow

ROTOR_BGCOLOR = "#BBAA77"       # Background color for the rotor
ROTOR_WIDTH = 24                # Width of the setting indicator
ROTOR_HEIGHT = 26               # Height of the setting indicator
ROTOR_FRAME_WIDTH = 40          # Width of clickable area
ROTOR_FRAME_HEIGHT = 100        # Height of clickable area
ROTOR_COLOR = "Black"           # Text color of the rotor
ROTOR_LABEL_DY = 9              # Offset from center to baseline  

ROTOR_FONT = "bold 24px 'Helvetica Neue',Helvetica,sans-serif"

# This array specifies the coordinates of each rotor display

ROTOR_LOCATIONS = [
    (244, 94),
    (329, 94),
    (412, 94)
]

# Constants that define the keys on the Enigma keyboard

KEY_RADIUS = 24                 # Outer radius of a key in pixels
KEY_BORDER = 3                  # Width of the key border
KEY_BORDER_COLOR = "#CCCCCC"    # Fill color of the key border
KEY_BGCOLOR = "#666666"         # Background color of the key
KEY_UP_COLOR = "#CCCCCC"        # Text color when the key is up
KEY_DOWN_COLOR = "#CC3333"      # Text color when the key is down
KEY_LABEL_DY = 10               # Offset from center to baseline  

KEY_FONT = "bold 28px 'Helvetica Neue',Helvetica,sans-serif"

# This array determines the coordinates of a key for each letter index

KEY_LOCATIONS = {
    "A": (140, 566),
    "B": (471, 640),
    "C": (319, 639),
    "D": (294, 567),
    "E": (268, 495),
    "F": (371, 567),
    "G": (448, 567),
    "H": (523, 567),
    "I": (650, 496),
    "J": (598, 567),
    "K": (674, 567),
    "L": (699, 641),
    "M": (624, 641),
    "N": (547, 640),
    "O": (725, 497),
    "P": ( 92, 639),
    "Q": (115, 494),
    "R": (345, 495),
    "S": (217, 566),
    "T": (420, 496),
    "U": (574, 496),
    "V": (395, 639),
    "W": (192, 494),
    "X": (242, 639),
    "Y": (168, 639),
    "Z": (497, 496)
}

# Constants that define the lamps above the Enigma keyboard

LAMP_RADIUS = 23                # Radius of a lamp in pixels
LAMP_BORDER_COLOR = "#111111"   # Line color of the lamp border
LAMP_BGCOLOR = "#333333"        # Background color of the lamp
LAMP_OFF_COLOR = "#666666"      # Text color when the lamp is off
LAMP_ON_COLOR = "#FFFF99"       # Text color when the lamp is on
LAMP_LABEL_DY = 9               # Offset from center to baseline  

LAMP_FONT = "bold 24px 'Helvetica Neue',Helvetica,sans-serif"

# This array determines the coordinates of a lamp for each letter index

LAMP_LOCATIONS = {
    "A": (144, 332),
    "B": (472, 403),
    "C": (321, 402),
    "D": (296, 333),
    "E": (272, 265),
    "F": (372, 333),
    "G": (448, 334),
    "H": (524, 334),
    "I": (650, 266),
    "J": (600, 335),
    "K": (676, 335),
    "L": (700, 403),
    "M": (624, 403),
    "N": (549, 403),
    "O": (725, 267),
    "P": ( 94, 401),
    "Q": (121, 264),
    "R": (347, 265),
    "S": (220, 332),
    "T": (423, 265),
    "U": (574, 266),
    "V": (397, 402),
    "W": (197, 264),
    "X": (246, 402),
    "Y": (170, 401),
    "Z": (499, 265)
}
