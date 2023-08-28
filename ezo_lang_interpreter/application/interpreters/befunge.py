import time
from application.models import StatusCodes, BefungeDirections, BefungeStringMode
from .utilites import parse_to_int_array, parse_to_str_representation
from ezo_lang_interpreter.settings import APPLICATION_SETTINGS


def code_to_2d_array(code: str):
    output = [[]]

    for symbol in code:
        if symbol == '\n': output.append([])
        else: output[-1].append(symbol)

    breaks = lambda a: [" "] * a
    max_x = 0

    for line in output:
        max_x = max(max_x, len(line))

    for i, line in enumerate(output):
        output[i] += breaks(max_x - len(line))

    return output

def code_from_2d_array(array):
    print(array)
    return "\n".join(["".join(row) for row in array])


class BefungeInterperet():

    def __init__(self, program_instance, memory_input=None):
        self.max_interations = APPLICATION_SETTINGS["BEFUNGE"]["MAX_ITERATIONS"]
        self.max_output_size = APPLICATION_SETTINGS["BEFUNGE"]["OUTPUT_MAX_SIZE"]

        self.code = code_to_2d_array(program_instance['code'])
        self.name = program_instance['name']
        self.output = program_instance['output']

        self.ptr_x = program_instance['ptr_x']
        self.ptr_y = program_instance['ptr_y']

        self.memory_stack = parse_to_int_array(program_instance['memory_stack'])
        self.memory_stack_pointer = program_instance['memory_stack_pointer']

        if memory_input:
            self.push(memory_input)

        self.current_direction = program_instance['current_direction']

        self.status_code = program_instance['status_code']
        self.string_mode = program_instance['string_mode']

        self.max_x = len(self.code)
        self.max_y = len(self.code[0])

        
    def retrieve(self):
        return dict(
            code = code_from_2d_array(self.code),
            name = self.name,
            output = self.output,
            ptr_x = self.ptr_x,
            ptr_y = self.ptr_y,
            max_x = self.max_x,
            max_y = self.max_y,
            memory_stack = parse_to_str_representation(self.memory_stack),
            memory_stack_pointer = self.memory_stack_pointer,
            status_code = self.status_code
        )


    def retrieve_instance(self, instance):
        instance.output = self.output
        instance.ptr_x = self.ptr_x
        instance.ptr_y = self.ptr_y
        instance.max_x = self.max_x
        instance.max_y = self.max_y
        instance.memory_stack = parse_to_str_representation(self.memory_stack)
        instance.memory_stack_pointer = self.memory_stack_pointer
        instance.status_code = self.status_code

        return instance


    #----------------#
    # MAIN FUNCTIONS #
    #----------------#

    def run(self):
        it = 0
        while self.status_code == StatusCodes.running:
            current_symbol = self.code[self.ptr_x][self.ptr_y]
            # time.sleep(0.2)
            # print(f"{self.ptr_x} {self.ptr_y} {current_symbol} {self.output} {self.memory_stack[:10]}")
            
            if self.string_mode == BefungeStringMode.true: 
                self.step_with_string_mode(current_symbol)
            else:
                self.step_without_string_mode(current_symbol)
        
            self.move()

            it += 1
            if it >= self.max_interations: self.status_code = StatusCodes.out_of_time
        
        if self.status_code == StatusCodes.running: self.status_code = StatusCodes.finished


    def step_with_string_mode(self, symbol):
        if symbol == '"':
            self.toggle_string_mode()
        else:
            self.push_char_to_stack(symbol)


    def step_without_string_mode(self, symbol):
        if symbol == '+':
            self.add()
        elif symbol == '-':
            self.sub()
        elif symbol == '*':
            self.multiplication()
        elif symbol == '/':
            self.division()
        elif symbol == '%':
            self.modulo()
        elif symbol == '!':
            self.negation()
        elif symbol == '`':
            self.greater_than()
        elif symbol == '>':
            self.change_direction(BefungeDirections.right)
        elif symbol == 'v':
            self.change_direction(BefungeDirections.down)
        elif symbol == '<':
            self.change_direction(BefungeDirections.left)
        elif symbol == '^':
            self.change_direction(BefungeDirections.up)
        elif symbol == '?':
            self.randomise_direction()
        elif symbol == '_':
            self.horizontal_if()
        elif symbol == '|':
            self.vertical_if()
        elif symbol == '"':
            self.toggle_string_mode()
        elif symbol == ':':
            self.duplicate()
        elif symbol == '\\':
            self.swap()
        elif symbol == '$':
            self.pop_or_empty()
        elif symbol == '.':
            self.pop_and_output_as_int()
        elif symbol == ',':
            self.pop_and_output_as_char()
        elif symbol == '#':
            self.move()
        elif symbol == 'g':
            self.get_call()
        elif symbol == 'p':
            self.put_call()
        elif symbol == '@':
            self.status_code = StatusCodes.finished
        elif symbol in set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
            self.push_integer_to_stack(int(symbol))
        elif symbol == '~':
            self.read_character_input()
        elif symbol == '&':
            self.read_numeric_input()
            

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


    #-------------------#
    # PROGRAM FUNCTIONS #
    #-------------------#

    def move(self):
        if self.current_direction == BefungeDirections.right: self.ptr_y += 1
        elif self.current_direction == BefungeDirections.left: self.ptr_y -= 1
        elif self.current_direction == BefungeDirections.down: self.ptr_x += 1
        elif self.current_direction == BefungeDirections.up: self.ptr_x -= 1

        if self.ptr_x < 0: self.ptr_x = self.max_x - 1
        if self.ptr_x >= self.max_x: self.ptr_x = 0
        if self.ptr_y < 0: self.ptr_y = self.max_y - 1
        if self.ptr_y >= self.max_y: self.ptr_y = 0


    def add(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b + a)


    def sub(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b - a)


    def multiplication(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b * a)


    def division(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b // a)


    def modulo(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(b % a)

    
    def negation(self):
        self.push(1 if self.pop_or_empty() == 0  else 0)


    def greater_than(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(1 if b > a else 0)

    
    def change_direction(self, new_direction):
        self.current_direction = new_direction

    
    # TODO 
    def randomise_direction(self):
        pass

    
    def horizontal_if(self):
        if (self.pop_or_empty() == 0): self.change_direction(BefungeDirections.right)
        else: self.change_direction(BefungeDirections.left)


    def vertical_if(self):
        if (self.pop_or_empty() == 0): self.change_direction(BefungeDirections.down)
        else: self.change_direction(BefungeDirections.up)


    def toggle_string_mode(self):
        self.string_mode = BefungeStringMode.negate(self.string_mode)

    
    def push_char_to_stack(self, symbol):
        self.push(ord(symbol))
        

    def push_integer_to_stack(self, number):
        self.push(number)

    
    def pop_and_output_as_char(self):
        a = self.pop_or_empty()
        self.output += chr(a % 65536)
        if len(self.output) >= self.max_output_size:
            self.status_code = StatusCodes.output_out_of_memory


    def pop_and_output_as_int(self):
        a = self.pop_or_empty()
        self.output += str(a)
        if len(self.output) >= self.max_output_size:
            self.status_code = StatusCodes.output_out_of_memory
        

    def duplicate(self):
        a = self.pop_or_empty()
        self.push(a)
        self.push(a)

    
    def swap(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        self.push(a)
        self.push(b)

    
    def get_call(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        
        if (a < 0 or a >= self.max_x or b < 0 or b >= self.max_y):
            return
        
        self.push(ord(self.code[a][b]))


    def put_call(self):
        a = self.pop_or_empty()
        b = self.pop_or_empty()
        v = self.pop_or_empty()
        
        if (a < 0 or a >= self.max_x or b < 0 or b >= self.max_y):
            return
        
        self.code[a][b] = chr(v % 65536)


    def read_character_input(self):
        self.status_code = StatusCodes.waiting_for_char_input

    
    def read_numeric_input(self):
        self.status_code = StatusCodes.waiting_for_num_input

    