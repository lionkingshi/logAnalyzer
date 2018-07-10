import pytest
from dax31CommonTestProcedure import *
from dax31ConstantTestData import *

# register the logging configuration
endpoint_type_in_module = AUDIO_DEVICE_OUT_STEREO_SPEAKER
_current_directory = dirname(realpath(__file__))
logging_file_name = abspath(join(_current_directory, 'log', endpoint_type_in_module, __name__))
logger = Logger(log_name=logging_file_name + '.log', log_level='1',
                logger_name=endpoint_type_in_module).get_log

# define adb logcat output redirected into default file if not specified
log_file_name = abspath(join('.', 'log', 'log.txt'))


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         dynamic_profile_default_value_test_data)
def test_log_dynamic_profile_default_value_verify_landscape(content_name, content_type,
                                                            dap_status, dap_profile,
                                                            dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Description: Verify default parameter's values in four profile parsed from log are same as ones parsed from xml
                      for internal speaker port, dax-default.xml provide at least two important tuning device name :
                      speaker_landscape and speaker_portrait

    Test Check Point: DAP parameter's value in dynamic profile is expected as xml parsing ones
                      And it is effective for speaker landscape mode
    """
    caller_name = test_log_dynamic_profile_default_value_verify_landscape.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_landscape
    )

    assert_specified_profile_default_values_result(
        profile_name[0],
        speaker_tuning_name[dap_tuning_device_name_speaker_landscape],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         dynamic_profile_default_value_test_data)
def test_log_dynamic_profile_default_value_verify_portrait(content_name, content_type,
                                                            dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Description:
        Verify DAP default parameter's values in four profile parsed from log are same as ones parsed from xml
        for internal speaker port, dax-default.xml provide at least two important tuning device name :
        speaker_landscape and speaker_portrait

    Test Check Point: DAP parameter's value in dynamic profile is expected as xml parsing ones
                      And it is only effective for speaker portrait mode
    """
    caller_name = test_log_dynamic_profile_default_value_verify_portrait.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_portrait
    )

    assert_specified_profile_default_values_result(
        profile_name[0],
        speaker_tuning_name[dap_tuning_device_name_speaker_portrait],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         movie_profile_default_value_test_data)
def test_log_movie_profile_default_value_verify_landscape(content_name, content_type,
                                                          dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in movie profile is expected as xml parsing ones
                      And it is only effective for speaker landscape mode
    """
    caller_name = test_log_movie_profile_default_value_verify_landscape.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_landscape
    )

    assert_specified_profile_default_values_result(
        profile_name[1],
        speaker_tuning_name[dap_tuning_device_name_speaker_landscape],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         movie_profile_default_value_test_data)
def test_log_movie_profile_default_value_verify_portrait(content_name, content_type,
                                                          dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in movie profile is expected as xml parsing ones
                      And it is only effective for speaker portrait mode
    """
    caller_name = test_log_movie_profile_default_value_verify_portrait.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_portrait
    )

    assert_specified_profile_default_values_result(
        profile_name[1],
        speaker_tuning_name[dap_tuning_device_name_speaker_portrait],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         music_profile_default_value_test_data)
def test_log_music_profile_default_value_verify_landscape(content_name, content_type,
                                                          dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in music profile is expected as xml parsing ones
                      And it is only effective for speaker landscape mode
    """
    caller_name = test_log_music_profile_default_value_verify_landscape.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_landscape
    )

    assert_specified_profile_default_values_result(
        profile_name[2],
        speaker_tuning_name[dap_tuning_device_name_speaker_landscape],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         music_profile_default_value_test_data)
def test_log_music_profile_default_value_verify_portrait(content_name, content_type,
                                                          dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in music profile is expected as xml parsing ones
                      And it is only effective for speaker portrait mode
    """
    caller_name = test_log_music_profile_default_value_verify_portrait.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_portrait
    )

    assert_specified_profile_default_values_result(
        profile_name[2],
        speaker_tuning_name[dap_tuning_device_name_speaker_portrait],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         custom_profile_default_value_test_data)
