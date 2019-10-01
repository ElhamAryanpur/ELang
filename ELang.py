from core.languages import cpp
from core.misc import helper, EUtil, logger
import yaml
import os

if __name__ == "__main__":

    checkup = helper.Checkup(logger.Log(), EUtil)
    details = checkup.init()
    if details['config']['language'] == "c++": # Here details['config'] might give 
                                               # error in IDEs, but it works!
        ELangObject = cpp.ELang(details['config'])
        compileCode = ELangObject.compile()
        os.system(compileCode[0])