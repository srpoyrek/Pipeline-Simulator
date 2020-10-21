############################################################################################################################################################################################
############################################################################################################################################################################################
#File Name: Poyrekar.1808531.py
#Date Created: 08th may 2019
#Course: Advance Topics in Computer Architecture
#Course Number: ECE-6373
#Project: Pipeline Simulation (Integer)
#logic used: check if stalls print stall else print the stage and the instruction. Only Load causes 2 stalls, if forwarding than no stalls.
#so check for load instruction causing stall, no need to do anything for forwarding or bypassing. get the target address in the ID stage
#and Compute branch taken in EX stage, so empty the instructions in the ID/IF registers if branch and fetch the new instructions in next cycle
#(predict not taken branch prediction technique)
#Name:Shreyas Poyrekar
#UHID: 1808531
############################################################################################################################################################################################
############################################################################################################################################################################################
#README
#Enter the input file name when asked (make sure you have the file in the same directory)(files should be .txt specify the extension as well).
#Enter the output file to be created or overwritten when asked.
#See the output in the terminal, press any key when done.
#Open the output file you have named in the program to see the timing information, new register and memory values
############################################################################################################################################################################################
############################################################################################################################################################################################
import math
import sys
import turtle
import string
import copy

Registers=[-1]*32 #define 32 Registers 0-31
Memory=[-1]*125   # define 125 memory locations each storing 8 byte data so 0-992
Instructions=[] #instruction queue

#print all the register values which are used.
def print_registers(Reg):
    for x in range(0,len(Reg)):
        if(Reg[x]!=-1) and not(x==0) :
            print("R{} {}".format(x,Reg[x]))
            
#print all the Memory values which are used.        
def print_memory(Mem):
    for x in range(0,len(Mem)):
        if(Mem[x]!=-1):
            print("{} {}".format(x*8,Mem[x]))

#print all the Memory values which are used.        
def print_inst(Inst):
    for x in Inst:
        print("Add:{}\tI{}\tImm:{}\tD: R{}\tS: R{}\tT: R{}\tJ:{}".format(x['a'],x['n'],x['imm'],x['reg_d'],x['reg_s'],x['reg_t'],x['j']))
        
############################################################################################################################################################################################
#read the register, memory and Instructions sequence
def readFile(filename):
    print("Input:")
    with open(filename) as fp:
        line = fp.readline()
        temp=line.split('\n')
        #read the register values write the values on to the register 
        if(temp[0]=='REGISTERS'):
            print("REGISTERS")
            line = fp.readline()
            temp=line.split(' ')
            while((temp[0]!='MEMORY\n') and (temp[0]!='MEMORY')):
                #print(temp)
                Registers[int(temp[0][1])] = int(temp[1])
                #print(Registers)
                line = fp.readline()
                #print(line)
                temp=line.split(' ')
                #print(temp)
            Registers[0]=0
            print_registers(Registers)
        temp=line.split('\n')
        #print(temp)
        #read the memory input and write the memory blocks
        if(temp[0]=='MEMORY')or (temp[0]=='MEMORY '):
            print("MEMORY")
            line = fp.readline()
            temp=line.split(' ')
            while((temp[0]!='CODE\n') and (temp[0]!='CODE')):
                #print(temp)
                Memory[int(round(int(temp[0])/8))]=int(temp[1])
                line = fp.readline()
                temp=line.split(' ')
            print_memory(Memory)
        
        temp=line.split('\n')
        #read all the instructions
        if(temp[0]=='CODE'):
            print("CODE")
            line = fp.readline()
            temp=line.split(' ')
            cnt=1
            while line:
                print((line.split('\n')[0]))
                #print(temp)
                if temp[0]=='':
                    #print("No Label")
                    if(temp[6]=='LD' or temp[6]=='SD'):
                        Instructions.append({'a':'','n':cnt,'i':temp[6],'imm':int(temp[8][0]),'reg_d':-1,'reg_s':int(temp[8][3]),'reg_t':int(temp[7][1]),'j':''})
                    elif(temp[6]=='DADD' or temp[6]=='SUB'):
                        Instructions.append({'a':'','n':cnt,'i':temp[6],'imm':-1,'reg_d':int(temp[7][1]),'reg_s':int(temp[8][1]),'reg_t':int(temp[9][1]),'j':''})
                    elif(temp[6]=='BNEZ'):
                        Instructions.append({'a':'','n':cnt,'i':temp[6],'imm':-1,'reg_d':int(temp[7][1]),'reg_s':-1,'reg_t':-1,'j':((temp[8]).split('\n'))[0]})
                    elif(temp[6]=='DDADI' or temp[6]=='SUBI'):
                        Instructions.append({'a':'','n':cnt,'i':temp[6],'imm':int(temp[9][1]),'reg_d':int(temp[7][1]),'reg_s':int(temp[8][1]),'reg_t':-1,'j':''})
                else:
                    #print("Label {}".format(temp[0]))
                    if(temp[1]=='LD' or temp[1]=='SD'):
                        Instructions.append({'a':((temp[0]).split(':'))[0],'n':cnt,'i':temp[1],'imm':int(temp[3][0]),'reg_d':-1,'reg_s':int(temp[3][3]),'reg_t':int(temp[2][1]),'j':''})
                    elif(temp[1]=='DADD' or temp[1]=='SUB'):
                        Instructions.append({'a':((temp[0]).split(':'))[0],'n':cnt,'i':temp[1],'imm':-1,'reg_d':int(temp[2][1]),'reg_s':int(temp[3][1]),'reg_t':int(temp[4][1]),'j':''})
                    elif(temp[1]=='BNEZ'):
                        Instructions.append({'a':((temp[0]).split(':'))[0],'n':cnt,'i':temp[1],'imm':-1,'reg_d':int(temp[2][1]),'reg_s':-1,'reg_t':-1,'j':((temp[3]).split('\n'))[0]})
                    elif(temp[1]=='DDADI' or temp[1]=='SUBI'):
                        Instructions.append({'a':'','n':cnt,'i':temp[1],'imm':int(temp[4][1]),'reg_d':int(temp[3][1]),'reg_s':int(temp[3][1]),'reg_t':-1,'j':''})
                line = fp.readline()
                temp=line.split(' ')
                #print(Instructions[cnt-1])
                cnt+=1
            #print_inst(Instructions)