def test_log_custom_profile_default_value_verify_landscape(content_name, content_type,
                                                           dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in Custom profile is expected as xml parsing ones
                      And it is only effective for speaker landscape mode
    """
    caller_name = test_log_custom_profile_default_value_verify_landscape.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_landscape
    )

    assert_specified_profile_default_values_result(
        profile_name[3],
        speaker_tuning_name[dap_tuning_device_name_speaker_landscape],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         custom_profile_default_value_test_data)
def test_log_custom_profile_default_value_verify_portrait(content_name, content_type,
                                                           dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in Custom profile is expected as xml parsing ones
                      And it is only effective for speaker portrait mode
    """
    caller_name = test_log_custom_profile_default_value_verify_portrait.__name__
    specified_profile_default_value_test_procedure_dax3(
        caller_name,
        endpoint_type_in_module,
        content_name,
        content_type,
        dap_profile,
        _tuning_port=dap_tuning_port_internal_speaker,
        _tuning_device_name=dap_tuning_device_name_speaker_portrait
    )

    assert_specified_profile_default_values_result(
        profile_name[3],
        speaker_tuning_name[dap_tuning_device_name_speaker_portrait],
        endpoint_type_in_module,
        content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         custom_profile_default_value_test_data)
def test_log_new_added_profiles_default_value_verify_landscape(
        content_name,
        content_type,
        dap_status,
        dap_profile,
        dap_feature_type,
        dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in new added profile is expected as xml parsing ones
                      And it is only effective for speaker landscape mode
    """
    caller_name = test_log_new_added_profiles_default_value_verify_landscape.__name__

    new_added_profile_num = 1
    total_profile_number = (new_added_profile_num + 4)
    add_new_profiles_in_xml_file_and_then_push_to_device(new_added_profile_num)

    # iterate all new added profiles to verify the default value is expected
    for index in xrange(0, total_profile_number, 1):
        specified_profile_default_value_test_procedure_dax3(
            caller_name,
            endpoint_type_in_module,
            content_name,
            content_type,
            str(index),
            _tuning_port=dap_tuning_port_internal_speaker,
            _tuning_device_name=dap_tuning_device_name_speaker_landscape
        )

        assert_specified_profile_default_values_result(
            index,
            speaker_tuning_name[dap_tuning_device_name_speaker_landscape],
            endpoint_type_in_module,
            content_type)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         custom_profile_default_value_test_data)
def test_log_new_added_profiles_default_value_verify_portrait(
        content_name,
        content_type,
        dap_status,
        dap_profile,
        dap_feature_type,
        dap_feature_value):
    """
    Test Case ID    : TC-new

    Test Check Point: DAP parameter's value in new added profile is expected as xml parsing ones
                      And it is only effective for speaker portrait mode
    """
    caller_name = test_log_new_added_profiles_default_value_verify_portrait.__name__

    new_added_profile_num = 12
    total_profile_number = (new_added_profile_num + 4)
    add_new_profiles_in_xml_file_and_then_push_to_device(new_added_profile_num)

    # iterate all new added profiles to verify the default value is expected
    for index in xrange(0, total_profile_number, 1):
        specified_profile_default_value_test_procedure_dax3(
            caller_name,
            endpoint_type_in_module,
            content_name,
            content_type,
            str(index),
            _tuning_port=dap_tuning_port_internal_speaker,
            _tuning_device_name=dap_tuning_device_name_speaker_portrait
        )

        assert_specified_profile_default_values_result(
            index,
            speaker_tuning_name[dap_tuning_device_name_speaker_portrait],
            endpoint_type_in_module,
            content_type)


@pytest.mark.bass
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
    be_test_procedure_dax3(caller_name, endpoint_type_in_module, content_name, content_type, dap_feature_value)

    be_and_vb_expected_dictionary = {'beon': '1', 'vbon': '1', 'vbm': "3"}
    assert_dap_be_related_feature_result(endpoint_type_in_module, content_type, be_and_vb_expected_dictionary)


@pytest.mark.bass
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
    be_test_procedure_dax3(caller_name, endpoint_type_in_module, content_name, content_type, dap_feature_value)

    be_and_vb_expected_dictionary = {'beon': '0', 'vbon': '1', 'vbm': "0"}
    assert_dap_be_related_feature_result(endpoint_type_in_module, content_type, be_and_vb_expected_dictionary)


@pytest.mark.mi
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
    assert_dap_mi_and_vl_related_feature_result(endpoint_type_in_module, content_type, mi_off_expected_dictionary)


@pytest.mark.mi
@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         mi_on_test_data)
def test_log_mi_on_verify(content_name, content_type, dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-57, 58, 59, 68

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   verify MI steer and MI controlling features' status are ok.

    Test Check Point:   msce, mdee, miee, mdle, mave values are equal to 1
    """
    caller_name = test_log_mi_on_verify.__name__
    mi_on_test_procedure_another(caller_name, endpoint_type_in_module, content_name, content_type, dap_status,
                                 dap_profile, PROJECT_ID_DAX3)

    mi_on_expected_dictionary = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}
    assert_dap_mi_and_vl_related_feature_result(endpoint_type_in_module, content_type, mi_on_expected_dictionary)


@pytest.mark.sv
@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_vsv_off_test_data)
def test_log_up_mix_sv_off_verify_landscape(content_name, content_type,
                                            dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   non-Dolby and Dolby content can not be up mixed to 5.1.2 when sv off

    Test Check Point:
    """
    # tuning device name : speaker landscape
    caller_name = test_log_up_mix_sv_off_verify_landscape.__name__
    up_mix_and_sv_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type,
                                     spk_tuning_device_name_id=dap_tuning_device_name_speaker_landscape)

    dom = {'dom': '0,0,1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384'}
    # output mode = 1 : output channel count is 2 with order L, R
    dap_output_mode = '1'
    dap_mix_matrix = 'null'
    ddp_down_mix = '0'
    assert_up_mix_related_feature_result(endpoint_type_in_module, content_type,
                                         dap_output_mode, dap_mix_matrix, dom,
                                         _down_mix=ddp_down_mix)


@pytest.mark.sv
@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_vsv_off_test_data)
def test_log_up_mix_sv_off_verify_portrait(content_name, content_type,
                                           dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   non-Dolby and Dolby content can not be up mixed to 5.1.2 when sv off

    Test Check Point:
    """
    # tuning device name : speaker portrait
    caller_name = test_log_up_mix_sv_off_verify_portrait.__name__
    up_mix_and_sv_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type,
                                     spk_tuning_device_name_id=dap_tuning_device_name_speaker_portrait)

    ddp_down_mix = '0'
    dom = {'dom': '0,0,0,16384,16384'}
    # output mode = 1 : output channel count is 2 with order L, R
    if content_type in content_type_dolby:
        dap_output_mode = '1'
        dap_mix_matrix = 'null'
    elif content_type in content_type_non_dolby:
        dap_output_mode = '0'
        dap_mix_matrix = 'custom'

    assert_up_mix_related_feature_result(endpoint_type_in_module, content_type,
                                         dap_output_mode, dap_mix_matrix, dom,
                                         _down_mix=ddp_down_mix,
                                         _tuning_device_name=dap_tuning_device_name_speaker_portrait)


