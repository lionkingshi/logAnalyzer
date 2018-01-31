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
content_processing_param_list = ('deon', 'dvle', 'ieon', 'dvme', 'dom', 'msce', 'miee', 'mdle', 'mdee', 'mave', 'ngon')
# define device processing parameters
device_processing_param_list = ('aoon', 'beon', 'vbon', 'vbm', 'bexe', 'geon', 'aron', 'arde', 'arra', 'arod', 'artp',
                                'arbs')
# define qmf process expected parameter list
para_list_in_qmf_process = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vol', 'dom', 'bew', 'dvla', 'dfsa',
                            'dhsa', 'dvmc', 'msce', 'mdee', 'miee', 'mdle', 'dvle', 'dvme', 'mave', 'vcbf', 'becf',
                            'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli', 'dhfm', 'deon', 'ieon', 'ngon',
                            'dvlo', 'gebs', 'iebs', 'aobs')
# define global process expected parameter list
para_list_in_global_process = ('dea', 'iea', 'dsa', 'beb', 'plb', 'vmb', 'dsb', 'ded', 'vbm', 'dom', 'bew', 'dvla',
                               'arra', 'dfsa', 'dhsa', 'dvmc', 'arod', 'msce', 'arde', 'mdee', 'miee', 'mdle', 'dvle',
                               'dvme', 'mave', 'vcbf', 'becf', 'vbmf', 'vbsf', 'preg', 'vbhg', 'vbog', 'vbsg', 'dvli',
                               'dhfm', 'vbon', 'beon', 'deon', 'geon', 'ieon', 'ngon', 'aoon', 'aron', 'dvlo', 'artp',
                               'pstg', 'gebs', 'iebs', 'aobs', 'arbs')
# define the key word in log filter
FLAG_FILTER_GLOBAL_PARA_IN_GLOBAL_PROCESS = 'effect parameter'
FLAG_FILTER_CONTENT_PROCESSING_PARA_IN_GLOBAL_PROCESS = 'content processing parameter'
FLAG_FILTER_QMF_PARA_IN_QMF_PROCESS = 'udc effect parameter'
FLAG_FILTER_DEVICE_PROCESSING_PARA_IN_QMF_PROCESS = 'device processing parameter'

# define the process name as first filter key word in log file
qmf_process_name = 'DlbDap2QmfProcess'
global_process_name = 'DlbDap2Process'


