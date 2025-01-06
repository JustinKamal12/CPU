# Justin Kamal
# I pledge my honor that I have abided by the Stevens Honor System.

import sys

def binary_to_integer(binary_string, digit_index, total_digits):
    """Converts a binary string to an integer."""
    result = 0
    for i in range(digit_index + 1):
        result += int(binary_string[i]) * (2 ** (total_digits - i))
    return result

def adjust_binary_length(binary_str, target_length, is_signed=False):
    """Adjusts the length of a binary string to match the target length."""
    if len(binary_str) > target_length:
        return binary_str[-target_length:]
    if len(binary_str) < target_length:
        padding_char = binary_str[0] if is_signed and binary_str[0] == '1' else '0'
        padding = padding_char * (target_length - len(binary_str))
        return padding + binary_str
    return binary_str

# Open input file
file = open(str(sys.argv[1]), "r")
instructions = file.readlines()

# Open output files for text (instructions) and data
text_image_file = open("text_image", "w")
data_image_file = open("data_image", "w")

# Headers for output files
text_segment = "v3.0 hex words addressed\n00: "
data_segment = "v3.0 hex words addressed\n00: "

# Define supported opcodes
opcodes = {"addn": 320, "ldr": 834, "str": 1088, "addr": 256, "mov": 320, "cmp": 12, "b.eq": 65, "b": 192, "mul": 272}

# Helper variables
labels = {}  # Stores label positions
usesIntermediates = ["addn", "ldr", "str", "mov"]
branching = ["b.eq", "b"]
line_number = 0
j = 0

# Determine current segment (default is None until we encounter `.text` or `.data`)
current_segment = None
text_instructions = []
data_instructions = []

# Parse instructions and separate by segment
for line in instructions:
    tokens = line.strip().split()

    # Ignore empty lines or comments
    if not tokens or tokens[0].startswith("#"):
        continue

    # Handle segment directives
    if tokens[0] == ".text":
        current_segment = "text"
        print("Switching to .text segment")
        continue
    elif tokens[0] == ".data":
        current_segment = "data"
        print("Switching to .data segment")
        continue

    # Process labels
    if tokens[0].endswith(":"):
        label_name = tokens[0][:-1]
        print(f"Label detected: {label_name}")
        if current_segment == "data":
            # Attach label to the next instruction in the data segment
            data_instructions.append([label_name] + tokens[1:])
        else:
            labels[label_name] = line_number
        continue

    # Add instructions to the appropriate segment
    if current_segment == "text":
        text_instructions.append((line_number, tokens))
        line_number += 1
    elif current_segment == "data":
        data_instructions.append(tokens)

# DEBUG: Print parsed data instructions
print("\nParsed Data Instructions:")
print(data_instructions)

# Process text (instruction) segment
for line_number, tokens in text_instructions:
    if not tokens:  # Safety check to avoid empty `tokens`
        continue
    parsed_instruction = ""
    if tokens[0] in opcodes:
        try:
            # Handle branching instructions
            if tokens[0] in branching:
                target_label = tokens[1].strip()
                if target_label in labels:
                    opcode = adjust_binary_length(bin(opcodes[tokens[0]])[2:], 11)
                    rn = adjust_binary_length("0", 5)
                    rd = adjust_binary_length("0", 5)
                    offset = labels[target_label] - line_number - 1
                    imm = adjust_binary_length(bin(offset)[2:], 11, is_signed=True)
                    full_binary = opcode + imm + rn + rd
                    parsed_instruction += adjust_binary_length(hex(int(full_binary, 2))[2:], 8)
                else:
                    raise SyntaxError(f"Undefined label: {target_label}")

            # Handle intermediate instructions
            elif tokens[0] in usesIntermediates:
                opcode = adjust_binary_length(bin(opcodes[tokens[0]])[2:], 11)
                rd = adjust_binary_length(bin(int(tokens[1][1:].strip(',')))[2:], 5)
                if tokens[0] == "mov":
                    imm = adjust_binary_length(bin(int(tokens[2].strip()))[2:], 11)
                    rn = adjust_binary_length("0", 5)
                else:
                    rn = adjust_binary_length(bin(int(tokens[2][1:].strip(',')))[2:], 5)
                    imm = adjust_binary_length(bin(int(tokens[3].strip()))[2:], 11)
                full_binary = opcode + imm + rn + rd
                parsed_instruction += adjust_binary_length(hex(int(full_binary, 2))[2:], 8)

            # Handle comparison instructions
            elif tokens[0] == "cmp":
                opcode = adjust_binary_length(bin(opcodes["cmp"])[2:], 11)
                rn = adjust_binary_length(bin(int(tokens[1][1:].strip(',')))[2:], 5)
                rm = adjust_binary_length(bin(int(tokens[2][1:].strip()))[2:], 5)
                rd = adjust_binary_length("0", 5)
                imm = adjust_binary_length("0", 6)
                full_binary = opcode + imm + rm + rn + rd
                parsed_instruction += adjust_binary_length(hex(int(full_binary, 2))[2:], 8)

            # Append instruction to text segment
            text_segment += parsed_instruction + " "
        except Exception as e:
            print(f"Error processing instruction: {tokens} -> {e}")

# Process data segment
for tokens in data_instructions:
    if len(tokens) < 2:  # Avoid index errors
        continue
    if tokens[1] == ".quad":
        try:
            # Convert data to binary and format as hex
            data_value = adjust_binary_length(bin(int(tokens[2]))[2:], 32)
            hex_value = hex(int(data_value, 2))[2:]  # Convert to hex
            data_segment += adjust_binary_length(hex_value, 8) + " "
        except Exception as e:
            print(f"Error processing data: {tokens} -> {e}")

# DEBUG: Print final segments before writing
print("\nFinal Text Segment:")
print(text_segment)
print("\nFinal Data Segment:")
print(data_segment)

# Write final output to files
text_image_file.write(text_segment)
data_image_file.write(data_segment)
text_image_file.close()
data_image_file.close()
file.close()

print("Assembly completed. Text and data segments written to files.")
