This project is a custom assembler for a simulated CPU, designed to convert assembly instructions into machine code. 
The assembler reads an input assembly program, processes the instructions into binary format, and generates two output files: one for text (instruction memory) and another for data (data memory). 
These files can be loaded into the Logisim RAM module to execute the program.

Key Features:

Assembly to Machine Code Conversion: Converts assembly instructions into binary machine code and formats it as hexadecimal.
Support for Labels: Handles branching instructions by resolving labels in the assembly code.
Instruction Segmentation: Differentiates between .text (instructions) and .data (data values) segments in the input file.
Error Handling: Detects and reports undefined labels, invalid instructions, and formatting issues.
Customizable Opcodes: Includes predefined opcodes for supported instructions such as addn, ldr, str, cmp, b.eq, and more.
Output Files:
text_image: Contains the machine code for instructions.
data_image: Contains the machine code for data.
Technologies Used:

Python: Implements the assembler logic.
Logisim: Simulated CPU for loading and testing the generated machine code.
Usage Instructions:

Ensure Python is installed on your system.
Place your assembly program file in the same directory as the assembler script.
Run the assembler using the following command:
bash
Copy code
python assembler.py [program.s]
Replace [program.s] with the name of your assembly file.
The assembler generates two output files:
text_image: Instruction memory in hexadecimal.
data_image: Data memory in hexadecimal.
Load these files into the Logisim RAM module to execute the program.
Supported Assembly Features:

General-purpose registers: X0 to X31.
Immediate values: Range from -1024 to 1023.
Labels for branching and control flow.
Arithmetic, memory, and branching instructions.
Prerequisites:

Python installed with no additional libraries required.
Logisim installed for testing the output.
This assembler simplifies the process of converting human-readable assembly code into machine-readable instructions, making it ideal for educational projects and custom CPU simulations.
