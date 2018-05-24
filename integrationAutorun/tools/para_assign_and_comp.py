#!/usr/bin/python
"""
Created on May 18st, 2018 (my son has just already one year and seven month)
@author: hshi
"""
import sys
from os.path import abspath, join, exists
from collections import OrderedDict
# import logging
from filter_para_config import *

# define constant string represents the disable status
__disable_status = '0'
# define empty tuple object
__assembled_device_processing_para_list = ()
__assembled_content_processing_para_list = ()
__assembled_ac4_para_list = ()
# define empty dictionary object
__assembled_device_processing_para_dict = OrderedDict()
__assembled_content_processing_para_dict = OrderedDict()
__assembled_ac4_para_dict = OrderedDict()
# define empty assembled qmf process parameter dictionary
__assembled_qmf_process_para_dict = OrderedDict()
# define empty assembled global process parameter dictionary
__assembled_global_process_para_dict = OrderedDict()
# define specified parameter name for content processing in global process
__assembled_specified_content_processing_in_global_process = OrderedDict()
# define empty assembled ac4 decoder parameter dictionary
__assembled_ac4_decoder_para_dict = OrderedDict()


def produce_three_type_para(_key_word_para_dict):
    produce_qmf_process_para(_key_word_para_dict)
    produce_global_process_para(_key_word_para_dict)
    produce_ac4_decoder_para_dict(_key_word_para_dict)
    pass


def assemble_para():
    assemble_content_processing_para()
    assemble_device_processing_para()
    assemble_ac4_para()
    pass


def assemble_device_processing_para():
    global __assembled_device_processing_para_list
    assert isinstance(VIRTUAL_BASS, object)
    __assembled_device_processing_para_list = AUDIO_OPTIMIZER + AUDIO_REGULATOR + BASS_ENHANCER + BASS_EXTRACTION + \
                                              VIRTUAL_BASS + GRAPHIC_EQUALIZER + COMPLEX_EQUALIZER
    # print_a_list(__assembled_device_processing_para_list)
    print ("assemble device processing parameters over!")
    pass


def get_assembled_device_processing_para_list():
    global __assembled_device_processing_para_list
    return __assembled_device_processing_para_list
    pass


def assemble_content_processing_para():
    global __assembled_content_processing_para_list
    _temp_list = [CALIBRATION_BOOST, VOL_MAX_BOOST, SURROUND_DECODER]
    __assembled_content_processing_para_list = DIALOG_ENHANCER + \
                                               VOLUME_LEVELER + VOLUME_MODELER + \
                                               INTELLIGENT_EQUALIZER + \
                                               MEDIA_INTELLIGENT + \
                                               VIRTUALIZER + SPEAKER_VIRTUALIZER
    # print_a_list(__assembled_content_processing_para_list)
    print ("assemble content processing parameters over!")
    return _temp_list


def get_assembled_content_processing_para_list():
    global __assembled_content_processing_para_list
    return __assembled_content_processing_para_list
    pass


def assemble_ac4_para():
    global __assembled_ac4_para_list
    __assembled_ac4_para_list = PARA_LIST_AC4
    # print_a_list(__assembled_content_processing_para_list)
    print ("assemble ac4 parameters over!")
    pass


def get_assembled_ac4_para_list():
    global __assembled_ac4_para_list
    return __assembled_ac4_para_list
    pass


def produce_para(_key_word_para_dict):
    produce_content_processing_para(_key_word_para_dict)
    produce_device_processing_para(_key_word_para_dict)
    pass


def produce_device_processing_para(_key_word_para_dict):
    global __assembled_device_processing_para_dict
    global __assembled_device_processing_para_list
    assert isinstance(_key_word_para_dict, dict)

    for index in range(len(__assembled_device_processing_para_list)):
        __m_key = __assembled_device_processing_para_list[index]
        __m_value = 'non-exist'

        if __m_key in _key_word_para_dict.keys():
            __m_value = _key_word_para_dict[__m_key]

        # when value not exist, would assign 'non-exist' to it as the default value
        __assembled_device_processing_para_dict[__m_key] = __m_value
        pass

    print("produce device processing parameters over!")
    pass


def get_assembled_device_processing_para_dict():
    global __assembled_device_processing_para_dict
    return __assembled_device_processing_para_dict


def produce_content_processing_para(_key_word_para_dict):
    global __assembled_content_processing_para_dict
    global __assembled_content_processing_para_list
    assert isinstance(_key_word_para_dict, dict)

    for index in range(len(__assembled_content_processing_para_list)):
        __m_key = __assembled_content_processing_para_list[index]
        __m_value = 'non-exist'

        if __m_key in _key_word_para_dict.keys():
            __m_value = _key_word_para_dict[__m_key]

        # when value not exist, would assign 'non-exist' to it as the default value
        __assembled_content_processing_para_dict[__m_key] = __m_value
        pass

    print("produce content processing parameters over!")
    pass


