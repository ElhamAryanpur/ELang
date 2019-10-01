from core.languages import cpp
from core.misc import helper, EUtil, logger
import yaml
import os

if __name__ == "__main__":

    checkup = helper.Checkup(logger.Log(), EUtil)
    checkup.init()