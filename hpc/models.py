# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 11-09-2017 11:14
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Models representing different HPC environments
"""

import os
import abc
# Application imports
import config_manager
from .exceptions import HpcServiceFactoryException, HpcServiceException


class HpcServiceFactory:
    # Constants
    _HPC_TYPE_LSF = 'lsf'
    _HPC_TYPE_NONE = 'no_hpc_environment_present'

    @staticmethod
    def get_hpc_service():
        if HpcServiceFactory.get_hpc_environment_type() == HpcServiceFactory._HPC_TYPE_LSF:
            return HpcServiceLsf()
        raise HpcServiceFactoryException("NO HPC Environment present")

    @staticmethod
    def get_hpc_environment_type():
        # More HPC environments will be added in the future
        if os.environ.get('LSB_JOBID'):
            return HpcServiceFactory._HPC_TYPE_LSF
        return HpcServiceFactory._HPC_TYPE_NONE


class HpcService(metaclass=abc.ABCMeta):
    pass


class HpcServiceLsf:
    # Constants
    _ENVIRONMENT_VAR_JOB_ID = 'LSB_JOBID'

    def __init__(self):
        self._logger = config_manager \
            .get_app_config_manager() \
            .get_logger_for("{}.{}".format(__name__, type(self).__name__))

    def get_current_job_id(self):
        if os.environ.get(HpcServiceLsf._ENVIRONMENT_VAR_JOB_ID):
            return os.environ.get(HpcServiceLsf._ENVIRONMENT_VAR_JOB_ID)
        raise HpcServiceException("Could not retrieve LSF Job ID from environment variable '{}'"
                                  .format(HpcServiceLsf._ENVIRONMENT_VAR_JOB_ID))