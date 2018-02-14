from tools.common import *
from tools.logger import *


def be_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_feature_value):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if dap_feature_value == dap_feature_value_be_on:
        tmp_status = 'on'
    else:
        tmp_status = 'off'
    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify VB & BE are {} when playing {} Dolby content using {} ".format(
                tmp_status, content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify VB & BE are {} when playing {} non Dolby content using {} ".format(
                tmp_status, content_type, endpoint_id))

    # step 2 : change dap feature
    if tmp_status == 'on':
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                               dap_feature_type_be, dap_feature_value_be_off)
    else:
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                               dap_feature_type_be, dap_feature_value_be_on)

    feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                           dap_feature_type_be, dap_feature_value)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)
    # print ("module name is :" + __name__)
    # step 4 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    __assert_no_double_processing_by_content_type(content_type)

    if dap_feature_value == dap_feature_value_be_on:
        if (endpoint_id == AUDIO_DEVICE_OUT_MONO_SPEAKER) \
                or (endpoint_id == AUDIO_DEVICE_OUT_STEREO_SPEAKER):
            __comparison_result(content_type, be_on_expected_value_speaker_endpoint)
        else:
            __comparison_result(content_type, be_on_expected_value_except_speaker_endpoint)
    elif dap_feature_value == dap_feature_value_be_off:
        __comparison_result(content_type, be_off_expected_value)


def assert_be_related_feature_result(_content_type, _be_value_dict):
    __assert_no_double_processing_by_content_type(_content_type)
    __comparison_result(_content_type, _be_value_dict)


def mi_off_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)
    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is off when playing {} Dolby content using {}".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is off when playing {} non Dolby content using {} ".format(
                content_type, endpoint_id))

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    __assert_no_double_processing_by_content_type(content_type)

    __comparison_result(content_type, mi_off_expected_result)


def mi_on_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is on when playing {} channel Dolby content using {}".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is on when playing {} channel non Dolby content using {}".format(
                content_type, endpoint_id))

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    # step 5 : even through changing volume level to off for dolby content , values should always be true
    # to make qmf output level from line-mode -31db to portable mode -14db
    assert_mi_related_feature_result(content_type, True, dap_feature_value_vl_on)

    execute(adb_broadcast_intent +
            intent_change_dap_high_level_feature.format(dap_feature_type_vl, dap_feature_value_vl_off))

    # step 6 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'new_' + content_name)

    # step 7 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    assert_mi_related_feature_result(content_type, True, dap_feature_value_vl_off)

    # step 8 : turn off dap and verify mi feature is expected (off)
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status_off)
    # capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dap_off_' + content_name)
    assert_mi_related_feature_result(content_type, False, dap_feature_value_vl_off)

    # step 9 : turn on dap and verify mi feature is expected (on)
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status_on)
    # capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dap_on_' + content_name)
    assert_mi_related_feature_result(content_type, True, dap_feature_value_vl_on)


def assert_mi_related_feature_result(_content_type, _mi_expected_value, _vl_expected_value):
    # verify no dap double processing
    __assert_no_double_processing_by_content_type(_content_type)

    # verify mi related value is expected
    if _mi_expected_value:
        if _content_type in content_type_2_channel_dolby:
            __comparison_result(_content_type, mi_on_2_channel_expected_result)
        elif _content_type in content_type_dolby:
            __comparison_result(_content_type, mi_on_multi_channel_expected_result)
        else:
            __comparison_result(_content_type, mi_on_non_dolby_content_expected_result)
    else:
        __comparison_result(_content_type, mi_off_expected_result)

    # verify volume level will always turn on for dolby content
    assert_vl_related_feature_result(_content_type, _vl_expected_value)


def assert_vl_related_feature_result(_content_type, _vl_expected_value):
    if _content_type in content_type_dolby:
        vl_actual_value = get_feature_value_from_qmf_process("dvle")
        assert '1' == vl_actual_value, \
            "!!!!!error: Volume leveler turned off unexpectedly when playing dolby content!"
    else:
        vl_actual_value = get_feature_value_from_global_process("dvle")
        assert _vl_expected_value == vl_actual_value, \
            "!!!!! error: Volume leveler should off but on when playing non dolby content!"


