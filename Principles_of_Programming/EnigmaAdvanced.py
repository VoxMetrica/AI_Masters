import warnings
from enigma import *
import itertools as it
import random as rm
import re

class AdvancedPlugLead:
    """
    This class represents a plug lead on an advanced Enigma machine. The
    primary purpose of this class is to map a pair of letters/numbers to each other, simulating the physical connection of
    an actual plug lead on the plug board of my simulated machine.
    """
    def __init__(self, mapping):
        """
        This init method helps instantiate a Pluglead object so that the encode method can correctly correspond
        characters. The init method also sets up the pair attribute, which is a set containing the two characters
        that are connect to each other, facilitating comparison of AdvancedPlugLeads and allowing plug leads to be rewired.
        :param mapping: String. Must enter a string containing  two upper case letters. The order of the letters
        does not matter - 'AB' is equivalent to 'BA'.
        """
        if type(mapping) != str:
            raise ValueError("You need to enter a string")
        for char in mapping:
            if not (char.isupper() or char.isalpha() or char.isnumeric):
                raise ValueError("Pairs must be composed of upper case letters or numbers")
        # adding extra error catcher after initial one once the input has been stripped so that a non-string input
        # is caught by the custom error before the strip method is applied.
        mapping = mapping.strip()
        if len(mapping) != 2:
            raise ValueError("You need to enter only two characters")
        if mapping[0] == mapping[1]:
            raise ValueError("You cannot connect a character to itself")

        self.pair = {mapping[0], mapping[1]}
        self.first_letter = min(self.pair)
        self.last_letter = max(self.pair)

    def __eq__(self,other):
        if isinstance(other, AdvancedPlugLead):
            return self.pair == other.pair
        return False

    def __hash__(self):
        return hash(frozenset(self.pair))

    def encode(self, character):
        if type(character) != str or not ((character.isalpha() and character.isupper()) or character.isnumeric()) or len(character) != 1:
            raise ValueError("You need to input a single upper case alphabetical string")
        character = character.strip()
        if character in self.pair:
            return next(iter(self.pair - {character}))
        else:
            return character

    def rewire(self,new_mapping):
        if type(new_mapping) != str or not new_mapping.isalpha() or not new_mapping.isupper():
            raise ValueError("You need to enter a string with a pair of upper case letters or numbers")
        # adding extra error catcher after initial one once the input has been stripped so that a non-string input
        # is caught by the custom error before the strip method is applied.
        new_mapping = new_mapping.strip()
        if len(new_mapping) != 2:
            raise ValueError("You need to enter a pair of upper case letters or numbers ")
        self.pair = {new_mapping[0], new_mapping[1]}

class AdvancedPlugboard:
    connection_limit = 18

    def __init__(self,leads=None):
        self.connections = set()
        self.occupied_letters = set()
        if leads is not None:
            for lead in leads:
                self.add(AdvancedPlugLead(lead))

    def add(self, pl):
        if not isinstance(pl,AdvancedPlugLead):
            raise ValueError("You can only add AdvancedPlugLead objects to the plug board")

        if pl.first_letter in self.occupied_letters and pl.last_letter in self.occupied_letters:
            raise ValueError(f"The letters {pl.first_letter} and {pl.last_letter} are already occupied on the plug board. Try again.")
        elif pl.first_letter in self.occupied_letters:
            raise ValueError(f"The letter {pl.first_letter} is already occupied on the plug board. Try again.")
        elif pl.last_letter in self.occupied_letters:
            raise ValueError(f"The letter {pl.last_letter} is already occupied on the plug board. Try again.")
        if pl in self.connections:
            warnings.warn("This plug lead is already connected. The plug board remains unchanged.")
        if len(self.connections) >= self.connection_limit:
            warnings.warn("The plug board has ten connections. Using any more would be cheating.")
            return
        else:
            # Note that a pl that already exists does not alter the plug board because the connections attribute is
            # a set.
            self.connections.add(pl)
            self.occupied_letters |= pl.pair

    def remove(self,pl):
        if not isinstance(pl,AdvancedPlugLead):
            raise ValueError("You can only remove AdvancedPlugLead objects from the plug board")
        if pl in self.connections:
            self.connections.remove(pl)
        else:
            raise ValueError("That plug lead is not in the plugboard")

    def reset(self,leads=None):
        self.connections = set()
        if leads is not None:
            for lead in leads:
                self.add(AdvancedPlugLead(lead))



    def encode(self,character):
        i = 0
        for pl in self.connections:
            i += 1
            if character in pl.pair or i == len(self.connections):
                return pl.encode(character)
        raise ValueError("This input could not be evaluated by the AdvancedPlugLead encode method")