class LogComparison:
    EFFECT_PARAS_DICT = OrderedDict()
    CONTENT_PARAS_DICT = OrderedDict()
    ARENDERER_PARAS_DICT = OrderedDict()
    DEVICE_PARAS_DICT = OrderedDict()

    def __init__(self, logger_name=''):
        self.logger = logging.getLogger(logger_name)
        LogComparison.initialize_device_para_ordered_dict()
        LogComparison.initialize_global_para_ordered_dict()
        LogComparison.initialize_qmf_para_ordered_dict()
        pass

    @property
    def get_logger(self):
        return self.logger

    # define global dap parameters
    # for non-dolby content ,
    # for dolby content ,
    @staticmethod
    def initialize_global_para_ordered_dict():
        for index in range(len(para_list_in_global_process)):
            LogComparison.EFFECT_PARAS_DICT[para_list_in_global_process[index]] = 'non-exist'

    # define content-processing dap parameters
    # for non-dolby content ,
    # for dolby content ,
    @staticmethod
    def initialize_qmf_para_ordered_dict():
        for index in range(len(para_list_in_qmf_process)):
            LogComparison.ARENDERER_PARAS_DICT[para_list_in_qmf_process[index]] = 'non-exist'

    # define 12 device parameters
    @staticmethod
    def initialize_device_para_ordered_dict():
        for index in range(len(device_processing_param_list)):
            LogComparison.DEVICE_PARAS_DICT[device_processing_param_list[index]] = 'non-exist'

    # define content processing parameters
    @staticmethod
    def initialize_content_para_ordered_dict():
        for index in range(len(content_processing_param_list)):
            LogComparison.CONTENT_PARAS_DICT[content_processing_param_list[index]] = 'non-exist'

    def filter_from_log(self, filter_process_name, filter_key_word, input_file_name):
        self.logger.info('Welcome to DAP Parameters filter !')
        self.logger.info('start to filter %s in %s process ' % (filter_key_word, filter_process_name))
        # initial the order dictionary to align with audio dump parameter list
        if not exists(abspath(input_file_name)):
            self.logger.error(" the specified log file for filter not exist : %s " % input_file_name)
        else:
            self.logger.info(" the specified log file for filter exist ! ")
            self.logger.info(" start to parse the log ! ")
            # Read data from log file
            with open(input_file_name, 'r') as fp_r:
                lines = fp_r.readlines()
                fp_r.close()

            for line in lines:
                line = line.strip('\n')
                line = line.replace(' ', '')  # remove empty char
                if line != "":
                    if filter_process_name in line:
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
                                self.logger.debug(
                                    "the param name and its value : %s = %s " % (fourcc_name, fourcc_value))
                                if FLAG_FILTER_GLOBAL_PARA_IN_GLOBAL_PROCESS == filter_key_word:
                                    LogComparison.EFFECT_PARAS_DICT[fourcc_name] = fourcc_value
                                elif FLAG_FILTER_CONTENT_PROCESSING_PARA_IN_GLOBAL_PROCESS == filter_key_word:
                                    LogComparison.CONTENT_PARAS_DICT[fourcc_name] = fourcc_value
                                elif FLAG_FILTER_QMF_PARA_IN_QMF_PROCESS == filter_key_word:
                                    LogComparison.ARENDERER_PARAS_DICT[fourcc_name] = fourcc_value
                                elif FLAG_FILTER_DEVICE_PROCESSING_PARA_IN_QMF_PROCESS == filter_key_word:
                                    LogComparison.DEVICE_PARAS_DICT[fourcc_name] = fourcc_value
                                else:
                                    self.logger.error("not expected filter key words !")
                    else:
                        # self.logger.debug("find no dolby related process name [{}:{}] in log !".
                        #                   format(qmf_process_name, global_process_name))
                        pass
                else:
                    # self.logger.debug("read empty line in log !")
                    pass

        self.logger.info('End to filter %s in %s process ' % (filter_key_word, filter_process_name))

    def parse_global_parameter_in_global_process(self, input_file_name):
        self.logger.info("===== filter global parameters in global process start=====---")
        self.filter_from_log(global_process_name, FLAG_FILTER_GLOBAL_PARA_IN_GLOBAL_PROCESS, input_file_name)
        self.logger.info("===== filter global parameters in global process end  =====---")

    def parse_content_processing_parameter_in_global_process(self, input_file_name):
        self.logger.info("===== filter content processing parameters in global process start=====---")
        self.filter_from_log(global_process_name, FLAG_FILTER_CONTENT_PROCESSING_PARA_IN_GLOBAL_PROCESS,
                             input_file_name)
        self.logger.info("===== filter content processing parameters in global process end=====---")

    def parse_qmf_parameter_in_qmf_process(self, input_file_name):
        self.logger.info("===== filter content processing parameters in qmf process start=====---")
        self.filter_from_log(qmf_process_name, FLAG_FILTER_QMF_PARA_IN_QMF_PROCESS, input_file_name)
        self.logger.info("===== filter content processing parameters in qmf process end  =====---")

    def parse_device_processing_parameter_in_qmf_process(self, input_file_name):
        self.logger.info("===== filter device processing parameters in global process start=====---")
        self.filter_from_log(qmf_process_name, FLAG_FILTER_DEVICE_PROCESSING_PARA_IN_QMF_PROCESS, input_file_name)
        self.logger.info("===== filter device processing parameters in global process end  =====---")

    def write_content_to_file(self, input_order_diction, output_file_name):
        self.logger.info("Welcome to DAP Parameters write !")
        self.logger.info("start to write para to specified file : %s" % output_file_name)
        assert isinstance(input_order_diction, OrderedDict)
        with open(output_file_name, 'w') as fp_w:
            for key, value in input_order_diction.items():
                content = key + "=" + value + '\n'
                temp_content = content.strip('\n')
                self.logger.debug("write content to file : %s " % temp_content)
                # print("write content to file :" + content)
                fp_w.write(content)
            fp_w.close()
            self.logger.info("End to DAP Parameters write !")

    def write_global_parameter_to_file(self, output_file_name):
        self.logger.info("===== write global parameters filtered in global process start=====---")
        self.write_content_to_file(LogComparison.EFFECT_PARAS_DICT, output_file_name)
        self.logger.info("===== write global parameters filtered in global process end  =====---")

    def write_qmf_parameter_to_file(self, output_file_name):
        self.logger.info("===== write content processing parameters filtered in qmf process start=====---")
        self.write_content_to_file(LogComparison.ARENDERER_PARAS_DICT, output_file_name)
        self.logger.info("===== write content processing parameters filtered in qmf process end  =====---")

    def write_device_processing_parameter_in_qmf_process_to_file(self, output_file_name):
        self.logger.info("===== write device processing parameters filtered in global process start=====---")
        self.write_content_to_file(LogComparison.DEVICE_PARAS_DICT, output_file_name)
        self.logger.info("===== write device processing parameters filtered in global process end  =====---")

    def write_content_processing_parameter_in_global_process_to_file(self, output_file_name):
        self.logger.info("===== write content processing parameters filtered in global process start=====---")
        self.write_content_to_file(LogComparison.CONTENT_PARAS_DICT, output_file_name)
        self.logger.info("===== write content processing parameters filtered in global process end  =====---")

    def write_dap_cp_dp_params_to_file(self, input_file_name, output_file_name):
        self.logger.info("===== transfer to dap cp dp parameters start")
        if exists(input_file_name):
            transfer_para(input_file_name, output_file_name)
            self.logger.info("Congratulation. transfer dap cp dp parameter succeed ")
        else:
            self.logger.error("===== transfer dap cp dp parameter fails ")
            self.logger.error("===== input file not exist : %s " % input_file_name)
        self.logger.info("===== transfer to dap cp dp parameters end  ")

    def filter_para_from_log(self, input_file_name, effect_para_output_file_name, arendered_para_file_name, dap_cp_dp_file_name):
        self.parse_global_parameter_in_global_process(input_file_name)
        self.write_global_parameter_to_file(effect_para_output_file_name)
        self.parse_qmf_parameter_in_qmf_process(input_file_name)
        self.write_qmf_parameter_to_file(arendered_para_file_name)
        self.parse_content_processing_parameter_in_global_process(input_file_name)
        self.parse_device_processing_parameter_in_qmf_process(input_file_name)
        self.write_dap_cp_dp_params_to_file(effect_para_output_file_name, dap_cp_dp_file_name)

    def get_parameter_value_in_global_process(self, effect_fourcc_name):
        if effect_fourcc_name in para_list_in_global_process:
            temp_value = LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name]
            self.logger.info(
                "Congratulation. Get effect parameter value in global process: %s = %s " % (
                    effect_fourcc_name, temp_value))
            return temp_value
        else:
            self.logger.error(
                "wrong parameter fourcc name or not exist in param list in global process : %s " % effect_fourcc_name)
            pass

    def get_parameter_value_in_qmf_process(self, effect_fourcc_name):
        if effect_fourcc_name in para_list_in_qmf_process:
            temp_value = LogComparison.ARENDERER_PARAS_DICT[effect_fourcc_name]
            self.logger.info(
                "Congratulation. Get effect parameter value in qmf process : %s = %s " % (
                    effect_fourcc_name, temp_value))
            return temp_value
        else:
            self.logger.error(
                "wrong parameter fourcc name or not exist in param list in qmf process : %s " % effect_fourcc_name)
            pass

    def verify_content_processing_parameter_in_global_process_equals_to_zero(self):
        result = True
        for effect_fourcc_name in content_processing_param_list:
            if LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name] != '0':
                self.logger.error("double content processing in global process ")
                temp_string = LogComparison.EFFECT_PARAS_DICT[effect_fourcc_name]
                self.logger.error("=====- %s = %s " % (effect_fourcc_name, temp_string))
                result = False
            if LogComparison.CONTENT_PARAS_DICT[effect_fourcc_name] != '0':
                self.logger.error("double content processing in global process ")
                temp_string = LogComparison.CONTENT_PARAS_DICT[effect_fourcc_name]
                self.logger.error("===== %s = %s " % (effect_fourcc_name, temp_string))
                result = False
                pass
        if result:
            self.logger.info(" Congratulation ! No double content processing in global process.")
        return result

    def verify_device_processing_parameter_in_qmf_process_not_exist(self):
        result = True
        for effect_fourcc_name in device_processing_param_list:
            if effect_fourcc_name in LogComparison.ARENDERER_PARAS_DICT:
                self.logger.error("double device processing in qmf process ")
                temp_string = LogComparison.ARENDERER_PARAS_DICT[effect_fourcc_name]
                self.logger.error("=====- %s = %s " % (effect_fourcc_name, temp_string))
                result = False
                pass
            if LogComparison.DEVICE_PARAS_DICT[effect_fourcc_name] != 'non-exist':
                self.logger.error("double device processing in qmf process ")
                temp_string = LogComparison.DEVICE_PARAS_DICT[effect_fourcc_name]
                self.logger.error("=====- %s = %s " % (effect_fourcc_name, temp_string))
                result = False
                pass
        if result:
            self.logger.info(" Congratulation ! No double device processing in qmf process.")
        return result

    def verify_no_double_processing_for_dolby_content(self):
        result = True
        self.logger.info("--- verify content double processing parameter in global process equals to 0 ")
        result_content_double_processing = self.verify_content_processing_parameter_in_global_process_equals_to_zero()
        self.logger.info("--- verify no content double processing in global process end   ")
        self.logger.info("--- verify device double processing parameter didn't exist in qmf process ")
        result_device_double_processing = self.verify_device_processing_parameter_in_qmf_process_not_exist()
        self.logger.info("--- verify no device double processing in qmf process end   ")

        if not result_content_double_processing:
            result = False
            pass
        if not result_device_double_processing:
            result = False
            pass

        return result

    def verify_no_qmf_parameter_for_non_dolby_content(self):
        result = True
        self.logger.info("--- verify effect parameter didn't exist in qmf process ")

        for key, value in LogComparison.ARENDERER_PARAS_DICT.items():
            if value != 'non-exist':
                self.logger.error("===== effect parameter exist in qmf process for non dolby content")
                self.logger.error("===== %s = %s " % (key, value))
                result = False
                pass

        for effect_fourcc_name in device_processing_param_list:
            if LogComparison.DEVICE_PARAS_DICT[effect_fourcc_name] != 'non-exist':
                self.logger.error("===== effect parameter exist in qmf process for non dolby content")
                temp_string = LogComparison.DEVICE_PARAS_DICT[effect_fourcc_name]
                self.logger.error("===== %s = %s " % (effect_fourcc_name, temp_string))
                result = False
                pass

        if result:
            self.logger.info(" Congratulation ! No effect parameter in qmf process for non Dolby content .")
            self.logger.info("--- verify no effect parameter in qmf process end   ")
        return result


