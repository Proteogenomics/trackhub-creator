# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 30-10-2017 09:33
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This pipeline publishes the given trackhub to trackhubregistry.org

A JSON formatted file is given as a parameter to the pipeline
    trackhub_description=input_file.json
And this file contains the following information:
{
    "trackhubUrl": "Name for the trackhub being published",
    "public": "1",
    "type": "PROTEOMICS",
    "pipelineReportFilePath": "pipeline.report"
}

Description of parameters:
    pipelineReportFilePath  ->  Absolute path to a JSON formatted file that contains information about the pipeline
                                execution
"""

import os
import json
# Application imports
import config_manager
from pipelines.template_pipeline import Director, DirectorConfigurationManager

# Globals
__configuration_file = None
__pipeline_arguments = None
__pipeline_director = None


# TODO Pipeline Singleton Accessors

# Pipeline Configuration Manager
class ConfigManager(DirectorConfigurationManager):
    # Command Line Arguments for this pipeline look like
    #   # This is a JSON formatted file that contains all the relevant information needed for publishing the trackhub
    #   trackhub_description=input_file.json

    # Command Line Argument keys
    _CONFIG_COMMAND_LINE_ARGUMENT_KEY_TRACKHUB_DESCRIPTOR_FILE = 'trackhub_description'

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super().__init__(configuration_object, configuration_file, pipeline_arguments)
        # Lazy Process command line arguments
        self.__pipeline_arguments_object = None
        self.__running_mode = None

    def _get_allowed_configuration_keys(self):
        return {self._CONFIG_COMMAND_LINE_ARGUMENT_KEY_TRACKHUB_DESCRIPTOR_FILE}

    def get_trackhub_descriptor_file_path(self):
        return self._get_value_for_pipeline_argument_key(
            self._CONFIG_COMMAND_LINE_ARGUMENT_KEY_TRACKHUB_DESCRIPTOR_FILE)

    def get_file_path_pipeline_report(self):
        return os.path.join(config_manager.get_app_config_manager().get_session_working_dir(),
                            "pipeline-publish_trackhub.report")


class PipelineData:
    """
    This class models the data used by the pipeline, and given as input of it in the command line parameter
    """
    # Keys
    _PIPELINE_DATA_KEY_TRACKHUB_URL = 'trackhubUrl'
    _PIPELINE_DATA_KEY_TRACKHUB_PUBLIC = 'public'
    _PIPELINE_DATA_KEY_TRACKHUB_TYPE = 'type'
    _PIPELINE_DATA_KEY_PIPELINE_REPORT_FILE_PATH = 'pipelineReportFilePath'

    def __init__(self, pipeline_data_file_path):
        self.__pipeline_data_file_path = pipeline_data_file_path
        self.__pipeline_data_object = None

    def _get_pipeline_data_object(self):
        if not self.__pipeline_data_object:
            self.__pipeline_data_object = json.load(self.__pipeline_data_file_path)
        return self.__pipeline_data_object


# Pipeline Director
class TrackhubPublisher(Director):
    pass