class AdvancedRotor(Rotor):
    lineup = [chr(65 + i) for i in range(26)] + [chr(48 + i) for i in range(10)]
    count_custom_numeric_w_notch = 0
    count_custom_numeric_no_notch = 0

    def __init__(self,rotor_type,ring=1,position='A'):

        if type(ring) != int or ring < 1 or ring > 36:
            raise ValueError("ring must be an integer between 1 and 36 inclusive")
        if not ((position.isalpha() and position.isupper()) or position.isnumeric()):
            raise ValueError("position must be an upper-case character or number")

        self.ring = ring
        self.position = position
        self.rotor_input = rotor_type

        self.tuple_bool = type(rotor_type) == tuple and len(rotor_type) == 2 and len(rotor_type[0]) == 36 and \
                          len(rotor_type[0]) == len(set(rotor_type[0])) and \
                     all([(i.isupper() and i.isalpha()) or i.isnumeric() for i in rotor_type[0]]) and type(rotor_type[1])\
                     == str and ((rotor_type[1].isupper() and rotor_type[1].isalpha()) or rotor_type[1].isnumeric())
        self.list_bool = len(rotor_type) == 36 and all([(i.isupper() and i.isalpha()) or i.isnumeric() for i in rotor_type])

        self.is_reflector = False

        if self.tuple_bool:
            self.mapping = rotor_type[0]
            self.notch = rotor_type[1]
            self.name = f'custom_w_notch_numeric{AdvancedRotor.count_custom_numeric_w_notch}'
            AdvancedRotor.count_custom_numeric_w_notch += 1
        elif self.list_bool:
            self.mapping = rotor_type
            self.notch = None
            self.name = f'custom_no_notch_numeric{AdvancedRotor.count_custom_numeric_no_notch}'
            AdvancedRotor.count_custom_numeric_no_notch += 1
        else:
            super().__init__(rotor_type,ring,position)

    def advance_position(self):
        if self.tuple_bool or self.list_bool:
            if self.position == '9':
                self.position = 'A'
            else:
                predex = AdvancedRotor.lineup.index(self.position)
                postdex = predex + 1
                self.position = AdvancedRotor.lineup[postdex]
        else:
            super().advance_position()

    def encode_right_to_left(self,char):
        if self.tuple_bool or self.list_bool:
            if not ((char.isupper() and char.isalpha()) or char.isnumeric()):
                raise ValueError("The input to this method must be an upper-case character or number")
            return self.mapping[AdvancedRotor.lineup.index(char)]
        else:
            return super().encode_right_to_left(char)

    def encode_left_to_right(self,char):
        if self.tuple_bool or self.list_bool:
            if not ((char.isupper() and char.isalpha()) or char.isnumeric()):
                raise ValueError("The input to this method must be an upper-case character or number")
            return AdvancedRotor.lineup[self.mapping.index(char)]
        else:
            return super().encode_left_to_right(char)

    def encode_offset_rtl(self,char):
        if self.tuple_bool or self.list_bool:
            offset = AdvancedRotor.lineup.index(self.position) - self.ring + 1
            offset_char = AdvancedRotor.lineup[(AdvancedRotor.lineup.index(char) + offset) % 36]
            encode_char = self.encode_right_to_left(offset_char)
            encode_reverse_offset_char = AdvancedRotor.lineup[(AdvancedRotor.lineup.index(encode_char) - offset) % 36]
            return encode_reverse_offset_char
        else:
            return super().encode_offset_rtl(char)

    def encode_offset_ltr(self,char):
        if self.tuple_bool or self.list_bool:
            offset = AdvancedRotor.lineup.index(self.position) - self.ring + 1
            offset_char = AdvancedRotor.lineup[(AdvancedRotor.lineup.index(char) + offset) % 36]
            encode_char = self.encode_left_to_right(offset_char)
            encode_reverse_offset_char = AdvancedRotor.lineup[(AdvancedRotor.lineup.index(encode_char) - offset) % 36]
            return encode_reverse_offset_char
        else:
            return super().encode_offset_ltr(char)

    def valid_reflector(self):
        if self.tuple_bool or self.list_bool:
            if self.notch is not None:
                return False
            dic = {key: value for key, value in zip(AdvancedRotor.lineup, self.mapping)}
            for key in dic:
                if dic[key] != list(dic.keys())[list(dic.values()).index(key)]:
                    return False
            return True
        else:
            return super().valid_reflector()

