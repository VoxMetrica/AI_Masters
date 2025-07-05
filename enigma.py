from abc import ABC, abstractmethod
import warnings
class PlugLead:
    """
    This class represents a plug lead on a classic Enigma machine, with all the restrictions entailed therein. The
    primary purpose of this class is to map a __pair of letters to each other, simulating the physical connection of
    an actual plug lead on the plug board of a real enigma machine.

    The PlugLead class simulates a physical connection between two letters on the Enigma machine's plugboard.
    """
    def __init__(self, mapping):
        """
        This init method helps instantiate a Pluglead object so that the encode method can correctly correspond
        characters. The init method also sets up the __pair attribute, which is a set containing the two characters
        that are connect to each other, facilitating comparison of PlugLeads and allowing plug leads to be rewired.
        :param mapping: String. Must enter a string containing  two upper case letters. The order of the letters
        does not matter - 'AB' is equivalent to 'BA'.
        """
        if type(mapping) != str or not mapping.isalpha() or not mapping.isupper():
            raise ValueError("You need to enter a string with a __pair of upper case alphabetical characters")
        # adding extra error catcher after initial one once the input has been stripped so that a non-string input
        # is caught by the custom error before the strip method is applied.
        mapping = mapping.strip()
        if len(mapping) != 2:
            raise ValueError("You need to enter a pair of upper case alphabetical characters")
        if mapping[0] == mapping[1]:
            raise ValueError("You cannot connect a character to itself")

        self.__pair = {mapping[0], mapping[1]}
        self.__first_letter = min(self.__pair)
        self.__last_letter = max(self.__pair)

    def __eq__(self,other):
        if isinstance(other, PlugLead):
            return self.__pair == other.__pair
        return False

    def __hash__(self):
        return hash(frozenset(self.__pair))

    def encode(self, character):
        if type(character) != str or not character.isalpha() or not character.isupper() or len(character) != 1:
            raise ValueError("You need to input a single upper case alphabetical string")
        character = character.strip()
        if character in self.__pair:
            return next(iter(self.__pair - {character}))
        else:
            return character

    def rewire(self,new_mapping):
        if type(new_mapping) != str or not new_mapping.isalpha() or not new_mapping.isupper():
            raise ValueError("You need to enter a string with a __pair of upper case alphabetical characters")
        # adding extra error catcher after initial one once the input has been stripped so that a non-string input
        # is caught by the custom error before the strip method is applied.
        new_mapping = new_mapping.strip()
        if len(new_mapping) != 2:
            raise ValueError("You need to enter a __pair of upper case alphabetical characters")
        self.__pair = {new_mapping[0], new_mapping[1]}

class Plugboard:
    connection_limit = 10

    def __init__(self,leads=None):
        self.__connections = set()
        self.__occupied_letters = set()
        if leads is not None:
            for lead in leads:
                self.add(PlugLead(lead))

    def add(self, pl):
        if not isinstance(pl,PlugLead):
            raise ValueError("You can only add PlugLead objects to the plug board")

        if pl._PlugLead__first_letter in self.__occupied_letters and pl._PlugLead__last_letter in self.__occupied_letters:
            raise ValueError(f"The letters {pl.__first_letter} and {pl.__last_letter} are already occupied on the plug board. Try again.")
        elif pl._PlugLead__first_letter in self.__occupied_letters:
            raise ValueError(f"The letter {pl._PlugLead__first_letter} is already occupied on the plug board. Try again.")
        elif pl._PlugLead__last_letter in self.__occupied_letters:
            raise ValueError(f"The letter {pl._PlugLead__last_letter} is already occupied on the plug board. Try again.")
        if pl in self.__connections:
            warnings.warn("This plug lead is already connected. The plug board remains unchanged.")
        if len(self.__connections) >= self.connection_limit:
            warnings.warn("The plug board has ten __connections. Using any more would be cheating.")
            return
        else:
            # Note that a pl that already exists does not alter the plug board because the __connections attribute is
            # a set.
            self.__connections.add(pl)
            self.__occupied_letters |= pl._PlugLead__pair

    def remove(self,pl):
        if not isinstance(pl,PlugLead):
            raise ValueError("You can only remove PlugLead objects from the plug board")
        if pl in self.__connections:
            self.__connections.remove(pl)
        else:
            raise ValueError("That plug lead is not in the plugboard")

    def reset(self,leads=None):
        self.__connections = set()
        if leads is not None:
            for lead in leads:
                self.add(PlugLead(lead))



    def encode(self,character):
        i = 0
        for pl in self.__connections:
            i += 1
            if character in pl._PlugLead__pair or i == len(self.__connections):
                return pl.encode(character)
        raise ValueError("This input could not be evaluated by the PlugLead encode method")
