

def parse_to_int_array(s: str) -> list[int]:
    return [int(cell) for cell in s.split(",") if cell]


def parse_to_str_representation(l: list[int]) -> str:
    return ",".join([str(cell) for cell in l])



def parse_to_int_str_map(s: str):
    output = {}
    for pair in s.split(","):
        if not pair: continue
        splitted_pair = pair.split('=')
        output[int(splitted_pair[0])] = splitted_pair[1]
    return output


def parse_int_str_map_to_str_representation(m) -> str:
    output = []
    for key, value in m.items():
        output.append(f"{key}={value}")
    return ",".join(output)