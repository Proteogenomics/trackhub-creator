# 
# Author    : Manuel Bernal Llinares
# Project   : trackhub-creator
# Timestamp : 11-07-2017 10:40
# ---
# © 2017 Manuel Bernal Llinares <mbdebian@gmail.com>
# All rights reserved.
# 

"""
Unit Tests for the download manager module
"""

import unittest
# App imports
import config_manager
from download_manager.manager import Manager as DownloadManager


class TestDownloadManager(unittest.TestCase):
    __logger = config_manager.get_app_config_manager().get_logger_for(__name__)

    def test_success_on_sample_files_download(self):
        urls = ['http://mirror.internode.on.net/pub/test/50meg.test',
                'http://mirror.internode.on.net/pub/test/100meg.test',
                'http://mirror.internode.on.net/pub/test/10meg.test',
                'http://error.nodomain.on.net/pub/test/1meg.tes']
        destination_folder = config_manager.get_app_config_manager().get_folder_run()
        # Log the test environment
        self.__logger.info("Sample file URLs to download: {}".format(",".join(urls)))
        self.__logger.info("Destination folder for the downloads, '{}'".format(destination_folder))
        # Get the download manager and start the downloads
        download_manager = DownloadManager(urls, destination_folder, self.__logger)
        download_manager.start_downloads()
        download_manager.wait_all()
        self.assertTrue(download_manager.is_success(), "Files downloaded successfully")
