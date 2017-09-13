# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 12-09-2017 16:10
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This file contains different models for the execution of subprocesses / external processes, e.g. via the command line
"""

import abc
import threading
import subprocess
# App imports
import config_manager
from .exceptions import ParallelRunnerException


# Execution of commands
class CommandLineRunnerFactory:
    @staticmethod
    def get_command_line_runner():
        # TODO - This Factory is creating only local runners in the first iteration
        return CommandLineRunnerAsThread()


class ParallelManager:
    pass


class ParallelRunner(metaclass=abc.ABCMeta, threading.Thread):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))
        self._stdout = b' '
        self._stderr = b' '
        self._done = False
        self._shutdown = False

    @abc.abstractmethod
    def _run(self):
        ...

    def run(self):
        self._logger.debug("--- START ---")
        try:
            self._run()
        finally:
            self._done = True

    def cancel(self):
        self._logger.debug("--- CANCEL ---")
        self._shutdown = True
        self._stop()

    def wait(self):
        self._logger.debug("--- WAIT ---")
        self.join()

    def get_stdout(self):
        # Never give it back until the runner is done with whatever it is doing
        if not self._done:
            raise ParallelRunnerException("Runner is NOT DONE doing its job, thus 'stdout' is NOT AVAILABLE")
        return self._stdout

    def get_stderr(self):
        # Never give it back until the runner is done with whatever it is doing
        if not self._done:
            raise ParallelRunnerException("Runner is NOT DONE doing its job, thus 'stderr' is NOT AVAILABLE")
        return self._stderr


class CommandLineRunner(ParallelRunner):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))
        self.command = None
        self.timeout = None
        self.current_working_directory = None


class CommandLineRunnerAsThread(CommandLineRunner):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))

    def _run(self):
        self._logger.debug("Preparing for running command '{}', "
                           "current working directory at '{}', "
                           "timeout '{}s'".format(self.command,
                                                  self.current_working_directory,
                                                  self.timeout))
        command_subprocess = subprocess.Popen(self.command,
                                              cwd=self.current_working_directory,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              shell=True)
        self._logger.debug("Communicating with subprocess for command '{}', "
                           "current working directory at '{}', "
                           "timeout '{}s'".format(self.command,
                                                  self.current_working_directory,
                                                  self.timeout))
        try:
            self._stdout, self._stderr = command_subprocess.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired as e:
            command_subprocess.kill()

class CommandLineRunnerOnHpc(CommandLineRunner):
    def __init__(self):
        super().__init__()
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}-{}".format(__name__, type(self).__name__, threading.current_thread().getName()))

    def _run(self):
        pass
