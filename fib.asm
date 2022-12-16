LDI 1
STA 0x20
LDI 0
loop:
    STA 0x21
    LDA 0x20
    ADD 0x21
    OUT
    STA 0x20
    LDA 0x21
    ADD 0x20
    JC stop
    OUT
    JMP loop
stop:
    HLT