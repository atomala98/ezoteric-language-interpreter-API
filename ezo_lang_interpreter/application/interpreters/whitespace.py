from application.models import StatusCodes
from .utilites import parse_to_int_array, parse_to_str_representation, parse_int_str_map_to_str_representation, parse_to_int_str_map
from ezo_lang_interpreter.settings import APPLICATION_SETTINGS


def filter_code(s: str) -> str:
    output = ""
    for letter in s:
        if letter == "\n" or letter == "\t" or letter == " ":
            output += letter
    return output


class WhitespaceInterperet():

    def __init__(self, program_instance, memory_input=0):
        self.max_interations = APPLICATION_SETTINGS["WHITESPACE"]["MAX_ITERATIONS"]
        self.max_output_size = APPLICATION_SETTINGS["WHITESPACE"]["OUTPUT_MAX_SIZE"]

        self.max_stack_size = APPLICATION_SETTINGS["WHITESPACE"]["HEAP_SIZE"]
        self.max_labels_size = APPLICATION_SETTINGS["WHITESPACE"]["LABELS_SIZE"]

        self.code = filter_code(program_instance['code'])
        self.name = program_instance['name']
        self.output = program_instance['output']
        self.pointer = program_instance['pointer']

        self.memory_stack = parse_to_int_array(program_instance['loop_stack'])
        self.memory_stack_pointer = program_instance['loop_stack_pointer']

        self.heap = parse_to_int_str_map(program_instance["heap"])
        self.labels = parse_to_int_str_map(program_instance["labels"])

        self.status_code = program_instance['status_code']

        self.code_length = len(self.code)

        
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

            status_code = self.status_code
        )


    def retrieve_instance(self, instance):
        instance.code = self.code
        instance.name = self.name,
        instance.output = self.output,
        instance.pointer = self.pointer,

        instance.memory_stack = parse_to_str_representation(self.memory_stack),
        instance.memory_stack_pointer = self.memory_stack_pointer,

        instance.heap = parse_int_str_map_to_str_representation(self.heap),
        instance.labels = parse_int_str_map_to_str_representation(self.labels),

        instance.status_code = self.status_code

        return instance


    def run(self):
        it = 0
        while self.pointer < self.code_length and self.status_code == StatusCodes.running:
            break

            self.pointer += 1
            it += 1
            if it >= self.max_interations: self.status_code = StatusCodes.out_of_time
        
        if self.status_code == StatusCodes.running: self.status_code = StatusCodes.finished

