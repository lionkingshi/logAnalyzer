import pytest
from tools.common import *
from tools.logger import *

# register the logging configuration
endpoint_type_in_module = log_file_name_for_diff_endpoint[3]
logging_file_name = abspath(join('.', 'log', endpoint_type_in_module, __name__))
logger = Logger(log_name=logging_file_name + '.log', log_level='1',
                logger_name=endpoint_type_in_module).get_log

# define adb logcat output redirected into default file if not specified
log_file_name = abspath(join('.', 'log', 'log.txt'))


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         be_on_test_data)
def test_log_bass_on_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-82
    Test Condition  : make sure device endpoint is usb headphone

    Test Description: Verify VB & BE are on when Bass enhance button is on
    Test Check Point: vbon = 0 and beon = 1
    """

    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_type_in_module)
    if content_type:
        logger.info("===== Verify VB & BE are on when playing Dolby content start using %s "
                    % endpoint_type_in_module)
    else:
        logger.info("===== Verify VB & BE are on when playing non Dolby content start using %s "
                    % endpoint_type_in_module)

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value)

    # step 3 : capture adb log to a file
    temp_log_name = logFileNameFormat.format(functionName=test_log_bass_on_verify.__name__,
                                             endpoint_type=endpoint_type_in_module,
                                             log_type=content_name.replace('.', '_'))
    be_log_file_name = abspath(join('.', 'log', endpoint_type_in_module, temp_log_name))
    generate_log_file(be_log_file_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    parse_dap_feature_value_from_log_file(be_log_file_name)

    verify_no_double_processing_dap_parameter(content_type)

    base_enhancer_value = get_feature_value_from_global_process('beon')
    virtual_base_value = get_feature_value_from_global_process('vbon')
    assert base_enhancer_value == '1', "bass enhance expected value : 1 but {}".format(base_enhancer_value)
    assert virtual_base_value == '0', "virtual bass expected value : 1 but {}".format(virtual_base_value)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         be_off_test_data)
def test_log_bass_off_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-83
    Test Condition  : make sure device endpoint is usb headphone

    Test Description: Verify VB & BE are off when Bass enhance button is off
    Test Check Point: vbon = 0 and beon = 0
    """

    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_type_in_module)
    if content_type:
        logger.info("===== Verify VB & BE are on when playing Dolby content start using %s "
                    % endpoint_type_in_module)
    else:
        logger.info("===== Verify VB & BE are on when playing non Dolby content start using %s "
                    % endpoint_type_in_module)

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value)

    # step 3 : capture adb log to a file
    temp_log_name = logFileNameFormat.format(functionName=test_log_bass_off_verify.__name__,
                                             endpoint_type=endpoint_type_in_module,
                                             log_type=content_name.replace('.', '_'))
    be_log_file_name = abspath(join('.', 'log', endpoint_type_in_module, temp_log_name))
    generate_log_file(be_log_file_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    parse_dap_feature_value_from_log_file(be_log_file_name)

    verify_no_double_processing_dap_parameter(content_type)

    base_enhancer_value = get_feature_value_from_global_process('beon')
    virtual_base_value = get_feature_value_from_global_process('vbon')
    assert base_enhancer_value == '0', "bass enhance expected value : 0 but {}".format(base_enhancer_value)
    assert virtual_base_value == '0', "virtual bass expected value : 0 but {}".format(virtual_base_value)
