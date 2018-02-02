import inspect
import os
import time

import pytest
from tools.common import *
from tools.logger import *

from tools.filter_para import LogComparison

# register the logging configuration
logging_file_name = abspath(join('.', 'log', log_file_name_for_diff_endpoint[0], __name__))
logger = Logger(log_name=logging_file_name+'.log', log_level='1', logger_name=log_file_name_for_diff_endpoint[0]).get_log

# define adb logcat redirected into which file
log_file_name = abspath(join('.', 'log', 'log.txt'))


# define test data
be_stereo_speaker_test_data_dolby_content = [
    ('stereo_dd_25fps_channel_id.m4a', dap_status_on, dap_profile_custom,
     dap_feature_type_be, dap_feature_value_be_on),
]

be_stereo_speaker_test_date_non_dolby_content = [
    ('stereo_channel_id.wav', dap_status_on, dap_profile_custom,
     dap_feature_type_be, dap_feature_value_be_on)
]


def feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str=''):
    # register logger name to record all command to logger file except session setup() function
    register_logger_name(log_file_name_for_diff_endpoint[0])

    execute(adb_broadcast_intent + intent_play_content + content_name)
    time.sleep(1)
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status)
    time.sleep(1)
    execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile)
    time.sleep(1)
    if dap_feature_type == dap_feature_type_gebg:
        execute(adb_broadcast_intent + intent_change_dap_gebg_feature.format(dap_feature_type, dap_feature_value))
    elif len(dap_feature_type) == 4:
        execute(adb_broadcast_intent + intent_change_dap_low_level_feature.format(dap_feature_type, dap_feature_value))
    else:
        execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(dap_feature_type, dap_feature_value))
    time.sleep(1)
    execute(adb_broadcast_intent + "--es step record_log ")
    time.sleep(1)
    current_method_name = inspect.stack()[1][3]
    current_method_name1 = inspect.stack()[0][3]
    current_method_name2 = inspect.stack()[2][3]
    print ("current test method name : %s " % current_method_name)
    print ("current test method name1 : %s " % current_method_name1)
    print ("current test method name2 : %s " % current_method_name2)
    global log_file_name
    log_file_name = logFileLocation + log_file_name_for_diff_endpoint[0] + '/' + current_method_name + '_' + \
                    dap_feature_type + '_' + dap_feature_value + '_' + content_name.replace('.', '_')
    print log_file_name
    print os.getcwd()
    print __file__
    time.sleep(SLEEP_TIME_BEFORE_RECORD_LOG)
    execute(adb_record_log + log_file_name + '.txt')


@pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         be_stereo_speaker_test_data_dolby_content)
def test_log_tc78_bass(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str=''):
    """
    Test Description: Verify VB & BE are on when Bass enhance button is on
    """
    logger.info("===== Verify VB & BE are on when playing Dolby content start ")

    feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value)

    # first specified the log file we want to filter effect parameters
    log_file_abs_path = os.path.abspath(log_file_name + '.txt')
    logger.info("specified log file : %s" % log_file_abs_path)
    # specified the output file name , and default it will be saved at current location
    effect_paras_output_file_abs_path = abspath(log_file_name + "_effect_params_from_log.txt")
    arendered_param_output_file_abs_path = abspath(log_file_name + "_arendered_params_from_log.txt")
    dap_cp_dp_param_output_file_abs_path = abspath(log_file_name + "_dap_cp_dp_from_log.txt")
    logger.debug("effect para in global process saved at : %s" % effect_paras_output_file_abs_path)
    logger.debug("effect para in qmf process saved at : %s" % arendered_param_output_file_abs_path)
    logger.debug("dap cp and dp para saved at : %s" % dap_cp_dp_param_output_file_abs_path)

    em1 = LogComparison(log_file_name_for_diff_endpoint[0])
    em1.filter_para_from_log(log_file_abs_path, effect_paras_output_file_abs_path,
                             arendered_param_output_file_abs_path, dap_cp_dp_param_output_file_abs_path)

    if em1.verify_no_double_processing_effect_for_dolby_content():
        assert True
    else:
        assert False

    base_enhancer_value = em1.get_parameter_value_in_global_process('beon')
    virtual_base_value = em1.get_parameter_value_in_global_process('vbon')

    if base_enhancer_value == '1':
        logger.info("get bass enhancer value is 1 .")
        pass
    else:
        assert 0
        pass
    if virtual_base_value == '1':
        logger.info("get virtual bass value is 1 .")
        pass
    else:
        assert 0
        pass


@pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         be_stereo_speaker_test_date_non_dolby_content)
def test_log_tc79_bass(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Description: Verify VB & BE are on when Bass enhance button is on
    """
    logger.info("===== Verify VB & BE are on when playing non Dolby content start ")

    feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value)

    # first specified the log file we want to filter effect parameters
    log_file_abs_path = os.path.abspath(log_file_name + '.txt')
    logger.info("specified log file : %s" % log_file_abs_path)
    # specified the output file name , and default it will be saved at current location
    effect_paras_output_file_abs_path = abspath(log_file_name + "_effect_params_from_log.txt")
    arendered_param_output_file_abs_path = abspath(log_file_name + "_arendered_params_from_log.txt")
    dap_cp_dp_param_output_file_abs_path = abspath(log_file_name + "_dap_cp_dp_from_log.txt")
    logger.debug("effect para in global process saved at : %s" % effect_paras_output_file_abs_path)
    logger.debug("effect para in qmf process saved at : %s" % arendered_param_output_file_abs_path)
    logger.debug("dap cp and dp para saved at : %s" % dap_cp_dp_param_output_file_abs_path)

    em1 = LogComparison(log_file_name_for_diff_endpoint[0])
    em1.filter_para_from_log(log_file_abs_path, effect_paras_output_file_abs_path,
                             arendered_param_output_file_abs_path, dap_cp_dp_param_output_file_abs_path)
    if em1.verify_no_double_processing_effect_for_non_dolby_content():
        assert True
    else:
        assert False

    base_enhancer_value = em1.get_parameter_value_in_global_process('beon')
    virtual_base_value = em1.get_parameter_value_in_global_process('vbon')

    if base_enhancer_value == '1':
        logger.info("get bass enhancer value is 1 .")
        pass
    else:
        assert 0
        pass
    if virtual_base_value == '1':
        logger.info("get virtual bass value is 1 .")
        pass
    else:
        assert 0
        pass