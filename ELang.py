#!/bin/python3
# encoding:utf-8

"""
ELang.py -- A translator between humans and computers
Copyright(c) 2019, Elham Aryanpur

"""

"""
Error Codes:

0000 - No error happened. Yay!
0001 - Cannot import system modules
0002 - Cannot import core modules
0003 - Cannot import third-party modules
0004 - Cannot initialize configuration
0005 - An error occured while importing the compiler
0006 - Compiler not found
0007 - Force program to quit
0008 - No value error (e.g.: When -c or --config switch
       has no value next to them)
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
    print(e)
    sys.exit(1)

else:
    # Set constants for the program.
    PROGRAM_NAME = "ELang"
    PROGRAM_TAGLINE = "A translator between humans and computers"
    PROGRAM_VERSION = "0.0.0.2"  # TODO: @Elham, please change this :)
    PROGRAM_TITLE = "{0} v{1} -- {2} ".format(
        PROGRAM_NAME, PROGRAM_VERSION, PROGRAM_TAGLINE)
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
    # ? Why does flake8 tells us the yaml.load is imported but unused?
    from yaml import load

except ImportError as e:
    print("[E] ERROR #0003: Cannot import third-party modules!")
    traceback.print_exc()
    log.error("Cannot import third-party modules")
    log.error(str(e))
    log.info("SystemExit with error code 3.")
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
    log.info("ProperExit with error code 4.")
    SimpleLib().proper_exit(4)


class Main():
    """
    class Main():
        The main class of ELang.py program.

        parameters:
        obj logger      :: The logger to use.
        str config_file :: The configuration file path.
        bool debug_mode :: This is set to `True` if debug mode is on.
    """

    def __init__(self, logger, config_file="config.yml", debug_mode=False):
        """
        def __init__():
            The initialization method for Main() class.
        """

        logger.info("__init__() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        logger.info("Setting global variables.")
        global PROGRAM_NAME
        global PROGRAM_TITLE
        global PROGRAM_VERSION
        global compilers
        logger.info("Putting variables to self.")
        self.PROGRAM_NAME = PROGRAM_NAME
        self.PROGRAM_TITLE = PROGRAM_TITLE
        self.PROGRAM_VERSION = PROGRAM_VERSION
        self.compilers = compilers
        self.logger = logger  # Set the logger.
        self.config_file = config_file
        self.debug = debug_mode

    def generate_config(self, wizard_mode, config_file=None, elpp_filename="compile.elpp"):
        """
        def generate_config():
            Generate configuration file and sample source code.
        """

        self.logger.info("generate_config() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        if config_file is None:
            config_file = self.config_file

        self.logger.info("Checking if wizard_mode is False...")
        if wizard_mode == False:
            self.logger.info("wizard_mode is false.")
            try:
                self.logger.info("Writing to configuration file ({0})...".format(config_file))
                if SimpleLib().path_exists(config_file):
                    self.logger.warning("Config file ({0}) already exists, asking user what to do...")
                    printer.Printer().print_with_status(
                        "Configuration file already exists! ({0})".format(
                            config_file), 1)
                    while True:
                        try:
                            confirmation = str(input("Do you want to overwrite the existing file? (y/n): "))
                            if confirmation.lower() == 'y':
                                self.logger.info("User said yes.")
                                break

                            elif confirmation.lower() == 'n':
                                self.logger.info("User said no.")
                                return 0

                            else:
                                self.logger.info("User entered an unknown value, going back to start of loop.")
                                continue

                        except(ValueError, TypeError, KeyboardInterrupt, EOFError) as e:
                            self.logger.error("{0}; Going back to start of loop.".format(str(e)))
                            continue

                with open(os.path.join(os.getcwd(), config_file), "w") as f:
                    self.logger.info("Writing data...")
                    data = """\