@pytest.mark.sv
@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_vsv_on_test_data)
def test_log_up_mix_sv_on_verify_landscape(content_name, content_type,
                                           dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   content should be up mixed to 5.1.2 when sv on
                           except 2 channel dolby content up mixed to 5.1

    Test Check Point:
    """
    # tuning device name : speaker landscape
    caller_name = test_log_up_mix_sv_on_verify_landscape.__name__
    up_mix_and_sv_on_test_procedure(caller_name, endpoint_type_in_module,
                                    content_name, content_type,
                                    spk_tuning_device_name_id=dap_tuning_device_name_speaker_landscape)

    # this means speaker virtualizer with height and input will be up mixed to 5.1.2
    # except 2 channel dolby content type
    # 2 channel dolby content will be up mixed to 5.1 channel, instead of up mixing to 5.1.2
    dom = {'dom': '1,0,1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384'}
    # output mode = 11 : output channel count is 8 with order L, R, C, LFE, Ls, Rs, Ltm, Rtm
    # output mode = 10 : output channel count is 6 with order L, R, C, LFE, Ls, Rs
    if content_type in content_type_2_channel_dolby:
        dap_output_mode = '10'
    else:
        dap_output_mode = '11'
    dap_mix_matrix = 'custom'
    ddp_down_mix = '0'
    assert_up_mix_related_feature_result(endpoint_type_in_module, content_type,
                                         dap_output_mode, dap_mix_matrix, dom,
                                         _down_mix=ddp_down_mix)


@pytest.mark.sv
@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_vsv_on_test_data)
def test_log_up_mix_sv_on_verify_portrait(content_name, content_type,
                                          dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   content should be up mixed to 5.1.2 when sv on
                           except 2 channel dolby content up mixed to 5.1

    Test Check Point:
    """
    # tuning device name : speaker portrait
    caller_name = test_log_up_mix_sv_on_verify_portrait.__name__
    up_mix_and_sv_on_test_procedure(caller_name, endpoint_type_in_module,
                                    content_name, content_type,
                                    spk_tuning_device_name_id=dap_tuning_device_name_speaker_portrait)

    ddp_down_mix = '0'
    # in Speaker_portrait tuning element in dax-default.xml file , the virtualizer is disable now
    # so the dom expect value is dom = {'dom': '0,0,0,16384,16384'}
    # if change the value to true , the expect result is dom = {'dom': '1,0,0,16384,16384'}
    # so please first check virtualizer setting in dax-default.xml file
    # in the feature , it'd better that
    # the expected result depends on values parsed from the xml , not hard code in this way
    dom = {'dom': '0,0,0,16384,16384'}
    # output mode = 1 : output channel count is 2 with order L, R
    if content_type in content_type_dolby:
        dap_output_mode = '1'
        dap_mix_matrix = 'null'
    elif content_type in content_type_non_dolby:
        dap_output_mode = '0'
        dap_mix_matrix = 'custom'

    assert_up_mix_related_feature_result(endpoint_type_in_module, content_type,
                                         dap_output_mode, dap_mix_matrix, dom,
                                         _down_mix=ddp_down_mix,
                                         _tuning_device_name=dap_tuning_device_name_speaker_portrait)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         up_mix_and_hv_on_test_data)