def get_assembled_content_processing_para_dict():
    global __assembled_content_processing_para_dict
    return __assembled_content_processing_para_dict


def produce_ac4_para(_key_word_para_dict):
    global __assembled_ac4_para_dict
    global __assembled_ac4_para_list
    assert isinstance(_key_word_para_dict, dict)

    for index in range(len(__assembled_ac4_para_list)):
        __m_key = __assembled_ac4_para_list[index]
        __m_value = 'non-exist'

        if __m_key in _key_word_para_dict.keys():
            __m_value = _key_word_para_dict[__m_key]

        # when value not exist, would assign 'non-exist' to it as the default value
        __assembled_ac4_para_dict[__m_key] = __m_value
        pass

    print("produce ac4 parameters over!")
    pass


def get_assembled_ac4_para_dict():
    global __assembled_ac4_para_dict
    return __assembled_ac4_para_dict


def set_specified_content_processing_para_to_disable(_key_word_para_dict):
    global __assembled_specified_content_processing_in_global_process
    for index in range(len(CONTENT_PROCESSING_PARAM_LIST)):
        __m_key = CONTENT_PROCESSING_PARAM_LIST[index]
        __m_value = __disable_status
        __assembled_specified_content_processing_in_global_process[__m_key] = __m_value

    set_dom_para_to_disable(_key_word_para_dict)
    pass


def set_dom_para_to_disable(_key_word_para_dict):
    global __assembled_specified_content_processing_in_global_process
    assert isinstance(_key_word_para_dict, dict)

    if 'dom' in _key_word_para_dict.keys():
        # reassign value to dom name
        __dom_value = _key_word_para_dict['dom']
        if len(__dom_value) > 0:
            __dom_value = __disable_status + __dom_value[1:]
            __assembled_specified_content_processing_in_global_process['dom'] = __dom_value
            pass
    pass


def produce_global_process_para(_key_word_para_dict):
    global __assembled_global_process_para_dict
    global __assembled_device_processing_para_dict
    global __assembled_device_processing_para_list

    assemble_device_processing_para()

    produce_device_processing_para(_key_word_para_dict)

    for __m_key, __m_value in __assembled_device_processing_para_dict.items():
        __assembled_global_process_para_dict[__m_key] = __m_value

    set_specified_content_processing_para_to_disable(_key_word_para_dict)

    for __m_key, __m_value in __assembled_specified_content_processing_in_global_process.items():
        __assembled_global_process_para_dict[__m_key] = __m_value

    print("produce global process parameters over!")

    pass


def get_assembled_global_process_para_dict():
    global __assembled_global_process_para_dict
    return __assembled_global_process_para_dict


def produce_qmf_process_para(_key_word_para_dict):
    global __assembled_qmf_process_para_dict
    global __assembled_content_processing_para_dict
    global __assembled_content_processing_para_list

    assemble_content_processing_para()

    produce_content_processing_para(_key_word_para_dict)

    for __m_key, __m_value in __assembled_content_processing_para_dict.items():
        __assembled_qmf_process_para_dict[__m_key] = __m_value
    print('produce qmf process parameters over!')
    pass


def get_assembled_qmf_process_para_dict():
    global __assembled_qmf_process_para_dict
    return __assembled_qmf_process_para_dict


def produce_ac4_decoder_para_dict(_key_word_para_dict):
    global __assembled_ac4_decoder_para_dict
    global __assembled_ac4_para_dict
    global __assembled_ac4_para_list

    assemble_ac4_para()

    produce_ac4_para(_key_word_para_dict)

    for __m_key, __m_value in __assembled_ac4_para_dict.items():
        __assembled_ac4_decoder_para_dict[__m_key] = __m_value

    if 'dom' in _key_word_para_dict.keys():
        __assembled_ac4_decoder_para_dict['dom'] = _key_word_para_dict['dom']
    else:
        __assembled_ac4_decoder_para_dict['dom'] = 'non-exist'

    if 'ieon' in _key_word_para_dict.keys():
        __assembled_ac4_decoder_para_dict['ieon'] = _key_word_para_dict['ieon']
    else:
        __assembled_ac4_decoder_para_dict['ieon'] = 'non-exist'

    if 'iebs' in _key_word_para_dict.keys():
        __assembled_ac4_decoder_para_dict['iebs'] = _key_word_para_dict['iebs']
    else:
        __assembled_ac4_decoder_para_dict['iebs'] = 'non-exist'

    print('produce ac4 decoder parameters over!')


