class Assembler(object):
    def __init__(self, asmpath='', mripath='', rripath='', ioipath='') -> None:
        """
        Assembler class constructor.

        Initializes 7 important properties of the Assembler class:
        -   self.__address_symbol_table (dict): stores labels (scanned in the first pass)
            as keys and their locations as values.
        -   self.__bin (dict): stores locations (or addresses) as keys and the binary 
            representations of the instructions at these locations (job of the second pass) 
            as values.
        -   self.__asmfile (str): the file name of the assembly code file. This property
            is initialized and defined in the read_code() method.
        -   self.__asm (list): list of lists, where each outer list represents one line of 
            assembly code and the inner list is a list of the symbols in that line.
            for example:
                ORG 100
                CLE
            will yiels __asm = [['org', '100'] , ['cle']]
            Notice that all symbols in self.__asm are in lower case.
        -   self.__mri_table (dict): stores memory-reference instructions as keys, and their
            binary representations as values.
        -   self.__rri_table (dict): stores register-reference instructions as keys, and their
            binary representations as values.
        -   self.__ioi_table (dict): stores input-output instructions as keys, and their
            binary representations as values.
        
        Thie constructor receives four optional arguments:
        -   asmpath (str): path to the assembly code file.
        -   mripath (str): path to text file containing the MRI instructions. The file should
            include each intruction and its binary representation separated by a space in a
            separate line. Their must be no empty lines in this file.
        -   rripath (str): path to text file containing the RRI instructions. The file should
            include each intruction and its binary representation separated by a space in a
            separate line. Their must be no empty lines in this file.
        -   ioipath (str): path to text file containing the IOI instructions. The file should
            include each intruction and its binary representation separated by a space in a
            separate line. Their must be no empty lines in this file.
        """
        super().__init__()
        # Address symbol table dict -> {symbol: location}
        self.__address_symbol_table = {}
        # Assembled machine code dict -> {location: binary representation}
        self.__bin = {}
        # Load assembly code if the asmpath argument was provided.
        if asmpath:
            self.read_code(asmpath)   
        # memory-reference instructions
        self.__mri_table = self.__load_table(mripath) if mripath else {}
        # register-reference instructions
        self.__rri_table = self.__load_table(rripath) if rripath else {}
        # input-output instructions
        self.__ioi_table = self.__load_table(ioipath) if ioipath else {}
    

    def read_code(self, path:str):
        """
        opens .asm file found in path and stores it in self.__asmfile.
        Returns None
        """
        assert path.endswith('.asm') or path.endswith('.S'), \
                        'file provided does not end with .asm or .S'
        self.__asmfile = path.split('/')[-1] # on unix-like systems
        with open(path, 'r') as f:
            # remove '\n' from each line, convert it to lower case, and split
            # it by the whitespaces between the symbols in that line.
            self.__asm = [s.rstrip().lower().split() for s in f.readlines()]


    def assemble(self, inp='') -> dict:
        assert self.__asm or inp, 'no assembly file provided'
        if inp:
            assert inp.endswith('.asm') or inp.endswith('.S'), \
                        'file provided does not end with .asm or .S'
        # if assembly file was not loaded, load it.
        if not self.__asm:
            self.read_code(inp)
        # remove comments from loaded assembly code.
        self.__rm_comments()
        # do first pass.
        self.__first_pass()
        # do second pass.
        self.__second_pass()
        # The previous two calls should store the assembled binary
        # code inside self.__bin. So the final step is to return
        # self.__bin
        return self.__bin


    # PRIVATE METHODS
    def __load_table(self, path) -> dict:
        """
        loads any of ISA tables (MRI, RRI, IOI)
        """
        with open(path, 'r') as f:
            t = [s.rstrip().lower().split() for s in f.readlines()]
        return {opcode:binary for opcode,binary in t}


    def __islabel(self, string) -> bool:
        """
        returns True if string is a label (ends with ,) otherwise False
        """
        return string.endswith(',')


    def __rm_comments(self) -> None:
        """
        remove comments from code
        """
        for i in range(len(self.__asm)):
            for j in range(len(self.__asm[i])):
                if self.__asm[i][j].startswith('/'):
                    del self.__asm[i][j:]
                    break


    def __first_pass(self) -> None:
        """
        Runs the first pass over the assmebly code in self.__asm.
        Should search for labels, and store the labels alongside their locations in
        self.__address_symbol_table. The location must be in binary (not hex or dec).
        Returns None
        """
        pass



    def __second_pass(self) -> None:
        """
        Runs the second pass on the code in self.__asm.
        Should translate every instruction into its binary representation using
        the tables self.__mri_table, self.__rri_table and self.__ioi_table. It should
        also store the translated instruction's binary representation alongside its 
        location (in binary too) in self.__bin.
        """
        pass