class Commercial_enigma_advanced:

    def __init__(self,rotors,rings=None,positions=None):
        if len(rotors) not in (4,5):
            raise ValueError("You must enter a list of four or five rotors, including the reflector in the first position")
        self.rotors = [AdvancedRotor(input) for input in rotors]
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
            if type(ring) != int or ring < 1 or ring > 36:
                raise ValueError("ring must be an integer between 1 and 36 inclusive")
            self.rotors[i+1].ring = rings[i]

    def position_settings(self,positions):
        if len(positions) != len(self.rotors) - 1:
            raise ValueError("The number of position settings must match the number of rotors")
        for i in range(len(positions)):
            position = positions[i]
            if not ((position.isalpha() and position.isupper()) or position.isnumeric()):
                raise ValueError("position must be an upper-case character")
            self.rotors[i+1].position = positions[i]

    def get_rotors(self):
        return self.rotors

    def swap_rotors(self,rotors):
        if len(rotors) not in (4,5):
            raise ValueError("You must enter a list of four or five rotors, including the reflector in the first position")
        if len(rotors) != len(self.ring_length) + 1 or len(rotors) != len(self.position_length) + 1:
            raise ValueError("The number of rotors (including reflector) must be one more than the number of ring and position settings. If you want to change the number of rotors in the machine, please reconfigure from scratch.")
        self.rotors = [AdvancedRotor(input) for input in rotors]