def up_mix_and_sv_off_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify no up mix when sv off and playing {} Dolby content using {} ".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify no up mix when sv off and playing {} channel non Dolby content using {} ".format(
                content_type, endpoint_id))

    # step 2 : change dap feature according to endpoint type
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                       AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        # feature_test_procedure(content_name, dap_status_on, dap_profile_music,
        #                        dap_feature_type_vsv, dap_feature_value_vsv_on)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                               dap_feature_type_vsv, dap_feature_value_vsv_off)
    elif endpoint_id in (AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                         AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        # feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
        #                        dap_feature_type_hv, dap_feature_value_hv_on)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                               dap_feature_type_hv, dap_feature_value_hv_off)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    # __assert_no_double_processing_by_content_type(content_type)
    # __assert_dap_output_mode_setting(content_type, endpoint_id, dap_feature_value_vsv_off)
    #
    # __comparison_result(content_type, up_mix_and_sv_off_expected_value)


def up_mix_and_sv_on_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_dolby:
        if content_type in content_type_2_channel_dolby:
            logging.getLogger(endpoint_id).info(
                "===== Verify up mix to 5.1 when sv on and playing {} channel Dolby content using {} ".format(
                    content_type, endpoint_id))
        else:
            logging.getLogger(endpoint_id).info(
                "===== Verify up mix to 5.1.2 when sv on and playing {} Dolby content using {} ".format(
                    content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify up mix to 5.1.2 when sv on and playing {} channel non Dolby content using {} ".format(
                content_type, endpoint_id))

    # step 2 : change dap feature
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER, AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        # feature_test_procedure(content_name, dap_status_on, dap_profile_music,
        #                        dap_feature_type_vsv, dap_feature_value_vsv_on)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                               dap_feature_type_vsv, dap_feature_value_vsv_on)
    elif endpoint_id in (AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                         AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        # feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
        #                        dap_feature_type_hv, dap_feature_value_hv_off)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                               dap_feature_type_hv, dap_feature_value_hv_on)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)

    # step 4 : verify dap feature is correct or not , and include below step
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    # __assert_no_double_processing_by_content_type(content_type)
    # __assert_dap_output_mode_setting(content_type, endpoint_id, dap_feature_value_vsv_on)
    #
    # if endpoint_id == AUDIO_DEVICE_OUT_MONO_SPEAKER:
    #     __comparison_result(content_type, up_mix_and_sv_on_mono_spk_expected_value)
    # elif endpoint_id == AUDIO_DEVICE_OUT_STEREO_SPEAKER:
    #     __comparison_result(content_type, up_mix_and_sv_on_stereo_spk_expected_value)
    # elif (endpoint_id == AUDIO_DEVICE_OUT_WIRED_HEADPHONE) \
    #         or (endpoint_id == AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET):
    #     __comparison_result(content_type, up_mix_and_sv_on_headphone_expected_value)
    # elif endpoint_id == AUDIO_DEVICE_OUT_BLUETOOTH_A2DP:
    #     __comparison_result(content_type, up_mix_and_sv_on_blue_tooth_expected_value)


def assert_up_mix_related_feature_result(_content_type, _dap_output_mode, _dap_mix_matrix, _dom, _down_mix=None):
    __assert_no_double_processing_by_content_type(_content_type)
    __comparison_result(_content_type, _dom)
    if _content_type in content_type_dolby:
        # for dolby content , output mode value should print in qmf process
        _output_mode_in_process = DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX
        temp_down_mix = _down_mix
    else:
        # for dolby content , output mode value should print in global process
        _output_mode_in_process = DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX
        # for non dolby content , down mix value should not exist
        temp_down_mix = None
    _temp_output_mode = get_dap_output_mode_set_value(_content_type)
    if _temp_output_mode is not None or _content_type in content_type_dolby:
        __assert_equal(SPECIFIED_FEATURE_KEY_WORDS_LIST[_output_mode_in_process],
                       _dap_output_mode,
                       _temp_output_mode)
        __assert_equal(SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_MIX_MATRIX_INDEX],
                       _dap_mix_matrix,
                       get_dap_output_mode_mix_matrix())
        __assert_equal(SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_JOC_FORCE_DOWN_MIX_INDEX],
                       temp_down_mix,
                       get_dap_joc_force_down_mix_mode_value())


def __generate_and_parse_log_file(_caller_name, _endpoint_id, _content_name):
    # generate log file
    temp_log_name = logFileNameFormat.format(functionName=_caller_name,
                                             endpoint_type=_endpoint_id,
                                             log_type=_content_name.replace('.', '_'))
    sv_log_file_name = abspath(join('.', 'log', _endpoint_id, temp_log_name))
    generate_log_file(sv_log_file_name)
    # parse log file
    parse_dap_feature_value_from_log_file(sv_log_file_name)


def __comparison_result(_content_type, _expected_list):
    for _four_cc_name in _expected_list.keys():
        expected_value = _expected_list[_four_cc_name]
        actual_value = get_feature_value_from_global_process(_four_cc_name)
        if _content_type in content_type_dolby:
            if _four_cc_name in CONTENT_PROCESSING_PARAM_LIST:
                actual_value = get_feature_value_from_qmf_process(_four_cc_name)
        __assert_equal(_four_cc_name, expected_value, actual_value)
        assert expected_value == actual_value, \
            "{} expected value : {} but {}".format(_four_cc_name, expected_value, actual_value)


def __assert_equal(_key_word, _expected_value, _actual_value):
    # if _expected_value is None:
    #     __expected_value = 'null'
    assert _expected_value == _actual_value, \
        "{} expected value : {} but {}".format(_key_word, _expected_value, _actual_value)


def __assert_no_double_processing_by_content_type(_content_type):
    if _content_type in content_type_dolby:
        no_double_processing_result = verify_no_double_processing_dap_parameter(True)
        assert no_double_processing_result, "!!!!!! double processing error "
    else:
        no_double_processing_result = verify_no_double_processing_dap_parameter(False)
        assert no_double_processing_result, "!!!!!! double processing error "



