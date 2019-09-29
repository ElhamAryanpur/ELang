#!/bin/env python3
# encoding:utf-8

"""
ELang.py -- A translator between humans and computers
Copyright(c) 2019, Elham Aryanpur

"""

# Import system modules
import os

COMPILER_NAME = "C++"
COMPILER_DATA = {
    # * The contents must always be in str format.
    "G++Path": "",
    "Flags": "''"
}


class ELang():
    """
    class ELang():
        The main ELang C++ compiler.
    """

    def __init__(self):
        """
        def __init__():
            The initialization of ELang() class.
        """

        self.config = {}
        self.filename = "c.elpp"
        self.data = []
        self.comp_data = []
        self.commands = []
        self.vars = {}
        self.func_var = {}
        self.read_finalize = False
        self.write_finalize = False
        self.append_finalize = False
        self.func = False
        self.data_types = ["string", "int"]
        self.features = [
            "show",
            "variable",
            "add",
            "subtract",
            "multiply",
            "divide",
            "take",
            "read",
            "write",
            "append",
            "if",
            "end",
            "define",
            "function",
            "change",
            "native",
            "run"
        ]

    def reader(self, file_name=None):
        """
        def reader():
            Reads the file (elpp program) contents to be compiled.
        """

        if file_name is None:
            # If filename is empty
            try:
                PATH = str(os.path.join(os.getcwd(), self.filename))
                if os.path.isfile(PATH):
                    # If file_name does exist:
                    with open(str(self.filename), "r") as f:
                        # Read file line by line and save it to golobal variable data:
                        self.data = f.readlines()
                else:
                    # If file_name does not exist:
                    print("ERR: FILE {} DOES NOT EXIST!".format(str(self.filename)))
            except FileNotFoundError:
                print("ERR: FILE {} NOT FOUND!".format(str(self.filename)))

        else:
            # If filename is not empty
            try:
                # Reading the file extention
                extention = str(file_name)[-4:]
                if extention != "elpp":
                    # If file extention is wrong:
                    print("ERR: WRONG FILE EXTENTION FOR {}! \nMUST BE: .elpp".format(str(file_name)))
                    exit()

                PATH = str(os.path.join(os.getcwd(), str(file_name)))
                if os.path.isfile(PATH):
                    # If file_name does exist:
                    with open(str(file_name), "r") as f:
                        # Read file line by line and save it to golobal variable data:
                        self.data = f.readlines()
                    del file_name
                    del extention
                else:
                    # If file_name does not exist:
                    print("ERR: FILE {} DOES NOT EXIST!".format(str(file_name)))

            except FileNotFoundError:
                print("ERR: FILE {} NOT FOUND!".format(str(file_name)))

    def clean(self):
        """
        def clean():
            Clean the elpp code that comes with newlines and blankspaces.
        """

        # let's make our first list to gather first datas
        data = []
        for i in self.data:
            # This will replace any new line from every lines and append to data list
            i = str(i).replace("\n", "")
            data.append(i)

        # let's make second list to save second loop data
        new_data = []
        for i in data:
            # and now let's delete any lines that is blank and append to new_data list
            if i != "": new_data.append(i)

        # Let's change values of data by redefining it to contain new_data values
        data = new_data

        # Save data to global data and delete useless variables
        self.data = data
        del data
        del new_data

    def indentify(self):
        """
        def indentify():
            Identify and save keywords to `self.commands`.
        """

        # Do a loop in data
        for i in self.data:
            # Split each to have clear view
            o = i.split()
            # Check if first word is a keyword!
            if o[0].lower() in self.features:
                # Deleting the keyword and putting them into a list
                i = i.replace(str(str(o[0]) + " "), "")
                data = [o[0].lower(), [i]]
                # And appending it to commands
                self.commands.append(data)

    def parse(self):
        """
        def parse():
            Parse the commands.
        """

        data = []
        for i in self.commands:
            o = i[1][0].split()
            if i[0] == self.features[0]:
                data.append(i)
            elif i[0] == self.features[1]:
                var_data = str(i[1][0])
                data_word = str(o[0])
                equalt_word = str(o[1])
                var_data = var_data.replace(str(data_word + " "), "")
                var_data = var_data.replace(str(equalt_word) + " ", "")
                this_data = ["var", [o[0], var_data]]
                data.append(this_data)
            elif i[0] == self.features[2]:
                this_data = ["add", [o[0], o[2], o[4]]]
                data.append(this_data)
            elif i[0] == self.features[3]:
                this_data = ["sub", [o[0], o[2], o[4]]]
                data.append(this_data)
            elif i[0] == self.features[4]:
                this_data = ["mul", [o[0], o[2], o[4]]]
                data.append(this_data)
            elif i[0] == self.features[5]:
                this_data = ["div", [o[0], o[2], o[4]]]
                data.append(this_data)
            elif i[0] == self.features[6]:
                this_data = ["take", [o[0], o[1]]]
                data.append(this_data)
            elif i[0] == self.features[7]:
                this_data = ["read", [o[0], o[2]]]
                data.append(this_data)
            elif i[0] == self.features[8]:
                this_data = ["write", [o[0], o[2]]]
                data.append(this_data)
            elif i[0] == self.features[9]:
                this_data = ["append", [o[0], o[2]]]
                data.append(this_data)
            elif i[0] == self.features[10]:
                this_data = ["if", [o[0], o[1], o[2]]]
                data.append(this_data)
            elif i[0] == self.features[11]:
                data.append(["end"])
            elif i[0] == self.features[12]:
                this_data = ["def", [o[0]], []]
                del o[0]
                del o[0]
                for p in o:
                    this_data[2].append(p)
                data.append(this_data)
            elif i[0] == self.features[13]:
                this_data = ["func", o[0], []]
                del o[0]
                for p in o:
                    this_data[2].append(p)
                data.append(this_data)
            elif i[0] == self.features[14]:
                this_data = ["change", [o[0], o[2]]]
                data.append(this_data)
            elif i[0] == self.features[15]:
                data.append(i)
            elif i[0] == self.features[16]:
                data.append(i)

        self.data = data

    def compile(self):
        """
        def compile():
            Translate the elpp file into a working C++ (cpp) program
        """

        name = config["FileName"]
        self.reader(name)
        self.clean()
        self.indentify()
        self.parse()
        self.commands = []
        for i in self.data:
            if i[0] == "show":
                self.comp_data = i[1]
                self.show()
            elif i[0] == "var":
                if self.func:
                    self.func_var[i[1][0]] = i[1][1]
                else:
                    self.vars[i[1][0]] = i[1][1]
                self.comp_data = [i[1][0], i[1][1]]
                self.var()
            elif i[0] == "add":
                self.comp_data = [i[1][0], i[1][1], i[1][2]]
                self.add()
            elif i[0] == "sub":
                self.comp_data = [i[1][0], i[1][1], i[1][2]]
                self.sub()
            elif i[0] == "mul":
                self.comp_data = [i[1][0], i[1][1], i[1][2]]
                self.mul()
            elif i[0] == "div":
                self.comp_data = [i[1][0], i[1][1], i[1][2]]
                self.div()
            elif i[0] == "take":
                self.comp_data = [i[1][0], i[1][1]]
                self.take()
            elif i[0] == "read":
                self.comp_data = [i[1][0], i[1][1]]
                self.read()
            elif i[0] == "write":
                self.comp_data = [i[1][0], i[1][1]]
                self.write()
            elif i[0] == "append":
                self.comp_data = [i[1][0], i[1][1]]
                self.append()
            elif i[0] == "if":
                self.comp_data = [i[1][0], i[1][1], i[1][2]]
                self.if_statement()
            elif i[0] == "end":
                self.comp_data = [i[0]]
                self.end()
            elif i[0] == "def":
                self.comp_data = [i[1], i[2]]
                self.define()
            elif i[0] == "func":
                self.comp_data = [i[1], i[2]]
                self.function()
            elif i[0] == "change":
                self.comp_data = [i[1][0], i[1][1]]
                self.change()
            elif i[0] == "native":
                self.comp_data = i[1]
                self.native()
            elif i[0] == "run":
                self.comp_data = i[1]
                self.run()

        code = self.finalize()
        comp = config["CompileOnly"]

        comp_name = str(name).replace(".elpp", "") + ".cpp"
        # TODO: Put the following try/except blocks here:
        # TODO: FileNotFoundError, IOError, PermissionError, IsADirectoryError, EOFError
        with open(comp_name, "w") as f:
            f.write(code)

        compile_command = str(config["G++Path"] + " -o " + config["Name"] + " " + \
             comp_name + " " + config["Flags"])

        print(compile_command)  # Shows the command used.

        os.system(compile_command)

        if comp == True:
            pass
        else:
            comp_path = os.path.join(os.getcwd(), comp_name)
            os.remove(comp_path)

    def show(self):
        """
        def show():
            Translate the show command to C++ equivalent.
        """

        if self.func:
            if self.comp_data[0] not in self.func_var:
                to_show = '    cout << "' + self.comp_data[0] + '" << endl;\n'

            else:
                to_show = '    cout << ' + self.comp_data[0] + ' << endl;\n'

        else:
            if self.comp_data[0] not in self.vars:
                to_show = '    cout << "' + self.comp_data[0] + '" << endl;\n'

            else:
                to_show = '    cout << ' + self.comp_data[0] + ' << endl;\n'

        self.commands.append(to_show)

    def var(self):
        """
        def ver():
            Translate var command to C++ equivalent.
        """

        try:
            data = int(self.comp_data[1])
            type_of_data = "int"
        except ValueError:
            data = self.comp_data[1]
            type_of_data = "string"

        if type_of_data == "string":
            to_show = '    ' + type_of_data + ' ' + self.comp_data[0] + ' = "' + data + '";\n'
        else:
            to_show = '    ' + type_of_data + ' ' + self.comp_data[0] + ' = ' + str(data) + ';\n'

        self.commands.append(to_show)

    def add(self):
        """
        def add():
            Translate add command to C++ equivalent.
        """

        if self.comp_data[2] in self.vars:
            data_on_var = True
        else:
            data_on_var = False

        if self.comp_data[1] in self.vars:
            comp_data1 = self.comp_data[1]
        else:
            comp_data1 = self.comp_data[1]

        if self.comp_data[0] in self.vars:
            comp_data0 = self.comp_data[0]
        else:
            comp_data0 = self.comp_data[0]

        try:
            data0 = int(comp_data0)
            data1 = int(comp_data1)
        except ValueError:
            data0 = comp_data0
            data1 = comp_data1

        if data_on_var:
            to_show = '    ' + self.comp_data[2] + ' = ' + str(data0) + ' + ' + str(data1) + ';\n'
        else:
            to_show = '    auto ' + self.comp_data[2] + ' = ' + str(data0) + ' + ' + str(data1) + ';\n'

            try:
                self.vars[self.comp_data[2]] = data0 + data1
            except ValueError:
                self.vars[self.comp_data[2]] = str(data0) + str(data1)

        self.commands.append(to_show)

    def sub(self):
        """
        def sub():
            Translate sub command to C++ equivalent.
        """

        if self.comp_data[2] in self.vars:
            data_on_var = True
        else:
            data_on_var = False

        if self.comp_data[1] in self.vars:
            comp_data1 = self.vars[self.comp_data[1]]
        else:
            comp_data1 = self.comp_data[1]

        if self.comp_data[0] in self.vars:
            comp_data0 = self.vars[self.comp_data[0]]
        else:
            comp_data0 = self.comp_data[0]

        try:
            data0 = int(comp_data0)
            data1 = int(comp_data1)
            type_of_data = "int"

        except ValueError:
            data0 = comp_data0
            data1 = comp_data1
            type_of_data = "string"

        if type_of_data == "string":
            print("ERR: YOU CAN NOT SUBTRACT STRINGS!\n ERR ON {} AND {}".format(comp_data0, comp_data1))
            exit()

        if data_on_var:
            to_show = '    ' + self.comp_data[2] + ' = ' + str(data0) + ' - ' + str(data1) + ';\n'
        else:
            to_show = '    auto ' + self.comp_data[2] + ' = ' + str(data0) + ' - ' + str(data1) + ';\n'
            try:
                self.vars[self.comp_data[2]] = data0 - data1
            except ValueError:
                self.vars[self.comp_data[2]] = str(data0) + str(data1)

        self.commands.append(to_show)

    def mul(self):
        """
        def mul():
            Translate mul command to C++ equivalent.
        """

        if self.comp_data[2] in self.vars:
            data_on_var = True
        else:
            data_on_var = False

        if self.comp_data[1] in self.vars:
            comp_data1 = self.vars[self.comp_data[1]]
        else:
            comp_data1 = self.comp_data[1]

        if self.comp_data[0] in self.vars:
            comp_data0 = self.vars[self.comp_data[0]]
        else:
            comp_data0 = self.comp_data[0]

        try:
            data0 = int(comp_data0)
            data1 = int(comp_data1)
            type_of_data = "int"

        except ValueError:
            data0 = comp_data0
            data1 = comp_data1
            type_of_data = "string"

        try:
            type_int = True
            data1 = int(data1)
        except ValueError:
            type_int = False

        if type_int == False:
            print("ERR: YOU CAN NOT MULTIPLY STRINGS WITH STRING OR MULTIPLY!\n ERR ON {} AND {}".format(comp_data0, comp_data1))

        else:
            if type_of_data == "string":
                if type_int:
                    if data_on_var:
                        to_show = '    for(int i = 0; i > ' + str(data1) + ' ; i++){ ' + self.comp_data[2] + ' += "' + str(data0) + '"};\n'
                    else:
                        to_show = '    auto ' + self.comp_data[2] + ' =  "";' + \
                        '\n    for(int i = 0; i < ' + str(data1) + ' ; i++){ ' + self.comp_data[2] + ' += "' + str(data0) + '";}\n'
                        try:
                            self.vars[self.comp_data[2]] = data0 * data1
                        except ValueError:
                            self.vars[self.comp_data[2]] = str(data0) * str(data1)
            else:
                if data_on_var:
                    to_show = '    ' + self.comp_data[2] + ' = ' + str(data0) + ' * ' + str(data1) + ' ;\n'
                else:
                    to_show = '    auto ' + self.comp_data[2] + ' = ' + str(data0) + ' * ' + str(data1) + ' ;\n'
                    try:
                        self.vars[self.comp_data[2]] = data0 * data1
                    except ValueError:
                        self.vars[self.comp_data[2]] = str(data0) * str(data1)

            self.commands.append(to_show)

    def div(self):
        """
        def div():
            Translate div command to C++ equivalent.
        """

        if self.comp_data[2] in self.vars:
            data_on_var = True
        else:
            data_on_var = False

        if self.comp_data[1] in self.vars:
            comp_data1 = self.vars[self.comp_data[1]]
        else:
            comp_data1 = self.comp_data[1]

        if self.comp_data[0] in self.vars:
            comp_data0 = self.vars[self.comp_data[0]]
        else:
            comp_data0 = self.comp_data[0]

        try:
            data0 = int(comp_data0)
            data1 = int(comp_data1)
            type_of_data = "int"
        except ValueError:
            data0 = comp_data0
            data1 = comp_data1
            type_of_data = "string"

        if type_of_data == "string":
            print("ERR: YOU CAN NOT DIVIDE STRINGS!\n ERR ON {} AND {}".format(comp_data0, comp_data1))
            exit()

        if data_on_var:
            to_show = '    ' + self.comp_data[2] + ' = ' + str(data1) + ' / ' + str(data0) + ';\n'
        else:
            to_show = '    auto ' + self.comp_data[2] + ' = ' + str(data1) + ' / ' + str(data0) + ';\n'
            try:
                self.vars[self.comp_data[2]] = data0 / data1
            except ValueError:
                self.vars[self.comp_data[2]] = ""

        self.commands.append(to_show)

    def take(self):
        """
        def take():
            Translate take command to C++ equivalent.
        """

        if self.comp_data[0] in self.vars:
            to_show = '    cin >> ' + self.comp_data[1] + ' ;\n'
        else:
            if self.comp_data[0] == self.data_types[0]:
                to_show = '    ' + self.comp_data[0] + ' ' + self.comp_data[1] + ' ;\n    getline (cin, ' + self.comp_data[1] + ') ;\n'
                self.vars[self.comp_data[1]] = ""
            else:
                to_show = '    ' + self.comp_data[0] + ' ' + self.comp_data[1] + ' ;\n    cin >> ' + self.comp_data[1] + ';\n'
                self.vars[self.comp_data[1]] = ""

        print(self.vars)
        self.commands.append(to_show)

    def read(self):
        """
        def read():
            Translate read command to C++ equivalent.
        """

        self.read_finalize = True

        if self.comp_data[1] in self.vars:
            in_var = True
        else:
            in_var = False

        if in_var:
            to_show = '    ' + self.comp_data[1] + ' = read( ' + self.comp_data[0] + ' );'
        else:
            to_show = '    string ' + self.comp_data[1] + ' = read( "' + self.comp_data[0] + '" );'
            self.vars[self.comp_data[1]] = ""

        self.commands.append(to_show)

    def write(self):
        """
        def write():
            Translate write command to C++ equivalent.
        """

        self.write_finalize = True

        if self.comp_data[0] not in self.vars:
            print("ERR: YOU NEED A VARIABLE TO WRITE DATA ON FILE! ERR ON {}, {}".format(self.comp_data[0], self.comp_data[1]))
        else:
            to_show = '    write((char *)"' + self.comp_data[1] + '", (char *)"' + self.vars[self.comp_data[0]] + '");\n'

        self.commands.append(to_show)

    def append(self):
        """
        def append():
            Translate append command to C++ equivalent.
        """

        self.append_finalize = True

        if self.comp_data[0] not in self.vars:
            print("ERR: YOU NEED A VARIABLE TO APPEND DATA ON FILE! ERR ON {}, {}".format(self.comp_data[0], self.comp_data[1]))
        else:
            to_show = '    append((char *)"' + self.comp_data[1] + '", (char *)"' + self.vars[self.comp_data[0]] + '");\n'

        self.commands.append(to_show)

    def if_statement(self):
        """
        def if_statement():
            Translate an if statement to C++ equivalent.
        """

        if self.comp_data[0] not in self.vars:
            data1 = False
        else:
            data1 = True
        if self.comp_data[2] not in self.vars:
            data2 = False
        else:
            data2 = True

        try:
            self.comp_data[0] = int(self.comp_data[0])
            data1_int = True
        except ValueError:
            data1_int = False
            pass

        try:
            self.comp_data[2] = int(self.comp_data[2])
            data2_int = True
        except ValueError:
            data2_int = False
            pass

        if data1:
            if data2:
                to_show = '    if (' + str(self.comp_data[0]) + ' ' + self.comp_data[1] + ' ' + str(self.comp_data[2]) + "){\n"
            else:
                if data2_int:
                    to_show = '    if (' + str(self.comp_data[0]) + ' ' + self.comp_data[1] + ' ' + str(self.comp_data[2]) + "){\n"
                else:
                    to_show = '    if (' + str(self.comp_data[0]) + ' ' + self.comp_data[1] + ' "' + str(self.comp_data[2]) + '"){\n'
        else:
            if data2:
                if data1_int:
                    to_show = '    if (' + str(self.comp_data[0]) + ' ' + self.comp_data[1] + ' ' + str(self.comp_data[2]) + "){\n"
                else:
                    to_show = '    if ("' + str(self.comp_data[0]) + '" ' + self.comp_data[1] + ' ' + str(self.comp_data[2]) + "){\n"
            else:
                if data1_int:
                    if data2_int:
                        to_show = '    if (' + str(self.comp_data[0]) + ' ' + self.comp_data[1] + ' ' + str(self.comp_data[2]) + "){\n"
                    else:
                        to_show = '    if (' + str(self.comp_data[0]) + ' ' + self.comp_data[1] + ' "' + str(self.comp_data[2]) + '"){\n'
                else:
                    if data2_int:
                        to_show = '    if ("' + str(self.comp_data[0]) + '" ' + self.comp_data[1] + ' ' + str(self.comp_data[2]) + "){\n"
                    else:
                        to_show = '    if ("' + str(self.comp_data[0]) + '" ' + self.comp_data[1] + ' "' + str(self.comp_data[2]) + '"){\n'

        self.commands.append(to_show)

    def end(self):
        """
        def end():
            End block; Place curly brackets.
        """

        if self.func:
            self.commands.append('    };\n')
            self.func = False
        else:
            self.commands.append('    }\n')

    def define(self):
        """
        def define():
            Define a function.
        """

        self.func = True
        self.func_var = {}

        for i in self.comp_data[1]:
            self.func_var[i] = ""

        to_show = '    auto ' + self.comp_data[0][0] + ' = []('
        for i in self.comp_data[1]:
            to_show += ' string ' + i + ','

        to_show = to_show[:-1]
        to_show += '){\n'
        self.commands.append(to_show)

    def function(self):
        """
        def function():
            Define a function call.
        """

        to_show = '    ' + self.comp_data[0] + '('
        for i in self.comp_data[1]:
            to_show += ' ' + i + ','
        to_show = to_show[:-1]
        to_show += ');\n'
        self.commands.append(to_show)

    def change(self):
        """
        def change():
            Change value of a variable.
        """

        to_show = "    " + self.comp_data[0] + ' = ' + self.comp_data[1] + ';\n'

        self.commands.append(to_show)

    def native(self):
        """
        def native():
            TODO: Define this method.
        """

        self.commands.append('    ' + self.comp_data[0] + '\n')

    def run(self):
        """
        def run():
            Run a system command.
        """

        to_show = '    os.system("' + self.comp_data[0] + '");\n'
        self.commands.append(to_show)

    def finalize(self):
        """
        def finalize():
            Completes the output code.
        """

        first_parts = '#include <iostream>'

        if self.read_finalize == True or self.write_finalize == True or self.append_finalize == True:
            first_parts += "\n#include <fstream>\n#include <sstream>"

        namespace = "\nusing namespace std;\n"

        if self.read_finalize:
            namespace += """\nstring read(string filename){

    std::ifstream inFile;
    inFile.open(filename); //open the input file

    std::stringstream strStream;
    strStream << inFile.rdbuf(); //read the file
    std::string str = strStream.str(); //str holds the content of the file

    inFile.close();
    return str;

}"""
        if self.write_finalize:
            namespace += """\nint write(char filename[], char to_write[]){
    FILE *fptr;
    fptr = fopen(filename,"w");
    if(fptr == NULL)
    {
        printf("Error!");   
        exit(1);             
    }
    fprintf(fptr,"%s",to_write);
    fclose(fptr);
    return 0;
}"""
        
        if self.append_finalize:
            namespace += """\nint append(char filename[], char to_write[]){
    FILE *fptr;
    fptr = fopen(filename,"ab");
    if(fptr == NULL)
    {
        printf("Error!");
        exit(1);
    }
    fprintf(fptr,"%s",to_write);
    fclose(fptr);
    return 0;
}"""

        namespace += "\nint main(){\n\n"
        first_parts += namespace

        for i in self.commands:
            first_parts += str(i)
        first_parts += '\n    return 0;'
        first_parts += "\n}"
        return first_parts