def test_log_sv_always_enabled_in_music_profile_verify_landscape(content_name, content_type,
                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-2627, 2628, 2629, 2630, 2631, 2632, 2633 and 169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is wired headphone

    Test Description:   virtual is always enabled in music profile for dolby content
                        virtual could be changed in music profile for non dolby content
    """
    caller_name = test_log_sv_always_enabled_in_music_profile_verify_landscape.__name__
    sv_always_enabled_in_music_profile_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type,
                                                      spk_tuning_device_name_id=dap_tuning_device_name_speaker_landscape
                                                      )

    if content_type in content_type_dolby:
        # for 2 channel dolby content, vir will be disable, instead of up mixing to 5.1.2
        # for 1 channel dolby content with acmod value equal to 1, it will be treated as dolby 5.1 channel content
        dom = {'dom': '1,0,1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384'}
        # output mode = 11 : output channel count is 8 with order L, R, C, LFE, Ls, Rs, Ltm, Rtm
        # output mode = 10 : output channel count is 6 with order L, R, C, LFE, Ls, Rs
        if content_type in content_type_2_channel_dolby:
            dom = {'dom': '0,0,1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384'}
            dap_output_mode = '1'
            dap_mix_matrix = 'null'
        else:
            dap_output_mode = '11'
            dap_mix_matrix = 'custom'
    else:
        dom = {'dom': '0,0,1,16384,0,0,16384,11583,11583,8192,8192,16384,0,0,16384,16384,0,0,16384'}
        # output mode = 1 : output channel count is 2 with order L, R
        dap_output_mode = '1'
        dap_mix_matrix = 'null'

    ddp_down_mix = '0'

    assert_up_mix_related_feature_result(endpoint_type_in_module, content_type,
                                         dap_output_mode, dap_mix_matrix, dom, ddp_down_mix)


@pytest.mark.log
@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         dap_off_test_data)
def test_log_print_situation_when_dap_off_verify(content_name, content_type,
                                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    """
    Test Case ID    :   TC-169, 170, 171, 172, 173

    Test Condition  :   make sure device endpoint is stereo speaker

    Test Description:   no log print when dap off for non dolby content
                        qmf log print when dap off for dolby content

    Test Check Point:   dap parameter relating log print in stand output
    """
    caller_name = test_log_print_situation_when_dap_off_verify.__name__
    log_print_when_dap_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)

    if content_type in content_type_non_dolby:
        assert_no_log_print_when_dap_off_for_non_dolby_content(endpoint_type_in_module)
    elif content_type in content_type_dolby:
        assert_apply_dap_off_profile_values_when_dap_off_for_dolby_content(endpoint_type_in_module)
    elif content_type in content_type_ac4:
        assert_apply_dap_off_profile_values_when_dap_off_for_ac4_content(endpoint_type_in_module)


# @pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
#                          decoder_joc_force_down_mix_test_data)
# def test_log_decoder_joc_force_down_mix_verify(content_name, content_type,
#                                                dap_status, dap_profile, dap_feature_type, dap_feature_value):
#     """
#     Test Case ID    :   TC-4021
#
#     Test Condition  :   make sure device endpoint is stereo speaker
#
#     Test Description:   always decode object for headphone, usb, stereo speaker endpoint
#
#     Test Check Point:   in udc decoder , its value should be 0 for stereo speaker
#     """
#     caller_name = test_log_decoder_joc_force_down_mix_verify.__name__
#     up_mix_and_sv_on_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)
#
#     decoder_down_mix = '0'
#     assert_decoding_joc_down_mix_related_feature_result(endpoint_type_in_module, content_type, decoder_down_mix)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         reference_level_test_data)
def test_log_reference_level_when_dap_off_verify(content_name, content_type,
                                                 dap_status, dap_profile, dap_feature_type, dap_feature_value):
    caller_name = test_log_reference_level_when_dap_off_verify.__name__
    reference_level_when_dap_off_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)

    ref_lvl_expected_dictionary = {'dvle': '1', 'dvla': '5', 'dvli': '-496', 'dvlo': '-224', 'vmb': '144'}
    if dap_profile in (dap_profile_dynamic, dap_profile_movie):
        ref_lvl_expected_dictionary['dvla'] = '7'
    elif dap_profile == dap_profile_music:
        ref_lvl_expected_dictionary['dvla'] = '4'
    elif dap_profile == dap_profile_custom_dax3:
        ref_lvl_expected_dictionary['dvla'] = '0'

    if content_type in content_type_dolby:
        ref_lvl_expected_dictionary['dvle'] = '1'
        ref_lvl_expected_dictionary['dvlo'] = '-272'
        ref_lvl_expected_dictionary['vol'] = '0'
        ref_lvl_expected_dictionary.pop('vmb')
    else:
        ref_lvl_expected_dictionary['dvle'] = '0'
        ref_lvl_expected_dictionary.pop('dvlo')
        ref_lvl_expected_dictionary.pop('vmb')
        ref_lvl_expected_dictionary.pop('vol')

    assert_dap_reference_level_related_feature_result(endpoint_type_in_module, content_type,
                                                      ref_lvl_expected_dictionary, PROJECT_ID_DAX3)
    assert_endpoint_type_in_dom_list(endpoint_type_in_module, dap_status_off)


