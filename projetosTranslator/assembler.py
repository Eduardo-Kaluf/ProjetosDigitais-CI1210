def to_twos_complement(n: int, bits: int = 4) -> str:
    if n >= 0:
        return f"{n:0{bits}b}"
    else:
        return f"{(1 << bits) + n:0{bits}b}"

# "INSTRUCTION": (RD, RS1, RS2, IMM, OPCODE)
opcodes = {
    "ADD":  (True, True, True, False, "0000"),
    "ADDI": (True, True, False, True, "0001"),
    "SUB":  (True, True, True, False, "0010"),
    "SLLI": (True, True, False, True, "0011"),
    "JAL":  (True, False, False, True, "0100"),
    "JALR": (True, True, False, True, "0101"),
    "LW":   (True, True, False, True, "0110"),
    "SW":   (False, True, True, True, "0111"),
    "BEQ":  (False, True, True, True, "1000"),
    "BNE":  (False, True, True, True, "1001"),
    "BLT":  (False, True, True, True, "1010"),
    "BGE":  (False, True, True, True, "1011"),
    "AND":  (True, True, True, False, "1100"),
    "OR":   (True, True, True, False, "1101"),
    "HALT": (False, False, False, False, "1110"),
    "RESET": (False, False, False, False, "1111"),
}

registers = {
    "X0": "0000",
    "SP": "0001",
    "T0": "0010",
    "T1": "0011",
    "T2": "0100",
    "T3": "0101",
    "S0": "0110",
    "S1": "0111",
    "S2": "1000",
    "S3": "1001",
    "S4": "1010",
    "S5": "1011",
    "A0": "1100",
    "A1": "1101",
    "A2": "1110",
    "RA": "1111"
}

output = []
odd_cases = ["SW", "BEQ", "BNE", "BLT", "BGE"]

with open("teste_geral.txt", "r") as inputFile:
    lines = inputFile.readlines()

    fb = open("binary_output.txt", "w")
    fh = open("hex_output.txt", "w")

    for line in lines:
        command = ""

        info = [element.strip() for element in line.split(",")]
        command_name = info[0]

        # IMM
        if opcodes[command_name][3] == True:
            if (command_name == "JAL"):
                command = command + to_twos_complement(int(info[2]), 8)
                print(command)
            else:
                command = command + to_twos_complement(int(info[3]), 8)
                print(command)
        else:
            command = command + "00000000"

        # OPCODE
        command = command + opcodes[command_name][4]
        
        # RS2
        if command_name in odd_cases:
            command = command + registers[info[2]]
        elif opcodes[command_name][2] == True:
            command = command + registers[info[3]]
        else:
            command = command + "0000"
   
        # RS1
        if command_name in odd_cases:
            command = command + registers[info[1]]
        elif opcodes[command_name][1] == True:
            command = command + registers[info[2]]
        else:
            command = command + "0000"
        
        # RD
        if opcodes[command_name][0] == True:
            command = command + registers[info[1]]
        else:
            command = command + "0000"

        hexadecimal_number = hex(int(command, 2))[2:]

        fb.write(command + "\n")
        fh.write(hexadecimal_number + "\n")


fb.close()
fh.close()
