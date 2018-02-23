import pytest
from commonTestProcedure import *

# register the logging configuration
endpoint_type_in_module = AUDIO_DEVICE_OUT_STEREO_SPEAKER
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

    Test Check Point: vbon = 1 and beon = 1 for speaker
                      vbon = 0 and beon = 1 for other endpoint except speaker
    """
    caller_name = test_log_bass_on_verify.__name__
    be_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type, dap_feature_value)

    be_and_vb_expected_dictionary = {'beon': '1', 'vbon': '1'}
    assert_dap_be_related_feature_result(content_type, be_and_vb_expected_dictionary)


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

    be_and_vb_expected_dictionary = {'beon': '0', 'vbon': '0'}
    assert_dap_be_related_feature_result(content_type, be_and_vb_expected_dictionary)


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

    mi_off_expected_dictionary = {'msce': '0', 'mdee': '0', 'miee': '0', 'mdle': '0', 'mave': '0'}
    ref_lvl_expected_dictionary = {'dvle': '1', 'dvla': '5', 'dvli': '-496', 'dvlo': '-176', 'vmb': '144'}
    if dap_profile in (dap_profile_dynamic, dap_profile_movie) :
        ref_lvl_expected_dictionary['dvla'] = '7'
    elif dap_profile in (dap_profile_game, dap_profile_music):
        ref_lvl_expected_dictionary['dvla'] = '0'
    elif dap_profile == dap_profile_music:
        ref_lvl_expected_dictionary['dvla'] = '4'
    elif dap_profile == dap_profile_custom:
        ref_lvl_expected_dictionary['dvla'] = '5'

    assert_dap_mi_and_vl_related_feature_result(content_type, mi_off_expected_dictionary, ref_lvl_expected_dictionary)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_2_channel_dolby_test_data)
def test_log_mi_on_2ch_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-54, 68

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   for 2 channel dolby content , msce, mdee, miee, mdle, mave values are equal to 1
                        meanwhile volume level can't be turn off ig dvle = 1 in qmf process
    """
    caller_name = test_log_mi_on_2ch_verify.__name__
    mi_on_test_procedure(caller_name, endpoint_type_in_module,
                         content_name, content_type, dap_status, dap_profile)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_multi_channel_dolby_test_data)
def test_log_mi_on_multi_channel_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type,
                                        dap_feature_value):
    """
    Test Case ID    :   TC-55, 68

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   for multiple channel dolby content ,
                              msce, mdee, miee, mdle, values are equal to 1
                              mave = 0 (Jie told me it should be 1)
                        meanwhile volume level can't be turn off ig dvle = 1 in qmf process
    """
    caller_name = test_log_mi_on_multi_channel_verify.__name__
    mi_on_test_procedure(caller_name, endpoint_type_in_module,
                         content_name, content_type, dap_status, dap_profile)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_non_dolby_test_data)
def test_log_mi_on_non_dolby_content_verify(content_name, content_type,
                                            dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-56, 68

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   for non dolby content , msce, mdee, miee, mdle, mave values are equal to 1
                        meanwhile volume level can be turn off ig dvle = 0 in global process
    """
    caller_name = test_log_mi_on_non_dolby_content_verify.__name__
    mi_on_test_procedure(caller_name, endpoint_type_in_module,
                         content_name, content_type, dap_status, dap_profile)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_vsv_off_test_data)
def test_log_up_mix_sv_off_verify(content_name, content_type,
                                  dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   non-Dolby and Dolby content can not be up mixed to 5.1.2 when sv off

    Test Check Point:   dom : 0
    """
    caller_name = test_log_up_mix_sv_off_verify.__name__
    up_mix_and_sv_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)
    dom = {'dom': '0'}
    # output channel count is 2 with order L, R
    dap_output_mode = '1'
    dap_mix_matrix = 'null'
    ddp_down_mix = '0'
    assert_up_mix_related_feature_result(content_type, dap_output_mode, dap_mix_matrix, dom, ddp_down_mix)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_vsv_on_test_data)