########################################################################################################################################################################################               
#pipeline simulation function          
def pipeline(inst,outfile):
    queue_len=0
    IF1_reg=copy.deepcopy(inst[0])
    IF2_reg=[]
    ID_reg=[]
    EX_reg=[]
    MEM1_reg=[]
    MEM2_reg=[]
    MEM3_reg=[]
    WB_reg=[]
    stall_EX=0
    stall_ID=0
    stall_IF1=0
    stall_IF2=0
    jumperAddress=''
    n_stall=0
    taken=0
    stall_cycle=0
    ints_n=0
    cnt=1
    f= open(outfile, "w")
    print("\nOutput:")
    print("Timing Information")
    #f.write("c#"+str(cnt)+" ")
    #print("c#{}".format(cnt),end=' ')
    while (IF1_reg or IF2_reg or ID_reg or EX_reg or MEM1_reg or MEM2_reg or MEM3_reg) or not (WB_reg):
        #print the cycle
        if cnt!=1:
            f.write("\nc#"+str(cnt)+" ")
            print("\nc#{}".format(cnt),end=' ')
        else:
            f.write("c#"+str(cnt)+" ")
            print("c#{}".format(cnt),end=' ') 
        #print(x)
        if stall_cycle==0:
            #if cnt==7:
             #   print("True")
            stall_EX=0
            stall_ID=0
            stall_IF2=0
            stall_IF1=0
        else:
            stall_cycle= stall_cycle-1

        #check if stall due to LD instruction
        if EX_reg and ID_reg:
            if (EX_reg['i']=='LD'):
                if (EX_reg['reg_t']==ID_reg['reg_s']) or (EX_reg['reg_t']==ID_reg['reg_t']):
                    #print("Stall")
                    n_stall=ID_reg['n']
                    #print(n_stall)
                    stall_EX=1
                    stall_ID=1
                    stall_IF2=1
                    stall_IF1=1
                    stall_cycle=1            
        #shift values form pipeline registers to next pipeline register
        if cnt!=1:
            WB_reg=MEM3_reg
            MEM3_reg=MEM2_reg
            MEM2_reg=MEM1_reg
            MEM1_reg=EX_reg
            EX_reg=ID_reg
            #do not shift is stall
            if not (stall_EX):
                ID_reg=IF2_reg
            else:
                EX_reg=[]
            #do not shift is stall
            if not stall_ID:
                IF2_reg=IF1_reg

            #fetch stage
            if(ints_n<len(inst)-1):
                if not (stall_EX or stall_ID or stall_IF2 or stall_IF1):
                    ints_n+=1
                    queue_len+=1
                    IF1_reg=copy.deepcopy(inst[ints_n])
                    if queue_len>ints_n:
                        IF1_reg['n']=queue_len+1
            else:
                IF1_reg=[]

        #decode stage
        if (ID_reg):
            if ID_reg['i']=='BNEZ':
                jumperAddress=ID_reg['j']
                #print(ID_reg['j'])


        #Execution stage
        if (EX_reg):
            Registers[0]=0
            if EX_reg['i']=='LD':
                Registers[EX_reg['reg_t']]= Memory[int((EX_reg['imm'] + Registers[EX_reg['reg_s']])/8)]  
            if EX_reg['i']=='SD':
                Memory[int((EX_reg['imm'] + Registers[EX_reg['reg_s']])/8)]= Registers[EX_reg['reg_t']]
            if EX_reg['i']=='DADD':
                Registers[EX_reg['reg_d']] = Registers[EX_reg['reg_s']] + Registers[EX_reg['reg_t']]
            if EX_reg['i']=='SUB':
                Registers[EX_reg['reg_d']] = Registers[EX_reg['reg_s']] - Registers[EX_reg['reg_t']]
            if EX_reg['i']=='DADDI':
                Registers[EX_reg['reg_d']] = Registers[EX_reg['reg_s']] + EX_reg['imm']
            if EX_reg['i']=='SUBI':
                Registers[EX_reg['reg_d']] = Registers[EX_reg['reg_s']] - EX_reg['imm']
            if EX_reg['i']=='BNEZ':
                if Registers[EX_reg['reg_d']]!=0:
                    for s in range(0,len(inst)):
                        if(inst[s]['a']==jumperAddress):
                            ints_n=s-1
                            taken=1
                        #print(taken)
        #print/write the timing informatioin
        if WB_reg:
            f.write("I"+str(WB_reg['n'])+"-WB ")
            print("I{}-WB".format(WB_reg['n']),end=" ")
        if MEM3_reg:
            f.write("I"+str(MEM3_reg['n'])+"-MEM3 ")
            print("I{}-MEM3".format(MEM3_reg['n']),end=" ")
        if MEM2_reg:
            f.write("I"+str(MEM2_reg['n'])+"-MEM2 ")
            print("I{}-MEM2".format(MEM2_reg['n']),end=" ")
        if MEM1_reg:
            f.write("I"+str(MEM1_reg['n'])+"-MEM1 ")
            print("I{}-MEM1".format(MEM1_reg['n']),end=" ")
        if EX_reg:
            if not stall_EX:
                f.write("I"+str(EX_reg['n'])+"-EX ")
                print("I{}-EX".format(EX_reg['n']),end=" ")
            else:
                f.write("I"+str(EX_reg['n'])+"-stall ")
                print("I{}-stall".format(EX_reg['n']),end=" ")
        if ID_reg:
            if not stall_ID:
                f.write("I"+str(ID_reg['n'])+"-ID ")
                print("I{}-ID".format(ID_reg['n']),end=" ")
            else:
                f.write("I"+str(ID_reg['n'])+"-stall ")
                print("I{}-stall".format(ID_reg['n']),end=" ")
        if IF2_reg:
            if not stall_IF2:
                f.write("I"+str(IF2_reg['n'])+"-IF2 ")
                print("I{}-IF2".format(IF2_reg['n']),end=" ")
            else:
                f.write("I"+str(IF2_reg['n'])+"-stall ")
                print("I{}-stall".format(IF2_reg['n']),end=" ")
        if IF1_reg:
            if not stall_IF1:
                f.write("I"+str(IF1_reg['n'])+"-IF1 ")
                print("I{}-IF1".format(IF1_reg['n']),end=" ")
            else:
                f.write("I"+str(IF1_reg['n'])+"-stall ")
                print("I{}-stall".format(IF1_reg['n']),end=" ")
        # empty the instructions if taken branch
        if taken:
            #print(ints_n)
            ID_reg=[]
            IF2_reg=[]
            IF1_reg=[]
            taken=0
            
        cnt+=1
    # write reg and mem values in file
    f.write("\nREGISTERS")
    for x in range(0,len(Registers)):
        if(Registers[x]!=-1) and not(x==0) :
            f.write("\nR"+str(x)+" "+str(Registers[x]))
            #print("R{} {}".format(x,Reg[x]))
    f.write("\nMEMORY")
    for x in range(0,len(Memory)):
        if(Memory[x]!=-1):
            f.write("\n"+str(x*8)+" "+str(Memory[x]))
            #print("{} {}".format(x*8,Mem[x]))
    f.close()
###########################################################################################################################################################################################    
def main():
    #get the input file and output file name
    inputfile=input("\nEnter the Input Text File with Extension: ")
    outputfile=input(("Enter the Name of the Output File to be Created with Extension: "))
    #read the file
    readFile(inputfile)
    #pass the instructions in pipeline
    pipeline(Instructions,outputfile)
    #print the register values
    print("\n\nREGISTERS")
    #print the memory values
    print_registers(Registers)
    print("\nMEMORY")
    print_memory(Memory)
    input('\nPress any key to close')
    #End

if __name__ == '__main__':
    main()