# You will need to write more classes, which can be done here or in separate files, you choose.

class Rotor:
    count_custom_w_notch = 0
    count_custom_no_notch = 0

    def __init__(self,rotor_type,ring=1,position='A'):
        if type(ring) != int or ring < 1 or ring > 26:
            raise ValueError("ring must be an integer between 1 and 26 inclusive")
        if not position.isalpha() or not position.isupper():
            raise ValueError("position must be an upper-case character")
        self.name = rotor_type
        self.ring = ring
        self.position = position
        self.double_step = False
        if rotor_type == 'I':
            self.mapping = ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J']
            self.notch = 'Q'
            self.is_reflector = False
        elif rotor_type == 'II':
            self.mapping = ['A','J','D','K','S','I','R','U','X','B','L','H','W','T','M','C','Q','G','Z','N','P','Y','F','V','O','E']
            self.notch = 'E'
            self.is_reflector = False
        elif rotor_type == 'III':
            self.mapping = ['B','D','F','H','J','L','C','P','R','T','X','V','Z','N','Y','E','I','W','G','A','K','M','U','S','Q','O']
            self.notch = 'V'
            self.is_reflector = False
        elif rotor_type == 'IV':
            self.mapping = ['E','S','O','V','P','Z','J','A','Y','Q','U','I','R','H','X','L','N','F','T','G','K','D','C','M','W','B']
            self.notch = 'J'
            self.is_reflector = False
        elif rotor_type == 'V':
            self.mapping = ['V','Z','B','R','G','I','T','Y','U','P','S','D','N','H','L','X','A','W','M','J','Q','O','F','E','C','K']
            self.notch = 'Z'
            self.is_reflector = False
        elif rotor_type == 'Beta':
            self.mapping = ['L','E','Y','J','V','C','N','I','X','W','P','B','Q','M','D','R','T','A','K','Z','G','F','U','H','O','S']
            self.notch = None
            self.is_reflector = False
        elif rotor_type == 'Gamma':
            self.mapping = ['F','S','O','K','A','N','U','E','R','H','M','B','T','I','Y','C','W','L','Q','P','Z','X','V','G','J','D']
            self.notch = None
            self.is_reflector = False
        elif rotor_type == 'A':
            self.mapping = ['E','J','M','Z','A','L','Y','X','V','B','W','F','C','R','Q','U','O','N','T','S','P','I','K','H','G','D']
            self.notch = None
            self.is_reflector = True
        elif rotor_type == 'B':
            self.mapping = ['Y','R','U','H','Q','S','L','D','P','X','N','G','O','K','M','I','E','B','F','Z','C','W','V','J','A','T']
            self.notch = None
            self.is_reflector = True
        elif rotor_type == 'C':
            self.mapping = ['F','V','P','J','I','A','O','Y','E','D','R','Z','X','W','G','C','T','K','U','Q','S','B','N','M','H','L']
            self.notch = None
            self.is_reflector = True
        elif type(rotor_type) == tuple and type(rotor_type[0]) == list and len(rotor_type[0]) == 26 and all([letter.isalpha() and letter.isupper() for letter in rotor_type[0]]) and type(rotor_type[1]) == str and rotor_type[1].isalpha() and rotor_type[1].isupper() and len(rotor_type[1]) == 1:
            self.mapping = rotor_type[0]
            self.notch = rotor_type[1]
            self.is_reflector = False
            self.name = f'custom_w_notch{Rotor.count_custom_w_notch}'
            Rotor.count_custom_w_notch += 1
        elif type(rotor_type) == list and len(rotor_type) == 26:
            self.mapping = rotor_type
            self.notch = None
            self.is_reflector = False
            self.name = f'custom_no_notch{Rotor.count_custom_no_notch}'
            Rotor.count_custom_no_notch += 1
        else:
            raise ValueError(f"The inputted type - {rotor_type} - is invalid")

    def advance_position(self):
        if self.position == 'Z':
            self.position = 'A'
        else:
            self.position = chr(ord(self.position) + 1)

    def check_notch(self):
        return self.position == self.notch

    def encode_right_to_left(self,char):
        if not char.isupper() or not char.isalpha():
            raise ValueError("The input to this method must be an upper-case character")
        return self.mapping[ord(char) - ord('A')]

    def encode_left_to_right(self,char):
        if not char.isupper() or not char.isalpha():
            raise ValueError("The input to this method must be an upper-case character")
        return chr(self.mapping.index(char) + ord('A'))

    def encode_offset_rtl(self,char):
        offset = ord(self.position) - ord('A') - self.ring + 1
        offset_char= chr(((ord(char) - 65 + offset) % 26) + 65)
        encode_char = self.encode_right_to_left(offset_char)
        encode_reverse_offset_char = chr(((ord(encode_char) - 65 - offset) % 26) + 65)
        return encode_reverse_offset_char

    def encode_offset_ltr(self,char):
        offset = ord(self.position) - ord('A') - self.ring + 1
        offset_char = chr(((ord(char) - 65 + offset) % 26) + 65)
        encode_char = self.encode_left_to_right(offset_char)
        encode_reverse_offset_char = chr(((ord(encode_char) - 65 - offset) % 26) + 65)
        return encode_reverse_offset_char

    def valid_reflector(self):
        abc = [chr(65 + i) for i in range(26)]
        if self.notch is not None:
            return False
        dic = {key: value for key, value in zip(abc, self.mapping)}
        for key in dic:
            if dic[key] != list(dic.keys())[list(dic.values()).index(key)]:
                return False
        return True

