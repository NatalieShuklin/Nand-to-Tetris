#author - Natalia Shuklin
# the parser file for the 7th project in Nand 2 Tetris course


class Parser:

    CommandTypes = {"C_ARITHMETIC",
                    "C_PUSH",
                    "C_POP",
                    "C_LABEL",
                    "C_GOTO",
                    "C_IF",
                    "C_FUNCTION",
                    "C_CALL"}

    def __init__(self, file):
        """
        Opens the input file or stream and gets ready to parse it
        :param file: input file
        """
        self.file = open(file)
        self.lineCounter = 0
        self.currCommand = ""  # current command to parse
        self.lines = self.file.readlines()  # split file lines
        self.lines = [line.split("//")[0] for line in self.lines]  # uncomment line
        self.lines = [line.replace('\r\n', '') for line in self.lines]  #remove linux new line
        self.lines = [line.replace('\n', '') for line in self.lines]  # removes '\n'
        self.lines = [line for line in self.lines if line != '']  # removes empty lines


    def hasMoreCommands(self):
        """
        Are there more commands in the input?
        :return: true if yes otherwise false
        """
        return self.lineCounter < len(self.lines)

    def advance(self):
        """
        Reads the next command from the input and
        makes it the current command. Should be
        called only if hasMoreCommands() is
        true. Initially there is no current command.
        :return:
        """

        self.currCommand = self.lines[self.lineCounter]
        self.lineCounter += 1
        return self.currCommand

    def commandType(self):
        """
        Returns the type of the current command.
        C_ARITHMETIC is returned for all the
        arithmetic VM commands.
        :return: type of current command from the Commands dictionary
        """
        if("sub" or " add" or "neg" or "eq" or "gt" or "lt" or "and" or "or" or "not") in self.currCommand:
            return "C_ARITHMETIC"
        if "push" in self.currCommand:
            return "C_PUSH"
        if "pop" in self.currCommand:
            return "C_POP"
        # if "label" in self.currCommand:
        #     return "C_LABEL"
        # if "if-goto" in self.currCommand:
        #     return "C_IF"
        # if "goto" in self.currCommand:
        #     return "C_GOTO"
        # if "function" in self.currCommand:
        #     return "C_FUNCTION"
        # if "return" in self.currCommand:
        #     return "C_RETURN"
        # if "call" in self.currCommand:
        #     return "C_CALL"

    def arg1(self):
        """
        Returns the first argument of the current
        command. In the case of C_ARITHMETIC,
        the command itself (add, sub, etc.) is
        returned. Should not be called for
        C_RETURN.
        :return: first arg in curr. command
        """
        if self.commandType() == "C_PUSH" or self.commandType() == "C_POP":
            return self.currCommand.split(" ")[1]
        else:
            return self.currCommand

    def arg2(self):
        """
        Returns the second argument of the current
        command. Should be called only if the
        current command is C_PUSH, C_POP,
        C_FUNCTION, or C_CALL.
        :return: 2nd arg of curr. command
        """
        return self.currCommand.split(" ")[2]