#!/usr/bin/python
"""
Created on Apr 18st, 2018 (my son has just already one and half year)
@author: twang and hshi
"""
import sys
from os.path import abspath, join
import logging

# Input File
INPUT = 'effect_params.txt'

# Output File
OUTPUT = 'dap_cpdp.txt'

UTF_8 = 'utf-8'

# define output mode
DAP_CPDP_PROCESS_1 = '0'
DAP_CPDP_PROCESS_2 = '1'
DAP_CPDP_PROCESS_2_HEADPHONE = '8'
DAP_CPDP_PROCESS_2_HEADPHONE_HEIGHT = '9'
DAP_CPDP_PROCESS_5_1_SPEAKER = '10'
DAP_CPDP_PROCESS_5_1_2_SPEAKER = '11'

STEREO = '1'
HEADPHONE = '9'

# define unique added four cc name in dax3 project
DAX3_UNIQUE_PARA = ('vol', 'ceon', 'ceqt')

# define project name for the script
PROJECT_NAME_DAX2 = 'dax2'
PROJECT_NAME_DAX3 = 'dax3'
PREDICTED_PROJECT_NAME = PROJECT_NAME_DAX2
PROCESS_NAME_QMF = 'qmf'
PROCESS_NAME_GLOBAL = 'global'
PREDICTED_PROCESS_NAME = PROCESS_NAME_GLOBAL
# define orientation type
ORIENTATION_LANDSCAPE = '1'
ORIENTATION_PORTRAIT = '0'
ORIENTATION_NA = '2'
# define endpoint type
ENDPOINT_TYPE_SPEAKER = '0'
ENDPOINT_TYPE_HEADPHONE = '1'
ENDPOINT_TYPE_HDMI = '2'
ENDPOINT_TYPE_MIRACAST = '3'
ENDPOINT_TYPE_OTHER = '4'
# deine virtual enable status
VIRTUAL_STATUS_ON = '1'
VIRTUAL_STATUS_OFF = '0'
# define dom key index
START_INDEX_DOM_VALUE_IN_DOM_LIST = 6
VIRTUAL_STATUS_INDEX_IN_DOM = 0
ENDPOINT_TYPE_INDEX_IN_DOM = 2
ORIENTATION_INDEX_IN_DOM = 4
# special handle for 2 chanel content
FLAG_2_CHANNEL_CONTENT = False

#  "DAPv1 parameters name" to "DAPv2 parameters name"
DAP1_2_DAP2 = {
    'dea'      :   'dialog-enhancer-amount',
    'iea'      :   'ieq-amount',
    'dsa'      :   'virtualizer-surround-speaker-angle',
    'beb'      :   'bass-enhancer-boost',
    'plb'      :   'calibration-boost',
    'vmb'      :   'volmax-boost',
    'dsb'      :   'surround-boost',
    'ded'      :   'dialog-enhancer-ducking',
    'vbm'      :   'virtual-bass-mode',
    'dom'      :   'output-mode',
    'bew'      :   'bass-enhancer-width',
    'dvla'     :   'volume-leveler-amount',
    'arra'     :   'regulator-relaxation-amount',
    'dfsa'     :   'virtualizer-front-speaker-angle',
    'dhsa'     :   'virtualizer-height-speaker-angle',
    'dvmc'     :   'volume-modeler-calibration',
    'arod'     :   'regulator-overdrive',
    'msce'     :   'mi-surround-compressor-steering-enable',
    'arde'     :   'regulator-speaker-dist-enable',
    'mdee'     :   'mi-dialog-enhancer-steering-enable',
    'miee'     :   'mi-ieq-steering-enable',
    'mdle'     :   'mi-dv-leveler-steering-enable',
    'dvle'     :   'volume-leveler-enable',
    'dvme'     :   'volume-modeler-enable',
    'mave'     :   'mi-adaptive-virtualizer-steering-enable',
    'vcbf'     :   'NOT USED',
    'becf'     :   'bass-enhancer-cutoff-frequency',
    'vbmf'     :   'virtual-bass-mix-freqs',
    'vbsf'     :   'virtual-bass-src-freqs',
    'vbhg'     :   'virtual-bass-subgains',
    'vbog'     :   'virtual-bass-overall-gain',
    'vbsg'     :   'virtual-bass-slope-gain',
    'dvli'     :   'volume-leveler-in-target',
    'dhfm'     :   'height-filter-mode',
    'vbon'     :   'virtual-bass-process-enable',
    'beon'     :   'bass-enhancer-enable',
    'deon'     :   'dialog-enhancer-enable',
    'geon'     :   'graphic-equalizer-enable',
    'ieon'     :   'ieq-enable',
    'ngon'     :   'surround-decoder-enable',
    'aoon'     :   'audio-optimizer-enable',
    'aron'     :   'regulator-enable',
    'dvlo'     :   'volume-leveler-out-target',
    'artp'     :   'regulator-timbre-preservation',
    'preg'     :   'pregain',
    'pstg'     :   'postgain',
    'gebs'     :   'graphic-equalizer-bands',
    'iebs'     :   'ieq-bands',
    'aobs'     :   'audio-optimizer-bands',
    'arbs'     :   'regulator-tuning',
    'vol'      :   'system-gain',
    'ceon'     :   'complex-equalizer-enable',
    'ceqt'     :   'complex-equalizer-tuning'
}

