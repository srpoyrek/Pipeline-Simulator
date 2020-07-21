from pathlib import Path

dir = 'C:/Users/shrey/Documents/pipeline_simulator/test_cases'
debug_mode = True
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
                register_bank[int(line[0].split('R')[1])] = hex(int(line[1].split('\n')[0]))
            if RMC == MEMORY:
                memory_bank[int(line[0])] = hex(int(line[1].split('\n')[0]))
            if RMC == CODE:
                
                pass
                #print(line)
    #print(register_bank)
    #print(memory_bank)
            
        
        
#driver code
read_file()
