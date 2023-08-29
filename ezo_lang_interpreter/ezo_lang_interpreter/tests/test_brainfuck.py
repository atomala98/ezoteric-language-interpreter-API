import pytest
from  rest_framework.test import APIClient
from application.models import BrainfuckProgram, StatusCodes
from ezo_lang_interpreter.settings import APPLICATION_SETTINGS

brainfuck_settings = APPLICATION_SETTINGS["BRAINFUCK"]

client = APIClient()

# Basic tests

def test_pytest_working():
    assert True == True

    
def test_empty_body_post_request():
    response = client.post('/brainfuck/')
    assert response.status_code == 400
    

@pytest.mark.django_db
def test_basic_body_post_request():
    name = "test"
    data = {
        "code": "+",
        "name": name
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.finished
    assert program.name == name
    

@pytest.mark.django_db
def test_basic_output_equal_2():
    code = "+" * 50 + "."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.finished
    assert program.output == "2"

# Status tests    

@pytest.mark.django_db
def test_out_of_time_status():
    code = "+[]"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.out_of_time
    
   
@pytest.mark.django_db
def test_out_of_output_memory_status():
    code = "+[.]"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.output_out_of_memory

           
@pytest.mark.django_db
def test_waiting_for_input_status():
    code = ",+++"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.waiting_for_char_input


@pytest.mark.django_db
def test_waiting_for_input_status_complex():
    code = ",+."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()

    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "a"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.finished
    assert program.output == "b"

       
@pytest.mark.django_db
def test_mising_opening_bracket_status():
    code = "]+++"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.missing_opening_bracket

       
@pytest.mark.django_db
def test_mising_closing_bracket_status():
    code = "[+++"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.missing_closing_bracket

    
@pytest.mark.django_db
def test_loop_stack_out_of_memory_status():
    code = "+[" * (brainfuck_settings["LOOP_STACK_SIZE"] + 1) + "]"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.loop_stack_out_of_memory

# Program tests

@pytest.mark.django_db
def test_hello_world_basic():
    code = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.finished
    assert program.output == "Hello World!\n"


@pytest.mark.django_db
def test_hello_world_complex():
    code = ">++++++++[-<+++++++++>]<.>>+>-[+]++>++>+++[>[->+++<<+++>]<<]>-----.>->+++..+++.>-.<<+[>[+>+]>>]<--------------.>>.+++.------.--------.>+.>+."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.finished
    assert program.output == "Hello World!\n"


@pytest.mark.django_db
def test_hello_world_complex_short():
    code = "--<-<<+[+[<+>--->->->-<<<]>]<<--.<++++++.<<-..<<.<+.>>.>>.<<<.+++.>>.>>-.<<<+."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.finished
    assert program.output == "Hello, World!"


@pytest.mark.django_db
def test_hello_world_shortest():
    code = "+[-->-[>>+>-----<<]<--<---]>-.>>>+.>>..+++[.>]<<<<.+++.------.<<-.>>>>+."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()
    assert program.status_code == StatusCodes.finished
    assert program.output == "Hello, World!"


@pytest.mark.django_db
def test_cat_program():
    code = ",[.,]"
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()

    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "a"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.waiting_for_char_input
    assert program.output == "a"
    
    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "b"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.waiting_for_char_input
    assert program.output == "ab"
    
    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "c"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.waiting_for_char_input
    assert program.output == "abc"
    assert program.id == 1
 

@pytest.mark.django_db
def test_muliplication_program():
    code = ",>,>++++++++[<------<------>>-]<<[>[>+>+<<-]>>[<<+>>-]<<<-]>>>++++++[<++++++++>-]<."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()

    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "2"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.waiting_for_char_input
    assert program.output == ""
    
    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "3"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.finished
    assert program.output == "6"
     

@pytest.mark.django_db
def test_addition_program():
    code = ",>++++++[<-------->-],[<+>-]<."
    data = {
        "code": code,
        "name": "test"
    }
    response = client.post('/brainfuck/', data=data)
    assert response.status_code == 201
    program = BrainfuckProgram.objects.first()

    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "2"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.waiting_for_char_input
    assert program.output == ""
    
    put_response = client.put(f'/brainfuck/{program.id}/', data={"input_value": "3"})
    program = BrainfuckProgram.objects.first()
    assert put_response.status_code == 200
    assert program.status_code == StatusCodes.finished
    assert program.output == "5"