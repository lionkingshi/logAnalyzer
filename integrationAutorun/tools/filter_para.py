import sys
import logging
from collections import OrderedDict
from os.path import abspath, join, exists, realpath
from transfer_para import transfer_para
from transfer_para import set_content_channel_num_equal_to_two
from transfer_para import set_content_channel_num_not_equal_to_two
from transfer_para import register_transfer_para_logger_name
from filter_para_config import *

# define the logging basic configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s ->> %(message)s',
#     datefmt='%a, %d %b %Y %H:%M:%S')

EMPTY_STRING_FLAG = 'non-exist'


class LogComparison:
    EFFECT_PARAS_DICT = OrderedDict()
    A_RENDERER_PARAS_DICT = OrderedDict()
    AC4_PARAS_DICT = OrderedDict()
    SPECIFIED_FEATURE_PARAS_DICT = OrderedDict()

    def __init__(self, logger_name=''):
        self.logger = None
        LogComparison.__initialize_all_para_ordered_dict()
        pass

    def set_logger_name(self, logger_name, _level_no=logging.DEBUG):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(_level_no)
        register_transfer_para_logger_name(logger_name, _level=_level_no)

    @property
    def get_logger(self):
        return self.logger

    # wrapper all initialize function
    @staticmethod
    def __initialize_all_para_ordered_dict():
        LogComparison.__initialize_global_para_ordered_dict()
        LogComparison.__initialize_qmf_para_ordered_dict()
        LogComparison.__initialize_specified_para_ordered_dict()
        LogComparison.__initialize_ac4_para_ordered_dict()

    # initialize global dap parameters
    @staticmethod
    def __initialize_global_para_ordered_dict():
        for index in range(len(PARA_LIST_IN_GLOBAL_PROCESS)):
            LogComparison.EFFECT_PARAS_DICT[PARA_LIST_IN_GLOBAL_PROCESS[index]] = EMPTY_STRING_FLAG

    # initialize dap parameters in OMX component
    @staticmethod
    def __initialize_qmf_para_ordered_dict():
        for index in range(len(PARA_LIST_IN_QMF_PROCESS)):
            LogComparison.A_RENDERER_PARAS_DICT[PARA_LIST_IN_QMF_PROCESS[index]] = EMPTY_STRING_FLAG

    # initialize specified feature value
    @staticmethod
    def __initialize_specified_para_ordered_dict():
        for index in range(len(SPECIFIED_FEATURE_KEY_WORDS_LIST)):
            LogComparison.SPECIFIED_FEATURE_PARAS_DICT[SPECIFIED_FEATURE_KEY_WORDS_LIST[index]] = EMPTY_STRING_FLAG

    # initialize AC4 parameters value in OMX component
    @staticmethod
    def __initialize_ac4_para_ordered_dict():
        for index in range(len(PARA_LIST_AC4)):
            LogComparison.AC4_PARAS_DICT[PARA_LIST_AC4[index]] = EMPTY_STRING_FLAG

    # common function to filter expected key word in string
    def __search_dap_para_line_by_line(self, process_name, line):
        if process_name in line:
            # dap parameter begin with '(' and end with '=''
            fourcc_name_start_index = line.find('(')
            fourcc_name_end_index = line.find('=')

            if (fourcc_name_start_index >= 0) and (fourcc_name_end_index >= 0):
                # dap parameter value begin with '[' and end with ']'
                fourcc_value_start_index = line.find('[')
                fourcc_value_end_index = line.find(']')

                if (fourcc_value_start_index >= 0) and (fourcc_value_end_index >= 0):
                    fourcc_name = line[(fourcc_name_start_index + 1):fourcc_name_end_index]
                    fourcc_value = line[(fourcc_value_start_index + 1):fourcc_value_end_index]
                    # self.logger.debug(
                    #     ">>>>>  %s = %s " % (fourcc_name, fourcc_value))
                    if GLOBAL_PROCESS_NAME == process_name:
                        LogComparison.EFFECT_PARAS_DICT[fourcc_name] = fourcc_value
                    elif QMF_PROCESS_NAME == process_name:
                        LogComparison.A_RENDERER_PARAS_DICT[fourcc_name] = fourcc_value
                    elif AC4_PROCESS_NAME == process_name:
                        LogComparison.AC4_PARAS_DICT[fourcc_name] = fourcc_value
                    else:
                        self.logger.error("not expected filter key words !")
        else:
            # self.logger.debug("find no dolby related process name [{}:{}] in log !".
            #                   format(qmf_process_name, global_process_name))
            pass

    # record specified key words in dictionary
    @staticmethod
    def __search_dap_specified_feature_by_file(_line):
        for key in SPECIFIED_FEATURE_KEY_WORDS_LIST:
            if key in _line:
                LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key] = _line
                # print LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]

    # filter all dap parameter from log file
    def __filter_dap_para_from_log(self, input_file_name):
        self.logger.info('>>>>> Welcome to DAP Parameters filter !')
        if not exists(abspath(input_file_name)):
            self.logger.error("!!!!! the specified log file for filter not exist : %s " % input_file_name)
        else:
            self.logger.debug(">>>>> the specified log file for filter exist ! ")
            # Read data from log file
            try:
                with open(input_file_name, 'r') as fp_r:
                    lines = fp_r.readlines()
                    fp_r.close()
            except EnvironmentError, e:
                print ("!!!!!failed to open logcat file captured from device :" + e.message)

            # start to parse the log using four cc key word defined before
            self.logger.info('>>>>> start to filter dap parameter in global and qmf process ')
            ceqt_combined_list = ''
            for line in lines:
                line = line.strip('\n')
                line = line.strip('\b')
                self.__search_dap_specified_feature_by_file(line)
                line = line.replace(' ', '')  # remove empty char
                # add code to handle specified ceqt filer law in dax3 project
                if GLOBAL_PROCESS_NAME in line:
                    if 'ceqt' in line:
                        if 'setParam(ceqt' in line:
                            ceqt_combined_list = line
                        elif 'ceqtcontinue' in line:
                            ceqt_combined_list += line.split(':')[-1]
                        else:
                            ceqt_combined_list = ''
                            self.logger.error("ceqt format is not expected ! error in filter !")

                if line != "":
                    self.__search_dap_para_line_by_line(GLOBAL_PROCESS_NAME, line)
                    self.__search_dap_para_line_by_line(QMF_PROCESS_NAME, line)
                    self.__search_dap_para_line_by_line(AC4_PROCESS_NAME, line)
                else:
                    # self.logger.debug("read empty line in log !")
                    pass
            # add code to handle specified ceqt filer law in dax3 project
            if ceqt_combined_list != "":
                # self.logger.info("++++++"+ceqt_combined_list)
                new_ceqt_combined_string = ceqt_combined_list.replace(',])', '])')
                new_ceqt_combined_string = ceqt_combined_list[:-4]
                # self.logger.info("++++++" + new_ceqt_combined_string)
                new_ceqt_combined_string += '])'
                # self.logger.info("++++++" + new_ceqt_combined_string)
                self.__search_dap_para_line_by_line(GLOBAL_PROCESS_NAME, new_ceqt_combined_string)

        self.logger.info(">>>>> End to filter dap parameters ")

    # common write function : write content in ordered dictionary to a specified file with line by line
    def __write_content_to_file(self, input_order_diction, output_file_name):
        # self.logger.info("<<<<< Welcome to DAP Parameters write !")
        # self.logger.info("<<<<< start to write para to specified file : %s" % output_file_name)
        assert isinstance(input_order_diction, OrderedDict)
        try:
            with open(output_file_name, 'w') as fp_w:
                for key, value in input_order_diction.items():
                    content = key + "=" + value + '\n'
                    temp_content = content.strip('\n')
                    self.logger.debug("<<<<< %s " % temp_content)
                    # print("write content to file :" + content)
                    fp_w.write(content)
                fp_w.close()
        except EnvironmentError, e:
            self.logger.debug("!!!!!failed to open input file"+e.message)

    # write global dap parameters to a file whose name is suffixed with *_effect_paras_*.txt
    def __write_global_parameter_to_file(self, output_file_name):
        self.logger.info("<<<<< write dap parameters in global process start")
        self.__write_content_to_file(LogComparison.EFFECT_PARAS_DICT, output_file_name)
        self.logger.info("<<<<< write dap parameters in global process end  ")
        if exists(output_file_name):
            self.logger.info("<<<<< Congratulation. filter dap param in global process succeed ")
            self.logger.warning("<<<<< Please refer to the file : %s " % output_file_name)
        else:
            self.logger.error("!!!!! failed to filter effect param in global process")

    # write qmf dap parameters to a file whose name is suffixed with *_arenderer_paras_*.txt
    def __write_qmf_parameter_to_file(self, output_file_name):
        self.logger.info("<<<<< write dap parameters in qmf process start")
        self.__write_content_to_file(LogComparison.A_RENDERER_PARAS_DICT, output_file_name)
        self.logger.info("<<<<< write dap parameters in qmf process end  ")
        if exists(output_file_name):
            self.logger.info("<<<<< Congratulation. filter dap param in qmf process succeed ")
            self.logger.warning("<<<<< Please refer to the file : %s " % output_file_name)
        else:
            self.logger.error("!!!!! failed to write effect param in qmf process to file")

    # write ac4 parameters to a file whose name is suffixed with *_ac4_paras_*.txt
    def __write_ac4_parameter_to_file(self, output_file_name):
        self.logger.info("<<<<< write dap ac4 parameters start")
        self.__write_content_to_file(LogComparison.AC4_PARAS_DICT, output_file_name)
        self.logger.info("<<<<< write dap ac4 parameters end  ")
        if exists(output_file_name):
            self.logger.info("<<<<< Congratulation. filter dap ac4 param succeed ")
            self.logger.warning("<<<<< Please refer to the file : %s " % output_file_name)
        else:
            self.logger.error("!!!!! failed to write dap ac4 param to file")

    # special handle for 2 channel content when creating binary command line
    @staticmethod
    def set_special_flag_for_specified_channel_num(channel_num_two_flag=False):
        if channel_num_two_flag:
            set_content_channel_num_equal_to_two()
        else:
            set_content_channel_num_not_equal_to_two()

    # transfer global dap effect parameters to dap ca dp parameter
    # and saved in a file as suffixed with *dap_cp_dp_*.txt
    # new created file could be used as a input of a stand alone library (dap_cp_dp.exe)
    def __write_dap_cp_dp_params_to_file(self, input_file_name, output_file_name):
        if output_file_name is None:
            return None

        self.logger.info("<<<<< Transfer to dap cp dp parameters start")
        if exists(input_file_name):
            transfer_para(input_file_name, output_file_name)
            # set_content_channel_num_not_equal_to_two()
        else:
            self.logger.error("<<<<< failed to transfer dap cp dp parameter!")
            self.logger.error("<<<<< input file not exist : %s " % input_file_name)
        self.logger.info("<<<<< transfer to dap cp dp parameters end  ")
        if exists(output_file_name):
            self.logger.info("<<<<< Congratulation. transfer dap cp dp parameter succeed ")
            self.logger.warning("<<<<< Please refer to the file : %s " % output_file_name)
        else:
            self.logger.error("!!!!! failed to transfer dap cp dp param")

    # filter dap effect parameters from log captured by command : adb logcat
    # and then save the params to three file
    def filter_para_from_log(self,
                             input_file_name,
                             effect_para_output_file_name,
                             a_renderer_para_file_name,
                             dap_global_cp_dp_file_name,
                             dap_qmf_cp_dp_file_name):
        self.__initialize_all_para_ordered_dict()
        self.__filter_dap_para_from_log(input_file_name)
        filter_audio_key_word_from_log(KEY_WORDS_IN_AUDIO_CHAIN_FOR_DOLBY_CONTENT,
                                       input_file_name, input_file_name + ".key")
        if not verify_all_dap_global_parameters_equals_to_non_exist():
            self.__write_global_parameter_to_file(effect_para_output_file_name)
            self.__write_dap_cp_dp_params_to_file(effect_para_output_file_name, dap_global_cp_dp_file_name)
        if not verify_all_dap_decoder_parameters_equals_to_non_exist():
            self.__write_qmf_parameter_to_file(a_renderer_para_file_name)
            self.__write_dap_cp_dp_params_to_file(a_renderer_para_file_name, dap_qmf_cp_dp_file_name)
        if not verify_all_ac4_decoder_parameters_equals_to_non_exist():
            _ac4_para_file_name = a_renderer_para_file_name.replace('arenderer', 'ac4')
            self.__write_ac4_parameter_to_file(_ac4_para_file_name)

    # get value through four cc name from global dap effect parameters
    # But if the input argument is None , return all dap parameters dictionary
    def get_parameter_value_in_global_process(self, effect_fourcc_name=None):
        result = None
        if effect_fourcc_name is None:
            return LogComparison.EFFECT_PARAS_DICT
        else:
            if effect_fourcc_name in PARA_LIST_IN_GLOBAL_PROCESS:
                temp_value = LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name]
                if EMPTY_STRING_FLAG != temp_value:
                    self.logger.info("in global process: %s = %s " % (effect_fourcc_name, temp_value))
                    result = temp_value
                else:
                    self.logger.error("!!!!! Found no specified dap four cc name in global process : %s "
                                      % effect_fourcc_name)
            else:
                self.logger.error(
                    "!!!!! Please specify correct dap para four cc name in global process: %s " % effect_fourcc_name)
                pass
            return result

    # get value though four cc name from qmf dap effect parameters
    def get_parameter_value_in_qmf_process(self, effect_fourcc_name=None):
        result = None
        if effect_fourcc_name is None:
            return LogComparison.A_RENDERER_PARAS_DICT
        else:
            if effect_fourcc_name in PARA_LIST_IN_QMF_PROCESS:
                temp_value = LogComparison.A_RENDERER_PARAS_DICT[effect_fourcc_name]
                if EMPTY_STRING_FLAG != temp_value:
                    self.logger.info("in qmf process : %s = %s " % (effect_fourcc_name, temp_value))
                    result = temp_value
                else:
                    self.logger.error("!!!!! Found no specified dap four cc name in qmf process : %s "
                                      % effect_fourcc_name)
            else:
                self.logger.error(
                    "!!!!! Please specify correct dap para four cc name in qmf process: %s " % effect_fourcc_name)
                pass
            return result

    # get value though four cc name from dap ac4 effect parameters
    def get_parameter_value_in_ac4_decoder(self, effect_fourcc_name=None):
        result = None
        if effect_fourcc_name is None:
            return LogComparison.AC4_PARAS_DICT
        else:
            if effect_fourcc_name in PARA_LIST_AC4:
                temp_value = LogComparison.AC4_PARAS_DICT[effect_fourcc_name]
                if EMPTY_STRING_FLAG != temp_value:
                    self.logger.info("in ac4 decoder : %s = %s " % (effect_fourcc_name, temp_value))
                    result = temp_value
                else:
                    self.logger.error("!!!!! Found no specified dap four cc name in ac4 decoder : %s "
                                      % effect_fourcc_name)
            else:
                self.logger.error(
                    "!!!!! Please specify correct dap ac4 para four cc name in ac4 decoder: %s " % effect_fourcc_name)
                pass
            return result

    # get dap force down mix value
    def get_decoder_joc_force_down_mix_mode_value_in_ddp_joc_decoder(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_JOC_FORCE_DOWN_MIX_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != EMPTY_STRING_FLAG:
            value = value.strip('\n')
            result = value.split(" ")[-1]
            self.logger.info("in ddp decode config , force down mix value : %s " % result)
            pass
        return result

    # get dap output mode setting value
    def get_dap_output_mode_set_value_in_global_process(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != EMPTY_STRING_FLAG:
            value = value.strip('\n')
            # DlbDap2Process: DAP output mode set to 11 with 2 output channels and custom mix matrix.
            result = value.split(" ")[INDEX_OUTPUT_MODE_IN_GLOBAL_PROCESS_LIST]
            self.logger.info("in global process , dap output mode set to %s with 2 output channels and " % result)
            pass
        return result

    # get dap output mode setting value
    def get_dap_output_mode_set_value_in_qmf_process(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != EMPTY_STRING_FLAG:
            value = value.strip('\n')
            result = value.split(" ")[INDEX_OUTPUT_MODE_IN_QMF_PROCESS_LIST]
            # DlbDap2QmfProcess: DAP output mode set to 1 with 2 output channels and null mix matrix.
            self.logger.info("in qmf process , dap output mode set to %s with 2 output channels and " % result)
            pass
        return result

    # get dap output mode mix matrix
    def get_dap_output_mode_mix_matrix(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_MIX_MATRIX_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != EMPTY_STRING_FLAG:
            value = value.strip('\n')
            result = value.split(" ")[-3]
            self.logger.info(".................. %s mix matrix" % result)
            pass
        return result

    # get dap output mode mix matrix in qmf process
    def get_mix_matrix_in_qmf_process(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != EMPTY_STRING_FLAG:
            value = value.strip('\n')
            # DlbDap2QmfProcess: DAP output mode set to 1 with 2 output channels and null mix matrix.
            result = value.split(" ")[INDEX_MIX_MATRIX_IN_QMF_PROCESS_LIST]
            self.logger.info(".................. %s mix matrix (QMF)" % result)
            pass
        return result

    # get dap output mode mix matrix in global process
    def get_mix_matrix_in_global_process(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != EMPTY_STRING_FLAG:
            value = value.strip('\n')
            # DlbDap2QmfProcess: DAP output mode set to 1 with 2 output channels and null mix matrix.
            result = value.split(" ")[INDEX_MIX_MATRIX_IN_GLOBAL_PROCESS_LIST]
            self.logger.info(".................. %s mix matrix" % result)
            pass
        return result

    # For some content playback , check no double content processing in global process
    def __verify_content_processing_parameter_in_global_process_equals_to_zero(self):
        result = True
        for effect_fourcc_name in CONTENT_PROCESSING_PARAM_LIST:
            # edit code for dax3 project ,
            # dom list contains 19 elements and the first element means vir on or off
            # For dax2 project , dom list only has 1 element and the first element means vir on or off
            if LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name][0] != '0':
                self.logger.error("!!!!! double content processing in global process ")
                temp_string = LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name]
                self.logger.error("!!!!! %s = %s " % (effect_fourcc_name, temp_string))
                result = False
        if result:
            self.logger.info("----- Congratulation ! No double content processing in global process.")
        return result

    # For some content playback , check no double device processing in qmf process
    def __verify_device_processing_parameter_in_qmf_process_not_exist(self):
        result = True
        for effect_fourcc_name in DEVICE_PROCESSING_PARAM_LIST:
            if effect_fourcc_name in LogComparison.A_RENDERER_PARAS_DICT:
                temp_string = LogComparison.A_RENDERER_PARAS_DICT[effect_fourcc_name]
                if temp_string != EMPTY_STRING_FLAG:
                    self.logger.error("!!!!! double device processing in qmf process ")
                    self.logger.error("!!!!! %s = %s " % (effect_fourcc_name, temp_string))
                    result = False
                pass
        if result:
            self.logger.info("----- Congratulation ! No double device processing in qmf process.")
        return result

    #
    def verify_no_double_processing_effect_for_dolby_content(self):
        result = True
        self.logger.info("----- verify no double processing effect for Dolby content ")
        self.logger.info("----- verify content processing parameter in global process equals to 0 ")
        result_content_double_processing = self.__verify_content_processing_parameter_in_global_process_equals_to_zero()

        self.logger.info("----- verify device processing parameter didn't exist in qmf process ")
        result_device_double_processing = self.__verify_device_processing_parameter_in_qmf_process_not_exist()

        if not result_content_double_processing:
            result = False
            pass
        if not result_device_double_processing:
            result = False
            pass
        if result:
            self.logger.info("----- Congratulation ! No double processing for Dolby content .")

        return result

    def verify_no_double_processing_effect_for_non_dolby_content(self):
        result = True
        self.logger.info("----- verify effect parameter didn't exist in qmf process for non Dolby content ")

        for key, value in LogComparison.A_RENDERER_PARAS_DICT.items():
            if EMPTY_STRING_FLAG != value:
                self.logger.error("!!!!! effect parameter exist in qmf process for non dolby content")
                self.logger.error("!!!!! %s = %s " % (key, value))
                result = False
                pass
        if result:
            self.logger.info("----- Congratulation ! No effect parameter in qmf process for non Dolby content .")
        return result


def verify_all_dap_parameters_equals_to_non_exist():
    result = True
    if not verify_all_dap_global_parameters_equals_to_non_exist():
        result = False

    if not verify_all_dap_decoder_parameters_equals_to_non_exist():
        result = False
    # for key in PARA_LIST_IN_GLOBAL_PROCESS:
    #     if LogComparison.EFFECT_PARAS_DICT[key] != EMPTY_STRING_FLAG:
    #         result = True
    # for key_other in PARA_LIST_IN_QMF_PROCESS:
    #     if LogComparison.A_RENDERER_PARAS_DICT[key_other] != EMPTY_STRING_FLAG:
    #         result = True
    return result


def verify_all_dap_global_parameters_equals_to_non_exist():
    result = True
    for key in PARA_LIST_IN_GLOBAL_PROCESS:
        if LogComparison.EFFECT_PARAS_DICT[key] != EMPTY_STRING_FLAG:
            result = False
    return result


def verify_all_dap_decoder_parameters_equals_to_non_exist():
    result = True
    for key_other in PARA_LIST_IN_QMF_PROCESS:
        if LogComparison.A_RENDERER_PARAS_DICT[key_other] != EMPTY_STRING_FLAG:
            result = False
    return result


def verify_all_ac4_decoder_parameters_equals_to_non_exist():
    result = True
    for key_other in PARA_LIST_AC4:
        if LogComparison.AC4_PARAS_DICT[key_other] != EMPTY_STRING_FLAG:
            result = False
    return result


# filter by key word from log file
def filter_audio_key_word_from_log(key_word_list, input_file_name, output_file_name):
    # Read data from log file
    lines = ''
    try:
        with open(input_file_name, 'r') as fp_r:
            lines = fp_r.readlines()
            fp_r.close()
    except EnvironmentError, e:
        print ("!!!!!failed to open logcat file captured from device"+e.message)

    try:
        with open(output_file_name, 'w') as fp_w:
            for line in lines:
                for _key_word in key_word_list:
                    if _key_word in line:
                        fp_w.write(line)
                        pass
        fp_w.close()
    except EnvironmentError, e1:
        print ("!!!!!failed to open file saved audio key words:" + e1.message)

help_content = (
    "this is used to : \n"
    "1. filter audio processing four cc key words from the Android Logcat output . \n"
    "2. convert the four cc key words to binary command line . \n"
    "Usage: \n"
    "1. python filter_para.py -i log.txt \n"
    "2. python filter_para.py -i log.txt -2 \n"
    "\n"
    "Mandatory parameters:\n"
    "-i/--input\t: Followed by log file name captured from the command : adb logcat \n"
    "Optional parameters: \n"
    "-2/--channel\t: For 2 channel Dolby content, add this flag \n"
    "\n")


def main(argvs):
    # define the logging basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s[%(lineno)d] %(levelname)s ->> %(message)s')
    em1 = LogComparison()
    temp_logger_name = 'test'
    em1.set_logger_name(temp_logger_name, logging.INFO)
    em1.get_logger.setLevel(logging.WARNING)

    import getopt
    try:
        opts, args = getopt.getopt(argvs, 'hi:2', ['help', 'input', 'channel'])
    except Exception, e:
        print e
        sys.exit(0)
    if len(opts) == 0:
        logging.getLogger(temp_logger_name).warning(
            "Please specify the input file name captured from the command : adb logcat")
        sys.exit(0)

    input_file_name = None
    flaf_channel_num_two = False

    logging.getLogger(temp_logger_name).debug(" opts :" + str(opts))

    try:
        for op, value in opts:
            if op in ('-h', '--help'):
                print help_content
                sys.exit(0)
            if op in ('-i', '--input'):
                logging.getLogger(temp_logger_name).debug("input log file name :" + value)
                input_file_name = value
                if input_file_name is None:
                    logging.getLogger(temp_logger_name).error(
                        'Please set the log file name captured from adb logcat command')
                    sys.exit(0)
            if op in ('-2', '--channel'):
                flaf_channel_num_two = True
                logging.getLogger(temp_logger_name).warning("content channel num is 2 : "+str(flaf_channel_num_two))

        # first specified the log file we want to filter effect parameters
        input_file_abs_path = abspath(join('.', input_file_name))
        logging.getLogger(temp_logger_name).info("specified log file : %s" % input_file_abs_path)
        # specified the output file name , and default it will be saved at current location
        effect_paras_output_file_abs_path = abspath(join('.', "effect_params.txt"))
        a_renderer_param_output_file_abs_path = abspath(join('.', "ARenderer_params.txt"))
        dap_global_cp_dp_param_output_file_abs_path = abspath(join('.', "dap_global_cp_dp.txt"))
        dap_qmf_cp_dp_param_output_file_abs_path = abspath(join('.', "dap_qmf_cp_dp.txt"))
        logging.getLogger(temp_logger_name).debug(
            "dap effect para in global process saved at : %s" % effect_paras_output_file_abs_path)
        logging.getLogger(temp_logger_name).debug(
            "dap effect para in qmf process saved at : %s" % a_renderer_param_output_file_abs_path)
        logging.getLogger(temp_logger_name).debug(
            "dap global cp and dp para saved at : %s" % dap_global_cp_dp_param_output_file_abs_path)
        logging.getLogger(temp_logger_name).debug(
            "dap qmf cp and dp para saved at : %s" % dap_qmf_cp_dp_param_output_file_abs_path)

        if flaf_channel_num_two:
            em1.set_special_flag_for_specified_channel_num(channel_num_two_flag=True)

        em1.filter_para_from_log(input_file_abs_path,
                                 effect_paras_output_file_abs_path,
                                 a_renderer_param_output_file_abs_path,
                                 dap_global_cp_dp_param_output_file_abs_path,
                                 dap_qmf_cp_dp_param_output_file_abs_path)

        em1.set_special_flag_for_specified_channel_num(channel_num_two_flag=False)
    except Exception, e:
        logging.getLogger(temp_logger_name).error('Encounter an exception : %s' % e)


if __name__ == "__main__":
    main(sys.argv[1:])