def main(argvs):
    # define the logging basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s ->> %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S')
    import getopt
    try:
        opts, args = getopt.getopt(argvs, 'hf:i:o:e:', ['isdolbycontent', 'input', 'output', 'expectedresult'])
    except Exception, e:
        print e
        sys.exit(0)
    if len(opts) == 0:
        print("please specify the effect process name , input file name and output file name ....")
        sys.exit(0)

    flag_is_dolby_content = False  # 'dap2'
    input_file_name = None  # 'effect_params.txt'
    output_file_name = None  # 'effect_params_from_log_parse.txt'
    expected_fourcc_para = None
    expected_fourcc_value = None
    print(" opts :" + str(opts))

    try:
        for op, value in opts:
            if op in ('-h', '--help'):
                print help_content
                sys.exit(0)
            if op in ('-f', '--isdolbycontent'):
                print ("is dolby content :" + value)
                flag_is_dolby_content = value
                # if value.lower() in ('qmf', 'dap2'):
                # 	process_name = value.lower()
                # else:
                # 	print('Please set the process name where you want to parse the dap parameters !')
                # 	sys.exit(0)
            if op in ('-i', '--input'):
                print("input file name :" + value)
                input_file_name = value
                if input_file_name is None:
                    print 'Please set the log file name which is filted from logcat !'
                    sys.exit(0)
            if op in ('-o', '--output'):
                output_file_name = value
                print("output file name :" + value)
                if output_file_name is None:
                    print 'Better to set the output file name which would be parsed from input file ! '
                    print 'If not specified , use default value : effect_params_from_log_parse.txt !'
            if op in ('-e', '--expectedresult'):
                expected_fourcc_para = value.split('=')[0]
                expected_fourcc_value = value.split('=')[1]
                if expected_fourcc_para is None:
                    print 'expected result format is wrong. use this format : dom=0 .'
                    sys.exit(0)
                if expected_fourcc_value is None:
                    print 'expected result format is wrong. use this format : dom=0 .'
                    sys.exit(0)

        # first specified the log file we want to filter effect parameters
        input_file_abs_path = abspath(join('.', input_file_name))
        logging.getLogger().info("specified log file : %s" % input_file_abs_path)
        # specified the output file name , and default it will be saved at current location
        effect_paras_output_file_abs_path = abspath(join('.', "effect_params.txt"))
        arendered_param_output_file_abs_path = abspath(join('.', "arendered_params.txt"))
        dap_cp_dp_param_output_file_abs_path = abspath(join('.', "dap_cp_dp.txt"))
        logging.getLogger().debug("effect para in global process saved at : %s" % effect_paras_output_file_abs_path)
        logging.getLogger().debug("effect para in qmf process saved at : %s" % arendered_param_output_file_abs_path)
        logging.getLogger().debug("dap cp and dp para saved at : %s" % dap_cp_dp_param_output_file_abs_path)

        em1 = LogComparison()
        em1.filter_para_from_log(input_file_abs_path, effect_paras_output_file_abs_path,
                                 arendered_param_output_file_abs_path, dap_cp_dp_param_output_file_abs_path)
        em1.verify_no_double_processing_for_dolby_content()
        em1.get_parameter_value_in_global_process('arbs')
        em1.get_parameter_value_in_qmf_process('arbs')
        em1.get_parameter_value_in_global_process('aron')
        em1.get_parameter_value_in_qmf_process('aron')
        em1.get_parameter_value_in_global_process('dea')
        em1.get_parameter_value_in_qmf_process('dea')
    except Exception, e:
        logging.getLogger().error('Encounter an exception : %s' % e)


if __name__ == "__main__":
    main(sys.argv[1:])
