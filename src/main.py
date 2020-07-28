#main.py
#updated: 7/27/2020

from read_in import read_file

def main():
    register_bank, memory_bank, intruction_bank = read_file()
    print(intruction_bank)
    

if __name__ == "__main__":
    main()
