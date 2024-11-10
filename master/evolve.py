import random
import struct
from utils import generate_random_strings

def xor_byte(byte_value: str) -> str:
    """Perform XOR on a byte with a fixed mask."""
    mask = 0xAA
    return chr(ord(byte_value) ^ mask)

def flip_random_bit(byte_value: str) -> str:
    """Flip a random bit in the provided byte."""
    bit_position = random.randint(0, 7)
    flipped_byte = ord(byte_value) ^ (1 << bit_position)
    return chr(flipped_byte)

def invert_byte(byte_value: str) -> str:
    """Invert all bits in the provided byte."""
    return chr(~ord(byte_value) & 0xFF)

def mutate(payload: str) -> str:
    """Applies a random mutation to a given payload."""
    mutations = {
        1: lambda field: field[:-1] if field else "",  # Decrease length safely
        2: lambda field: field + "AAAA",  # Increase length - add bytes
        3: lambda _: "",  # Make an input field empty
        4: lambda field, pos: field[:pos] + "\x00" + field[pos + 1:],  # Null byte insertion
        5: lambda field, pos: field[:pos] + "\n" + field[pos + 1:],  # Newline insertion
        6: lambda field, pos: field[:pos] + ";" + field[pos + 1:],  # Semicolon insertion
        7: lambda field, pos: field[:pos] + struct.pack("<I", 0x7FFFFFFF).decode('latin1') + field[pos + 4:],  # MAXINT
        8: lambda field, pos: field[:pos] + struct.pack("<I", 0x80000000).decode('latin1') + field[pos + 4:],  # MININT
        9: lambda field, pos: field[:pos] + struct.pack("b", -ord(field[pos])).decode('latin1') + field[pos + 1:],  # Flip sign
        10: lambda field, pos: field[:pos] + random.choice(["%s", "%n", "%x"]) + field[pos:],  # Insert format code
        11: lambda field, pos: field[:pos] + flip_random_bit(field[pos]) + field[pos + 1:],  # Flip bit
        12: lambda field, pos: field[:pos] + invert_byte(field[pos]) + field[pos + 1:],  # Invert bits
        13: lambda field, pos: field[:pos] + xor_byte(field[pos]) + field[pos + 1:],  # XOR
    }

    lines = payload.split("\r\n")
    fields = [line.split() for line in lines if line]

    # Choose a field to mutate; exclude the first field to avoid corrupting HTTP method
    if len(fields) > 1:
        mutated_field_index = random.randint(1, len(fields) - 1)
        mutated_field = fields[mutated_field_index][1]
        
        if mutated_field:  # Ensure field is non-empty
            mutation = random.choice(list(mutations.keys()))
            mutation_position = random.randint(0, len(mutated_field) - 1)
            mutated_field = (mutations[mutation](mutated_field, mutation_position) 
                             if mutation > 3 else mutations[mutation](mutated_field))

            # Update mutated field in fields list
            fields[mutated_field_index][1] = mutated_field

    return "\r\n".join(" ".join(field) for field in fields if field) + "\r\n"



def init_pop(pop_size: int =20) -> list[str]:
    """
    Generate an initial population of HTTP payloads with random headers.

    :param population_size: The number of unique payloads to generate
    :return: A list of randomly generated HTTP payloads
    """

    init_population_list = []
    
    for _ in range(pop_size):
        # Generate unique random values for HTTP headers
        host = next(generate_random_strings(1))
        agent = next(generate_random_strings(1))
        accept = next(generate_random_strings(1))
        
        # Construct the HTTP payload with randomized headers
        payload = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: {agent}\r\n"
            f"Accept: {accept}\r\n"
        )
        
        # Append the payload to the population list
        init_population_list.append(payload)
        
    return init_population_list

from utils import levenshtein_distance

def fitness(population: list[str]) -> dict:
    """
    Calculate the Levenshtein distance of each payload in the population from a target string.
    
    :param population: List of HTTP payloads to evaluate
    :return: A dictionary containing the payloads with the maximum and minimum edit distances, 
             along with their respective distances.
    """
    target = "GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: Firefox\r\nAccept: */*\r\n"
    
    # Calculate Levenshtein distances
    distances = [(payload, levenshtein_distance(payload, target)) for payload in population]
    
    # Determine payloads with max and min distances
    max_distance_payload = max(distances, key=lambda x: x[1])
    min_distance_payload = min(distances, key=lambda x: x[1])
    
    return {
        "max_distance_payload": max_distance_payload[0],
        "max_distance": max_distance_payload[1],
        "min_distance_payload": min_distance_payload[0],
        "min_distance": min_distance_payload[1]
    }

def crossover(father_payload: str, mother_payload: str, n: int = 20) -> list[str]:
    """
    Generate a new population by combining fields of two parent payloads with added randomness.
    
    :param father_payload: First parent payload (string)
    :param mother_payload: Second parent payload (string)
    :param n: Number of new payloads to generate (default is 10)
    :return: List of `n` diverse payloads created by combining fields from both parents
    """
    def parse_payload(payload: str) -> list[list[str]]:
        """Parse the payload into a structured list of lines."""
        return [line.split(None, 1) for line in payload.splitlines() if line]

    father_fields = parse_payload(father_payload)
    mother_fields = parse_payload(mother_payload)

    max_len = min(len(father_fields), len(mother_fields))
    new_population = []

    for _ in range(n):
        new_request_list = []
        for i in range(max_len):
            selected_field = random.choice([father_fields[i][1], mother_fields[i][1]]) if len(father_fields[i]) > 1 else ""
            if random.random() < 0.5:  
                selected_field = ''.join(random.choice(father_fields[i][1] + mother_fields[i][1])
                                         for _ in range(len(selected_field)))
            field_type = father_fields[i][0]  # Take the first token (e.g., "Host:", "User-Agent:")
            new_request_list.append(f"{field_type} {selected_field}")

        new_payload = "\r\n".join(new_request_list) + "\r\n"
        new_population.append(new_payload)

    return new_population



