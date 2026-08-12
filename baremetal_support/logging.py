# Copyright (C) 2021 SUSE LLC
# SPDX-License-Identifier: GPL-3.0

import logging
import sys


class Logging:
    def __init__(self, name, level):
        self.logger = logging.getLogger(name)
        self.set_level(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
        )

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def set_level(self, level):
        self.debug("Setting loglevel to " + level)
        if level.upper == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif level.upper == "INFO":
            self.logger.setLevel(logging.INFO)
        elif level.upper == "WARN":
            self.logger.setLevel(logging.WARNING)
        elif level.upper == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif level.upper == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.NOTSET)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
