import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Optional app description')
parser.add_argument('input', type=str,
                    help='Input Assembly File')
parser.add_argument('output', type=str,
                    help='A required integer positional argument', default="out.bin")
args = parser.parse_args()



with open(args.input, 'r') as inputFile:
    lines = inputFile.read().splitlines()
lines = [i.split('//')[0].strip() for i in lines if i.split('//')[0]]  # Remove Comments

# Instruction byte count, instruction byte
instructions = {
    'NOP': (1, 0x00),
    'LDA': (2, 0x01),
    'ADD': (2, 0x02),
    'ADDI': (2, 0x03),
    'SUB': (2, 0x04),
    'SUBI': (2, 0x05),
    'STA': (2, 0x06),
    'LDI': (2, 0x07),
    'JMP': (2, 0x08),
    'OUT': (1, 0x09),
    'HLT': (1, 0x0A),
}
 
symbols = {}

binary = []

byteNum = 0
for line in lines:
    words = line.split()
    instructionData = instructions.get(words[0], None)
    if not instructionData:
        symbols[words[0][:-1]] = byteNum
        continue
    binary.append(instructionData[1])
    for i in range(1, instructionData[0]):
        if words[i].startswith('0x'):
            binary.append(int(words[i], 16))
        elif words[i].startswith('0b'):
            binary.append(int(words[i], 2))
        elif words[i].startswith('\''):
            binary.append(ord(words[i][1]))
        elif words[i].isnumeric():
            binary.append(int(words[i]))
        else:
            binary.append(words[i])
    byteNum += instructionData[0]

for i in range(len(binary)):
    if isinstance(binary[i], str):
        binary[i] = symbols[binary[i]]

with open(args.output, "wb") as f:
    f.write(bytes(binary))
