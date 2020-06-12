from pathlib import Path

dir = 'C:/Users/shrey/Documents/pipeline_simulator/test_cases'

def read_file():
    entries = Path(dir)
    for entry in entries.iterdir():
        print(entry.name)
    file_name = input("Enter the file name: ")
    file_object = open(dir + '/' +file_name,"r")
    
    #read the file and write onto instruction & data memory also the register bank

    file_object.close()
    
