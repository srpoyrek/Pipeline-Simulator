
FMT = None 
opcode = None
funct3 = None
funct7 = None
rd = None
rs1 = None
rs2 = None
imm = None

#FMT TYPES
R = 0
I = 1
S = 2
B = 3
J = 4
U = 5


def decode_format(line):
    global FMT, opcode, funct3, funct7, rd, rs1, rs2, imm
    try:
        inst_la = line[0].split('\t')
        label = None if inst_la[0] == '' else inst_la[0]
        inst = inst_la[1]
    except:
        print("Indentation Error: Use tab's")
        return -1
    if label is not None:
        pass
    if inst == 'ADD':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x00
        funct7 = 0x00
    elif inst =='SUB':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x00
        funct7 = 0x20
    elif inst =='XOR':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x04
        funct7 = 0x00
    elif inst =='OR':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x06
        funct7 = 0x00
    elif inst =='AND':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x07
        funct7 = 0x00
    elif inst =='SLL':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x01
        funct7 = 0x00
    elif inst =='SRL':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x05
        funct7 = 0x00
    elif inst =='SRA':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x05
        funct7 = 0x20
    elif inst =='SLT':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x02
        funct7 = 0x00
    elif inst =='SLTU':
        FMT = R
        opcode = 0b0110011
        funct3 = 0x03
        funct7 = 0x00
    elif inst =='ADDI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x00
        funct7 = None
    elif inst =='XORI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x04
        funct7 = None
    elif inst =='ORI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x06
        funct7 = None
    elif inst =='ANDI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x07
        funct7 = None
    elif inst =='SLLI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x01
        funct7 = 0x00
    elif inst =='SRLI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x05
        funct7 = 0x00
    elif inst =='SRAI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x05
        funct7 = 0x20
    elif inst =='SLTI':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x02
        funct7 = None
    elif inst =='SLTIU':
        FMT = I
        opcode = 0b0010011
        funct3 = 0x03
        funct7 = None 
    elif inst == 'LB':
        FMT = I
        opcode = 0b0000011
        funct3 = 0x00
    elif inst =='LH':
        FMT = I
        opcode = 0b0000011
        funct3 = 0x01
    elif inst =='LW':
        FMT = I
        opcode = 0b0000011
        funct3 = 0x02
    elif inst =='LBU':
        FMT = I
        opcode = 0b0000011
        funct3 = 0x04
    elif inst == 'LHU':
        FMT = I
        opcode = 0b0000011
        funct3 = 0x05
    elif inst == 'SB':
        FMT = S
        opcode = 0b0100011 
        funct3 = 0x00
    elif inst =='SH':
        FMT = S
        opcode = 0b0100011 
        funct3 = 0x01
    elif inst =='SW':
        FMT = S
        opcode = 0b0100011 
        funct3 = 0x02
    elif inst =='BEQ':
        FMT = B
        opcode = 0b1100011
        funct3 = 0x00
    elif inst == 'BNE':
        FMT = B
        opcode = 0b1100011
        funct3 = 0x01
    elif inst =='BLT':
        FMT = B
        opcode = 0b1100011
        funct3 = 0x04
    elif inst == 'BGE':
        FMT = B
        opcode = 0b1100011
        funct3 = 0x05
    elif inst =='BLTU':
        FMT = B
        opcode = 0b1100011
        funct3 = 0x06
    elif inst == 'BGEU':
        FMT = B
        opcode = 0b1100011
        funct3 = 0x07
    elif inst =='JAL':
        FMT = J
        opcode = 0b1101111
        funct3 = None
    elif inst == 'JALR':
        FMT = I
        opcode = 0b1101111
        funct3 = 0x00
    elif inst =='LUI':
        FMT = U
        opcode = 0b0110111
    elif inst == 'AUIPC':
        FMT = U
        opcode = 0b0010111
    elif inst =='ECALL':
        FMT = I
        imm = 0x01
    elif inst == 'EBREAK':
        FMT = I
        imm = 0x01
        
    if FMT == R:
        rd = int((line[1].split('R')[1]).split(',')[0])
        rs1 = int((line[2].split('R')[1]).split(',')[0])
        rs2 = int((line[3].split('R')[1]).split(',')[0])
        imm = None
    elif FMT == I:
        if opcode is not 0b111011:
            rd = int((line[1].split('R')[1]).split(',')[0])
            rs2 = None
            if opcode != 0b0000011 and opcode != 0b1101111:
                rs1 = int((line[2].split('R')[1]).split(',')[0])
                imm = int((line[3].split('#')[1]))
                if funct7 is not None:
                    imm = bin(imm)[5:]
            else:
                funct7 = None
                rs1 = int(((line[2].split('(')[1]).split('R')[1]).split(')')[0])
                imm = int(line[2].split('(')[0])
        else:
            rd = None
            rs1 = None
            rs2 = None
            opcode = 0b1110011
            funct7 = 0x00
    
    elif FMT == S:
        rd = None
        funct7 = None
        rs1 = int((line[1].split('R')[1]).split(',')[0])
        rs2 = int(((line[2].split('(')[1]).split('R')[1]).split(')')[0])
    elif FMT == B:
        funct7 = None
        rd = None
        rs1 = int((line[1].split('R')[1]).split(',')[0])
        rs2 = int((line[2].split('R')[1]).split(',')[0])
        imm = None # Needs to write the logic
    elif FMT == J:
        funct7 = None
        rd = int((line[1].split('R')[1]).split(',')[0])
        imm = line[2]
        rs1 = None
        rs2 = None
    elif FMT == U:
        funct3 = None
        funct7 = None
        rs1 = None
        rs2 = None
        rd = int((line[1].split('R')[1]).split(',')[0])
        
    return {"FMT":FMT, "opcode":opcode,"funct3":funct3,"funct7":funct7,"rd":rd, "rs1":rs1 ,"rs2":rs2, "imm":imm,"label":label}