def get_assembled_ac4_decoder_para_dict():
    global __assembled_ac4_decoder_para_dict
    return __assembled_ac4_decoder_para_dict


def print_specified_para(_name, _para1_dict, _para2_dict):
    assert isinstance(_name, str)
    assert isinstance(_para1_dict, dict)
    assert isinstance(_para2_dict, dict)

    __former_value = 'null'
    __latter_value = 'null'

    if _name in _para1_dict.keys():
        __former_value = _para1_dict[_name]
    if _name in _para2_dict.keys():
        __latter_value = _para2_dict[_name]

    if len(__former_value) > 4:
        __former_value = __former_value[:4]
    if len(__latter_value) > 4:
        __latter_value = __latter_value[:4]

    print ("==== {} ========= {} ========= {} ==========".format(_name, __former_value, __latter_value))
    pass


def print_para_dictionary(_para1_dict, _para2_dict):
    assert isinstance(_para1_dict, dict)
    assert isinstance(_para2_dict, dict)
    # a list contains all key strings
    __temp_name_list = list()
    for __key_1 in _para1_dict.keys():
        __temp_name_list.append(__key_1)
    for __key_2 in _para2_dict.keys():
        if __key_2 not in __temp_name_list:
            __temp_name_list.append(__key_2)

    if len(__temp_name_list) > 0:
        print "======================================================"
        print "==== name ========= value1 ========= value2 =========="

        for __name in __temp_name_list:
            print_specified_para(__name, _para1_dict, _para2_dict)

        print "======================================================"
    pass


def assemble_comparison_one_para(_name, _para1_dict, _para2_dict):
    assert isinstance(_name, str)
    assert isinstance(_para1_dict, dict)
    assert isinstance(_para2_dict, dict)

    __former_value = 'null'
    __latter_value = 'null'

    if _name in _para1_dict.keys():
        __former_value = _para1_dict[_name]
    if _name in _para2_dict.keys():
        __latter_value = _para2_dict[_name]

    if (__former_value == 'null') and (__latter_value == 'null'):
        return None
    __return_list = [_name, __former_value, __latter_value]
    return __return_list


def compare_one_para(_name, _para1_dict, _para2_dict):
    assert isinstance(_name, str)
    assert isinstance(_para1_dict, dict)
    assert isinstance(_para2_dict, dict)

    _comparison_result_list = assemble_comparison_one_para(_name, _para1_dict, _para2_dict)
    if _comparison_result_list is None:
        # print ("========== {} not exist in both dict ===========".format(_name))
        return None
    else:
        if len(_comparison_result_list) == 3:
            if _comparison_result_list[1] == _comparison_result_list[2]:
                return True
            else:
                if len(tuple(_comparison_result_list[1])) < 4:
                    _temp_1 = _comparison_result_list[1] + '   '
                else:
                    _temp_1 = _comparison_result_list[1][:4]

                if len(tuple(_comparison_result_list[2])) < 4:
                    _temp_2 = _comparison_result_list[2] + '   '
                else:
                    _temp_2 = _comparison_result_list[2][:4]

                # print ("==== {} ========= {} ========= {} ==========".format(
                #     _comparison_result_list[0], _temp_1, _temp_2))
                return False


def compare_para_dictionary(_para1_dict, _para2_dict):
    assert isinstance(_para1_dict, dict)
    assert isinstance(_para2_dict, dict)

    result = True
    # a list contains all key strings
    __temp_name_list = list()
    for __key_1 in _para1_dict.keys():
        __temp_name_list.append(__key_1)
    for __key_2 in _para2_dict.keys():
        if __key_2 not in __temp_name_list:
            __temp_name_list.append(__key_2)

    if len(__temp_name_list) > 0:
        # print "========== list all diff values ===================="
        # print "==== name ========= value1 ========= value2 =========="

        for __name in __temp_name_list:
            __comparison_result = compare_one_para(__name, _para1_dict, _para2_dict)
            if __comparison_result is False:
                result = False
        # print "======================================================"
    return result


def get_key_value_from_file(_file_name_abs_path):
    _temp_dict = dict()
    if exists(_file_name_abs_path):
        # Read data from file
        try:
            with open(_file_name_abs_path, 'r') as fp_r:
                lines = fp_r.readlines()
                fp_r.close()
            if lines is not None:
                for line in lines:
                    line = line.strip('\n')
                    line = line.strip('\b')
                    __key = line.split('=')[0]
                    __value = line.split('=')[1]
                    _temp_dict[__key] = __value
        except EnvironmentError, e:
            print ("!!!!!failed to open file :" + e.message)
    else:
        print("file did not exist: {}".format(_file_name_abs_path))

    # print_a_dictionary(_temp_dict)

    return _temp_dict


