# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaConstants import ALPHABET, ROTOR_PERMUTATIONS, REFLECTOR_PERMUTATION

# State Dicts for both key and lamp
key_state = {c: False for c in ALPHABET}
lamp_key_state = key_state.copy()


class EnigmaRotor:
    def __init__(self, index: int, offset: int = 0):
        self.permutation = ROTOR_PERMUTATIONS[index]
        self.offset = offset
        self.index = index
        self.inverted_permutation = self.invert_key(self.permutation)

    @staticmethod
    def invert_key(perm: str):
        """
        inverts the permutation key
        """
        new_perm = ""

        for p in range(26):
            new_perm += ALPHABET[perm.find(ALPHABET[p])]
        return new_perm

    def get_offset(self):
        """
        returns the current offset
        """
        return self.offset

    def get_permutation(self):
        """
        returns the permutation string
        """
        return self.permutation

    def get_inv_permutation(self):
        """
        returns the inverted permutation string
        """
        return self.inverted_permutation

    def get_rotor_letter(self):
        """
        returns the letter given from the offset
        """
        return ALPHABET[self.offset]

    def advance(self):
        """
        advances offset by 1
        """
        self.offset += 1

        if self.offset == 26:
            self.offset = 0
            if self.index != 0:
                return True
        return False

def apply_permutation(index: int, permutation: str, offset):
    """Compute the index of the letter after shifting it by the offset, wrapping around if necessary.
    Look up the character at that index in the permutation string.
    Return the index of the new character after subtracting the offset, wrapping if necessary.
    """
    offset_index = (index + offset - 1) % 26
    index_change = ALPHABET.find(permutation[offset_index]) - offset_index
    new_index = (index + index_change) % 26
    return ALPHABET[new_index]

slow_rotor = EnigmaRotor(0)
medium_rotor = EnigmaRotor(1)
fast_rotor = EnigmaRotor(2)

rotors = {
    0 : slow_rotor,
    1 : medium_rotor,
    2 : fast_rotor
}

class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self._views = [ ]

    def add_view(self, view):
        """Adds a view to this model."""
        self._views.append(view)

    def update(self):
        """Sends an update request to all the views."""
        for view in self._views:
            view.update()

    def is_key_down(self, letter):
        return key_state[letter]        # In the stub version, keys are never down

    def is_lamp_on(self, letter):
        return lamp_key_state[letter]        # In the stub version, lamps are always off

    def key_pressed(self, letter):
        if rotors[2].advance():
            if rotors[1].advance():
                rotors[0].advance()

        enc = apply_permutation(ALPHABET.find(letter), rotors[2].get_permutation(), rotors[2].get_offset())
        enc = apply_permutation(ALPHABET.find(enc), rotors[1].get_permutation(), rotors[1].get_offset())
        enc = apply_permutation(ALPHABET.find(enc), rotors[0].get_permutation(), rotors[0].get_offset())

        reflected_enc = REFLECTOR_PERMUTATION[ALPHABET.find(enc)]

        encrypted = apply_permutation(ALPHABET.find(reflected_enc), rotors[0].get_inv_permutation(), rotors[0].get_offset())
        encrypted = apply_permutation(ALPHABET.find(encrypted), rotors[1].get_inv_permutation(), rotors[1].get_offset())
        encrypted = apply_permutation(ALPHABET.find(encrypted), rotors[2].get_inv_permutation(), rotors[2].get_offset())

        self.lamp = encrypted
        key_state[letter] = True
        lamp_key_state[self.lamp] = True
        self.update()

    def key_released(self, letter):
        key_state[letter] = False
        lamp_key_state[self.lamp] = False
        self.update()

    def get_rotor_letter(self, index):
        return rotors[index].get_rotor_letter()          # In the stub version, all rotors are set to "A"

    def rotor_clicked(self, index):
        rotors[index].advance()
        self.update()

def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()
