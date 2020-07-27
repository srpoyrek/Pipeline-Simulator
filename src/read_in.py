from pathlib import Path

dir = 'C:/Users/shrey/Documents/pipeline_simulator/test_cases'
debug_mode = True

#Defined for read file
REGISTERS = 1
CODE = - 1
MEMORY = 0

#FMT TYPES
R = 0
I = 1
S = 2
B = 3
J = 4
U = 5

FMT = None 
opcode = None
funct3 = None
funct7 = None
rd = None
rs1 = None
rs2 = None
imm = None

register_bank = [hex(0)] * 32
memory_bank = [hex(0)] * 1024
intruction_bank = []


def read_file():
    # dir to choose the test case
    entries = Path(dir)
    if not debug_mode:
        for entry in entries.iterdir():
            print(entry.name)
        file_name = input("Enter the input file name: ")
    else:
        file_name = 'input-1.txt'
    print("Reading Testcase " + file_name )

    with open(dir + '/' +file_name,"r") as file_object:
        file_data = file_object.readlines()
    file_object.close()
    #print(file_data)
    global FMT ,opcode, funct3, funct7, rd, rs1, rs2, imm
    RMC = 1 #RMC = 1 0 -1 i.e registers memory code
    for line in file_data:
        if line == 'REGISTERS\n':
            RMC = REGISTERS
        elif line == 'MEMORY\n':
            RMC = MEMORY
        elif line == 'CODE\n':
            RMC = CODE
        else:
            line  = line.split(' ')
            if RMC == REGISTERS:
                #split the 'R'and assign each register value to register bank register array
                register_bank[int(line[0].split('R')[1])] = hex(int(line[1].split('\n')[0]))
                
            if RMC == MEMORY:
                #split and assign each mem value to memory bank array
                memory_bank[int(line[0])] = hex(int(line[1].split('\n')[0]))
            if RMC == CODE:
                try:
                    inst_la = line[0].split('\t')
                    label = None if inst_la[0] == '' else inst_la[0]
                    inst = inst_la[1]
                except:
                    print("Indentation Error: Use tab's")
                    return -1
                    break
                if label is not None:
                    pass
                #RV32I instructions 
                if inst == 'ADD':
                    FMT = R
                    opcode = 0b0110011
                    funct3 = 0x00
                    funct7 = 0x00
                    rd = int((line[1].split('R')[1]).split(',')[0])
                    rs1 = int((line[2].split('R')[1]).split(',')[0])
                    rs2 = int((line[3].split('R')[1]).split(',')[0])
                    imm = None
                elif inst =='SUB':
                    FMT = R
                    opcode = 0b0110011
                    funct3 = 0x00
                    funct7 = 0x20
                    rd = int((line[1].split('R')[1]).split(',')[0])
                    rs1 = int((line[2].split('R')[1]).split(',')[0])
                    rs2 = int((line[3].split('R')[1]).split(',')[0])
                    imm = None
                elif inst =='XOR':
                    FMT = R
                    opcode = 0b0110011
                    funct3 = 0x04
                    funct7 = 0x00
                    rd = int((line[1].split('R')[1]).split(',')[0])
                    rs1 = int((line[2].split('R')[1]).split(',')[0])
                    rs2 = int((line[3].split('R')[1]).split(',')[0])
                    imm = None
                elif inst =='OR':
                    FMT = R
                    opcode = 0b0110011
                    funct3 = 0x06
                    funct7 = 0x00
                    rd = int((line[1].split('R')[1]).split(',')[0])
                    rs1 = int((line[2].split('R')[1]).split(',')[0])
                    rs2 = int((line[3].split('R')[1]).split(',')[0])
                    imm = None
                elif inst =='AND':
                    pass
                elif inst =='SLL':
                    pass
                elif inst =='SRL':
                    pass
                elif inst =='SRA':
                    pass
                elif inst =='SLT':
                    pass
                elif inst =='SLTU':
                    pass
                elif inst =='ADDI':
                    FMT = I
                    opcode = 0b0010011
                    funct3 = 0x00
                    funct7 = None
                    rd = int((line[1].split('R')[1]).split(',')[0])
                    rs1 = int((line[2].split('R')[1]).split(',')[0])
                    rs2 = None
                    imm = int((line[3].split('#')[1]))
                elif inst =='SUBI':
                    pass
                elif inst =='XORI':
                    pass
                elif inst =='ORI':
                    pass
                elif inst =='ANDI':
                    pass
                elif inst =='SLLI':
                    pass
                elif inst =='SRLI':
                    pass
                elif inst =='SRAI':
                    pass
                elif inst =='SLTI':
                    pass
                elif inst =='SLTIU':
                    pass
                elif inst == 'LB':
                    pass
                elif inst =='LH':
                    pass
                elif inst =='LW':
                    pass
                elif inst =='LBU':
                    pass
                elif inst == 'LHU':
                    pass
                elif inst == 'SB':
                    pass
                elif inst =='SH':
                    pass
                elif inst =='SW':
                    pass
                elif inst =='BEQ':
                    pass
                elif inst == 'BNE':
                    FMT = B
                    opcode = 0b1100011
                    funct3 = 0x00
                    funct7 = None
                    rd = None
                    rs1 = int((line[1].split('R')[1]).split(',')[0])
                    rs2 = int((line[2].split('R')[1]).split(',')[0])
                    imm = None
                elif inst =='BLT':
                    pass
                elif inst == 'BGE':
                    pass
                elif inst =='BLTU':
                    pass
                elif inst == 'BGEU':
                    pass
                elif inst =='JAL':
                    pass
                elif inst == 'JALR':
                    pass
                elif inst =='LUI':
                    pass
                elif inst == 'AUIPC':
                    pass
                elif inst =='ECALL':
                    pass
                elif inst == 'EBREAK':
                    pass
                if opcode is not None:
                    intruction_bank.append({ "FMT":FMT, "opcode":opcode,"funct3":funct3,"funct7":funct7,"rd":rd, "rs1":rs1 ,"rs2":rs2, "imm":imm,"label":label})
                #print(line)
    #print(intruction_bank)            
    #print(register_bank)
    #print(memory_bank)
    return register_bank, memory_bank, intruction_bank
            
        
        
#driver code
#read_file()
