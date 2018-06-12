import logging
from os import mkdir
from os.path import abspath, join, exists
from constant import *

log_file_name_for_diff_endpoint = (AUDIO_DEVICE_OUT_MONO_SPEAKER,
                                   AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                                   AUDIO_DEVICE_OUT_WIRED_HEADPHONE,
                                   AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                                   AUDIO_DEVICE_OUT_BLUETOOTH_A2DP)

format_dict = {
    1: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),  # debug
    2: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),  # info
    3: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),  # waring
    4: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),  # error
    5: logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')   # critical
}


class Logger:
    def __init__(self, log_name, log_level='1', logger_name=''):
        """
        :param log_name: specify the file name log saved
        :param log_level: specify the print log level
        :param logger_name: specify the logger name , default is root
        """

        # create folder for log
        parent_abs_folder = abspath(join('.', 'log'))
        for index in range(len(log_file_name_for_diff_endpoint)):
            folder_name_abs_path = abspath(join(parent_abs_folder, log_file_name_for_diff_endpoint[index]))
            # folder_name_abs_path = parent_abs_folder + '/' + log_file_name_for_diff_endpoint[index]
            print ("create folder name is %s" % folder_name_abs_path)
            if not exists(folder_name_abs_path):
                mkdir(folder_name_abs_path)

        # create a logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        # create a file handler to write log to
        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.DEBUG)

        # create a stream handler to print log to system console
        sh = logging.StreamHandler()
        sh.setLevel(logging.ERROR)

        # create print format
        formatter = format_dict[int(log_level)]
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        # add handler to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    @property
    def get_log(self):
        return self.logger
        pass