@pytest.mark.parametrize('content_name,content_type,dap_status,dap_profile,dap_feature_type,dap_feature_value',
                         reference_level_test_data)
def test_log_reference_level_when_dap_on_verify(content_name, content_type,
                                                dap_status, dap_profile, dap_feature_type, dap_feature_value):
    caller_name = test_log_reference_level_when_dap_on_verify.__name__
    reference_level_when_dap_on_test_procedure(caller_name, endpoint_type_in_module, content_name, content_type)

    # for dolby content (except ac4 dolby content) when dap on and vl on or off in dax3 project ,
    # output reference level is equals to -14db (-224) no matter vl on or off
    # dvle value in qmf process should always be true no matter vl is on or off
    #            --> dvle = 1 in qmf and dvle = 0 in global process
    # dvlo=-320 in qmf process and vol=96 in global process when dap on and vl on , and totally -14db
    # dvlo=-272 in qmf process and vol=96 in global process when dap on and vl off , and totally -11db
    # dvlo=-272 in qmf process and vol=0 in global process when dap off , and totally -17db

    # for non-dolby content and dap and vl on , the output reference level is equals to -14db
    # dvle = 1 , then dvlo=-320 and vmb=96 ,and sum them to -14db
    # for non-dolby content and dap on and vl off , the output reference level depends on input audio
    # for non-dolby content and dap off , the output reference level depends on input audio

    # in current dax3 project , vl value in 4 profiles is always true and could not controlled by Consumer UI
    # two ways could change vl value in a profile , call DolbyAudioEffect class api or change dax-default.xml files .

    # for diff profile , the dvla value is diff
    # here dvla = 0 when custom profile is selected
    ref_lvl_expected_dictionary = {'dvle': '1', 'dvla': '5', 'dvli': '-496', 'dvlo': '-176', 'vmb': '144'}
    if dap_profile in (dap_profile_dynamic, dap_profile_movie):
        ref_lvl_expected_dictionary['dvla'] = '7'
    elif dap_profile == dap_profile_music:
        ref_lvl_expected_dictionary['dvla'] = '4'
    elif dap_profile == dap_profile_custom_dax3:
        ref_lvl_expected_dictionary['dvla'] = '0'

    if content_type in content_type_dolby:
        ref_lvl_expected_dictionary['dvle'] = '1'
        ref_lvl_expected_dictionary['dvlo'] = '-320'
        ref_lvl_expected_dictionary['vol'] = '96'
        ref_lvl_expected_dictionary.pop('vmb')
    else:
        ref_lvl_expected_dictionary['dvle'] = '1'
        ref_lvl_expected_dictionary['dvlo'] = '-320'
        ref_lvl_expected_dictionary['vmb'] = '96'
        ref_lvl_expected_dictionary.pop('vol')

    assert_dap_reference_level_related_feature_result(endpoint_type_in_module, content_type,
                                                      ref_lvl_expected_dictionary, PROJECT_ID_DAX3)
    assert_endpoint_type_in_dom_list(endpoint_type_in_module, dap_status_on)
