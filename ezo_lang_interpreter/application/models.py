from django.db import models
# Create your models here.

class StatusCodes(models.TextChoices):
    running = "Run", "Running"
    finished = "Fin", "Finished"
    waiting_for_char_input = "Wfc", "Waiting for character input"
    waiting_for_num_input = "Wfn", "Waiting for numeric input"
    out_of_time = "Oot", "Out of time"
    loop_stack_out_of_memory = "Ool", "Loop stack out of memory"
    out_of_memory = "Oom", "Out of memory"
    missing_closing_bracket = "Mcb", "Missing closing bracket"
    missing_opening_bracket = "Mob", "Missing opening bracket"
    output_out_of_memory = "Ooo", "Output out of memory"
    wrong_program_code = "Wpc", "Wrong program code"
    no_end_instruction = "Nei", "No end instruction"


class BrainfuckProgram(models.Model):

    id = models.IntegerField(primary_key=True, auto_created=True)

    code = models.TextField(blank=False)
    name = models.CharField(max_length=30)
    output = models.TextField(blank=False, default="")
    pointer = models.IntegerField(default=0)

    loop_stack = models.TextField()
    loop_stack_pointer = models.IntegerField(default=0)

    memory_array = models.TextField()
    memory_array_pointer = models.IntegerField(default=0)
    
    status_code = models.CharField(max_length=3, choices=StatusCodes.choices, default=StatusCodes.running)

    created = models.DateTimeField(auto_now_add=True)


class BefungeDirections(models.IntegerChoices):
    right = 0, "rigth"
    down = 1, "down"
    left = 2, "left"
    up = 3, "up"


class BefungeStringMode(models.IntegerChoices):
    true = 0, "on"
    false = 1, "off"

    @classmethod
    def negate(self, value):
        return self.true if value == self.false else self.false


class BefungeProgram(models.Model):

    id = models.IntegerField(primary_key=True, auto_created=True)

    code = models.TextField()
    name = models.CharField(max_length=30)
    output = models.TextField(blank=False, default="")

    memory_stack = models.TextField()
    memory_stack_pointer = models.IntegerField(default=-1)

    ptr_x = models.IntegerField(default=0)
    ptr_y = models.IntegerField(default=0)

    max_x = models.IntegerField()
    max_y = models.IntegerField()

    current_direction = models.IntegerField(choices=BefungeDirections.choices, default=BefungeDirections.right)
    string_mode = models.IntegerField(choices=BefungeStringMode.choices, default=BefungeStringMode.false)
    
    status_code = models.CharField(max_length=3, choices=StatusCodes.choices)

    created = models.DateTimeField(auto_now_add=True)
    

class WhitespaceProgram(models.Model):

    id = models.IntegerField(primary_key=True, auto_created=True)

    code = models.TextField()
    name = models.CharField(max_length=30)
    output = models.TextField(blank=False, default="")
    pointer = models.IntegerField(default=0)

    memory_stack = models.TextField()
    memory_stack_pointer = models.IntegerField(default=0)

    heap = models.TextField()
    labels = models.TextField()

    status_code = models.CharField(max_length=3, choices=StatusCodes.choices)

    created = models.DateTimeField(auto_now_add=True)