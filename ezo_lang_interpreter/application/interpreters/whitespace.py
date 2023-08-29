import time
from application.models import StatusCodes
from .utilites import parse_to_int_array, parse_to_str_representation, parse_int_str_map_to_str_representation, parse_to_int_str_map
from ezo_lang_interpreter.settings import APPLICATION_SETTINGS
from bitstring import BitArray


def filter_code(s: str) -> str:
    output = ""
    for letter in s:
        if letter == "\n" or letter == "\t" or letter == " ":
            output += letter
    return output

COMMANDS = {
    "\n": 3,
    "\t": 2,
    " ": 1
}

class WhitespaceInterperet():

    def __init__(self, program_instance, memory_input=None):
        self.max_interations = APPLICATION_SETTINGS["WHITESPACE"]["MAX_ITERATIONS"]
        self.max_output_size = APPLICATION_SETTINGS["WHITESPACE"]["OUTPUT_MAX_SIZE"]

        self.max_stack_size = APPLICATION_SETTINGS["WHITESPACE"]["HEAP_SIZE"]
        self.max_labels_size = APPLICATION_SETTINGS["WHITESPACE"]["LABELS_SIZE"]

        self.code = filter_code(program_instance['code'])
        self.name = program_instance['name']
        self.output = program_instance['output']
        self.pointer = program_instance['pointer']

        self.command_value = 0

        self.memory_stack = parse_to_int_array(program_instance['memory_stack'])
        self.memory_stack_pointer = program_instance['memory_stack_pointer']

        if memory_input != None:
            self.push(memory_input)

        self.heap = parse_to_int_str_map(program_instance["heap"])
        self.labels = parse_to_int_str_map(program_instance["labels"])

        self.subroutines_stack = parse_to_int_array(program_instance['subroutines_stack'])
        self.subroutines_stack_pointer = program_instance['subroutines_stack_pointer']

        self.status_code = program_instance['status_code']

        self.code_length = len(self.code)

        self.commands_mapping = {
            # Stack manipulation
            5: self.push_value_to_stack,
            29: self.duplicate,
            25: self.duplicate_to_top_of_the_stack,
            30: self.swap,
            31: self.pop_or_empty,
            27: self.push_n_times_to_stack,

            # Arithmetic
            149: self.add,
            150: self.sub,
            151: self.multiply,
            153: self.divide,
            154: self.modulo,

            # Heap control
            41: self.add_to_heap,
            42: self.get_from_heap,

            # Flow control
            53: self.add_label,
            55: self.get_label,
            54: self.start_subroutine,
            57: self.get_label_if_equal,
            58: self.get_label_if_negative,
            59: self.end_subroutine,
            63: self.end_program,

            # I/O stream
            181: self.character_output,
            182: self.numeric_output,
            185: self.character_input,
            186: self.numeric_input
        }

        
    def retrieve(self):
        return dict(
            code = self.code,
            name = self.name,
            output = self.output,
            pointer = self.pointer,

            memory_stack = parse_to_str_representation(self.memory_stack),
            memory_stack_pointer = self.memory_stack_pointer,

            heap = parse_int_str_map_to_str_representation(self.heap),
            labels = parse_int_str_map_to_str_representation(self.labels),

            subroutines_stack = parse_to_str_representation(self.subroutines_stack),
            subroutines_stack_pointer = self.subroutines_stack_pointer,

            status_code = self.status_code
        )


    def retrieve_instance(self, instance):
        instance.code = self.code
        instance.name = self.name
        instance.output = self.output
        instance.pointer = self.pointer

        instance.memory_stack = parse_to_str_representation(self.memory_stack)
        instance.memory_stack_pointer = self.memory_stack_pointer

        instance.heap = parse_int_str_map_to_str_representation(self.heap)
        instance.labels = parse_int_str_map_to_str_representation(self.labels)

        instance.subroutines_stack = parse_to_str_representation(self.subroutines_stack)
        instance.subroutines_stack_pointer = self.subroutines_stack_pointer

        instance.status_code = self.status_code

        return instance


    def run(self):
        it = 0
        while self.pointer < self.code_length and self.status_code == StatusCodes.running:
            try:
                current_symbol = self.code[self.pointer]
            except:
                self.status_code = StatusCodes.no_end_instruction            

            self.add_symbol_to_command(current_symbol)
            
            if self.command_value > 1024:
                self.status_code = StatusCodes.wrong_program_code

            if self.command_value in self.commands_mapping:
                self.run_command(self.commands_mapping[self.command_value])

            self.pointer += 1
            it += 1
            if it >= self.max_interations: self.status_code = StatusCodes.out_of_time
        
        if self.status_code == StatusCodes.running: self.status_code = StatusCodes.wrong_program_code
       

    #-----------------#
    # STACK FUNCTIONS #
    #-----------------#

    def push(self, value): 
        self.memory_stack_pointer += 1
        try:
            self.memory_stack[self.memory_stack_pointer] = value
        except:
            self.status_code = StatusCodes.out_of_memory


    def pop(self):
        try:
            output = self.memory_stack[self.memory_stack_pointer]
            self.memory_stack_pointer -= 1
            return output
        except:
            self.status_code = StatusCodes.out_of_memory


    def pop_or_empty(self):
        if self.memory_stack_pointer < 0: return 0
        else: return self.pop()


    def peek(self, idx=None):
        if idx == None:
            idx = self.memory_stack_pointer
        try:
            return self.memory_stack[idx]
        except:
            self.status_code = StatusCodes.out_of_memory


    # ------------------ #
    # NUMERIC OPERATIONS #
    # ------------------ #

    def add_symbol_to_command(self, symbol):
        self.command_value = (self.command_value * 4) + COMMANDS[symbol]


    def clear_command(self):
        self.command_value = 0


    def get_number_argument(self):
    
        def get_signed_integer(s):
            if len(s) == 0: 
                self.status_code = StatusCodes.no_end_instruction
                return
            
            sign = -1 if s[0] == "1" else 1
            output = 0
            multiplier = 1
            for num in s[-1:0:-1]:
                output += multiplier if num == '1' else 0
                multiplier *= 2
            return sign * output if sign > 0 else sign * output - 1

        self.pointer += 1
        output = ""
        while self.code[self.pointer] != '\n':
            output += "1" if self.code[self.pointer] == '\t' else "0"
            self.pointer += 1
        return get_signed_integer(output)

    #-------------------#
    # PROGRAM FUNCTIONS #
    #-------------------#

    
    def run_command(self, f):
        f()
        # print(f.__name__)
        self.clear_command()


    def push_value_to_stack(self):
        value = self.get_number_argument()
        self.push(value)


    def duplicate(self):
        a = self.pop_or_empty()
        self.push(a)
        self.push(a)


    def duplicate_to_top_of_the_stack(self):
        idx = self.get_number_argument()
        try:
            self.push(self.peek(idx))
        except:
            self.status_code = StatusCodes.out_of_memory

    
    def swap(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(a)
        self.push(b)


    def push_n_times_to_stack(self):
        n = self.get_number_argument()
        for _ in range(n):
            self.push(n)


    def add(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b + a)


    def sub(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b - a)


    def multiply(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b * a)


    def divide(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b // a)


    def modulo(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b % a)


    def add_to_heap(self):
        value = self.pop_or_empty()
        address = self.pop_or_empty()
        self.heap[address] = value


    def get_from_heap(self):
        address = self.pop_or_empty()
        self.push(self.heap[address])


    def add_label(self):
        pointer = self.pointer - 3

        label = self.get_number_argument()
        self.labels[label] = pointer

    
    def get_label(self):
        label = self.get_number_argument()
        try:
            self.pointer = self.labels[label]
        except:
            self.status_code = StatusCodes.label_does_not_exist
       
        
    def start_subroutine(self):
        label = self.get_number_argument()
        try:
            self.subroutines_stack_pointer += 1
            self.subroutines_stack[self.subroutines_stack_pointer] = self.pointer
        except:
            self.status_code = StatusCodes.out_of_subroutines_memory

        try:
            self.pointer = self.labels[label]
        except:
            self.status_code = StatusCodes.label_does_not_exist


    def get_label_if_equal(self):
        if not self.peek() == 0: return
        self.get_label()
        

    def get_label_if_negative(self):
        if not self.peek() < 0: return
        self.get_label()
        

    def end_subroutine(self):
        if self.subroutines_stack_pointer < 0:
            return
        else:
            self.pointer = self.subroutines_stack[self.subroutines_stack_pointer]
            self.subroutines_stack_pointer -= 1


    def end_program(self):
        self.status_code = StatusCodes.finished


    def character_output(self):
        self.output += chr(self.pop_or_empty() % 65536)


    def numeric_output(self):
        self.output += str(self.pop_or_empty())


    def character_input(self):
        self.status_code = StatusCodes.waiting_for_char_input


    def numeric_input(self):
        self.status_code = StatusCodes.waiting_for_num_input