from application.models import StatusCodes
from .utilites import parse_to_int_array, parse_to_str_representation
from ezo_lang_interpreter.settings import APPLICATION_SETTINGS


class BrainfuckInterperet():

    def __init__(self, program_instance, memory_input=0):
        self.max_interations = APPLICATION_SETTINGS["BRAINFUCK"]["MAX_ITERATIONS"]
        self.max_output_size = APPLICATION_SETTINGS["BRAINFUCK"]["OUTPUT_MAX_SIZE"]

        self.code = program_instance['code']
        self.name = program_instance['name']
        self.output = program_instance['output']
        self.pointer = program_instance['pointer']

        self.loop_stack = parse_to_int_array(program_instance['loop_stack'])
        self.loop_stack_pointer = program_instance['loop_stack_pointer']

        self.memory_array = parse_to_int_array(program_instance['memory_array'])
        self.memory_array_pointer = program_instance['memory_array_pointer']

        self.memory_array[self.memory_array_pointer] = memory_input

        self.status_code = program_instance['status_code']

        self.code_length = len(self.code)
        self.loop_stack_size = len(self.loop_stack)
        self.memory_array_size = len(self.memory_array)

        
    def retrieve(self):
        return dict(
            code = self.code,
            name = self.name,
            output = self.output,
            pointer = self.pointer,
            loop_stack = parse_to_str_representation(self.loop_stack),
            loop_stack_pointer = self.loop_stack_pointer,
            memory_array = parse_to_str_representation(self.memory_array),
            memory_array_pointer = self.memory_array_pointer,
            status_code = self.status_code
        )


    def retrieve_instance(self, instance):
        instance.output = self.output
        instance.pointer = self.pointer
        instance.loop_stack = parse_to_str_representation(self.loop_stack)
        instance.loop_stack_pointer = self.loop_stack_pointer
        instance.memory_array = parse_to_str_representation(self.memory_array)
        instance.memory_array_pointer = self.memory_array_pointer
        instance.status_code = self.status_code

        return instance


    def run(self):
        it = 0
        while self.pointer < self.code_length and self.status_code == StatusCodes.running:
            current_command = self.code[self.pointer]
            if current_command == '+': self.add()
            elif current_command == '-': self.sub()
            elif current_command == '<': self.move_left()
            elif current_command == '>': self.move_right()
            elif current_command == '.': self.output_char()
            elif current_command == ',': self.input_char()
            elif current_command == '[': self.start_loop()
            elif current_command == ']': self.finish_loop()

            self.pointer += 1
            it += 1
            if it >= self.max_interations: self.status_code = StatusCodes.out_of_time
        
        if self.status_code == StatusCodes.running: self.status_code = StatusCodes.finished


    def add(self):
        if (self.memory_array[self.memory_array_pointer] >= 255): self.memory_array[self.memory_array_pointer] = 0
        else: self.memory_array[self.memory_array_pointer] += 1


    def sub(self):
        if (self.memory_array[self.memory_array_pointer] <= 0): self.memory_array[self.memory_array_pointer] = 255
        else: self.memory_array[self.memory_array_pointer] -= 1


    def move_left(self):
        if (self.memory_array_pointer <= 0): self.memory_array_pointer = self.memory_array_size - 1
        else: self.memory_array_pointer -= 1


    def move_right(self):
        if (self.memory_array_pointer >= self.memory_array_size - 1): self.memory_array_pointer = 0
        else: self.memory_array_pointer += 1


    def output_char(self):
        self.output += chr(self.memory_array[self.memory_array_pointer])
        if len(self.output) >= self.max_output_size:
            self.status_code = StatusCodes.output_out_of_memory
        

    def input_char(self):
        self.status_code = StatusCodes.waiting_for_char_input


    def start_loop(self):
        if (self.memory_array[self.memory_array_pointer] != 0):
            self.loop_stack_pointer += 1
            try:
                self.loop_stack[self.loop_stack_pointer] = self.pointer
            except:
                self.status_code = StatusCodes.loop_stack_out_of_memory
        else:
            open_bracket_amount  = 0
            try:
                while open_bracket_amount >= 0:
                    self.pointer += 1
                    if self.code[self.pointer] == "[": open_bracket_amount += 1
                    if self.code[self.pointer] == "]": open_bracket_amount -= 1
            except:
                self.status_code = StatusCodes.missing_closing_bracket


    def finish_loop(self):
        if self.loop_stack_pointer <= 0:
            self.status_code = StatusCodes.missing_opening_bracket
        
        if self.memory_array[self.memory_array_pointer] != 0: self.pointer = self.loop_stack[self.loop_stack_pointer]
        else: self.loop_stack_pointer -= 1