Name: compile
FileName: {0}
G++Path: g++
Flags: ''
CompileOnly: false""".format(elpp_filename)
                    self.logger.info("Writing to config file...")
                    f.write(data)

                if SimpleLib().path_exists(elpp_filename):
                    self.logger.warning("ELPP file ({0}) already exists, asking user what to do...")
                    printer.Printer().print_with_status(
                        "ELPP file already exists! ({0})".format(
                            elpp_filename), 1)
                    while True:
                        try:
                            confirmation = str(input("Do you want to overwrite the existing file? (y/n): "))
                            if confirmation.lower() == 'y':
                                self.logger.info("User said yes.")
                                break

                            elif confirmation.lower() == 'n':
                                self.logger.info("User said no.")
                                return 0

                            else:
                                self.logger.info("User entered an unknown value, going back to start of loop.")
                                continue

                        except(ValueError, TypeError, KeyboardInterrupt, EOFError) as e:
                            self.logger.error("{0}; Going back to start of loop.".format(str(e)))
                            continue

                with open(os.path.join(os.getcwd(), elpp_filename), "w") as f:
                    self.logger.info("Writing to elpp file ({0})...".format(elpp_filename))
                    f.write("show Hello World!")
                    return 0

            except Exception as e:
                self.logger.error("Cannot initialize configuration.")
                self.logger.error(str(e))
                printer.Printer().print_with_status("ERROR #0004: Cannot initialize configuration!", 2)
                printer.Printer().print_with_status(str(e))
                return 4
                # self.logger.info("ProperExit with error code 4")
                # SimpleLib().proper_exit(4)

        else:
            self.logger.info("wizard_mode is true.")
            try:
                self.logger.info("Asking for program name.")
                program_name = str(input("Enter your program's name: "))
                self.logger.info("Program name is `{0}`".format(program_name))
                self.logger.info("Asking for program filename.")
                program_filename = str(input("Enter program's filename: "))
                if program_filename.endswith(".elpp") == False:
                    program_filename = "{0}.elpp".format(program_filename)

                self.logger.info("Programm filename is `{0}`".format(program_filename))
                print()
                self.logger.info("Showing a list of available compilers...")
                for compiler in self.compilers:
                    printer.Printer().print_with_status(compiler, 1)

                while True:
                    self.logger.info("Asking user what compiler we will use.")
                    compiler = str(input("Enter compiler to use (Case sensitive): "))
                    self.logger.info("User entered `{0}`".format(compiler))
                    try:
                        self.logger.info("Trying to get compiler object from dictionary...")
                        compiler = self.compilers[compiler]

                    except KeyError:
                        self.logger.error("Failed to get compiler object from dictionary, ERROR #0006.")
                        printer.Printer().print_with_status("ERROR #0006: Compiler not found")
                        continue

                    else:
                        self.logger.info("Successfully got the compiler object.")
                        compiler_data = {}
                        self.logger.info("Asking user for compiler-specific information.")
                        for keywords in compiler.COMPILER_DATA:
                            self.logger.info("Asking for `{0}` value.".format(keywords))
                            compiler_data[keywords] = str(input("{0}: ".format(keywords)))
                            self.logger.info("{0}: {1}".format(keywords, compiler_data[keywords]))

                        self.logger.info("Breaking loop...")
                        break

                while True:
                    try:
                        self.logger.info("Asking user for the value of compileonly variable...")
                        compileonly = str(input("Compile only? (y/n): "))
                        self.logger.debug("User entered `{0}`".format(compileonly))
                        if compileonly.lower() == 'y':
                            self.logger.info("compileonly is set to true.")
                            compileonly = 'true'  # Just making sure :p
                            break

                        elif compileonly.lower() == 'n':
                            self.logger.info("compileonly is set to false.")
                            compileonly = 'false'
                            break

                        else:
                            self.logger.info("Unknown input, going back to start of loop...")
                            continue

                    except(KeyboardInterrupt, EOFError):
                        self.logger.warning("ERROR #0007: Forcing program to quit...")
                        printer.Printer().print_with_status("ERROR #0007: Forcing program to quit...", 1)
                        return 7

                try:
                    self.logger.info("Writing to `{0}`...".format(config_file))

                    if SimpleLib().path_exists(config_file):
                        self.logger.warning("Config file ({0}) already exists, asking user what to do...")
                        printer.Printer().print_with_status(
                            "Configuration file already exists! ({0})".format(
                                config_file), 1)
                        while True:
                            try:
                                confirmation = str(input("Do you want to overwrite the existing file? (y/n): "))
                                if confirmation.lower() == 'y':
                                    self.logger.info("User said yes.")
                                    break

                                elif confirmation.lower() == 'n':
                                    self.logger.info("User said no.")
                                    return 0

                                else:
                                    self.logger.info("User entered an unknown value, going back to start of loop.")
                                    continue

                            except(ValueError, TypeError, KeyboardInterrupt, EOFError) as e:
                                self.logger.error("{0}; Going back to start of loop.".format(str(e)))
                                continue

                    with open(os.path.join(os.getcwd(), config_file), "w") as f:
                        data = """\