# define the logging basic configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s ->> %(message)s',
#     datefmt='%a, %d %b %Y %H:%M:%S')
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(name)s %(filename)s[line:%(lineno)d] %(levelname)s ->> %(message)s',
#     datefmt='%a, %d %b %Y %H:%M:%S')

# define logger name
logger_print = ''
logger_print_name = 'test'


def register_transfer_para_logger_name(_logger_name, _level=logging.DEBUG):
    global logger_print
    global logger_print_name
    logger_print_name = _logger_name
    logger_print = logging.getLogger(_logger_name)
    logger_print.setLevel(_level)


def mapping(id, value):
    if id == 'gebs':
        return gebs(value)
    elif id == 'iebs':
        return iebs(value)
    elif id == 'aobs':
        return aobs(value)
    elif id == 'arbs':
        return arbs(value)
    elif id == 'dom':
        return dom(value)
    elif id == 'vbmf' or id == 'vbsf':
        return value.replace(',', ':')
    elif id == 'ceqt':
        return ceqt(value)
    else:
        return value


def ceqt(value):
    parameter = ""
    # check the ceqt format is correctly set
    temp_ceqt = value.split(",")
    ceqt_length = len(temp_ceqt)
    channel_num = int(temp_ceqt[0])
    length_in_each_channel = int(temp_ceqt[1])
    # logging.getLogger(logger_print_name).info("ceqt length: {}:{}:{}".format(
    #     ceqt_length, channel_num, length_in_each_channel))

    if (channel_num*length_in_each_channel+2) == ceqt_length:
        effective_ceqt = temp_ceqt[2:]
        # logging.getLogger(logger_print_name).info("ceqt length temp: {}".format(len(effective_ceqt)))
        logging.getLogger(logger_print_name).debug("!!!!! ceqt format check succeed")
        for index_channel in range(channel_num):
            for index_channel_num_list in range(length_in_each_channel):
                if index_channel_num_list == (length_in_each_channel-1):
                    parameter += (effective_ceqt[index_channel*length_in_each_channel+index_channel_num_list] + ",")
                else:
                    parameter += (effective_ceqt[index_channel*length_in_each_channel+index_channel_num_list] + ":")
        result = parameter[:-1]
        flag_check_1 = False
        flag_check_2 = True
        if len(result.split(",")) == channel_num:
            # logging.getLogger(logger_print_name).info("ceqt format check succeed 2!!!!!")
            flag_check_1 = True
            for index_check in range(channel_num):
                # logging.getLogger(logger_print_name).info("ceqt format check succeed 3!!!!!")
                if len(result.split(",")[index_check].split(":")) != length_in_each_channel:
                    # logging.getLogger(logger_print_name).info("ceqt format check succeed 4!!!!!")
                    flag_check_2 = False
        if flag_check_1 and flag_check_2:
            logging.getLogger(logger_print_name).debug("complex-equalizer-tuning={}".format(result))
            return result
        else:
            logging.getLogger(logger_print_name).error("!!!!! return wrong ceqt value")
            return ","
        pass
    else:
        logging.getLogger(logger_print_name).info("!!!!! ceqt format check failed")
        pass
    pass


