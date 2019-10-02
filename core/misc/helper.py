'''
    COPYRIGHT 2019 Elham Aryanpur

    ELang version 0.2

    This is helping classes for main ELang compiler.
    For license, Please refer to LICENSE file in the master branch.
'''

# MAIN MODULES NEEDED
from platform import system
import yaml
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Checkup():
    '''
    This is a class for setting up the initialization of a simple project
    '''
    def __init__(self, logger, util):
        self.logger = logger
        self.EUtil = util

    def init(self):
        '''
        This will check up for required files and generate them if they were not present!
        '''

        self.EUtil.clearScreen()

        # set up path to config.yml
        PATH_TO_CONFIG = os.path.join(os.getcwd(), 'config.yml')
        PATH_TO_CODE = os.path.join(os.getcwd(), "compile.elpp")

        PATH_TO_WIN_GCC = os.path.join(os.getcwd(), "compilers")
        PATH_TO_WIN_GCC = os.path.join(PATH_TO_WIN_GCC, "cpp")
        PATH_TO_WIN_GCC = os.path.join(PATH_TO_WIN_GCC, "64")
        PATH_TO_WIN_GCC = os.path.join(PATH_TO_WIN_GCC, "bin")
        PATH_TO_WIN_GCC = os.path.join(PATH_TO_WIN_GCC, "g++")

        details = {"config": False, "code": False}

        # check for config.yml
        self.logger.logNormal("    Searching for config.yml\n")
        print(bcolors.HEADER + "    [[ SEARCHING FOR CONFIGURATION ]]    ")
        if os.path.isfile(PATH_TO_CONFIG):
            print("\n" + bcolors.OKGREEN + "FOUND CONFIGURATION AT {}".format(PATH_TO_CONFIG))

            # it exist!
            self.logger.logNormal('    config.yml FOUND!\n')

            # trying to load it
            try:
                print(bcolors.HEADER + "\n    [[ LOADING CONFIGURATION ]]    ")
                with open(PATH_TO_CONFIG, 'r') as f:
                    config = yaml.load(f.read())
                    print("\n" + bcolors.OKGREEN + "CONFIGURATION SUCCESSFULLY LOADED!")
                    self.logger.logNormal("    config.yml LOADED!\n")
                    details['config'] = config

            # If we can't load it...
            except Exception as e:
                error = "\nERROR: CAN'T READ CONFIGURATION AT {}! ERROR: {}".format(PATH_TO_CONFIG, e)
                print(bcolors.FAIL + error)
                self.logger.logError(
                    "    " + error,
                    PATH_TO_CONFIG
                )

        # If config.yml does not exist...
        else:
            self.logger.logNormal("COULD NOT FIND CONFIGURATION AT {}!\n".format(PATH_TO_CONFIG))
            print("\n" + bcolors.FAIL + "COULD NOT FIND CONFIGURATION AT {}".format(PATH_TO_CONFIG))
            print(bcolors.HEADER + "\n    [[ GENERATING A CONFIGURATION ]]    ")

            # Try to generate a config.yml...
            try:
                self.logger.logNormal('TRYING TO GENERATE CONFIGURATION FILE\n')
                if system() == "Windows":
                    with open(PATH_TO_CONFIG, 'w') as f:
                        f.write("Name: compile\nFileName: compile.elpp\nlanguage: c++\nG++Path: {}\nFlags: ''\nCompileOnly: false".format(PATH_TO_WIN_GCC))
                
                    config = {
                        "Name": "compile",
                        'FileName': 'compile.elpp',
                        'language': 'c++',
                        'G++Path': str(PATH_TO_WIN_GCC),
                        'Flags': '',
                        'CompileOnly': False
                    }
                
                elif system() == "Linux":
                    with open(PATH_TO_CONFIG, 'w') as f:
                        f.write("Name: compile\nFileName: compile.elpp\nlanguage: c++\nG++Path: g++\nFlags: ''\nCompileOnly: false")
                
                    config = {
                        "Name": "compile",
                        'FileName': 'compile.elpp',
                        'language': 'c++',
                        'G++Path': 'g++',
                        'Flags': '',
                        'CompileOnly': False
                    }

                print("\n" + bcolors.OKGREEN + "CONFIGURATION GENERATED!")
                self.logger.logNormal('LOADED GENERATED CONFIGURATION!')
                details['config'] = config

            # If can't generate...
            except Exception as e:
                error = "\nERROR: COULD NOT GENERATE CONFIGURATION AT {}! ERROR: {}".format(PATH_TO_CONFIG, e)
                print(bcolors.FAIL + error)
                self.logger.logError(
                    "    " + error,
                    PATH_TO_CONFIG
                )
        
        # Now it is time for main code 
        self.logger.logNormal("SEARCHING FOR COMPILE.ELPP\n")
        print(bcolors.HEADER + "\n    [[ SEARCHING FOR COMPILE CODE ]]    ")
        if os.path.isfile(PATH_TO_CODE):
            self.logger.logNormal("COMPILE.ELPP HAS BEEN FOUND!\n")
            print(bcolors.OKGREEN + "\nMAIN CODE HAS BEEN FOUND!")
            details['code'] = True

        # If it is not found...
        else:
            self.logger.logError("COULD NOT FIND COMPILE.ELPP!\n", PATH_TO_CODE)
            print(bcolors.FAIL + "\nMAIN CODE HAS NOT BEEN FOUND!")
            print(bcolors.HEADER + "\n    [[ GENERATING A MAIN CODE ]]    ")

            # Trying to generate a compile.elpp file
            self.logger.logNormal("TRYING TO GENERATE CODE FILE\n")
            try:
                with open(PATH_TO_CODE, "w") as f:
                    f.write("show Hello World!")
                self.logger.logNormal("SUCCESSFULLY GENERATED CODE FILE!\n")
                print(bcolors.OKGREEN + "\nMAIN CODE HAS BEEN GENERATED AT {}!".format(PATH_TO_CODE))
                details['code'] = True

            except Exception as e:
                error = "\nERROR: COULD NOT GENERATE CODE AT {}! ERROR: {}".format(PATH_TO_CONFIG, e)
                print(bcolors.FAIL + error)
                self.logger.logError(
                    "    " + error,
                    PATH_TO_CONFIG
                )
        
        return details
    
    def command(self, command):
        '''
        Run console commands and check the results if successful or failed!
        '''
        if os.system(command) == 0:
            print(bcolors.OKBLUE + "\nSUCCESSFUL!")
            self.logger.logNormal("COMMAND '{}' HAS BEEN RUN SUCCESSFULLY!\n".format(command))
        else:
            print(bcolors.FAIL + "\nFAILED!")
            self.logger.logError("COMMAND '{}' HAS BEEN RUN UNSUCCESSFULLY!\n".format(command), "COULD NOT COMPILE!")