def save_key_value_to_file(_input_dictionary, _file_name_abs_path, _name_suffix):
    assert isinstance(_file_name_abs_path, str)
    assert isinstance(_input_dictionary, dict)

    if not _file_name_abs_path:
        print("!!!!!file name argument is empty !")
    else:
        __temp_output_file_name = _file_name_abs_path[:-4] + _name_suffix
        try:
            with open(__temp_output_file_name, 'w') as fp_w:
                for key, value in _input_dictionary.items():
                    content = key + "=" + value + '\n'
                    # print("write content to file :" + content)
                    fp_w.write(content)
            fp_w.close()
        except EnvironmentError, e:
            print ("!!!!!failed to write value to file" + e.message)


def print_a_dictionary(_input_dictionary):
    assert isinstance(_input_dictionary, dict)

    print("============ display all value in dictionary ===============")
    for key, value in _input_dictionary.items():
        print(key + " = " + value)


def print_a_list(_input_list_or_tuple):

    print("============ display all value in list or tuple ===============")
    print("============ list or tuple length : " + str(len(_input_list_or_tuple)))
    for index in range(len(_input_list_or_tuple)):
        print(str(index) + " = " + _input_list_or_tuple[index])


help_content = (
    "this is used to : \n"
    "\t assign four cc key word to global and qmf process . \n"
    "Usage: \n"
    "1. python para_assign_and_comp.py -i effects_paras.txt \n"
    "   the default output file name : *_effect_params_assembled.txt and *_ARenderer_params_assembled.txt \n"
    "Mandatory parameters: \n"
    "-i/--input\t: Followed by file name containing four cc key words \n "
)


def main(argvs):
    # define the logging basic configuration
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format=' %(filename)s[%(lineno)d] %(levelname)s ->> %(message)s')
    # register_transfer_para_logger_name(logger_print_name, _level=logging.INFO)

    import getopt
    try:
        opts, args = getopt.getopt(argvs, 'hi:', ['help', 'input'])
    except Exception, e:
        print e.message
        sys.exit(0)

    if len(opts) == 0:
        print("Please specify the input file name containing four cc key words! ")
        sys.exit(0)

    # _input_file_name = None
    print (" opts :" + str(opts))

    try:
        for op, value in opts:
            if op in ('-h', '--help'):
                print help_content
                sys.exit(0)
            if op in ('-i', '--input'):
                print ("file name parsed from xml file : " + value)
                _input_file_name = abspath(join('.', value))
                _four_cc_key_word_dict = get_key_value_from_file(_input_file_name)
                # print_a_dictionary(_four_cc_key_word_dict)
                # print (bool(_four_cc_key_word_dict))
                if bool(_four_cc_key_word_dict):
                    produce_global_process_para(_four_cc_key_word_dict)
                    produce_qmf_process_para(_four_cc_key_word_dict)
                    produce_ac4_decoder_para_dict(_four_cc_key_word_dict)

                    _global_process_key_value = get_assembled_global_process_para_dict()
                    _qmf_process_key_value = get_assembled_qmf_process_para_dict()
                    _ac4_decoder_key_value = get_assembled_ac4_decoder_para_dict()
                    # print_a_dictionary(_qmf_process_key_value)

                    save_key_value_to_file(_global_process_key_value, _input_file_name, '_effect_params_assembled.txt')
                    save_key_value_to_file(_qmf_process_key_value, _input_file_name, '_ARenderer_params_assembled.txt')
                    save_key_value_to_file(_ac4_decoder_key_value, _input_file_name, '_ac4_params_assembled.txt')

                    result = compare_para_dictionary(_global_process_key_value, _qmf_process_key_value)
                    print ("compare global and qmf result : " + str(result))

                    result = compare_para_dictionary(_global_process_key_value, _global_process_key_value)
                    print ("compare global and global result : " + str(result))

                    result = compare_para_dictionary(_global_process_key_value, _ac4_decoder_key_value)
                    print ("compare global and ac4 result : " + str(result))
                else:
                    print ("specified input file did not contains four cc key words!")
    except Exception, e:
        print ('Encounter an exception : %s' % e)


if __name__ == "__main__":
    main(sys.argv[1:])
    # try:
    #     sys.exit(main(sys.argv[1:]))
    # except SystemExit:
    #     print ('!!!!! error info' + sys.exc_info()[0])
    #     print ('!!!!! fail DAP Parameters Converter ')
    #     pass