class Commercial_enigma:

    def __init__(self,rotors,rings=None,positions=None):
        if len(rotors) not in (4,5):
            raise ValueError("You must enter a list of four or five rotors, including the reflector in the first position")
        self.rotors = [Rotor(input) for input in rotors]
        if not self.rotors[0].is_reflector:
            if self.rotors[0].valid_reflector():
                self.rotors[0].is_reflector = True
            else:
                raise ValueError("The reflector is not a valid reflector")
        for rotor in self.rotors[1:]:
            if rotor.is_reflector:
                raise ValueError("You cannot have a reflector in the rotor positions")
        self.ring_length = len(rotors) - 1
        if rings is not None:
            self.ring_settings(rings)
        self.position_length = len(rotors) - 1
        if positions is not None:
            self.position_settings(positions)
        # NOT NECESSARY?
        # rotors[-2].double_step = True

    def rotate(self):
        rot1 = self.rotors[-1].position == self.rotors[-1].notch
        rot2 = self.rotors[-2].position == self.rotors[-2].notch

        self.rotors[-1].advance_position()

        if rot1:
            self.rotors[-2].advance_position()

        if rot2:
            if not rot1:
                self.rotors[-2].advance_position()

            self.rotors[-3].advance_position()

    def encode(self,char):
        self.rotate()
        for i in range(-1,-len(self.rotors)-1,-1):
            char = self.rotors[i].encode_offset_rtl(char)

        for i in range(1,len(self.rotors)):
            char = self.rotors[i].encode_offset_ltr(char)

        return char

    def encode_string(self,string):
        out = ""
        for char in string:
            out += self.encode(char)

        return out

    def ring_settings(self,rings):
        if len(rings) != len(self.rotors) - 1:
            raise ValueError("The number of ring settings must match the number of rotors")
        for i in range(len(rings)):
            ring = rings[i]
            if type(ring) != int or ring < 1 or ring > 26:
                raise ValueError("ring must be an integer between 1 and 26 inclusive")
            self.rotors[i+1].ring = rings[i]

    def position_settings(self,positions):
        if len(positions) != len(self.rotors) - 1:
            raise ValueError("The number of position settings must match the number of rotors")
        for i in range(len(positions)):
            position = positions[i]
            if not position.isalpha() or not position.isupper():
                raise ValueError("position must be an upper-case character")
            self.rotors[i+1].position = positions[i]

    def get_rotors(self):
        return self.rotors

    def swap_rotors(self,rotors):
        if len(rotors) not in (4,5):
            raise ValueError("You must enter a list of four or five rotors, including the reflector in the first position")
        if len(rotors) != len(self.ring_length) + 1 or len(rotors) != len(self.position_length) + 1:
            raise ValueError("The number of rotors (including reflector) must be one more than the number of ring and position settings. If you want to change the number of rotors in the machine, please reconfigure from scratch.")
        self.rotors = [Rotor(input) for input in rotors]



