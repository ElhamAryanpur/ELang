#!/bin/python3
#encoding:utf-8

"""
ELang.py -- A translator between humans and computers
Copyright(c) 2019, Elham Aryanpur

"""

"""
Error Codes:

0001 - Cannot import system modules
0002 - Cannot import core modules
0003 - Cannot import third-party modules
0004 - Cannot initialize configuration
0005 - An error occured while importing the compiler
0006 - Compiler not found
0007 - Force program to quit
0008 - 
0009 - 
0010 - Unknown error occured
"""

# Import system modules
try:
    import os
    import sys
    import time
    import importlib
    import traceback

except ImportError as e:
    print("[E] ERROR #0001: Cannot import system modules!")
    sys.exit(1)

else:
    # Set constants for the program.
    PROGRAM_NAME = "ELang"
    PROGRAM_TAGLINE = "A translator between humans and computers"
    PROGRAM_VERSION = "0.0.0.1"  # TODO: @Elham, please change this :)
    PROGRAM_TITLE = "{0} v{1} -- {2} ".format(PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_TAGLINE)
    PROGRAM_START = time.asctime()

# Import core modules
try:
    from core import simplelib
    from core import logger
    from core import printer

except ImportError:
    print("[E] ERROR #0002: Cannot import core modules!")
    traceback.print_exc()
    sys.exit(2)

else:
    SimpleLib = simplelib.SimpleLib  # Create a shortcut for SimpleLib class.

    # Create a logger instance.
    log = logger.LoggingObject(
        name="ELang",
        logfile="logfile.dat"
    )

    log.set_logging_level('NOTSET')
    log.info("{0} started on {1}".format(PROGRAM_NAME, PROGRAM_START))


# Import third-party modules
try:
    log.info("Importing third-party modules...")
    from yaml import load

except ImportError as e:
    print("[E] ERROR #0003: Cannot import third-party modules!")
    traceback.print_exc()
    log.error("Cannot import third-party modules")
    log.error(str(e))
    sys.exit(3)

# Import available compilers on core/compilers/*
try:
    log.info("Importing compilers...")
    # TODO: Import compilers here
    _compilers = os.listdir("core/compilers")  # List compilers available.
    global compilers  # Make compilers variable global
    compilers = {}
    for compiler in _compilers:
        try:
            if SimpleLib().isfile("core/compilers/{0}".format(compiler)) == True:
                log.info("Trying to import `{0}` compiler...".format(compiler))
                compiler_obj = importlib.import_module("core.compilers.{0}".format(compiler.partition(".py")[0]))

            else:
                log.info("Path is not file, continuing loop... ({0})".format(compiler))
                continue

        except Exception as e:
            log.error("An error occured while importing the compiler")
            log.error(str(e))
            printer.Printer().print_with_status("ERROR #0005: An error occured while importing the compiler:", 2)
            printer.Printer().print_with_status(str(e), 2)

        else:
            log.info("Adding {0}'s object to compilers list...".format(compiler_obj.COMPILER_NAME))
            compilers[compiler_obj.COMPILER_NAME] = compiler_obj

except Exception as e:
    # We need to use importlib to give more specific information
    # when the program failed to launch.
    log.critical("Cannot import compilers!")
    log.critical(str(e))
    printer.Printer().print_with_status("ERROR #0004: Cannot import compilers!", 2)
    printer.Printer().print_with_status(str(e), 2)
    SimpleLib().proper_exit(4)


