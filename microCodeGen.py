import copy
# Microcode binary values
HL = 0b1000000000000000 #Halt
RI = 0b0100000000000000 #RAM In
RO = 0b0010000000000000 #RAM Out
II = 0b0001000000000000 #Instruction Reg In
MI = 0b0000100000000000 #Memory Address Reg In
AI = 0b0000010000000000 #A Reg In
AO = 0b0000001000000000 #A Reg Out
BI = 0b0000000100000000 #B Reg In
DI = 0b0000000010000000 #Display In
IC = 0b0000000001000000 #Increment counter
CI = 0b0000000000100000 #Counter In
CO = 0b0000000000010000 #Counter Out
EO = 0b0000000000001000 #Sum Out
SU = 0b0000000000000100 #Subtract
RC = 0b0000000000000010 #Reset Microcode Counter

#First Byte Instruction, Second Byte Data
microcodeTemplate = [
    [CO|MI, RO|II|IC, RC], # NOP - 0X00
    [CO|MI, RO|II|IC, CO|MI, MI|RO|IC, RO|AI, RC], # LDA - 0X01
    [CO|MI, RO|II|IC, CO|MI, MI|RO|IC, RO|BI, EO|AI, RC], #ADD - 0X02
    [CO|MI, RO|II|IC, CO|MI, BI|RO|IC, EO|AI, RC], #ADDI - 0X03
    [CO|MI, RO|II|IC, CO|MI, MI|RO|IC, RO|BI, EO|AI|SU, RC], #SUB - 0X04
    [CO|MI, RO|II|IC, CO|MI, BI|RO|IC, EO|AI, RC], #SUBI - 0X05
    [CO|MI, RO|II|IC, CO|MI, MI|RO|IC, RI|AO, RC], #STA - 0X06
    [CO|MI, RO|II|IC, CO|MI, AI|RO|IC, RC], #LDI - 0X07
    [CO|MI, RO|II|IC, CO|MI, CI|RO, RC], #JMP - 0X08
    [CO|MI, RO|II|IC, RC], # JC - 0X09
    [CO|MI, RO|II|IC, RC], # JZ - 0X0a
    [CO|MI, RO|II|IC, AO|DI, RC], #OUT - 0X0b
    [CO|MI, RO|II|IC, HL, RC], #HLT - 0X0a
]
microcode = [None, None, None, None]
for instruction in microcodeTemplate:
    while len(instruction) < 16:
        instruction.append(0)
while len(microcodeTemplate) < 2**5:
    microcodeTemplate.append(microcodeTemplate[0])
flags = [0b00, 0b01, 0b10, 0b11]
for flag in flags:
    for instruction in microcodeTemplate:
        for i in range(len(microcode)):
            microcode[i] = copy.deepcopy(microcodeTemplate)
            if i == 0b01:
                microcode[i][0x09] = microcodeTemplate[0x08]
            if i == 0b10:
                microcode[i][0x0a] = microcodeTemplate[0x08]
            if i == 0b11:
                microcode[i][0x09] = microcodeTemplate[0x08]
                microcode[i][0x0a] = microcodeTemplate[0x08]

# print(microcode)
binary = [None] * 2**11
for flag in flags:
    for instructionIndex, instruction in enumerate(microcodeTemplate):
        for microCodeIndex, microcode in enumerate(instruction):
            address = instructionIndex | flag << 5 | microCodeIndex << 7
            binary[address] = microcode
for index, value in enumerate(binary):
    if value == None:
        print(format(index, '011b'))
with open("microcode.txt", "w") as f:
    for i in range(len(binary)):
        f.write(str(binary[i]))
EEPROMNUM = 0
for i in range(len(binary)):
    binary[i] = (binary[i] >> (EEPROMNUM * 8) & 0b11111111)
with open("microcode.bin", "wb") as f:
    f.write(bytes(binary))