# Microcode binary values
HL = 0b1000000000000000 #Halt
RI = 0b0100000000000000 #RAM In
RO = 0b0010000000000000 #RAM Out
II = 0b0001000000000000 #Instruction Reg In
MI = 0b0000100000000000 #Memory Address Reg In
AI = 0b0000010000000000 #A Reg In
AO = 0b0000001000000000 #A Reg Out
BI = 0b0000000100000000 #B Reg In
OI = 0b0000000010000000 #Output Reg In
IC = 0b0000000001000000 #Increment counter
CI = 0b0000000000100000 #Counter In
CO = 0b0000000000010000 #Counter Out
EO = 0b0000000000001000 #Sum Out
SU = 0b0000000000000100 #Subtract
RC = 0b0000000000000010 #Reset Microcode Counter

#First Byte Instruction, Second Byte Data
instructions = [
    [MI|CO, RO|II|IC, RC], # NOP
    [MI|CO, RO|II|IC, CO|MI, MI|RO|IC, RO|AI, RC], # LDA
    [MI|CO, RO|II|IC, CO|MI, MI|RO|IC, RO|BI, EO|AI, RC], #ADD
    [MI|CO, RO|II|IC, CO|MI, BI|RO|IC, EO|AI, RC], #ADDI
    [MI|CO, RO|II|IC, CO|MI, MI|RO|IC, RO|BI, EO|AI|SU, RC], #SUB
    [MI|CO, RO|II|IC, CO|MI, BI|RO|IC, EO|AI, RC], #SUBI
    [MI|CO, RO|II|IC, CO|MI, MI|RO|IC, RI|AO, RC], #STA
    [MI|CO, RO|II|IC, CO|MI, AI|RO|IC, RC], #LDI
    [MI|CO, RO|II|IC, CO|MI, CI|RO, RC], #JMP
]
for instruction in instructions:
    while len(instruction) < 16:
        instruction.append(0)
while len(instructions) < 256:
    instructions.append(instructions[0])
flags = [0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111]
binary = [None] * 2**15
for flag in flags:
    for instructionIndex, instruction in enumerate(instructions):
        for microCodeIndex, microcode in enumerate(instruction):
            address = instructionIndex << 7 | flag << 4 | microCodeIndex
            binary[address] = microcode


EEPROMNUM = 1
for i in range(len(binary)):
    binary[i] = (binary[i] >> (EEPROMNUM * 8) & 0b11111111)

with open("microcode.bin", "wb") as f:
    f.write(bytes(binary))