# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 07-09-2017 11:24
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This pipeline creates a trackhub for a PRIDE project, based on the information provided via a JSON formatted file, as it
can be seen on this sample:
{
  "trackHubName" : "PXD000625",
  "trackHubShortLabel" : "<a href=\"http://www.ebi.ac.uk/pride/archive/projects/PXD000625\">PXD000625</a> - Hepatoc...",
  "trackHubLongLabel" : "Experimental design For the label-free ...",
  "trackHubType" : "PROTEOMICS",
  "trackHubEmail" : "pride-support@ebi.ac.uk",
  "trackHubInternalAbsolutePath" : "/nfs/pride/prod/archive/2014/05/PXD000625/internal/trackHub",
  "trackMaps" : [ {
    "trackName" : "PXD000625_10090_Original",
    "trackShortLabel" : "<a href=\"http://www.ebi.ac.uk/pride/archive/projects/PXD000625\">PXD000625</a> - Mus musc...",
    "trackLongLabel" : "Experimental design For the label-free proteome analysis 17 mice were used composed of 5 ...",
    "trackSpecie" : "10090",
    "pogoFile" : "/nfs/pride/prod/archive/2014/05/PXD000625/internal/PXD000625-10090.pogo"
  } ]
}
"""

import time
# App imports
import config_manager
import toolbox.general as general_toolbox
from pipelines.template_pipeline import Director, DirectorConfigurationManager

# Globals
__configuration_file = None
__pipeline_arguments = None
__pipeline_director = None


# Pipeline properties access
def set_configuration_file(config_file):
    global __configuration_file
    if __configuration_file is None:
        __configuration_file = config_file
    return __configuration_file


def set_pipeline_arguments(pipeline_arguments):
    global __pipeline_arguments
    if __pipeline_arguments is None:
        __pipeline_arguments = pipeline_arguments
    return __pipeline_arguments


def get_pipeline_director():
    global __pipeline_director
    if __pipeline_director is None:
        __pipeline_director = TrackhubCreatorForProject(config_manager.read_config_from_file(__configuration_file),
                                                        __configuration_file,
                                                        __pipeline_arguments)
    return __pipeline_director


class ConfigManager(DirectorConfigurationManager):
    # Command Line Arguments for this pipeline look like
    #   # This is a JSON formatted file that contains all the relevant information needed for processing the project
    #   # data and create its trackhub
    #   project_data_file=project_data.json

    # Command Line Argument keys
    _CONFIG_COMMAND_LINE_ARGUMENT_KEY_PROJECT_DATA_FILE = 'project_data_file'

    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        super(ConfigManager, self).__init__(configuration_object, configuration_file, pipeline_arguments)
        # Lazy Process command line arguments
        self.__pipeline_arguments_object = None
        self.__running_mode = None


# Models for dealing with the data file that describes the project
class ProjectTrackDescriptor:
    # TODO
    # Project Data File keys relative to every TrackMap object
    _PROJECT_DATA_FILE_KEY_TRACK_NAME = 'trackName'
    _PROJECT_DATA_FILE_KEY_TRACK_SHORT_LABEL = 'trackShortLabel'
    _PROJECT_DATA_FILE_KEY_TRACK_LONG_LABEL = 'trackLongLabel'
    _PROJECT_DATA_FILE_KEY_TRACK_SPECIES = 'trackSpecie'
    _PROJECT_DATA_FILE_KEY_TRACK_POGO_FILE_PATH = 'pogoFile'

    def __init__(self, project_track_descriptor_object):
        self.__project_track_descriptor_object = project_track_descriptor_object

    def _get_value_for_key(self, key, default=""):
        if self.__project_track_descriptor_object and (key in self.__project_track_descriptor_object):
            return self.__project_track_descriptor_object[key]
        return default

    def get_track_name(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_NAME)

    def get_track_short_label(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_SHORT_LABEL)

    def get_track_long_label(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_LONG_LABEL)

    def get_track_species(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_SPECIES)

    def get_track_file_path_pogo(self):
        return self._get_value_for_key(self._PROJECT_DATA_FILE_KEY_TRACK_POGO_FILE_PATH)


class ProjectDescriptor:
    # TODO
    # Project Data File keys
    _PROJECT_DATA_FILE_KEY_TRACKHUB_NAME = 'trackHubName'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_SHORT_LABEL = 'trackHubShortLabel'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_LONG_LABEL = 'trackHubLongLabel'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_HUB_TYPE = 'trackHubType'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_EMAIL = 'trackHubEmail'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_INTERNAL_ABSOLUTE_PATH = 'trackHubInternalAbsolutePath'
    _PROJECT_DATA_FILE_KEY_TRACKHUB_SECTION_TRACKMAPS = 'trackMaps'

    def __init__(self, project_data_file_path):
        self.__project_data_file_path = project_data_file_path
        self.__project_data_object = None
        self.__trackmaps = None

    def _get_project_data_object(self):
        if not self.__project_data_object:
            self.__project_data_object = general_toolbox.read_json(self.__project_data_file_path)
        return self.__project_data_object

    def _get_value_for_key(self, key, default=""):
        # TODO - I should start thinking about refactoring this out
        pass


class TrackhubCreatorForProject(Director):
    # TODO
    def __init__(self, configuration_object, configuration_file, pipeline_arguments):
        runner_id = "{}-{}".format(__name__, time.time())
        super(TrackhubCreatorForProject, self).__init__(runner_id)
        self.__config_manager = ConfigManager(configuration_object, configuration_file, pipeline_arguments)
        self.__trackhub_destination_folder = None


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