def dom(value):
    if PREDICTED_PROJECT_NAME == PROJECT_NAME_DAX2:
        logging.getLogger(logger_print_name).info("predicted project name is dax2 and start to transfer dom value")
        if value == '0':
            return STEREO
        elif value == '2':
            return HEADPHONE
        else:
            parameter = '11:2:'
            result = create_mix_matrix(parameter, value)
            # for eachNum in range(8):
            #     parameter += (value.split(',')[2 * eachNum + 1]) + ',' + (value.split(',')[2 * eachNum + 2]) + ':'
            # result = parameter[:-1]
            return result
    elif PREDICTED_PROJECT_NAME == PROJECT_NAME_DAX3:
        logging.getLogger(logger_print_name).info("predicted project name is dax3 and start to transfer dom value")
        if PREDICTED_PROCESS_NAME == PROCESS_NAME_GLOBAL:
            if value[ENDPOINT_TYPE_INDEX_IN_DOM] == ENDPOINT_TYPE_SPEAKER:
                if value[ORIENTATION_INDEX_IN_DOM] == ORIENTATION_PORTRAIT:
                    # when endpoint is stereo speaker and orientation is portrait mode , mix matrix would be applied.
                    # But for mono speaker and portrait orientation mode , mix matrix would be null which is exception
                    # Must modify the ctl_cmd manually : output-mode=1
                    parameter = '0:2:'
                    output_mode_value = create_mix_matrix(parameter, value)
                    return output_mode_value
                elif value[ORIENTATION_INDEX_IN_DOM] == ORIENTATION_LANDSCAPE:
                    # when endpoint is stereo speaker , landscape orientation and vir enable ,
                    # mix matrix would be applied.
                    # for mono speaker , the vir status would always be false
                    if value[VIRTUAL_STATUS_INDEX_IN_DOM] == VIRTUAL_STATUS_ON:
                        parameter = '11:2:'
                        output_mode_value = create_mix_matrix(parameter, value)
                        return output_mode_value
                    else:
                        return DAP_CPDP_PROCESS_2
            elif value[ENDPOINT_TYPE_INDEX_IN_DOM] == ENDPOINT_TYPE_HEADPHONE:
                if value[VIRTUAL_STATUS_INDEX_IN_DOM] == VIRTUAL_STATUS_ON:
                    return DAP_CPDP_PROCESS_2_HEADPHONE_HEIGHT
                else:
                    return DAP_CPDP_PROCESS_2
            else:
                return DAP_CPDP_PROCESS_2
        elif PREDICTED_PROCESS_NAME == PROCESS_NAME_QMF:
            if value[VIRTUAL_STATUS_INDEX_IN_DOM] == VIRTUAL_STATUS_ON:
                # when sv status is enabled and endpoint type is headphone ,
                # for 2 channel content , the output mode is 8
                # for not 2 channel content , the output mode is 9
                # no mix matrix would be applied
                if value[ENDPOINT_TYPE_INDEX_IN_DOM] == ENDPOINT_TYPE_HEADPHONE:
                    if FLAG_2_CHANNEL_CONTENT:
                        return DAP_CPDP_PROCESS_2_HEADPHONE
                    else:
                        return DAP_CPDP_PROCESS_2_HEADPHONE_HEIGHT
                elif value[ENDPOINT_TYPE_INDEX_IN_DOM] == ENDPOINT_TYPE_SPEAKER:
                    # when sv status is enabled, endpoint type is speaker, and orientation mode is landscape
                    # for 2 channel content , the output mode is 10
                    # for not 2 channel content , the output mode is 11
                    # mix matrix would be applied
                    # But for portrait orientation mode , the output mode is 1 which is default setting
                    if value[ORIENTATION_INDEX_IN_DOM] == ORIENTATION_LANDSCAPE:
                        if FLAG_2_CHANNEL_CONTENT:
                            parameter = '10:2:'
                        else:
                            parameter = '11:2:'
                        # print("+++++code run this trip :", parameter)
                        output_mode_value = create_mix_matrix(parameter, value)
                        return output_mode_value
                    elif value[ORIENTATION_INDEX_IN_DOM] == ORIENTATION_PORTRAIT:
                        return DAP_CPDP_PROCESS_2
                else:
                    return DAP_CPDP_PROCESS_2
                pass
            else:
                return DAP_CPDP_PROCESS_2
                pass
        pass