Name: {0}
FileName: {1}
CompileOnly: {2}""".format(program_name, program_filename, compileonly)
                        self.logger.info("Adding compiler data to {0} file...".format(config_file))
                        for keywords in compiler_data:
                            data += "\n{0}: {1}".format(keywords, compiler_data[keywords])

                        self.logger.info("Writing to config.yml file...")
                        f.write(data)

                    if SimpleLib().path_exists(elpp_filename):
                        self.logger.warning("ELPP file ({0}) already exists, asking user what to do...")
                        printer.Printer().print_with_status(
                            "ELPP file already exists! ({0})".format(
                                elpp_filename), 1)
                        while True:
                            try:
                                confirmation = str(input("Do you want to overwrite the existing file? (y/n): "))
                                if confirmation.lower() == 'y':
                                    self.logger.info("User said yes.")
                                    break

                                elif confirmation.lower() == 'n':
                                    self.logger.info("User said no.")
                                    return 0

                                else:
                                    self.logger.info("User entered an unknown value, going back to start of loop.")
                                    continue

                            except(ValueError, TypeError, KeyboardInterrupt, EOFError) as e:
                                self.logger.error("{0}; Going back to start of loop.".format(str(e)))
                                continue

                    with open(os.path.join(os.getcwd(), elpp_filename), "w") as f:
                        self.logger.info("Writing to {0} file...".format(elpp_filename))
                        f.write("show Hello World!")
                        return 0

                except Exception as e:
                    self.logger.error("Cannot initialize configuration.")
                    self.logger.error(str(e))
                    printer.Printer().print_with_status("ERROR #0004: Cannot initialize configuration!", 2)
                    printer.Printer().print_with_status(str(e))
                    self.logger.info("ProperExit with error code 4")
                    SimpleLib().proper_exit(4)

            except(KeyboardInterrupt, EOFError):
                self.logger.warning("Forcing program to quit (ERR0007)")
                printer.Printer().print_with_status("ERROR #0007: Forcing program to quit...")
                self.cleanup()
                self.logger.info("ProperExit with error code 7.")
                SimpleLib.proper_exit(7)

    def compile(self):
        """
        def compile():
            Compile the ELang file.
        """

        self.logger.info("main() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))
        # TODO


    def help(self, panel="main"):
        """
        def help():
            Return help list.
        """

        self.logger.info("help() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        self.logger.info("Checking what panel to return...")
        self.logger.info("Caller is looking for `{0}` panel.".format(panel))
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

Copyright(c) 2019 -- https://github.com/ElhamAryanpur/ELang
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

        self.logger.info("cleanup() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        # ! Put things here when needed!

    def main(self):
        """
        def main():
            The main method of Main() class.
        """

        self.logger.info("main() method called by {0}().".format(sys._getframe().f_back.f_code.co_name))

        self.logger.info("Setting up jobs list...")
        jobs = {
            # If a job will be executed, it will be true.
            "generate": False,
            "compile": False
        }

        i = 0  # i is the most commonly used variable on while and for loops.
               # Just telling a story...

        # General switches
        # Other definition:
        # The commands and switches defined here are the
        # ones that doesn't need the next or previous argument.
        # (example, `generate --wizard`. generate needs the --wizard switch
        # to work properly, but it relies in the i variable)
        self.logger.info("Checking for general switches...")
        if "--debug" in sys.argv or "-d" in sys.argv:
            self.logger.info("Debug mode is now ON.")
            self.logger.enable_logging()

        # Commands and switches that needs arguments.
        self.logger.info("Entering command parsing while loop...")
        while i < len(sys.argv):
            self.logger.debug("i value is {0}".format(str(i)))
            arg = sys.argv[i]
            self.logger.debug("Current argument to parse is `{0}`.".format(str(arg)))
            if arg == sys.argv[0]:
                self.logger.info("arg is the filename. Continuing to next argument.")
                pass

            elif arg == "help":
                self.logger.info("arg is `help`. Parsing for more info.")
                try:
                    if sys.argv[i+1] == "generate":
                        self.logger.info("The user is looking for `generate` command's help panel.")
                        print(self.help("generate"))
                        self.logger.info("We saved one user's life!")
                        return 0

                    else:
                        self.logger.info("Looks like the next argument is not for the help command. Showing main panel insteads.")
                        print(self.help("main"))
                        self.logger.info("We saved one user's life!")
                        return 0

                except IndexError:
                    self.logger.info("No more arguments next to it! Showing main panel.")
                    print(self.help())
                    return 0

            elif arg == "generate":
                self.logger.info("User wants to generate a new config and elpp file.")
                try:
                    if sys.argv[i+1] == "--wizard":
                        self.logger.info("User wants to enable wizard mode for generate command.")
                        wizard_mode = True
                        i += 1  # Skip the argument that is already used.

                    else:
                        self.logger.info("The next argument is not a --wizard switch.")
                        wizard_mode = False

                except IndexError:
                    self.logger.info("No more arguments next to the current argument!")
                    wizard_mode = False

                self.logger.info("Setting jobs[\"generate\"] to True.")
                jobs["generate"] = True

            elif arg == "compile":
                self.logger.info("Setting jobs[\"compile\"] to True.")
                jobs["compile"] = True

            elif arg == "-c":
                self.logger.info("`-c` switch detected.")
                # ? This will not detect filepaths with spaces. Any ideas?
                try:
                    self.logger.info("Setting self.config_file to next argument...")
                    self.config_file = sys.argv[i+1]
                    i += 1

                except IndexError:
                    self.logger.info("No value error (E0008) on -c switch.")
                    printer.Printer().print_with_status("ERROR #0008: You must specify a filepath!", 2)
                    print(self.help())
                    return 8

            elif arg.startswith("--config="):
                self.logger.info("--config switch detected.")
                # ? This will not detect filepaths with spaces. Any ideas?
                try:
                    self.logger.info("Setting self.config_file to value after the `=` sign.")
                    self.config_file = arg.partition('=')[2]

                except IndexError:
                    self.logger.info("No value error (E0008) on --config switch.")
                    printer.Printer().print_with_status("You must specify a filepath!", 2)
                    print(self.help())
                    return 8

            else:
                self.logger.info("Unknown command, printing main help panel.")
                print(self.help("main"))
                return 0

            self.logger.info("Iterating i... (i+1; {0}+1)".format(i))
            i += 1

        self.logger.info("We got out of the loop.")

        # Do the jobs
        if jobs["generate"] == True:
            return self.generate_config(wizard_mode)

        if jobs["compile"] == True:
            return self.compile()

        if len(sys.argv) == 1:
            self.logger.info("There are no other arguments! Showing help menu.")
            print(self.help())
            return 0

        self.logger.critical("ERROR #0009: Hey devs! Why does the program go here?")
        return 9


if __name__ == "__main__":
    # * Run the main method and properly exit.
    error_code = Main(log).main()
    log.info("ProperExit with error code {0}".format(str(error_code)))
    SimpleLib.proper_exit(error_code)