#read.in.py
#updated: 7/27/2020
from pathlib import Path
from decode_RV32I import decode_format

dir = 'C:/Users/shrey/Documents/pipeline_simulator/test_cases'
debug_mode = True

#Defined for read file
REGISTERS = 1
CODE = - 1
MEMORY = 0

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
                #RV32I instructions
                intruction_bank.append(decode_format(line))
    return register_bank, memory_bank, intruction_bank
