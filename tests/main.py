#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets

from ui.main_window import MainWindow

import json, logging, logging.config
with open("tests/data/conf/logger.json", 'r') as logging_configuration_file:
        logger_config = json.load(logging_configuration_file)
logging.config.dictConfig(logger_config)
logger = logging.getLogger(__name__)
logger.info('Logger configured...')

# display GUI
try:
    application = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    application.exec_()
except:
    logger.exception("Catched top level exception!")
