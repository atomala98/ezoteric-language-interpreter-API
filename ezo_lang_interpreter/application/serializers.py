from django.contrib.auth.models import User

from rest_framework import serializers
from application.interpreters.brainfuck import BrainfuckInterperet, parse_to_int_array, parse_to_str_representation
from application.interpreters.befunge import BefungeInterperet
from application.interpreters.whitespace import WhitespaceInterperet

from ezo_lang_interpreter.settings import APPLICATION_SETTINGS
from .models import BefungeDirections, BefungeProgram, BefungeStringMode, BrainfuckProgram, StatusCodes, WhitespaceProgram

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# User serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
        )
    
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'password2')

    def validate(self, attrs):
        print(attrs)
        if attrs['password'] != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

BRAINFUCK_SETTINGS = APPLICATION_SETTINGS["BRAINFUCK"]

# Brainfuck serializers

class BrainfuckSerializer(serializers.ModelSerializer):


    class Meta:
        model = BrainfuckProgram
        fields = ['id', 'code', 'name', 'output', 'status_code']
        read_only_fields = ('id', 'output', 'status_code')

    def create(self, validated_data):
        
        validated_data["output"] = ""
        validated_data["pointer"] = 0

        validated_data["loop_stack"] = parse_to_str_representation([0] * BRAINFUCK_SETTINGS["LOOP_STACK_SIZE"])
        validated_data["loop_stack_pointer"] = 0

        validated_data["memory_array"] = parse_to_str_representation([0] * BRAINFUCK_SETTINGS["MEMORY_SIZE"])
        validated_data["memory_array_pointer"] = 0

        validated_data["status_code"] = StatusCodes.running
        
        interpreter = BrainfuckInterperet(validated_data)
        interpreter.run()

        return BrainfuckProgram.objects.create(**interpreter.retrieve())


class BrainfuckInputSerializer(serializers.ModelSerializer):

    input_value = serializers.CharField(write_only=True)

    class Meta:
        model = BrainfuckProgram
        fields = ['id', 'code', 'name', 'output', 'status_code', 'input_value']
        read_only_fields = ('id', 'code', 'name', 'output', 'status_code')

    def update(self, instance, validated_data):

        if instance.status_code != StatusCodes.waiting_for_char_input:
            raise Exception("Wrong status code")

        memory_input = ord(validated_data.get('input', '0'))
        instance.status_code = StatusCodes.running

        interpreter = BrainfuckInterperet(instance.__dict__, memory_input=memory_input)
        interpreter.run()

        instance = interpreter.retrieve_instance(instance)
        instance.save()

        return instance
    
    
BEFUNGE_SETTINGS = APPLICATION_SETTINGS["BEFUNGE"]

    
class BefungeSerializer(serializers.ModelSerializer):


    class Meta:
        model = BefungeProgram
        fields = ['id', 'code', 'name', 'output', 'status_code']
        read_only_fields = ('id', 'output', 'status_code')

    def create(self, validated_data):
        
        validated_data["output"] = ""
        validated_data["ptr_x"] = 0
        validated_data["ptr_y"] = 0

        validated_data["memory_stack"] = parse_to_str_representation([0] * BEFUNGE_SETTINGS["MAX_STACK_SIZE"])
        validated_data["memory_stack_pointer"] = -1

        validated_data["current_direction"] = BefungeDirections.right

        validated_data["status_code"] = StatusCodes.running
        validated_data["string_mode"] = BefungeStringMode.false
        
        interpreter = BefungeInterperet(validated_data)
        interpreter.run()

        return BefungeProgram.objects.create(**interpreter.retrieve())
    

class BefungeInputSerializer(serializers.ModelSerializer):

    input_value = serializers.CharField(write_only=True)

    class Meta:
        model = BefungeProgram
        fields = ['id', 'code', 'name', 'output', 'status_code', 'input_value']
        read_only_fields = ('id', 'code', 'name', 'output', 'status_code')

    def update(self, instance, validated_data):

        if instance.status_code == StatusCodes.waiting_for_char_input:
            try:
                memory_input = ord(validated_data["input_value"][0])
            except:
                raise Exception("Incorrect input for char input")

        elif instance.status_code == StatusCodes.waiting_for_num_input:
            try:
                memory_input = int(validated_data["input_value"])
            except:
                raise Exception("Incorrect input for integer")
            
        else:
            raise Exception("Wrong status code")
        
        instance.status_code = StatusCodes.running

        interpreter = BefungeInterperet(instance.__dict__, memory_input=memory_input)
        interpreter.run()

        instance = interpreter.retrieve_instance(instance)
        instance.save()

        return instance
    
        
WHITESPACE_SETTINGS = APPLICATION_SETTINGS["WHITESPACE"]

    
class WhitespaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BefungeProgram
        fields = ['id', 'code', 'name', 'output', 'status_code']
        read_only_fields = ('id', 'output', 'status_code')

    def create(self, validated_data):
        
        validated_data["output"] = ""
        validated_data["pointer"] = 0

        validated_data["memory_stack"] = parse_to_str_representation([0] * WHITESPACE_SETTINGS["MEMORY_SIZE"])
        validated_data["memory_stack_pointer"] = -1

        validated_data["heap"] = ""
        validated_data["labels"] = ""

        validated_data["status_code"] = StatusCodes.running

        interpreter = WhitespaceInterperet(validated_data)
        interpreter.run()

        return WhitespaceProgram.objects.create(**interpreter.retrieve())
    
    
class WhitespaceInputSerializer(serializers.ModelSerializer):

    input_value = serializers.CharField(write_only=True)

    class Meta:
        model = BefungeProgram
        fields = ['id', 'code', 'name', 'output', 'status_code', 'input_value']
        read_only_fields = ('id', 'code', 'name', 'output', 'status_code')

    def update(self, instance, validated_data):
        
        
        if instance.status_code == StatusCodes.waiting_for_char_input:
            try:
                memory_input = ord(validated_data["input_value"][0])
            except:
                raise Exception("Incorrect input for char input")

        elif instance.status_code == StatusCodes.waiting_for_num_input:
            try:
                memory_input = int(validated_data["input_value"])
            except:
                raise Exception("Incorrect input for integer")
            
        else:
            raise Exception("Wrong status code")
        
        instance.status_code = StatusCodes.running

        interpreter = WhitespaceInterperet(instance.__dict__, memory_input=memory_input)
        interpreter.run()

        instance = interpreter.retrieve_instance(instance)
        instance.save()

        return instance