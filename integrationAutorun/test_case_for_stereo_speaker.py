import pytest
from commonTestProcedure import *

# register the logging configuration
endpoint_type_in_module = log_file_name_for_diff_endpoint[1]
logging_file_name = abspath(join('.', 'log', endpoint_type_in_module, __name__))
logger = Logger(log_name=logging_file_name + '.log', log_level='1',
                logger_name=endpoint_type_in_module).get_log

# define adb logcat output redirected into default file if not specified
log_file_name = abspath(join('.', 'log', 'log.txt'))


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         be_on_test_data)
def test_log_bass_on_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-78

    Test Condition  : make sure device endpoint is stereo speaker

    Test Description: Verify VB & BE are on when Bass enhance button is on

    Test Check Point: vbon = 1 and beon = 1
    """
    caller_name = test_log_bass_on_verify.__name__
    be_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type, dap_feature_value)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         be_off_test_data)
def test_log_bass_off_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-79

    Test Condition  : make sure device endpoint is stereo speaker

    Test Description: Verify VB & BE are off when Bass enhance button is off

    Test Check Point: vbon = 0 and beon = 0
    """

    caller_name = test_log_bass_off_verify.__name__
    be_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type, dap_feature_value)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_off_test_data)
def test_log_mi_off_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-53

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer is off no matter what is playing content using any endpoint

    Test Check Point:   msce, mdee, miee, mdle, mave : all equal to 0
    """
    caller_name = test_log_mi_off_verify.__name__
    mi_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type, dap_status, dap_profile)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_2_channel_dolby_test_data)
def test_log_mi_on_2ch_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-54

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   for 2 channel dolby content , msce, mdee, miee, mdle, mave values are equal to 1
                        meanwhile volume level can't be turn off ig dvle = 1 in qmf process
    """
    caller_name = test_log_mi_on_2ch_verify.__name__
    mi_on_dolby_content_test_procedure(caller_name, endpoint_type_in_module,
                                       content_name, content_type, dap_status, dap_profile)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_multi_channel_dolby_test_data)
def test_log_mi_on_multi_channel_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-55

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   for multiple channel dolby content ,
                              msce, mdee, miee, mdle, values are equal to 1
                              mave = 0 (Jie told me it should be 1)
                        meanwhile volume level can't be turn off ig dvle = 1 in qmf process
    """
    caller_name = test_log_mi_on_multi_channel_verify.__name__
    mi_on_dolby_content_test_procedure(caller_name, endpoint_type_in_module,
                                       content_name, content_type, dap_status, dap_profile)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_non_dolby_test_data)
def test_log_mi_on_non_dolby_content(content_name, content_type,
                                     dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-56

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   for non dolby content , msce, mdee, miee, mdle, mave values are equal to 1
                        meanwhile volume level can be turn off ig dvle = 0 in global process
    """
    caller_name = test_log_mi_on_non_dolby_content.__name__
    mi_on_dolby_content_test_procedure(caller_name, endpoint_type_in_module,
                                       content_name, content_type, dap_status, dap_profile)