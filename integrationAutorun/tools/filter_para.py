import sys
import logging
from collections import OrderedDict
from os.path import abspath, join, exists, isfile
from transfer_para import transfer_para

# define the logging basic configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s ->> %(message)s',
#     datefmt='%a, %d %b %Y %H:%M:%S')

# define content processing parameters
CONTENT_PROCESSING_PARAM_LIST = ('deon', 'dvle', 'ieon', 'dvme', 'dom', 'msce', 'miee', 'mdle', 'mdee', 'mave', 'ngon')
# define device processing parameters
DEVICE_PROCESSING_PARAM_LIST = ('aoon', 'beon', 'vbon', 'vbm', 'bexe', 'geon', 'aron', 'arde', 'arra', 'arod', 'artp',
                                'arbs')
# define qmf process expected parameter list
PARA_LIST_IN_QMF_PROCESS = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vol', 'dom', 'bew', 'dvla', 'dfsa',
                            'dhsa', 'dvmc', 'msce', 'mdee', 'miee', 'mdle', 'dvle', 'dvme', 'mave', 'vcbf', 'becf',
                            'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli', 'dhfm', 'deon', 'ieon', 'ngon',
                            'dvlo', 'gebs', 'iebs', 'aobs')
# define global process expected parameter list
PARA_LIST_IN_GLOBAL_PROCESS = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla',
                               'arra', 'dfsa', 'dhsa', 'dvmc', 'arod', 'msce', 'arde', 'mdee', 'miee', 'mdle', 'dvle',
                               'dvme', 'mave', 'vcbf', 'becf', 'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli',
                               'dhfm', 'vbon', 'beon', 'deon', 'geon', 'ieon', 'ngon', 'aoon', 'aron', 'dvlo', 'artp',
                               'pstg', 'gebs', 'iebs', 'aobs', 'arbs')
# define the process name as first filter key word in log file
QMF_PROCESS_NAME = 'DlbDap2QmfProcess'
GLOBAL_PROCESS_NAME = 'DlbDap2Process'
# define key words in audio chain for dolby content
KEY_WORDS_IN_AUDIO_CHAIN_FOR_DOLBY_CONTENT = [
    'featureTest', 'AudioTrack', 'AudioFlinger', 'OMXMaster',
    'NuPlayer', 'ARenderer:', ' ACodec  :', 'MediaCodec:',
    'DlbDlbEffect', 'DlbDapCrossfadeProcess', 'DlbDapEndpointParamCache', 'DapController',
    'DMSService', 'DlbDap2Process', 'DlbDap2QmfProcess', 'DlbEffectContext',
    'DDP_JOCDecoder', 'evo_parser', 'udc_user', 'ddpdec_client_joc',
]
# define key words in audio chain for non dolby content
KEY_WORDS_IN_AUDIO_CHAIN_FOR_NON_DOLBY_CONTENT = [
    'featureTest', 'AudioTrack', 'AudioFlinger', 'OMXMaster',
    'NuPlayer', 'ARenderer:', ' ACodec  :', 'MediaCodec:',
    'DlbDlbEffect', 'DlbDapCrossfadeProcess', 'DlbDapEndpointParamCache', 'DapController',
    'DMSService', 'DlbDap2Process'
]
# define specified feature key word dictionary
DAP_JOC_FORCE_DOWN_MIX_INDEX = 0
DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX = 1
DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX = 2
DAP_MIX_MATRIX_INDEX = 3
SPECIFIED_FEATURE_KEY_WORDS_LIST = [
    'DDP_JOCDecoder: setMultiChannelPCMOutDownmix',
    'DlbDap2QmfProcess: DAP output mode set',  # for DlbDap2QmfProcess and DlbDap2Process
    'DlbDap2Process: DAP output mode set',  # for DlbDap2QmfProcess and DlbDap2Process
    'mix matrix'
]


