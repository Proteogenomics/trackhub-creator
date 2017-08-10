# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 03-08-2017 15:44
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
These are the models for representing and dealing with trackhubs
DISCLAIMER - This is the first iteration of the software to create the trackhubs. In this iteration we are going for the
simple version of the hubs, "trackhub quickstart guide" at https://genome.ucsc.edu/goldenpath/help/hubQuickStart.html
"""

# Application imports
import config_manager


# Now, different trackhub builders for the different types of trackhubs (quickstart, custom, etc.)
# DISCLAIMER - I'm aware this first iteration may look a little bit patchy, but it needs to be acknowledged that the
# documentation for modeling this is not very developer friendly, this module it is not meant to be a general module for
# building all sorts of trackhubs and this is the first iteration, so we're not very sure what we want
# TODO - How and where to define the building directors?


def key_value_to_str_if_not_none(key, value, separator=' ', suffix='\n'):
    """
    Helper method that, given a key, value, separator and suffix, it will return the string
    '<key><separator><value><suffix>' if value is not None, otherwise it will return the empty string ''
    :param key: key
    :param value: value
    :param separator: character to use as separator, default ' '
    :param suffix: character to use as suffix, default '\n'
    :return: '<key><separator><value><suffix>' if value not None, '' otherwise
    """
    if value:
        return "{}{}{}{}".format(key, separator, value, suffix)
    return ""


# Modeling TrackHubs
class TrackHubGenomeAssembly:
    # TODO
    pass


class TrackCollector:
    # TODO
    pass


# Model for a Track
class BaseTrack:
    _SEPARATOR_CHAR = ' '

    def __init__(self, track, short_label, long_label):
        # Client side of the model
        self.__track = track
        self.__short_label = short_label
        self.__long_label = long_label
        # Builder side of the model
        self.__type = None
        self.__big_data_url = None

    def __str__(self):
        return "track{}{}\n" \
               "type{}{}\n" \
               "bigDataUrl{}{}\n" \
               "shortLabel{}{}\n" \
               "longLabel{}{}" \
            .format(self._SEPARATOR_CHAR, self.get_track(),
                    self._SEPARATOR_CHAR, self.get_type(),
                    self._SEPARATOR_CHAR, self.get_big_data_url(),
                    self._SEPARATOR_CHAR, self.get_short_label(),
                    self._SEPARATOR_CHAR, self.get_long_label())

    def __identify_track_type_from_file(self, file_path):
        # TODO - We return the default type right now, but this will change in the future
        return 'bed'

    def set_type(self, file_path):
        self.__type = self.__identify_track_type_from_file(file_path)

    def set_big_data_url(self, big_data_url):
        self.__big_data_url = big_data_url

    def get_track(self):
        return self.__track

    def get_short_label(self):
        return self.__short_label

    def get_long_label(self):
        return self.__long_label

    def get_type(self):
        return self.__type

    def get_big_data_url(self):
        return self.__big_data_url

    def dump_to_track_db_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self))


# Model for a trackhub
class TrackHub:
    _SEPARATOR_CHAR = ' '

    def __init__(self, hub, short_label, long_label, email, description_url):
        self.__hub = hub
        self.__short_label = short_label
        self.__long_label = long_label
        self.__email = email
        self.__description_url = description_url
        # Default genomes file
        self.__genomes_file = 'genomes.txt'

    def __str__(self):
        return "hub{}{}\n" \
               "shortLabel{}{}\n" \
               "longLabel{}{}\n" \
               "genomesFile{}{}\n" \
               "email{}{}\n" \
               "descriptionUrl{}{}" \
            .format(self._SEPARATOR_CHAR, self.get_hub(),
                    self._SEPARATOR_CHAR, self.get_short_label(),
                    self._SEPARATOR_CHAR, self.get_long_label(),
                    self._SEPARATOR_CHAR, self.get_genomes_file(),
                    self._SEPARATOR_CHAR, self.get_email(),
                    self._SEPARATOR_CHAR, self.get_description_url())

    def get_hub(self):
        return self.__hub

    def get_short_label(self):
        return self.__short_label

    def get_long_label(self):
        return self.__long_label

    def get_email(self):
        return self.__email

    def get_description_url(self):
        return self.__description_url

    def get_genomes_file(self):
        return self.__genomes_file

    def dump_to_file(self, file_path):
        with open(file_path, 'w') as f:
            f.write(str(self))


if __name__ == '__main__':
    print("ERROR: This script is part of a pipeline collection and it is not meant to be run in stand alone mode")