class Main():
    """
    class Main():
        The main class of ELang.py program.

        parameters:
        str config_file :: The configuration file path.
        bool debug_mode :: This is set to `True` if debug mode is on.
    """

    def __init__(self, logger, config_file="config.yml", debug_mode=False):
        """
        def __init__():
            The initialization method for Main() class.
        """

        logger.info("__init__() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        global PROGRAM_NAME
        global PROGRAM_TITLE
        global PROGRAM_VERSION
        global compilers
        self.PROGRAM_NAME = PROGRAM_NAME
        self.PROGRAM_TITLE = PROGRAM_TITLE
        self.PROGRAM_VERSION = PROGRAM_VERSION
        self.compilers = compilers
        self.logger = logger  # Set the logger.
        self.config_file = config_file
        self.debug = debug_mode

    def generate_config(self, wizard_mode):
        """
        def generate_config():
            Generate configuration file and sample source code.
        """

        self.logger.info("generate_config() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        if wizard_mode == False:
            try:
                with open(os.path.join(os.getcwd(), "config.yml"), "w") as f:
                    data = """\
Name: compile
FileName: compile.elpp
G++Path: g++
Flags: ''
CompileOnly: false"""
                    self.logger.info("Writing to config.yml file...")
                    f.write(data)

                with open(os.path.join(os.getcwd(), "compile.elpp"), "w") as f:
                    self.logger.info("Writing to compile.elpp file...")
                    f.write("show Hello World!")

            except Exception as e:
                self.logger.error("Cannot initialize configuration.")
                self.logger.error(str(e))
                printer.Printer().print_with_status("ERROR #0004: Cannot initialize configuration!", 2)
                printer.Printer().print_with_status(str(e))
                SimpleLib().proper_exit(4)

        else:
            try:
                program_name = str(input("Enter your program's name: "))
                program_filename = str(input("Enter program's filename: "))
                print()
                for compiler in self.compilers:
                    printer.Printer().print_with_status(compiler, 1)

                compiler = str(input("Enter compiler to use (Case sensitive): "))
                try:
                    compiler = self.compilers[compiler]

                except KeyError:
                    printer.Printer().print_with_status("ERROR #0006: Compiler not found")

                else:
                    compiler_data = {}
                    for keywords in compiler.COMPILER_DATA:
                        compiler_data[keywords] = str(input("{0}: ".format(keywords)))

                while True:
                    compileonly = str(input("Compile only? (y/n): "))
                    if compileonly.lower() == 'y':
                        compileonly = 'true'  # Just making sure :p
                        break

                    elif compileonly.lower() == 'n':
                        compileonly = 'false'
                        break

                    else:
                        continue

                try:
                    with open(os.path.join(os.getcwd(), "config.yml"), "w") as f:
                        data = """\
Name: {0}
FileName: {1}
CompileOnly: {2}""".format(program_name, program_filename, compileonly)
                        self.logger.info("Adding compiler data to config.yml file...")
                        for keywords in compiler_data:
                            data += "\n{0}: {1}".format(keywords, compiler_data[keywords])

                        self.logger.info("Writing to config.yml file...")
                        f.write(data)

                    with open(os.path.join(os.getcwd(), "compile.elpp"), "w") as f:
                        self.logger.info("Writing to compile.elpp file...")
                        f.write("show Hello World!")

                except Exception as e:
                    self.logger.error("Cannot initialize configuration.")
                    self.logger.error(str(e))
                    printer.Printer().print_with_status("ERROR #0004: Cannot initialize configuration!", 2)
                    printer.Printer().print_with_status(str(e))
                    SimpleLib().proper_exit(4)

            except(KeyboardInterrupt, EOFError):
                printer.Printer().print_with_status("ERROR #0007: Forcing program to quit...")
                self.cleanup()

    def compile(self):
        """
        def compile():
            Compile the ELang file.
        """

        pass  # TODO


    def help(self, panel="main"):
        """
        def help():
            Return help list.
        """

        if panel == "main":
            data = """
{0}

USAGE:
    [1] {1} generate
    [2] (Edit compile.elpp and config.yml)
    [3] {1} compile

Commands:
    help                          ::        Show this help menu.
    generate                      ::        Generate config.yml and compile.elpp files. (see `help generate` for more info.)
    compile                       ::        Compile elpp files (see `help compile` for more info.)

Switches:
    -c --config=[FILEPATH]        ::        Set configuration file path manually.
    -d --debug                    ::        Enable debugging mode.
""".format(self.PROGRAM_TITLE, sys.argv[0])

        elif panel == "generate":
            data = """
{0}

USAGE:
    {1} generate  # This uses C++ by default.
    {1} generate --wizard

Switches:
    --wizard        ::        Enable wizard mode (step-by-step guide)
""".format(self.PROGRAM_TITLE, sys.argv[0])

        else:
            raise ValueError("Invalid panel name!")

        return data

    def cleanup(self):
        """
        def cleanup():
            Remove temporary files, data, variables, etc. before exiting.
        """

        # ! Put things here when needed!
        pass

    def main(self):
        """
        def main():
            The main method of Main() class.
        """

        self.logger.info("main() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        jobs = {
            # If a job will be executed, it will be true.
            "generate": False
        }

        i = 0
        arg = sys.argv[i]
        while i < len(sys.argv):
            if arg == sys.argv[0].lower():
                pass

            elif arg == "help":
                try:
                    if sys.argv[i+1] == "generate":
                        self.help("generate")

                    else:
                        self.help("main")

                except IndexError:
                    self.help()

            elif arg == "generate":
                try:
                    if sys.argv[i+1] == "--wizard":
                        wizard_mode = True

                    else:
                        wizard_mode = False

                except IndexError:
                    wizard_mode = False

                jobs["generate"] = True

            elif arg == "compile":
                try:
                    self.compile()

                except Exception:
                    pass

            elif arg in ("--debug", "-d"):
                self.logger.enable_logging()

            elif arg == "-c":
                # ? This will not detect filepaths with spaces. Any ideas?
                try:
                    self.config_file = sys.argv[arg+1]

                except IndexError:
                    printer.Printer().print_with_status("You must specify a filepath!", 2)
                    self.help()

            elif arg.startswith("--config="):
                # ? This will not detect filepaths with spaces. Any ideas?
                try:
                    self.config_file = arg.partition('=')[2]

                except IndexError:
                    printer.Printer().print_with_status("You must specify a filepath!", 2)

            else:
                pass

            i += 1

        if jobs["generate"] == True:
            self.generate_config(wizard_mode)


if __name__ == "__main__":
    Main(log).main()