class Enigma:

    def __init__(self,rotors,rings=None,positions=None,plugboard=None):
        self.ce = Commercial_enigma(rotors,rings,positions)
        if plugboard is None:
            self.pb = None
        else:
            self.pb = Plugboard(plugboard)

    def encode(self,char):
        if self.pb is None:
            return self.ce.encode(char)
        else:
            char = self.pb.encode(char)
            char = self.ce.encode(char)
            char = self.pb.encode(char)
            return char

    def encode_string(self,string):
        out = ""
        for char in string:
            out += self.encode(char)

        return out

    def ring_settings(self,rings):
        self.ce.ring_settings(rings)

    def position_settings(self,positions):
        self.ce.position_settings(positions)

    def replace_plugboard(self,plugboard=None):
        self.pb.reset(plugboard)

    def add_pluglead(self,lead):
        self.pb.add(PlugLead(lead))

    def remove_pluglead(self,lead):
        self.pb.remove(PlugLead(lead))

    def get_rotors(self):
        return self.ce.rotors

    def swap_rotors(self,rotors):
        self.ce.swap_rotors(rotors)

    def get_rings(self):
        return [rotor.ring for rotor in self.ce.rotors]

    def get_positions(self):
        return [rotor.position for rotor in self.ce.rotors]

if __name__ == "__main__":
    #You can use this section to write tests and demonstrations of your enigma code.
    ce = Commercial_enigma(['C','I','II','III','IV'],[7,11,15,19],['Q','E','V','Z'])
    print(ce.encode('Z'))


    plugboard = Plugboard()

    plugboard.add(PlugLead("SZ"))
    plugboard.add(PlugLead("GT"))
    plugboard.add(PlugLead("DV"))
    plugboard.add(PlugLead("KU"))

    print(plugboard.encode("A"))

    assert (plugboard.encode("K") == "U")
    assert (plugboard.encode("A") == "A")

    print(len({PlugLead('AB'),PlugLead('BA')}))

    AB = PlugLead('AB')
    CD = PlugLead('CD')

    print(f'should be false: {AB == CD}')

    CD.rewire('BA')

    print(f'should be true: {AB == CD}')

    pb = Plugboard()
    pb.add(PlugLead("AB"))
    pb.add(PlugLead("CD"))
    print(len(pb._Plugboard__connections))

    rotor = Rotor("I")
    assert (rotor.encode_right_to_left("A") == "E")
    assert (rotor.encode_left_to_right("A") == "U")

    enigma = Enigma(['A','IV','V','Beta','I'],[18,24,3,5],['E','Z','G','P'],['PC','XZ','FM','QA','ST','NB','HY','OR','EV','IU'])
    print(enigma.encode_string('BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI'))

    enigma = Enigma(['A','IV','V','Beta','I'])
    print(enigma.get_rotors()[0].mapping)