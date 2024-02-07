from utils import *

# Example input string
input_str_example = """
    Hannes Sakulin(
        CERN
    )
    ; Simone Scarfi(
        CERN
    )
    ; Michele Selvaggi(
        CERN
    )
    ; Archana Sharma(
        CERN
    )
    ; Ksenia Shchelina(
        CERN
    )
    ; Pedro Silva(
        CERN
    )
"""

# Format the example string
formatted_output = format_authors(input_str_example)
print(formatted_output)