class AdvancedEnigma:
    """
    I didn't really have time to create a docstring...
    """


    ring_perms = list(it.product(range(1, 37), repeat=3))
    position_perms = list(it.product(AdvancedRotor.lineup, repeat=3))
    swap_perms = list(it.permutations(range(3), 3))
    max_rand = 5

    def __init__(self,rotors,rings=None,positions=None,plugboard=None,advanced=['S','R','P']):
        self.initials = [rotors,rings,positions]
        self.ce = Commercial_enigma_advanced(rotors,rings,positions)
        if plugboard is None:
            self.pb = None
        else:
            self.pb = AdvancedPlugboard(plugboard)

        self.advanced = advanced

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
        self.pb.add(AdvancedPlugLead(lead))

    def remove_pluglead(self,lead):
        self.pb.remove(AdvancedPlugLead(lead))

    def get_rotors(self):
        return self.ce.rotors

    def get_rotor_types(self):
        return [rotor.rotor_input for rotor in self.get_rotors()]

    def swap_rotors(self,rotors):
        self.ce.swap_rotors(rotors)

    def get_rings(self):
        return [rotor.ring for rotor in self.ce.rotors]

    def get_positions(self):
        return [rotor.position for rotor in self.ce.rotors]

    def reset_to_original_position(self):
        self.ce = Commercial_enigma_advanced(*self.initials)

    def encode_advanced_string(self,string,unpacked):
        if unpacked != sorted(unpacked) or len(unpacked) != len(set(unpacked)) or max(unpacked) > len(string) - 1 or min(unpacked) <= 0:
            raise ValueError("You need to input an ordered list with integers greater than zero and less than the length of the message")

        pre = self.auxiliary_string()

        prencode = self.encode_string(pre)

        current_rotors = self.get_rotor_types()
        just3 = current_rotors[-3:]
        swapped_rotors = current_rotors.copy()[:-3] + [just3[i] for i in AdvancedEnigma.swap_perms[self.swapS]]
        current_rings = self.get_rings()[1:]
        current_positions = self.get_positions()[1:]
        if len(current_rotors) == 5:
            swapped_rings = [current_rings.copy()[0]] + list(AdvancedEnigma.ring_perms[self.swapR])
            swapped_positions = [current_positions.copy()[0]] + list(AdvancedEnigma.position_perms[self.swapP])
        else:
            swapped_rings = AdvancedEnigma.ring_perms[self.swapR]
            swapped_positions = AdvancedEnigma.position_perms[self.swapP]

        unpacked.append(len(string))
        partitioned = [string[i: j] for i, j in zip([0]+unpacked, unpacked)]

        active = True
        encode = ""
        for bit in partitioned:
            if active:
                self.ce = Commercial_enigma_advanced(swapped_rotors,swapped_rings,swapped_positions)
                encode += self.encode_string(bit)
                swapped_positions = self.get_positions()[1:]
                active = not active
            else:
                self.ce = Commercial_enigma_advanced(current_rotors,current_rings,current_positions)
                encode += self.encode_string(bit)
                current_positions = self.get_positions()[1:]
                active = not active

        return prencode + encode

    def decode_advanced_string(self,total_string,unpacked):
        if unpacked != sorted(unpacked) or len(unpacked) != len(set(unpacked)) or min(unpacked) <= 0:
            raise ValueError("You need to input an ordered list with integers greater than zero and less than the length of the message")

        jumbled_instructions = self.encode_string(total_string)
        # offending line
        end_instruction = re.search(r'([A-Z])\1',jumbled_instructions).span()[1]
        instruction = jumbled_instructions[:end_instruction]
        message = total_string[end_instruction:]

        if max(unpacked) > len(message) - 1:
            raise ValueError("You need to input an ordered list with integers greater than zero and less than the length of the message")

        settings = [int(i) for i in re.findall(r'\d+',instruction)]

        self.ce = Commercial_enigma_advanced(*self.initials)

        self.encode_string(instruction)

        current_rotors = self.get_rotor_types()
        for setting, param in zip(settings,self.advanced):
            if param == 'S':
                just3 = current_rotors[-3:]
                swapped_rotors = current_rotors.copy()[:-3] + [just3[i] for i in AdvancedEnigma.swap_perms[setting]]
            elif param == 'R':
                current_rings = self.get_rings()[1:]
                if len(current_rotors) == 5:
                    swapped_rings = [current_rings.copy()[0]] + list(AdvancedEnigma.ring_perms[setting])
                else:
                    swapped_rings = AdvancedEnigma.ring_perms[setting]
            elif param == 'P':
                current_positions = self.get_positions()[1:]
                if len(current_rotors) == 5:
                    swapped_positions = [current_positions.copy()[0]] + list(AdvancedEnigma.position_perms[setting])
                else:
                    swapped_positions = AdvancedEnigma.position_perms[setting]

        unpacked.append(len(message))
        partitioned = [message[i: j] for i, j in zip([0]+unpacked, unpacked)]

        active = True
        encode = ""
        for bit in partitioned:
            if active:
                self.ce = Commercial_enigma_advanced(swapped_rotors,swapped_rings,swapped_positions)
                encode += self.encode_string(bit)
                swapped_positions = self.get_positions()[1:]
                active = not active
            else:
                self.ce = Commercial_enigma_advanced(current_rotors,current_rings,current_positions)
                encode += self.encode_string(bit)
                current_positions = self.get_positions()[1:]
                active = not active
        return encode

    def auxiliary_string(self):
        alphabet = [chr(65+i) for i in range(26)]
        aux_string = ""
        for instruction in self.advanced:
            aux_string += self.random_gen(instruction)
            num_letters = rm.randint(1, AdvancedEnigma.max_rand)
            random_letters = rm.sample(alphabet, num_letters)
            aux_string += "".join(random_letters)
        repeater = rm.choice(alphabet)
        aux_string += repeater*2
        return aux_string

    def random_gen(self,instruction):
        if instruction == 'S':
            self.swapS = rm.randint(0,len(AdvancedEnigma.swap_perms)-1)
            return str(self.swapS)
        elif instruction == 'R':
            self.swapR = rm.randint(0,len(AdvancedEnigma.ring_perms)-1)
            return str(self.swapR)
        elif instruction == 'P':
            self.swapP = rm.randint(0,len(AdvancedEnigma.position_perms)-1)
            return str(self.swapP)
        else:
            raise ValueError('Inputted advanced instructions must be an ordered list of S, R, and P')


