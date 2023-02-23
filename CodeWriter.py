#author - Natalia Shuklin
# the codewriter file for the 7th project in Nand 2 Tetris course

class CodeWriter:
    def __init__(self, file):
        """
        Opens the output file/stream and gets ready
        to write into it.
        :param file:
        """
        self.file = open(file, 'w')
        self.variableCounter = 0

    codeSegments = {"local": "LCL", "argument": "ARG", "this": "THIS",
                    "that": "THAT", "pointer": "3", "temp": "5"}

    def binaryOperation(self, operation):
        """
        performing the binary operation
        """
        commandOutput = "@SP\n" + \
                        "M = M - 1\n" + \
                        "A = M \n" + \
                        "D = M\n" + \
                        "@SP\n" + \
                        "M = M - 1\n" + \
                        "A = M \n" + \
                        "M = M " + operation + "D\n" + \
                        "@SP\n" + \
                        "M = M + 1\n"
        return commandOutput

    def unaryOperation(self, operation):
        """
        performing the unary operation
        """
        commandOutput = "@SP\n" + \
                        "M = M - 1\n" + \
                        "A = M \n" + \
                        "M = " + operation + "M\n" + \
                        "@SP\n" + \
                        "M = M + 1\n"
        return commandOutput

    def compareOperation(self, command):
        """
        performs the eq/lt/gt comparison, without overflowing
        """
        self.variableCounter += 1
        commandOutput = "@SP\n" + \
                        "M = M - 1\n" +\
                        "A = M\n" +\
                        "D = M\n" +\
                        "@R13\n" +\
                        "M = D\n" +\
                        "@NegativeY" + str(self.variableCounter) + "\n" +\
                        "D;JLT\n" +\
                        "@SP\n" +\
                        "M = M - 1\n" +\
                        "A = M\n" +\
                        "D = M\n" +\
                        "@NegativeXPositiveY" + str(self.variableCounter) + "\n" +\
                        "D;JLT\n" +\
                        "@R13\n" +\
                        "D = D - M\n" +\
                        "@COMPARE" + str(self.variableCounter) + "\n" +\
                        "0;JMP\n" +\
                        "(NegativeY" + str(self.variableCounter) + ")\n" + \
                        "@SP\n" +\
                        "M = M - 1\n" +\
                        "A = M\n" +\
                        "D = M\n" +\
                        "@NegativeYPositiveX" + str(self.variableCounter) + "\n" +\
                        "D;JGT\n" +\
                        "@R13\n" +\
                        "D = D - M\n" +\
                        "@COMPARE" + str(self.variableCounter) + "\n" +\
                        "0;JMP\n" +\
                        "(NegativeXPositiveY" + str(self.variableCounter) + ")\n" + \
                        "D = -1\n" +\
                        "@COMPARE" + str(self.variableCounter)+ "\n" +\
                        "0;JMP\n" +\
                        "(NegativeYPositiveX" + str(self.variableCounter) + ")\n" + \
                        "D = 1\n" +\
                        "@COMPARE" + str(self.variableCounter) + "\n" +\
                        "0;JMP\n" +\
                        "(COMPARE" + str(self.variableCounter) + ")\n" + \
                        "@ISTRUE" + str(self.variableCounter) + "\n" +\
                        "D;J" + command.upper()+"\n" +\
                        "D = 0\n" +\
                        "@FINISH" + str(self.variableCounter) + "\n" +\
                        "0;JMP\n" +\
                        "(ISTRUE" + str(self.variableCounter) + ")\n" + \
                        "D = -1\n" +\
                        "@FINISH" + str(self.variableCounter) + "\n" +\
                        "0;JMP\n" +\
                        "(FINISH" + str(self.variableCounter) + ")\n" + \
                        "@SP\n" +\
                        "A = M\n" +\
                        "M = D\n" +\
                        "@SP\n" +\
                        "M = M + 1\n"

        return commandOutput

    def getCodeSegment(self, segment):
        """
        returns the assembly segment by the assumption of it in RAM location
        :param segment:
        :return:
        """
        return self.codeSegments[segment]

    def push(self):
        """
        push into our RAM stack the contents of current D
        """
        commandAssembly = "@SP\n" + \
                          "A=M\n" + \
                          "M=D\n" + \
                          "@SP\n" + \
                          "M=M+1\n"
        return commandAssembly

    def pop(self, segment, index):
        commandStr = "@" + index + "\n" + \
                     "D = A\n" + \
                     "@" + self.getCodeSegment(segment) + "\n"
        if (segment == "local") or (segment == "that") or (segment == "this") or (segment == "argument"):
            commandStr += "A = M\n"
        commandStr += "D = A + D\n" + \
                      "@R13\n" + \
                      "M = D\n" + \
                      "@SP\n" + \
                      "M = M - 1\n" + \
                      "A = M\n" + \
                      "D = M\n" + \
                      "@R13\n" + \
                      "A = M\n" + \
                      "M = D\n"

        return commandStr

    def  setFileName(self, fileName):
        """
        Informs the code writer that the translation of a new VM file is started.
        """
        print(" File translating has started, for - " +fileName)

    def writeArithmetic(self, command):
        """
        Writes the assembly code that is the
        translation of the given arithmetic command
        :param command:
        :return:
        """
        commandAssembly = ''
        if command == "add":
            commandAssembly = self.binaryOperation("+")
        elif command == "sub":
            commandAssembly = self.binaryOperation("-")
        elif command == "neg":
            commandAssembly = self.unaryOperation("-")
        elif command == "and":
            commandAssembly = self.binaryOperation("&")
        elif command == "or":
            commandAssembly = self.binaryOperation("|")
        elif command == "not":
            commandAssembly = self.unaryOperation("!")
        else:
            commandAssembly = self.compareOperation(command)

        self.file.write(commandAssembly)

    def writePushPop(self, command, segment, index):
        """
        Writes the assembly code that is the  translation of the given command, where
        command is one of the two enumerated values: C_PUSH or C_POP
        """
        commandAssembly = ''
        if command == "C_PUSH":
            if segment == "temp" or segment == "pointer":
                commandAssembly = "@" + index + "\n" + \
                                  "D = A\n" + \
                                  "@" + self.getCodeSegment(segment) + "\n" + \
                                  "A = A + D\n" + \
                                  "D = M\n" + \
                                  self.push()

            elif segment == "this" or segment == "that" or segment == "local" or segment == "argument":
                commandAssembly = "@" + index + "\n" + \
                                  "D = A\n" + \
                                  "@" + self.getCodeSegment(segment) + "\n" + \
                                  "A = M+D\n" + \
                                  "D = M\n" + \
                                  self.push()
            elif segment == "constant":
                commandAssembly = "@" + index + "\n" + \
                                  "D=A\n" + \
                                  self.push()
            elif segment == "static":
                commandAssembly = "@" + self.file.name.split(".")[0].replace('/', '.') + "." + index + "\n" + \
                                  "D = M\n" + \
                                  self.push()

        else:
            if segment == "static":
                commandAssembly = "@SP\n" + \
                                  "M = M - 1\n" + \
                                  "A = M\n" + \
                                  "D = M\n" + \
                                  "@" + self.file.name.split(".")[0].replace('/', '.') + "." + index + "\n" + \
                                  "M = D\n"
            else:
                commandAssembly = self.pop(segment, index)

        self.file.write(commandAssembly)

    def close(self):
        """
        close the output file
        """
        self.file.close()