def test_log_up_mix_sv_on_verify(content_name, content_type,
                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   content should be up mixed to 5.1.2 when sv on
                           except 2 channel dolby content up mixed to 5.1

    Test Check Point:   dom = 0 for blue tooth and mono speaker
                              2 for headphone
                              [1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384]
                                   for stereo speaker
    """
    caller_name = test_log_up_mix_sv_on_verify.__name__
    up_mix_and_sv_on_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)
    # this means speaker virtualizer with height and input will be up mixed to 5.1.2
    # not matter the content type
    dom = {'dom': '1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384'}
    # output channel count is 8 with order L, R, C, LFE, Ls, Rs, Ltm, Rtm
    dap_output_mode = '11'
    dap_mix_matrix = 'custom'
    ddp_down_mix = '0'
    assert_up_mix_related_feature_result(content_type, dap_output_mode, dap_mix_matrix, dom, ddp_down_mix)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         dap_off_test_data)
def test_log_on_log_print_when_dap_off_verify(content_name, content_type,
                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   no log print when dap off

    Test Check Point:   no dap parameter relating log print in stand output
    """
    caller_name = test_log_on_log_print_when_dap_off_verify.__name__
    no_log_print_when_dap_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         decoder_joc_force_down_mix_test_data)
def test_log_decoder_joc_force_down_mix_verify(content_name, content_type,
                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-4021

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   always decode object for headphone, usb, stereo speaker endpoint

    Test Check Point:   in udc decoder , its value should be 0 for stereo speaker
    """
    caller_name = test_log_decoder_joc_force_down_mix_verify.__name__
    up_mix_and_sv_on_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)

    decoder_down_mix = '1'
    assert_decoding_joc_down_mix_related_feature_result(content_type, decoder_down_mix)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         reference_level_test_data)
def test_log_reference_level_when_dap_off_verify(content_name, content_type,
                                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    caller_name = test_log_reference_level_when_dap_off_verify.__name__
    reference_level_when_dap_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)

    ref_lvl_expected_dictionary = {'dvle': '1', 'dvla': '5', 'dvli': '-496', 'dvlo': '-224', 'vmb': '144'}
    if dap_profile in (dap_profile_dynamic, dap_profile_movie):
        ref_lvl_expected_dictionary['dvla'] = '7'
    elif dap_profile in (dap_profile_game, dap_profile_music):
        ref_lvl_expected_dictionary['dvla'] = '0'
    elif dap_profile == dap_profile_music:
        ref_lvl_expected_dictionary['dvla'] = '4'
    elif dap_profile == dap_profile_custom:
        ref_lvl_expected_dictionary['dvla'] = '5'

    assert_dap_reference_level_related_feature_result(content_type, ref_lvl_expected_dictionary)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         reference_level_test_data)
def test_log_reference_level_when_dap_on_verify(content_name, content_type,
                                                dap_status, dap_profile, dap_feature_type, dap_feature_value):
    caller_name = test_log_reference_level_when_dap_on_verify.__name__
    reference_level_when_dap_on_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)

    # for diff profile , the dvla value is diff
    # here dvla = 5 when custom profile is selected
    ref_lvl_expected_dictionary = {'dvle': '1', 'dvla': '5', 'dvli': '-496', 'dvlo': '-176', 'vmb': '144'}
    if dap_profile in (dap_profile_dynamic, dap_profile_movie):
        ref_lvl_expected_dictionary['dvla'] = '7'
    elif dap_profile in (dap_profile_game, dap_profile_music):
        ref_lvl_expected_dictionary['dvla'] = '0'
    elif dap_profile == dap_profile_music:
        ref_lvl_expected_dictionary['dvla'] = '4'
    elif dap_profile == dap_profile_custom:
        ref_lvl_expected_dictionary['dvla'] = '5'

    assert_dap_reference_level_related_feature_result(content_type, ref_lvl_expected_dictionary)
