# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 23-08-2017 14:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
This module models the trackhub registry
"""

import json
import requests
# App imports
import config_manager
import ensembl.service
from . import models as trackhub_models
from . import exceptions as trackhub_exceptions


# Registry request body model
class TrackhubRegistryRequestBodyModel:
    def __init__(self):
        self.logger = config_manager.get_app_config_manager().get_logger_for(
            "{}.{}".format(__name__, type(self).__name__))
        # hub.txt URL
        self.url = None
        self.assembly_accession_map = {}

    def add_accession_for_assembly(self, assembly, accession):
        if assembly in self.assembly_accession_map:
            self.logger.error(
                "DUPLICATED Assembly '{}' add request, existing accession '{}', "
                "accession requested to be added '{}' - SKIPPED".format(assembly, self.assembly_accession_map[assembly],
                                                                        accession))
        else:
            self.assembly_accession_map[assembly] = accession
            self.logger.info("Assembly '{}' entry added to request body with accession '{}'"
                             .format(assembly, accession))

    def __str__(self):
        return json.dumps({'url': self.url, 'assemblies': self.assembly_accession_map})


# Visitor to export the trackhub as an instance of TrackhubRegistryRequestBodyModel
class TrackhubRegistryRequestBodyModelExporter(trackhub_models.TrackHubExporter):
    def __init__(self):
        super().__init__()

    def export_simple_trackhub(self, trackhub_builder):
        # In this case, the export summary will be an instance of TrackhubRegistryRequestBodyModelExporter
        if not self.export_summary:
            self.export_summary = TrackhubRegistryRequestBodyModel()
            ensembl_species_service = ensembl.service.get_service().get_species_data_service()
            for assembly in trackhub_builder.assemblies:
                self.export_summary \
                    .add_accession_for_assembly(assembly,
                                                ensembl_species_service.get_species_entry_for_assembly(assembly))
        return self.export_summary


class TrackhubRegistryService:
    __TRACKHUB_REGISTRY_API_SUBPATH_LOGIN = '/api/login'

    def __init__(self, username, password):
        self.logger = config_manager.get_app_config_manager().get_logger_for("{}.{}"
                                                                             .format(__name__, type(self).__name__))
        self.username = username
        self.password = password
        self.trackhub_registry_base_url = 'https://www.trackhubregistry.org'
        self.__auth_token = None

    def __login(self):
        if not self.__auth_token:
            response = requests.get("{}{}"
                                    .format(self.trackhub_registry_base_url,
                                            self.__TRACKHUB_REGISTRY_API_SUBPATH_LOGIN),
                                    auth=(self.username, self.password),
                                    verify=True)
            if not response.ok:
                raise trackhub_exceptions.TrackhubRegistryServiceException(
                    "LOGIN ERROR '{}', HTTP status '{}'".format(response.text, response.status_code))
            self.__auth_token = response.json()[u'auth_token']
        return self.__auth_token

    def __logout(self):
        # TODO
        pass

    def publish_trackhub(self, hub_url, trackhub_registry_model):
        # TODO
        pass


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
