# author - Natalia Shuklin
# the main file for the 7th project in Nand 2 Tetris course
# runs the VM translator

import sys
import os
import CodeWriter
import Parser


def translateFile(file, code):
    parse = Parser.Parser(file)
    while parse.hasMoreCommands():
        parse.advance()
        if parse.commandType() == "C_PUSH" or parse.commandType() == "C_POP":
            code.writePushPop(parse.commandType(), parse.arg1(), parse.arg2())
        else:
            code.writeArithmetic(parse.currCommand)


if __name__ == "__main__":
    """
    main function , gets user input the input directory/file
    and runs VM translator
    """
    userInput = sys.argv[1]

    if os.path.isdir(userInput):
        if userInput.endswith("/") or userInput.endswith("\\"):
            userInput = userInput[0:-1]


        files = os.listdir(userInput)
        for file in files:
            if file.endswith('.vm'):
                dirname = os.path.abspath(os.getcwd())
                filename = file.split(".vm")[0]
                if "\\" in userInput :
                    outputFile = userInput + "\\" + str(filename) + ".asm"
                else:
                    outputFile = userInput + "/" + str(filename) + ".asm"
                code = CodeWriter.CodeWriter(outputFile)
                code.setFileName(file)
                translateFile(userInput + "/" + file, code)
                code.close()
    else:
        outputFile = userInput.split('.')[0] + ".asm"
        code = CodeWriter.CodeWriter(outputFile)
        translateFile(userInput, code)
        code.close()