if __name__ == '__main__':
    rtr0 = (['E','K','M','F','L','G','D','Q','V','Z','N','T','O','0','W','Y','H','X','U','S','P','A','I','B','R','C','J','3','4','6','1','2','7','5','9','8'],'B')
    rtr1 = ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J','3','4','6','1','2','7','5','9','0','8']
    rtr2 = ['E','K','M','F','L','G','D','Q','V','Z','N','T','O','W','Y','H','X','U','S','P','A','I','B','R','C','J']
    rflctr = ['F','V','P','J','I','A','O','Y','E','D','R','Z','X','W','G','C','T','K','U','Q','S','B','N','M','H','L','0','6','2','7','9','8','1','3','5','4']
    AR0 = AdvancedRotor(rtr0,position='9')
    assert(AR0.position == '9')
    AR0.advance_position()
    assert(AR0.position == 'A')
    AR0.advance_position()
    assert(AR0.position == 'B')
    assert(AR0.check_notch())
    AR = AdvancedRotor(rtr2,position='S')
    assert(AR.position == 'S')
    AR.advance_position()
    assert(AR.position == 'T')

    assert(AR0.encode_right_to_left('B') == 'K')
    assert(AR0.encode_left_to_right('C') == 'Z')

    AR1 = AdvancedRotor(rtr1,ring=1,position='B')
    R1 = AdvancedRotor('I',ring=1,position='B')
    assert(AR1.encode_offset_rtl('J') == 'M')
    assert(R1.encode_offset_rtl('J') == 'M')

    assert(AR1.encode_offset_ltr('B') == 'X')
    assert(R1.encode_offset_ltr('B') == 'X')
    reflecrotor = AdvancedRotor(rflctr)
    assert(AR1.valid_reflector() == False)
    assert(reflecrotor.valid_reflector())
    assert(not AR0.valid_reflector())

    cer1 = (['4','K','M','F','L','9','0','D','Q','V','Z','N','T','O','W','Y','5','X','U','S','P','A','I','B','R','C','J','3','E','6','1','2','7','H','G','8'],'4')
    cer2 = (['4','K','M','W','L','9','D','Q','V','Z','N','T','O','F','Y','0','5','X','U','S','P','1','I','B','R','C','J','3','E','6','A','2','7','H','G','8'],'J')
    cer3 = ['4','K','C','0','W','L','9','D','Q','V','Z','N','T','O','F','Y','5','X','U','S','P','1','I','B','R','M','J','3','E','6','A','2','7','H','G','8']

    cea = Commercial_enigma_advanced([rflctr,cer3,cer2,cer1,rtr0])
    string = cea.encode_string('HEREISASTRINGABOUTFACEBOOK23524')
    cea = Commercial_enigma_advanced([rflctr, cer3, cer2, cer1, rtr0])
    assert(cea.encode_string(string) == 'HEREISASTRINGABOUTFACEBOOK23524')

    ae = AdvancedEnigma([rflctr,cer3,cer2,cer1],[3,31,23],['4','D','T'],['8U','RF','2M'])
    string = ae.encode_string('THEREARESOMANYSTRINGTOTESTTHISSTUFFLIKEMAYBE1994OR47321')
    ae = AdvancedEnigma([rflctr, cer3, cer2, cer1], [3, 31, 23], ['4', 'D', 'T'],['8U','RF','2M'])
    assert(ae.encode_string(string) == 'THEREARESOMANYSTRINGTOTESTTHISSTUFFLIKEMAYBE1994OR47321')

    lead = AdvancedPlugLead("A8")
    assert(lead.encode("A") == "8")
    assert(lead.encode("8") == "A")

    lead = AdvancedPlugLead("DA")
    assert(lead.encode("A") == "D")
    assert(lead.encode("D") == "A")

    lead = AdvancedPlugLead("69")
    assert(lead.encode("6") == "9")
    assert(lead.encode("9") == "6")

    plugboard = AdvancedPlugboard()

    plugboard.add(AdvancedPlugLead("SZ"))
    plugboard.add(AdvancedPlugLead("GT"))
    plugboard.add(AdvancedPlugLead("DV"))
    plugboard.add(AdvancedPlugLead("KU"))
    plugboard.add(AdvancedPlugLead("80"))
    plugboard.add(AdvancedPlugLead("W7"))

    assert(plugboard.encode("K") == "U")
    assert(plugboard.encode("A") == "A")
    assert(plugboard.encode("7") == "W")
    assert(plugboard.encode("8") == "0")

    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1], [3, 31, 23], ['4', 'D', 'T'],['8U','RF','2M'])
    advanced_string = ade.encode_advanced_string("HEREISACLASSICSTRINGHELLOWORLD", [3, 7, 10])
    print(advanced_string)
    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1], [3, 31, 23], ['4', 'D', 'T'],['8U','RF','2M'])
    print(ade.encode_string(advanced_string))
    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1], [3, 31, 23], ['4', 'D', 'T'],['8U','RF','2M'])
    print(ade.decode_advanced_string(advanced_string,[3,7,10]))

    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1,rtr0], [3, 31, 23,5], ['4', 'D', 'T','G'],['8U','RF','2M'])
    advanced_string = ade.encode_advanced_string("HEREISACLASSICSTRINGHELLOWORLD", [3, 7, 10])
    print(advanced_string)
    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1,rtr0], [3, 31, 23,5], ['4', 'D', 'T','G'],['8U','RF','2M'])
    print(ade.encode_string(advanced_string))
    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1,rtr0], [3, 31, 23,5], ['4', 'D', 'T','G'],['8U','RF','2M'])
    print(ade.decode_advanced_string(advanced_string,[3,7,10]))

    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1, rtr0], [3, 31, 23, 5], ['4', 'D', 'T', 'A'], ['8U', 'RF', '2M'],
                         ['P', 'R', 'S'])
    advanced_string = ade.encode_advanced_string("HEREISACLASSICSTRINGHELLOWORLD2023", [3, 7, 10])
    ade = AdvancedEnigma([rflctr, cer3, cer2, cer1, rtr0], [3, 31, 23, 5], ['4', 'D', 'T', 'A'], ['8U', 'RF', '2M'],
                         ['P', 'R', 'S'])
    assert (ade.decode_advanced_string(advanced_string, [3, 7, 10]) == "HEREISACLASSICSTRINGHELLOWORLD2023")