def create_mix_matrix(_prefix, _value):
    try:
        mix_matrix_value = _value[START_INDEX_DOM_VALUE_IN_DOM_LIST:]
        logging.getLogger(logger_print_name).debug("mix matrix value list :" + mix_matrix_value)
        parameter = _prefix
        mix_matrix_length = len(mix_matrix_value.split(','))
        logging.getLogger(logger_print_name).debug("mix matrix value list length: {}".format(mix_matrix_length))
        for eachNum in range(mix_matrix_length / 2):
            parameter += \
                (mix_matrix_value.split(',')[2 * eachNum]) + ',' + (mix_matrix_value.split(',')[2 * eachNum + 1]) + ':'
            result = parameter[:-1]
        return result
    except IndexError, e:
        logging.getLogger(logger_print_name).error("create mix matrix array error :"+e.message)
    except UnboundLocalError, e1:
        logging.getLogger(logger_print_name).error("create mix matrix array error :" + e1.message)


def set_content_channel_num_equal_to_two():
    global FLAG_2_CHANNEL_CONTENT
    FLAG_2_CHANNEL_CONTENT = True
    logging.getLogger(logger_print_name).debug("set content channel num to 2 ")


def set_content_channel_num_not_equal_to_two():
    global FLAG_2_CHANNEL_CONTENT
    FLAG_2_CHANNEL_CONTENT = False
    logging.getLogger(logger_print_name).debug("set content channel num not equals to 2 ")


def gebs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum+1]) + ':' + (value.split(',')[eachNum+21]) + ','
    result = parameter[:-1]
    return result


def iebs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum+1]) + ':' + (value.split(',')[eachNum+21]) + ','
    result = parameter[:-1]
    return result


def aobs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum + 2]) + ':' + (value.split(',')[eachNum + 22]) + ':' + \
                        (value.split(',')[eachNum + 42]) + ':' + (value.split(',')[eachNum + 62]) + ':' + \
                        (value.split(',')[eachNum + 82]) + ':' + (value.split(',')[eachNum + 102]) + ':' + \
                        (value.split(',')[eachNum + 122]) + ':' + (value.split(',')[eachNum + 142]) + ':' + \
                        (value.split(',')[eachNum + 162]) + ':' + (value.split(',')[eachNum + 182]) + ':' + \
                        (value.split(',')[eachNum + 202]) + ','
    result = parameter[:-1]
    return result


def arbs(value):
    parameter = ''
    for eachNum in range(20):
        parameter += (value.split(',')[eachNum+1]) + ':' + (value.split(',')[eachNum+21]) + ':' + \
                        (value.split(',')[eachNum + 41]) + ':' + (value.split(',')[eachNum + 61]) + ','
    result = parameter[:-1]
    return result


def translate(name, value):
    namev2 = DAP1_2_DAP2[name]
    valuev2 = mapping(name, value)
    if name == 'dom':
        logging.getLogger(logger_print_name).warning("!!!!! output-mode={}".format(valuev2))
    parameter = ' --' + namev2 + '=' + valuev2
    return parameter