class LogComparison:
    EFFECT_PARAS_DICT = OrderedDict()
    A_RENDERER_PARAS_DICT = OrderedDict()
    SPECIFIED_FEATURE_PARAS_DICT = OrderedDict()

    def __init__(self, logger_name=''):
        self.logger = None
        LogComparison.__initialize_all_para_ordered_dict()
        pass

    def set_logger_name(self, logger_name):
        self.logger = logging.getLogger(logger_name)

    @property
    def get_logger(self):
        return self.logger

    # wrapper all initialize function
    @staticmethod
    def __initialize_all_para_ordered_dict():
        LogComparison.__initialize_global_para_ordered_dict()
        LogComparison.__initialize_qmf_para_ordered_dict()
        LogComparison.__initialize_specified_para_ordered_dict()

    # initialize global dap parameters
    @staticmethod
    def __initialize_global_para_ordered_dict():
        for index in range(len(PARA_LIST_IN_GLOBAL_PROCESS)):
            LogComparison.EFFECT_PARAS_DICT[PARA_LIST_IN_GLOBAL_PROCESS[index]] = 'non-exist'

    # initialize dap parameters in OMX component
    @staticmethod
    def __initialize_qmf_para_ordered_dict():
        for index in range(len(PARA_LIST_IN_QMF_PROCESS)):
            LogComparison.A_RENDERER_PARAS_DICT[PARA_LIST_IN_QMF_PROCESS[index]] = 'non-exist'

    # initialize specified feature value
    @staticmethod
    def __initialize_specified_para_ordered_dict():
        for index in range(len(SPECIFIED_FEATURE_KEY_WORDS_LIST)):
            LogComparison.SPECIFIED_FEATURE_PARAS_DICT[SPECIFIED_FEATURE_KEY_WORDS_LIST[index]] = 'non-exist'

    # common function to filter expected key word in string
    def __search_dap_para_line_by_line(self, process_name, line):
        if process_name in line:
            # dap parameter begin with '(' and end with '=''
            fourcc_name_start_index = line.find('(')
            fourcc_name_end_index = line.find('=')

            if (fourcc_name_start_index >= 0) and (fourcc_name_end_index >= 0):
                # dap parameter value begin with '[' and end with ']'
                fourcc_value_start_index = line.find('[')
                fourcc_value_end_Index = line.find(']')

                if (fourcc_value_start_index >= 0) and (fourcc_value_end_Index >= 0):
                    fourcc_name = line[(fourcc_name_start_index + 1):fourcc_name_end_index]
                    fourcc_value = line[(fourcc_value_start_index + 1):fourcc_value_end_Index]
                    # self.logger.debug(
                    #     ">>>>>  %s = %s " % (fourcc_name, fourcc_value))
                    if GLOBAL_PROCESS_NAME == process_name:
                        LogComparison.EFFECT_PARAS_DICT[fourcc_name] = fourcc_value
                    elif QMF_PROCESS_NAME == process_name:
                        LogComparison.A_RENDERER_PARAS_DICT[fourcc_name] = fourcc_value
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
            self.logger.info(">>>>> the specified log file for filter exist ! ")
            # Read data from log file
            with open(input_file_name, 'r') as fp_r:
                lines = fp_r.readlines()
                fp_r.close()

            # start to parse the log using four cc key word defined before
            self.logger.info('>>>>> start to filter dap parameter in global and qmf process ')
            for line in lines:
                line = line.strip('\n')
                self.__search_dap_specified_feature_by_file(line)
                line = line.replace(' ', '')  # remove empty char
                if line != "":
                    self.__search_dap_para_line_by_line(GLOBAL_PROCESS_NAME, line)
                    self.__search_dap_para_line_by_line(QMF_PROCESS_NAME, line)
                else:
                    # self.logger.debug("read empty line in log !")
                    pass

        self.logger.info(">>>>> End to filter dap parameters ")

    # common write function : write content in ordered dictionary to a specified file with line by line
    def __write_content_to_file(self, input_order_diction, output_file_name):
        # self.logger.info("<<<<< Welcome to DAP Parameters write !")
        # self.logger.info("<<<<< start to write para to specified file : %s" % output_file_name)
        assert isinstance(input_order_diction, OrderedDict)
        with open(output_file_name, 'w') as fp_w:
            for key, value in input_order_diction.items():
                content = key + "=" + value + '\n'
                temp_content = content.strip('\n')
                self.logger.debug("<<<<< %s " % temp_content)
                # print("write content to file :" + content)
                fp_w.write(content)
            fp_w.close()

    # write global dap parameters to a file whose name is suffixed with *_effect_paras_*.txt
    def __write_global_parameter_to_file(self, output_file_name):
        self.logger.info("<<<<< write dap parameters in global process start")
        self.__write_content_to_file(LogComparison.EFFECT_PARAS_DICT, output_file_name)
        self.logger.info("<<<<< write dap parameters in global process end  ")
        if exists(output_file_name):
            self.logger.info("-----------------------------------------------------")
            self.logger.info("-----------------------------------------------------")
            self.logger.info("Congratulation. filter dap param in global process succeed ")
            self.logger.info(" Please refer to the file : %s " % output_file_name)
            self.logger.info("-----------------------------------------------------")
            self.logger.info("-----------------------------------------------------")
        else:
            self.logger.error("!!!!! failed to filter effect param in global process")

    # write qmf dap parameters to a file whose name is suffixed with *_arenderer_paras_*.txt
    def __write_qmf_parameter_to_file(self, output_file_name):
        self.logger.info("<<<<< write dap parameters in qmf process start")
        self.__write_content_to_file(LogComparison.A_RENDERER_PARAS_DICT, output_file_name)
        self.logger.info("<<<<< write dap parameters in qmf process end  ")
        if exists(output_file_name):
            self.logger.info("-----------------------------------------------------")
            self.logger.info("-----------------------------------------------------")
            self.logger.info("Congratulation. filter dap param in qmf process succeed ")
            self.logger.info(" Please refer to the file : %s " % output_file_name)
            self.logger.info("-----------------------------------------------------")
            self.logger.info("-----------------------------------------------------")
        else:
            self.logger.error("!!!!! failed to write effect param in qmf process to file")

    # transfer global dap effect parameters to dap ca dp parameter
    # and saved in a file with suffixed with *dap_cp_dp_*.txt
    # new created file could be used as a input of a stand alone library (dap_cp_dp.exe)
    def __write_dap_cp_dp_params_to_file(self, input_file_name, output_file_name):
        self.logger.info("<<<<< Transfer to dap cp dp parameters start")
        if exists(input_file_name):
            transfer_para(input_file_name, output_file_name)
        else:
            self.logger.error("<<<<< failed to transfer dap cp dp parameter!")
            self.logger.error("<<<<< input file not exist : %s " % input_file_name)
        self.logger.info("<<<<< transfer to dap cp dp parameters end  ")
        if exists(output_file_name):
            self.logger.info("-----------------------------------------------------")
            self.logger.info("-----------------------------------------------------")
            self.logger.info("Congratulation. transfer dap cp dp parameter succeed ")
            self.logger.info(" Please refer to the file : %s " % output_file_name)
            self.logger.info("-----------------------------------------------------")
            self.logger.info("-----------------------------------------------------")
        else:
            self.logger.error("!!!!! failed to transfer dap cp dp param")

    # filter dap effect parameters from log captured by command : adb logcat
    # and then save the params to three file
    def filter_para_from_log(self, input_file_name, effect_para_output_file_name,
                             a_renderer_para_file_name, dap_cp_dp_file_name):
        self.__initialize_all_para_ordered_dict()
        self.__filter_dap_para_from_log(input_file_name)
        filter_audio_key_word_from_log(KEY_WORDS_IN_AUDIO_CHAIN_FOR_DOLBY_CONTENT,
                                       input_file_name, input_file_name + ".key")
        self.__write_global_parameter_to_file(effect_para_output_file_name)
        self.__write_qmf_parameter_to_file(a_renderer_para_file_name)
        self.__write_dap_cp_dp_params_to_file(effect_para_output_file_name, dap_cp_dp_file_name)

    # get value though four cc name from global dap effect parameters
    def get_parameter_value_in_global_process(self, effect_fourcc_name):
        result = None
        if effect_fourcc_name in PARA_LIST_IN_GLOBAL_PROCESS:
            temp_value = LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name]
            if 'non-exist' != temp_value:
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
    def get_parameter_value_in_qmf_process(self, effect_fourcc_name):
        result = None
        if effect_fourcc_name in PARA_LIST_IN_QMF_PROCESS:
            temp_value = LogComparison.A_RENDERER_PARAS_DICT[effect_fourcc_name]
            if 'non-exist' != temp_value:
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

    # get dap force down mix value
    def get_dap_joc_force_down_mix_mode_value_in_ddp_joc_decoder(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_JOC_FORCE_DOWN_MIX_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != 'non-exist':
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
        if value != 'non-exist':
            value = value.strip('\n')
            result = value.split(" ")[-9]
            self.logger.info("in global process , dap output mode set to %s with 2 output channels and " % result)
            pass
        return result

    # get dap output mode setting value
    def get_dap_output_mode_set_value_in_qmf_process(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != 'non-exist':
            value = value.strip('\n')
            result = value.split(" ")[-9]
            self.logger.info("in qmf process , dap output mode set to %s with 2 output channels and " % result)
            pass
        return result

    # get dap output mode mix matrix
    def get_dap_output_mode_mix_matrix(self):
        result = None
        key = SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_MIX_MATRIX_INDEX]
        value = LogComparison.SPECIFIED_FEATURE_PARAS_DICT[key]
        if value != 'non-exist':
            value = value.strip('\n')
            result = value.split(" ")[-3]
            self.logger.info(".................. %s mix matrix" % result)
            pass
        return result

    # For some content playback , check no double content processing in global process
    def __verify_content_processing_parameter_in_global_process_equals_to_zero(self):
        result = True
        for effect_fourcc_name in CONTENT_PROCESSING_PARAM_LIST:
            if LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name] != '0':
                self.logger.error("!!!!! double content processing in global process ")
                temp_string = LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name]
                self.logger.error("!!!!! %s = %s " % (effect_fourcc_name, temp_string))
                result = False
        if result:
            self.logger.info(" Congratulation ! No double content processing in global process.")
        return result

    # For some content playback , check no double device processing in qmf process
    def __verify_device_processing_parameter_in_qmf_process_not_exist(self):
        result = True
        for effect_fourcc_name in DEVICE_PROCESSING_PARAM_LIST:
            if effect_fourcc_name in LogComparison.A_RENDERER_PARAS_DICT:
                self.logger.error("!!!!! double device processing in qmf process ")
                temp_string = LogComparison.A_RENDERER_PARAS_DICT[effect_fourcc_name]
                self.logger.error("!!!!! %s = %s " % (effect_fourcc_name, temp_string))
                result = False
                pass
        if result:
            self.logger.info(" Congratulation ! No double device processing in qmf process.")
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

        return result

    def verify_no_double_processing_effect_for_non_dolby_content(self):
        result = True
        self.logger.info("----- verify effect parameter didn't exist in qmf process for non Dolby content ")

        for key, value in LogComparison.A_RENDERER_PARAS_DICT.items():
            if 'non-exist' != value:
                self.logger.error("!!!!! effect parameter exist in qmf process for non dolby content")
                self.logger.error("!!!!! %s = %s " % (key, value))
                result = False
                pass
        if result:
            self.logger.info(" Congratulation ! No effect parameter in qmf process for non Dolby content .")
        return result


