#!/usr/bin/env python3
#
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 29-06-2017 11:47
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Pipeline Runner - Main Application
"""

import sys
import nose
import argparse
import unittest
# Modules from package
import config_manager

__DEFAULT_CONFIG_FILE = "config_default.json"

# Running mode
__run_test_mode = False
__logger = None


def get_cmdl():
    cmdl_version = '2017.06.29'
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--config_file",
                        help='Application configuration file')
    parser.add_argument('-v', '--version',
                        help='display version information',
                        action='version',
                        version=cmdl_version + ' %(prog)s ')
    parser.add_argument('pipeline_name',
                        help='Module Name that contains the director of the pipeline to run')
    args = parser.parse_args()
    return args


def app_bootstrap():
    global __run_test_mode
    global __logger
    args = get_cmdl()
    if args.config_file:
        config_manager.set_application_config_file(args.config_file)
    else:
        config_manager.set_application_config_file(__DEFAULT_CONFIG_FILE)
    if args.pipeline_name:
        config_manager.set_pipeline_name(args.pipeline_name)
        if args.pipeline_name == 'test':
            __run_test_mode = True
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)
    if __run_test_mode:
        __logger.info(
            "Session '{}' STARTED, RUNNING UNIT TESTS".format(config_manager.get_app_config_manager().get_session_id()))
    else:
        __logger.info(
            "Session '{}' STARTED, pipeline '{}'".format(config_manager.get_app_config_manager().get_session_id(),
                                                         args.pipeline_name))


def run_unit_tests():
    __logger.debug("Running Unit Tests")
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('.')
    nose.run(suite=test_suite)


def main():
    app_bootstrap()
    if __run_test_mode:
        run_unit_tests()
    else:
        pass


if __name__ == "__main__":
    main()
