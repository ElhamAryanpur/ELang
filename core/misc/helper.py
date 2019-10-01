'''
    COPYRIGHT 2019 Elham Aryanpur

    This is helping classes for main ELang compiler.
    For license, Please refer to LICENSE file in the master branch.

    There will be comments before every main action!
'''

# MAIN MODULES NEEDED
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
        This will check up for required files and make them if they were not present!
        '''

        self.EUtil.clearScreen()

        # set up path to config.yml
        PATH_TO_CONFIG = os.path.join(os.getcwd(), 'config.yml')

        # check for config.yml
        self.logger.logNormal("    Searching for config.yml\n")
        if os.path.isfile(PATH_TO_CONFIG):
            print("\n " + bcolors.OKGREEN + "FOUND CONFIGURATION AT {}".format(PATH_TO_CONFIG))

            # it exist!
            self.logger.logNormal('    config.yml FOUND!\n')

            # trying to load it
            try:
                with open(PATH_TO_CONFIG, 'r') as f:
                    config = yaml.load(f.read())
                    print("\nCONFIGURATION SUCCESSFULLY LOADED!")
                    self.logger.logNormal("    config.yml LOADED!\n")
                    return config

            # If we can't load it...
            except Exception as e:
                error = "ERR: CAN'T READ CONFIGURATION AT {}! ERROR: {}".format(PATH_TO_CONFIG, e)
                print(error)
                self.logger.logError(
                    "    " + error,
                    PATH_TO_CONFIG
                )
                return False

        # If config.yml does not exist...
        else:
            print("COULD NOT FIND CONFIGURATION AT {}".format(PATH_TO_CONFIG))

    def initialization(self, path):
        if os.path.isfile("config.yml"):
            with open(os.path.join(os.getcwd(), "config.yml"), "r") as c:
                config = c.read()
            try:
                config = yaml.load(config)
                #E = cpp.ELang(config)
            except Exception:
                print("ERR: CAN NOT READ CONFIG...")
                exit()
        else:
            try:
                with open(os.path.join(os.getcwd(), "config.yml"), "w") as f:
                    f.write("Name: compile\nFileName: compile.elpp\nlanguage: c++\nG++Path: g++\nFlags: ''\nCompileOnly: false")

                with open(os.path.join(os.getcwd(), "compile.elpp"), "w") as f:
                    f.write("show Hello World!")

            except Exception:
                print("ERR: CAN NOT INITIALIZE CONFIGURATION...")
                exit()