# filter by key word from log file
def filter_audio_key_word_from_log(key_word_list, input_file_name, output_file_name):
    # Read data from log file
    with open(input_file_name, 'r') as fp_r:
        lines = fp_r.readlines()
        fp_r.close()

    with open(output_file_name, 'w') as fp_w:
        for line in lines:
            for _key_word in key_word_list:
                if _key_word in line:
                    fp_w.write(line)
                    pass
    fp_w.close()

help_content = (
    "Usage: python filter_para.py -i log.txt \n"
    "\n"
    "Mandatory parameters:\n"
    "-i/--input\t\t: Followed by log file name captured from the command : adb logcat \n"
    "\n")


def main(argvs):
    # define the logging basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s ->> %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S')
    import getopt
    try:
        opts, args = getopt.getopt(argvs, 'hi:', ['help', 'input'])
    except Exception, e:
        print e
        sys.exit(0)
    if len(opts) == 0:
        print("Please specify the input file name captured from the command : adb logcat")
        sys.exit(0)

    input_file_name = None  # 'effect_params.txt'
    print(" opts :" + str(opts))

    try:
        for op, value in opts:
            if op in ('-h', '--help'):
                print help_content
                sys.exit(0)
            if op in ('-i', '--input'):
                print("input log file name :" + value)
                input_file_name = value
                if input_file_name is None:
                    print 'Please set the log file name captured from adb logcat command !'
                    sys.exit(0)

        # first specified the log file we want to filter effect parameters
        input_file_abs_path = abspath(join('.', input_file_name))
        logging.getLogger().info("specified log file : %s" % input_file_abs_path)
        # specified the output file name , and default it will be saved at current location
        effect_paras_output_file_abs_path = abspath(join('.', "effect_params.txt"))
        a_renderer_param_output_file_abs_path = abspath(join('.', "ARenderer_params.txt"))
        dap_cp_dp_param_output_file_abs_path = abspath(join('.', "dap_cp_dp.txt"))
        logging.getLogger().debug("dap effect para in global process saved at : %s" % effect_paras_output_file_abs_path)
        logging.getLogger().debug("dap effect para in qmf process saved at : %s" % a_renderer_param_output_file_abs_path)
        logging.getLogger().debug("dap cp and dp para saved at : %s" % dap_cp_dp_param_output_file_abs_path)

        em1 = LogComparison()
        em1.set_logger_name('test')
        em1.filter_para_from_log(input_file_abs_path, effect_paras_output_file_abs_path,
                                 a_renderer_param_output_file_abs_path, dap_cp_dp_param_output_file_abs_path)
        em1.verify_no_double_processing_effect_for_dolby_content()
        # em1.verify_no_double_processing_effect_for_non_dolby_content()
        em1.get_parameter_value_in_global_process('arbs')
        em1.get_parameter_value_in_qmf_process('arbs')
        em1.get_parameter_value_in_global_process('aron')
        em1.get_parameter_value_in_qmf_process('aron')
        em1.get_parameter_value_in_global_process('dea')
        em1.get_parameter_value_in_qmf_process('dea')
        force_down_mix_value = em1.get_dap_joc_force_down_mix_mode_value_in_ddp_joc_decoder()
        if force_down_mix_value is not None:
            print "force down value : %s" % force_down_mix_value
        dap_output_mode_set = em1.get_dap_output_mode_set_value_in_global_process()
        if dap_output_mode_set is not None:
            print "dap output mode set value :%s " % dap_output_mode_set
        dap_mix_matrix_value = em1.get_dap_output_mode_mix_matrix()
        if dap_mix_matrix_value is not None:
            print "dap mix matrix : %s " % dap_mix_matrix_value
    except Exception, e:
        logging.getLogger().error('Encounter an exception : %s' % e)


if __name__ == "__main__":
    main(sys.argv[1:])