def predict_process_project_name(lines):
    # for dax2 project , default value of 'ceon' key word should be non-exist
    # and dom value's length should be 1 or 16
    # Note : when dap off for dax3 project , dom default value length is also 1 which is only one exception.
    #        But it does not affect this code logic because the handle logic for dom is same between dax2 and dax3
    FLAG_CEON_FOUR_CC_EXIST = False
    FLAG_CEON_FOUR_CC_EQUAL_TO_NON_EXIST = True
    FLAG_DOM_VALUE_LENGTH_EQUAL_TO_3_5_19 = False
    for line in lines:
        if 'ceon' in line:
            FLAG_CEON_FOUR_CC_EXIST = True
            line = line.strip('\n')
            keys = (line.split('=')[0])
            values = (line.split('=')[1])
            if keys == 'ceon':
                if values != 'non-exist':
                    FLAG_CEON_FOUR_CC_EQUAL_TO_NON_EXIST = False
                else:
                    FLAG_CEON_FOUR_CC_EQUAL_TO_NON_EXIST = True
        if 'dom' in line:
            line.strip('\n')
            keys = line.split('=')[0]
            values = line.split('=')[1]
            if keys == 'dom':
                dom_length = len(values.split(','))
                if dom_length in (3, 5, 19):
                    FLAG_DOM_VALUE_LENGTH_EQUAL_TO_3_5_19 = True
                elif dom_length in (1, 16):
                    FLAG_DOM_VALUE_LENGTH_EQUAL_TO_3_5_19 = False
                else:
                    FLAG_DOM_VALUE_LENGTH_EQUAL_TO_3_5_19 = False

    global PREDICTED_PROJECT_NAME
    global PREDICTED_PROCESS_NAME
    # if four cc name list contains 'ceon' key words, the process name should be global process
    # otherwise it should be qmf process
    if FLAG_CEON_FOUR_CC_EXIST:
        PREDICTED_PROCESS_NAME = PROCESS_NAME_GLOBAL
        # if 'ceon' values are equal to 'non-exist' which is its default values, the project name should be dax2
        # otherwise it should be dax3
        if FLAG_CEON_FOUR_CC_EQUAL_TO_NON_EXIST:
            PREDICTED_PROJECT_NAME = PROJECT_NAME_DAX2
        else:
            PREDICTED_PROJECT_NAME = PROJECT_NAME_DAX3
    else:
        # if four cc name list not contain 'ceon' key words, the process name should be qmf process
        PREDICTED_PROCESS_NAME = PROCESS_NAME_QMF

    # if length of dom value is 3 ,5 ,19 (only one exception : when dap off ,the dom length is 1),
    # the project name should be dax3
    if FLAG_DOM_VALUE_LENGTH_EQUAL_TO_3_5_19:
        PREDICTED_PROJECT_NAME = PROJECT_NAME_DAX3
    else:
        PREDICTED_PROJECT_NAME = PROJECT_NAME_DAX2

    logging.getLogger(logger_print_name).warning('!!!!! predicted project name is {}'.format(PREDICTED_PROJECT_NAME))
    logging.getLogger(logger_print_name).warning('!!!!! predicted process name is {}'.format(PREDICTED_PROCESS_NAME))


