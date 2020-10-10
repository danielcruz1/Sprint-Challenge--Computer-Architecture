"""CPU functionality."""

import sys



class CPU:
    """Main CPU class."""

    def __init__(self):
        #STEP 1: Add constructor to cpu.py
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.register = [0] * 8
        self.running = True
        # self.reg = [0] * 8
        self.SP = 0xf4

        #STEP 9: Branch Table implementation
        self.branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100000: self.ADD,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b00010001: self.RET,
            0b01010000: self.CALL
        }

    def load(self, filename):
        """Load a program into memory."""
        # STEP 7 Un-hardcode the machine code
        filename = sys.argv[1]
        address = 0
        with open(filename) as f:
            #for address, line in enumerate(f):
                #line = line.split('#')
            for line in f:
                line = line.split('#')[0].strip()

                try:
                    #v = int(line[0], 2)
                    v = int(line, 2)
                except ValueError:
                    continue
                self.ram[address] = v
                #print([address], v)
                address += 1

    def alu(self, op, reg_a, reg_b):

        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        #elif op == "SUB": etc

        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    #STEP 2: add ram_read & ram_write
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def HLT(self):
        self.running = False

    def LDI(self):
        address = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.register[address] = value

    def PRN(self):
        address = self.ram_read(self.pc + 1)
        value = self.register[address]
        print(value)

    def ADD(self):
        operandA = self.ram_read(self.pc + 1)
        operandB = self.ram_read(self.pc + 2)
        self.alu('ADD', operandA, operandB)

    def MUL(self):
        operandA = self.ram_read(self.pc + 1)
        operandB = self.ram_read(self.pc + 2)
        self.alu('MUL', operandA, operandB)

    def PUSH(self):
        self.SP -= 1
        address = self.ram[self.pc + 1]
        value = self.register[address]
        self.ram[self.SP] = value

    def POP(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.SP]
        self.register[address] = value
        self.SP += 1

    def CALL(self):
        self.SP -= 1
        ret_address = self.pc + 2
        self.ram[self.SP] = ret_address
        reg = self.ram[self.pc + 1]
        self.pc = self.register[reg]

    def RET(self):
        ret_address = self.ram[self.SP]
        self.pc = ret_address
        self.SP += 1

    #STEP 3: Implement 'run' method
    def run(self):
        """Run the CPU."""
        
        while self.running:
            IR = self.ram_read(self.pc)
            if IR in self.branch_table:
                self.branch_table[IR]()
                operands = (IR & 0b11000000) >> 6
                param = (IR & 0b00010000) >> 4

                if not param:
                    self.pc += operands +1

'''                   
            #IR = _Instruction Register_
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            #STEP 4: Implement 'HLT' instruction handler
            ### Halt the CPU (and exit the emulator)
            if IR == prog['HLT']:
                self.running = False

            #STEP 5: Implement 'LDI' instruction
            ### Set the value of a register to an integer
            elif IR == prog['LDI']:
                address = operand_a
                value = operand_b
                self.register[address] = value
                self.pc += 3

            #STEP 6: Add 'PRN' instruction
            ### Print to the console the decimal integer value that is stored in the given register.
            elif IR == prog['PRN']:
                address = operand_a
                value = self.register[address]
                print(value)
                self.pc += 2

            #STEP 8: Implement a Multiply and print result
            elif IR == prog['MUL']:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            #STEP 10: System Stack (PUSH & POP)
            elif IR == prog['PUSH']:

                address = operand_a
                value = self.register[address]
                self.SP -= 1
                self.ram[self.SP] = value
                self.pc += 2

            elif IR == prog['POP']:
                address = operand_a
                value = self.ram[self.SP]
                self.register[address] = value

                self.SP += 1
                self.pc += 2

            else:
                print(f"Can't find {IR} with index of {self.pc}")
                sys.exit(1)
'''