def transfer_para(input_file_name=INPUT, output_file_name=OUTPUT):
    logging.getLogger(logger_print_name).info('Welcome to DAP Parameters Converter!')
    logging.getLogger(logger_print_name).debug("the input file name : {}".format(input_file_name))
    logging.getLogger(logger_print_name).debug("the output file name : {}".format(output_file_name))

    with open(input_file_name, 'r') as fp_r:
        lines = fp_r.readlines()
        fp_r.close()

    # default values
    content = 'dap_cpdp.exe --init=mi_process_disable=0,virtual_bass_process_enable=0,mode=0,max_num_objects=16\
    DapPcmInput.wav --out=processed.wav'

    # firstly traverse the file to predict the project and process name according to 'dom' value's length and 'ceon'
    predict_process_project_name(lines)

    # secondly traverse to translate strings and values
    for line in lines:
        line = line.strip('\n')
        keys = (line.split('=')[0])
        values = (line.split('=')[1])
        if keys == 'vcbf':
            continue
        if keys == 'vbon':
            if values == '1':
                content = content.replace('virtual_bass_process_enable=0', 'virtual_bass_process_enable=1')
                continue
            else:
                continue
        # add code for dax3 project
        if keys in DAX3_UNIQUE_PARA:
            if values == 'non-exist':
                continue
            else:
                content += translate(keys, values)
        else:
            if values == 'non-exist':
                continue
            else:
                content += translate(keys, values)

    # generate output
    # fp_w = codecs.open(OUTPUT, 'w', UTF_8)
    # fp_w.write(content)
    # fp_w.close()
    with open(output_file_name, 'w') as fp_w:
        fp_w.write(content)
        fp_w.close()

    logging.getLogger(logger_print_name).info('Done!')
    logging.getLogger(logger_print_name).info('Refer to %s ' % output_file_name)


help_content = (
    "this is used to : \n"
    "\t convert the four cc key words to binary command line . \n"
    "Usage: \n"
    "1. python transfer_para.py \n"
    "2. python transfer_para.py -2 \n"
    "3. python transfer_para.py -i effects_paras.txt \n"
    "4. python transfer_para.py -i effects_paras.txt -2 \n"
    "for item 1 and 2, the default input and output file name : effect_params.txt and dap_cpdp.txt \n"
    "Optional parameters: \n"
    "-i/--input\t: Followed by file name containing four cc key words and \n "
    "\t\t output file name would be suffixed with dap_cpdp_ under input file name \n"
    "-2/--channel\t: if content type is 2 channel Dolby content, add this flag \n"
)


def main(argvs):
    # define the logging basic configuration
    logging.basicConfig(
        level=logging.INFO,
        format=' %(filename)s[%(lineno)d] %(levelname)s ->> %(message)s')
    register_transfer_para_logger_name(logger_print_name, _level=logging.INFO)

    import getopt
    try:
        opts, args = getopt.getopt(argvs, 'hi:2', ['help', 'input', 'channel'])
    except Exception, e:
        print e
        sys.exit(0)
    # if len(opts) == 0:
    #     print("Please specify the input file name containing four cc key words! ")
    #     sys.exit(0)

    _input_file_name = None

    logging.getLogger(logger_print_name).debug(" opts :" + str(opts))
    FLAG_HAS_INPUT_FILE = False
    try:
        for op, value in opts:
            if op in ('-h', '--help'):
                print help_content
                sys.exit(0)
            if op in ('-i', '--input'):
                logging.getLogger(logger_print_name).debug("file name containing four cc key words :" + value)
                _input_file_name = abspath(join('.', value))
                _output_file_name = _input_file_name[:-4] + "_dap_cpdp.txt"
                FLAG_HAS_INPUT_FILE = True
                if _input_file_name is None:
                    logging.getLogger(logger_print_name).error('Please set file name containing four cc key words!')
                    sys.exit(0)
            if op in ('-2', '--channel'):
                logging.getLogger(logger_print_name).info("special handle for 2 channel num content!")
                set_content_channel_num_equal_to_two()

        if FLAG_HAS_INPUT_FILE:
            transfer_para(input_file_name=_input_file_name, output_file_name=_output_file_name)
        else:
            transfer_para()
        # finally set the 2 channel num flag to false
        set_content_channel_num_not_equal_to_two()
    except Exception, e:
        logging.getLogger(logger_print_name).error('Encounter an exception : %s' % e)


if __name__ == "__main__":
    main(sys.argv[1:])
    # try:
    #     sys.exit(main(sys.argv[1:]))
    # except SystemExit:
    #     print ('!!!!! error info' + sys.exc_info()[0])
    #     print ('!!!!! fail DAP Parameters Converter ')
    #     pass

