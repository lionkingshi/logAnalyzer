from tools.common import *
from tools.logger import *
from src.dax31.log_analysis.dax3XMLParser.XMLUpdater import *


def specified_profile_default_value_test_procedure_dax3(caller_name, endpoint_id, content_name, content_type,
                                                        _dap_profile,
                                                        _tuning_port=dap_tuning_port_internal_speaker,
                                                        _tuning_device_name=dap_tuning_device_name_speaker_landscape):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if _dap_profile == dap_profile_custom_dax3:
        _profile_name = 'Custom'
    elif _dap_profile == dap_profile_dynamic:
        _profile_name = 'Dynamic'
    elif _dap_profile == dap_profile_movie:
        _profile_name = 'Movie'
    elif _dap_profile == dap_profile_music:
        _profile_name = 'Music'

    index = _tuning_device_name
    logging.getLogger(endpoint_id).critical(
        "===== Verify DAP parameter's default values in {} profile".format(_profile_name))
    logging.getLogger(endpoint_id).critical(
        "=====            when playing {} content under {} ".format(content_type, endpoint_id))
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        logging.getLogger(endpoint_id).critical(
            "=====                          and {} mode".format(speaker_tuning_name[index]))

    # step 2 : change tuning device name for speaker port
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        if _tuning_device_name == dap_tuning_device_name_speaker_landscape:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                _tuning_port,
                dap_tuning_device_name_speaker_landscape))
        elif _tuning_device_name == dap_tuning_device_name_speaker_portrait:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                _tuning_port,
                dap_tuning_device_name_speaker_portrait))

    # step 3 : change dap profile
    if _dap_profile != dap_profile_custom_dax3:
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3)
        feature_test_procedure(content_name, dap_status_on, _dap_profile)
    else:
        feature_test_procedure(content_name, dap_status_on, dap_profile_dynamic)
        feature_test_procedure(content_name, dap_status_on, _dap_profile)

    # step 4 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def assert_specified_profile_default_values_result(_profile_name, tuning_device_name,
                                                   _endpoint_type=AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                                                   _content_type=content_type_2_channel_non_dolby):
    _current_directory = os.path.dirname(os.path.abspath(__file__))
    if _endpoint_type == AUDIO_DEVICE_OUT_MONO_SPEAKER:
        default_xml_file_name = abspath(
            join(_current_directory, 'dax3XMLParser', 'mono', 'dax3-default-mono-speaker.xml'))
    else:
        default_xml_file_name = abspath(
            join(_current_directory, 'dax3XMLParser', 'stereo', 'dax3-default-stereo-speaker.xml'))
    xml_parser_class = TuningFileParser(default_xml_file_name)
    post_para_dict_from_xml = xml_parser_class.print_expect_value(_profile_name=_profile_name,
                                                                  tuning_device_name_endpoint=tuning_device_name)

    if _content_type in content_type_non_dolby:
        __compare_para_default_value_for_non_dolby_content(post_para_dict_from_xml, _endpoint_type, _profile_name)
        logging.getLogger(_endpoint_type).critical(
            "====== for non dolby content playback, ")
    elif _content_type in content_type_dolby:
        __compare_para_default_value_for_dolby_content(
            post_para_dict_from_xml, _endpoint_type, _profile_name, _content_type)
        logging.getLogger(_endpoint_type).critical(
            "====== for dolby content playback, ")
    elif _content_type in content_type_ac4:
        __compare_para_default_value_for_dolby_content(
            post_para_dict_from_xml, _endpoint_type, _profile_name, _content_type)
        logging.getLogger(_endpoint_type).critical(
            "====== for AC4 content playback, ")
        pass

    logging.getLogger(_endpoint_type).critical(
        "====== default params in {} profile are same as ones parsing from xml !!!!!".format(_profile_name))


def __compare_para_default_value_for_dolby_content(post_para_dict_from_xml,
                                                   _endpoint_type,
                                                   _profile_name,
                                                   __content_type=content_type_51_dd):
    assert isinstance(post_para_dict_from_xml, dict)
    # produce expected parameters according to data parsed from xml file
    set_logger_name_for_para_assign(_endpoint_type)
    produce_three_type_para(post_para_dict_from_xml)
    _global_process_key_value_assembled = get_assembled_global_process_para_dict()
    _qmf_process_key_value_assembled = get_assembled_qmf_process_para_dict()
    _ac4_decoder_key_value_assembled = get_assembled_ac4_decoder_para_dict()

    # produce actual parameters accordingly to data captured from log file
    _global_para_dict_from_log = get_feature_value_from_global_process()
    _qmf_para_dict_from_log = get_feature_value_from_qmf_process()
    _ac4_para_dict_from_log = get_feature_value_from_ac4_decoder()

    # modified ac4 decoder parameter according to code implementation
    _ac4_decoder_key_value_assembled_after_special_handle = \
        __special_handle_ac4_expected_para_value(_ac4_decoder_key_value_assembled, _endpoint_type, _profile_name)

    _qmf_process_key_value_assembled_after_handle = \
        __special_handle_qmf_para_expected_value(_qmf_process_key_value_assembled, _profile_name, _endpoint_type)

    _global_process_key_value_assembled_after_handle = \
        __special_handle_global_para_expected_value(_global_process_key_value_assembled, _profile_name, _endpoint_type)

    # compare parameters
    if __content_type in content_type_dolby:
        __compare_qmf_para_for_dolby_content(_qmf_process_key_value_assembled_after_handle,
                                             _qmf_para_dict_from_log,
                                             _profile_name,
                                             _endpoint_type)

        __compare_global_para_for_dolby_content(_global_process_key_value_assembled_after_handle,
                                                _global_para_dict_from_log,
                                                _profile_name,
                                                _endpoint_type)
    elif __content_type in content_type_ac4:
        __compare_ac4_para_for_dolby_content(_ac4_decoder_key_value_assembled_after_special_handle,
                                             _ac4_para_dict_from_log,
                                             _profile_name,
                                             _endpoint_type)

        __compare_global_para_for_dolby_content(_global_process_key_value_assembled_after_handle,
                                                _global_para_dict_from_log,
                                                _profile_name,
                                                _endpoint_type)


def __compare_ac4_para_for_dolby_content(_ac4_decoder_key_value_assembled,
                                         _ac4_para_dict_from_log,
                                         _profile_name,
                                         _endpoint_type):
    assert isinstance(_ac4_para_dict_from_log, dict)
    assert isinstance(_ac4_decoder_key_value_assembled, dict)

    for __key_four_cc_name in _ac4_decoder_key_value_assembled.keys():
        # iea value depends to playback content
        if __key_four_cc_name != 'dea':
            __assert_equal(
                _endpoint_type,
                __key_four_cc_name,
                _ac4_decoder_key_value_assembled[__key_four_cc_name],
                _ac4_para_dict_from_log[__key_four_cc_name])
    pass


def __special_handle_ac4_expected_para_value(__qmf_process_key_value_assembled, __endpoint_type, __profile_name):
    assert isinstance(__qmf_process_key_value_assembled, dict)

    _ac4_decoder_key_value_assemble = OrderedDict()
    # directly copy value
    for __four_cc_name in PARA_LIST_AC4:
        if __four_cc_name in __qmf_process_key_value_assembled.keys():
            _ac4_decoder_key_value_assemble[__four_cc_name] = __qmf_process_key_value_assembled[__four_cc_name]
        else:
            _ac4_decoder_key_value_assemble[__four_cc_name] = EMPTY_STRING_FLAG

    # assemble ieid default value
    _ac4_decoder_key_value_assemble['ieid'] = \
        __assemble_ac4_ieid_expected_value(__qmf_process_key_value_assembled, __profile_name)

    # assemble endp default value
    # review set_endpoint_virtualization() method in ac4dec_wrapper.cpp file for more details
    _ac4_decoder_key_value_assemble['endp'] = __assemble_ac4_endp_expected_value(
        __qmf_process_key_value_assembled, __endpoint_type, __profile_name)

    _ac4_decoder_key_value_assemble['mixp'] = __assemble_ac4_mixp_expected_value()
    _ac4_decoder_key_value_assemble['prei'] = __assemble_ac4_prei_expected_value()
    _ac4_decoder_key_value_assemble['dvlo'] = __assemble_ac4_dvlo_expected_value(__qmf_process_key_value_assembled)
    _ac4_decoder_key_value_assemble['drc'] = __assemble_ac4_drc_expected_value_when_dap_on()

    return _ac4_decoder_key_value_assemble


def __special_handle_qmf_para_expected_value(__qmf_process_key_value_assembled, __profile_name, __endpoint_type):
    assert isinstance(__qmf_process_key_value_assembled, dict)
    qmf_process_key_value_assembled = __qmf_process_key_value_assembled
    assert isinstance(qmf_process_key_value_assembled, dict)

    # for music profile ,vir is always set to enabled
    qmf_process_key_value_assembled['dom'] = \
        __assemble_qmf_dom_expected_value(__qmf_process_key_value_assembled, __profile_name, __endpoint_type)

    return qmf_process_key_value_assembled


def __special_handle_global_para_expected_value(__global_process_key_value_assembled, __profile_name, __endpoint_type):
    assert isinstance(__global_process_key_value_assembled, dict)
    global_process_key_value_assembled = __global_process_key_value_assembled
    assert isinstance(global_process_key_value_assembled, dict)

    # for vbon value, it's always equal to 1 and vbm value represent virtual base enable/disable status
    global_process_key_value_assembled['vbm'] = \
        __assemble_global_vbm_expected_value(__global_process_key_value_assembled)

    global_process_key_value_assembled['vbon'] = '1'

    return global_process_key_value_assembled


def __assemble_qmf_dom_expected_value(__qmf_process_key_value_assembled, __profile_name, __endpoint_type):
    assert isinstance(__qmf_process_key_value_assembled, dict)
    __temp_dom_value_in_qmf_process = __qmf_process_key_value_assembled['dom']
    if 'dom' in __qmf_process_key_value_assembled.keys():
        # for music profile ,vir is always set to enabled
        if __profile_name == profile_name[2]:
            if __endpoint_type in \
                    (AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                     AUDIO_DEVICE_OUT_WIRED_HEADPHONE,
                     AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                     AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
                __temp_dom_value_in_qmf_process = \
                    '1' + __qmf_process_key_value_assembled['dom'][1:]
    return __temp_dom_value_in_qmf_process


def __assemble_global_vbm_expected_value(__global_process_key_value_assembled):
    assert isinstance(__global_process_key_value_assembled, dict)
    __temp_vbon_value_in_global_process = __global_process_key_value_assembled['vbon']
    if __temp_vbon_value_in_global_process == '1':
        __temp_vbm_value = '3'
    elif __temp_vbon_value_in_global_process == '0':
        __temp_vbm_value = '0'
    else:
        __temp_vbm_value = '1'
    return __temp_vbm_value


def __assemble_ac4_ieid_expected_value(__qmf_process_key_value_assembled, __profile_name):
    # assemble ieid default value
    __temp_ieid_value = EMPTY_STRING_FLAG
    if __qmf_process_key_value_assembled['ieon'] == '0':
        __temp_ieid_value = INDEX_IEQ_OFF
    elif __qmf_process_key_value_assembled['ieon'] == '1':
        _temp_iebs_string = __qmf_process_key_value_assembled['iebs']
        assert isinstance(_temp_iebs_string, str)
        if IEQ_BALANCED_SPECIFIED_STRING_IN_IEBS in _temp_iebs_string:
            __temp_ieid_value = INDEX_IEQ_BALANCED
        elif IEQ_WARM_SPECIFIED_STRING_IN_IEBS in _temp_iebs_string:
            __temp_ieid_value = INDEX_IEQ_WARM
        elif IEQ_DETAILED_SPECIFIED_STRING_IN_IEBS in _temp_iebs_string:
            __temp_ieid_value = INDEX_IEQ_DETAILED
        else:
            __temp_ieid_value = EMPTY_STRING_FLAG
    # for dynamic profile , force ieid to off
    if __profile_name == profile_name[0]:
        __temp_ieid_value = INDEX_IEQ_OFF

    return __temp_ieid_value


def __assemble_ac4_endp_expected_value(__qmf_process_key_value_assembled, __endpoint_type, __profile_name):
    assert isinstance(__qmf_process_key_value_assembled, dict)

    __temp_endp_value = EMPTY_STRING_FLAG
    __temp_vir_status_in_dom_list = __qmf_process_key_value_assembled['dom'][index_vir_status_in_dom]
    __temp_orientation_type_in_dom_list = __qmf_process_key_value_assembled['dom'][index_orientation_type_in_dom]
    # if virtual is disable or orientation is portrait, endp = 512 (disabled)
    if (__temp_vir_status_in_dom_list == SINGLE_STRING_DISABLE_STATUS) or \
            (__temp_orientation_type_in_dom_list == value_of_speaker_portrait_type_in_dom):
        __temp_endp_value = AC4DEC_OUT_CH_LO_RO
        # But for music profile , vir was set to enabled
        if __profile_name == profile_name[2]:
            if (__endpoint_type == AUDIO_DEVICE_OUT_STEREO_SPEAKER) and \
                    (__temp_orientation_type_in_dom_list == value_of_speaker_landscape_type_in_dom):
                __temp_endp_value = AC4DEC_OUT_CH_SPEAKER_VIRT
            elif __endpoint_type == AUDIO_DEVICE_OUT_WIRED_HEADPHONE or \
                            __endpoint_type == AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET or \
                            __endpoint_type == AUDIO_DEVICE_OUT_BLUETOOTH_A2DP:
                __temp_endp_value = AC4DEC_OUT_CH_HEADPHONE
            else:
                pass
    elif __endpoint_type == AUDIO_DEVICE_OUT_STEREO_SPEAKER:
        __temp_endp_value = AC4DEC_OUT_CH_SPEAKER_VIRT
    elif __endpoint_type == AUDIO_DEVICE_OUT_WIRED_HEADPHONE or \
                    __endpoint_type == AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET or \
                    __endpoint_type == AUDIO_DEVICE_OUT_BLUETOOTH_A2DP:
        __temp_endp_value = AC4DEC_OUT_CH_HEADPHONE
    else:
        __temp_endp_value = EMPTY_STRING_FLAG

    return __temp_endp_value


def __assemble_ac4_mixp_expected_value():
    __temp_mixp_value = AC4DEC_WRAPPER_MAIN_ASSO_PREF_DEFAULT
    return __temp_mixp_value


def __assemble_ac4_prei_expected_value():
    __temp_prei_value = AC4DEC_WRAPPER_PRESENTATION_INDEX_DEFAULT
    return __temp_prei_value


def __assemble_ac4_drc_expected_value_when_dap_on():
    __temp_drc_value = AC4DEC_WRAPPER_DRC_MODE_DEFAULT_DAP_ON
    return __temp_drc_value


def __assemble_ac4_dvlo_expected_value(__qmf_process_key_value_assembled):
    _temp_dvlo_db = int(__qmf_process_key_value_assembled['dvlo']) / 16
    return str(_temp_dvlo_db)


def __compare_global_para_for_dolby_content(_global_process_key_value_assembled,
                                            _global_para_dict_from_log,
                                            _profile_name,
                                            _endpoint_type):
    for _key_four_cc_name in _global_process_key_value_assembled.keys():
        # special handle for iebs when custom profile
        # for custom profile , ieq status is off and iebs values remains as previous
        if _profile_name == profile_name[3]:
            if _key_four_cc_name == 'iebs':
                continue

        if _key_four_cc_name == 'bexe':
            continue

        if _key_four_cc_name in VOLUME_LEVELER:
            continue

        if _key_four_cc_name in VOL_MAX_BOOST:
            continue

        __assert_equal(
            _endpoint_type,
            _key_four_cc_name,
            _global_process_key_value_assembled[_key_four_cc_name],
            _global_para_dict_from_log[_key_four_cc_name])
    pass


def __compare_qmf_para_for_dolby_content(_qmf_process_key_value_assembled,
                                         _qmf_para_dict_from_log,
                                         _profile_name,
                                         _endpoint_type):
    for _key_four_cc_name in _qmf_process_key_value_assembled.keys():
        # special handle for iebs when custom profile
        # for custom profile , ieq status is off and iebs values remains as previous
        if _profile_name == profile_name[3]:
            if _key_four_cc_name == 'iebs':
                continue

        if _key_four_cc_name == 'bexe':
            continue

        if _key_four_cc_name in VOLUME_LEVELER:
            continue

        if _key_four_cc_name in VOL_MAX_BOOST:
            continue

        # if _key_four_cc_name == 'dom':
        #     if _profile_name == profile_name[2]:
        #         if _endpoint_type != AUDIO_DEVICE_OUT_BLUETOOTH_A2DP:
        #             _qmf_process_key_value_assembled[_key_four_cc_name] = \
        #                 '1' + _qmf_process_key_value_assembled[_key_four_cc_name][1:]

        __assert_equal(
            _endpoint_type,
            _key_four_cc_name,
            _qmf_process_key_value_assembled[_key_four_cc_name],
            _qmf_para_dict_from_log[_key_four_cc_name])
    pass


def __compare_para_default_value_for_non_dolby_content(post_para_dict_from_xml, _endpoint_type, _profile_name):
    post_para_dict_from_log = get_feature_value_from_global_process()
    for __index in range(len(PARA_LIST_IN_GLOBAL_PROCESS)):
        four_cc_name = PARA_LIST_IN_GLOBAL_PROCESS[__index]
        if four_cc_name not in PARA_LIST_NOT_EXIST_XML_FILE:
            assert isinstance(post_para_dict_from_xml[four_cc_name], str)
            assert isinstance(post_para_dict_from_log[four_cc_name], str)

            if four_cc_name == 'ceqt':
                if len(post_para_dict_from_xml[four_cc_name]) == len(post_para_dict_from_log[four_cc_name]):
                    logging.getLogger(_endpoint_type).debug("ceqt length from log and xml is equals : {} !".format(
                        len(post_para_dict_from_log[four_cc_name]))
                    )
                    __assert_equal(
                        _endpoint_type,
                        four_cc_name,
                        post_para_dict_from_xml[four_cc_name],
                        post_para_dict_from_log[four_cc_name])
                else:
                    logging.getLogger(_endpoint_type).debug("ceqt length from xml:{} and log:{} is not equals !".format(
                        len(post_para_dict_from_xml[four_cc_name]), len(post_para_dict_from_log[four_cc_name]))
                    )
                    __assert_equal(
                        _endpoint_type,
                        four_cc_name,
                        post_para_dict_from_xml[four_cc_name],
                        post_para_dict_from_log[four_cc_name][:-4])
            else:
                # special handle for iebs when custom profile
                # for custom profile , ieq status is off and iebs values remains as previous
                if _profile_name == profile_name[3]:
                    if four_cc_name == 'iebs':
                        continue
                # special handle for vbm and vbon
                # index of vbon is smaller than vbm in list
                if four_cc_name == 'vbon':
                    temp_vbon_expected_value = '1'
                    __assert_equal(
                        _endpoint_type,
                        'vbon',
                        temp_vbon_expected_value,
                        post_para_dict_from_log['vbon'])
                    continue
                if four_cc_name == 'vbm':
                    post_para_dict_from_xml['vbm'] = __assemble_global_vbm_expected_value(post_para_dict_from_xml)

                __assert_equal(
                    _endpoint_type,
                    four_cc_name,
                    post_para_dict_from_xml[four_cc_name],
                    post_para_dict_from_log[four_cc_name])
        pass


def be_test_procedure_dax3(caller_name, endpoint_id, content_name, content_type, dap_feature_value):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if dap_feature_value == dap_feature_value_be_on:
        tmp_status = 'on'
    else:
        tmp_status = 'off'
    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).critical(
            "===== Verify VB & BE are {} when playing {} Dolby content using {} ".format(
                tmp_status, content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).critical(
            "===== Verify VB & BE are {} when playing {} non Dolby content using {} ".format(
                tmp_status, content_type, endpoint_id))

    # step 2 : change dap feature
    if tmp_status == 'on':
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_be_dax3, dap_feature_value_be_off)
    else:
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_be_dax3, dap_feature_value_be_on)

    feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                           dap_feature_type_be_dax3, dap_feature_value)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def assert_dap_be_related_feature_result(endpoint_id, _content_type, _be_value_dict):
    __assert_no_double_processing_by_content_type(endpoint_id, _content_type)
    __comparison_result(endpoint_id, _content_type, _be_value_dict)


def mi_off_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile, ):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)
    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).critical(
            "===== Verify mi steer is off when playing {} Dolby content using {}".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).critical(
            "===== Verify mi steer is off when playing {} non Dolby content using {} ".format(
                content_type, endpoint_id))

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def mi_on_test_procedure_another(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile,
                                 _project_id=PROJECT_ID_DAX2):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).critical(
            "===== Verify mi steer is on when playing {} channel Dolby content under {}".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).critical(
            "===== Verify mi steer is on when playing {} channel non Dolby content under {}".format(
                content_type, endpoint_id))

    # step 2 : change to dynamic profile
    execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile_custom_dax3)
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dynamic_' + content_name, content_type)


def mi_on_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile,
                         _project_id=PROJECT_ID_DAX2):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).critical(
            "===== Verify mi steer is on when playing {} channel Dolby content using {}".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).critical(
            "===== Verify mi steer is on when playing {} channel non Dolby content using {}".format(
                content_type, endpoint_id))

    # step 2 : change to dynamic profile
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dynamic_' + content_name, content_type)

    # step 4 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    # step 5 : even through changing volume level to off for dolby content , dvle values should always be true
    # to make qmf output level from line-mode -31db to portable mode -14db
    mi_on_expected_dictionary = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}
    ref_lvl_expected_dictionary = {'dvle': '1', 'dvla': '5', 'dvlo': '-320', 'vmb': '144', 'vol': '96'}

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
    assert_dap_mi_and_vl_related_feature_result(endpoint_id, content_type,
                                                mi_on_expected_dictionary, ref_lvl_expected_dictionary,
                                                PROJECT_ID_DAX3)

    # step 6 : turn off volume leveler when dap on
    execute(adb_broadcast_intent +
            intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_off))
    __generate_and_parse_log_file(caller_name, endpoint_id, 'vl_off_' + content_name, content_type)

    # step 7 :
    # dap on and vl off ,
    #     for dolby content : check reference level equals to -11db which is not expected !!!
    #     for non dolby content : check dvle = 0

    if content_type in content_type_dolby:
        ref_lvl_expected_dictionary['dvle'] = '1'
        ref_lvl_expected_dictionary['dvlo'] = '-320'
        ref_lvl_expected_dictionary['vol'] = '96'
    else:
        ref_lvl_expected_dictionary['dvle'] = '0'
        ref_lvl_expected_dictionary['dvlo'] = '-320'
        ref_lvl_expected_dictionary['vmb'] = '96'

    assert_dap_mi_and_vl_related_feature_result(endpoint_id, content_type,
                                                mi_on_expected_dictionary, ref_lvl_expected_dictionary,
                                                PROJECT_ID_DAX3)

    # step 8 :
    # turn off dap and verify mi feature is expected (off) all equals to 0
    # for dolby content , qmf and global process would apply values in off profile
    #         which means : dvle = 1 dvlo = -272 vol = 0 summed them and got -17db
    # for non dolby content , dap feature would be bypass abd value in global process remains as before
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status_off)
    execute(adb_broadcast_intent +
            intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_on))
    execute(adb_broadcast_intent +
            intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_off))
    # capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dap_off_' + content_name, content_type)
    mi_off_expected_dictionary = {'msce': '0', 'mdee': '0', 'miee': '0', 'mdle': '0', 'mave': '0'}
    # step 8 : dap off , check reference level equals to -17db
    if content_type in content_type_dolby:
        ref_lvl_expected_dictionary['dvle'] = '1'
        ref_lvl_expected_dictionary['dvlo'] = '-272'
        ref_lvl_expected_dictionary['vol'] = '0'
    else:
        ref_lvl_expected_dictionary['dvle'] = '0'

    if content_type in content_type_non_dolby:
        mi_off_expected_dictionary = mi_on_expected_dictionary

    assert_dap_mi_and_vl_related_feature_result(endpoint_id, content_type,
                                                mi_off_expected_dictionary, ref_lvl_expected_dictionary,
                                                PROJECT_ID_DAX3)

    # step 9 : turn on dap and verify mi feature is expected (on)
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status_on)
    # capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dap_on_' + content_name, content_type)
    # step 10 :
    # dap on and vl off ,
    #     for dolby content : check reference level equals to -11db which is not expected !!!
    #     for non dolby content : check dvle = 0
    if content_type in content_type_dolby:
        ref_lvl_expected_dictionary['dvle'] = '1'
        ref_lvl_expected_dictionary['dvlo'] = '-320'
        ref_lvl_expected_dictionary['vol'] = '96'
    else:
        ref_lvl_expected_dictionary['dvle'] = '0'
        ref_lvl_expected_dictionary['dvlo'] = '-320'
        ref_lvl_expected_dictionary['vmb'] = '96'

    assert_dap_mi_and_vl_related_feature_result(endpoint_id, content_type,
                                                mi_on_expected_dictionary, ref_lvl_expected_dictionary,
                                                PROJECT_ID_DAX3)


def up_mix_and_sv_off_test_procedure(caller_name, endpoint_id, content_name, content_type,
                                     spk_tuning_device_name_id=dap_tuning_device_name_internal_speaker):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    # if content_type in content_type_dolby:
    #     logging.getLogger(endpoint_id).critical(
    #         "===== Verify no up mix and virtualization when set sv off and playing {} Dolby content using {} ".format(
    #             content_type, endpoint_id))
    # else:
    #     logging.getLogger(endpoint_id).critical(
    #         "===== Verify no up mix when sv off and playing {} channel non Dolby content using {} ".format(
    #             content_type, endpoint_id))
    if endpoint_id == AUDIO_DEVICE_OUT_MONO_SPEAKER:
        logging.getLogger(endpoint_id).critical(
            "===== Verify for mono speaker endpoint")
        logging.getLogger(endpoint_id).critical(
            "=====        virtualization is always disable ")
        if content_type in content_type_dolby:
            logging.getLogger(endpoint_id).critical(
                "=====                       and UDC will do down mix task")
        logging.getLogger(endpoint_id).critical(
            "=====                              when playing {} channel content ".format(content_type))
    elif (endpoint_id == AUDIO_DEVICE_OUT_STEREO_SPEAKER) and \
            (dap_tuning_device_name_speaker_portrait == spk_tuning_device_name_id):
        logging.getLogger(endpoint_id).critical(
            "===== Verify for stereo speaker endpoint and tuning device name changed to portrait ")
        logging.getLogger(endpoint_id).critical(
            "=====        virtualization is always disable ")
        if content_type in content_type_dolby:
            logging.getLogger(endpoint_id).critical(
                "=====                       and DAP will do down mix task")
        logging.getLogger(endpoint_id).critical(
            "=====                              when playing {} channel content".format(content_type))
    else:
        if content_type in content_type_dolby:
            if content_type in content_type_2_channel_dolby:
                logging.getLogger(endpoint_id).critical(
                    "===== Verify virtualization could be turned off through calling API to turn virtual off ")
            else:
                logging.getLogger(endpoint_id).critical(
                    "===== Verify virtualization is always enabled even through call API to turn virtual off ")

            logging.getLogger(endpoint_id).critical(
                "=====       when playing {} channel Dolby content under {} ".format(content_type, endpoint_id))
        else:
            logging.getLogger(endpoint_id).critical(
                "===== Verify virtualization could be turned off through calling API to turn virtual off")
            logging.getLogger(endpoint_id).critical(
                "=====       when playing {} channel non Dolby content under {} ".format(content_type, endpoint_id))
        if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
            index = str(spk_tuning_device_name_id)
            logging.getLogger(endpoint_id).critical(
                "=====                          and {} mode".format(speaker_tuning_name[index]))
        if content_type in content_type_dolby:
            logging.getLogger(endpoint_id).critical(
                "===== and meanwhile DAP will do down mix task")

    # step 2 : change tuning device name for speaker port
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        if spk_tuning_device_name_id == dap_tuning_device_name_speaker_landscape:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                dap_tuning_port_internal_speaker,
                dap_tuning_device_name_speaker_landscape))
        elif spk_tuning_device_name_id == dap_tuning_device_name_speaker_portrait:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                dap_tuning_port_internal_speaker,
                dap_tuning_device_name_speaker_portrait))

    # step 3 : change dap feature according to endpoint type
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        feature_test_procedure(content_name, dap_status_on, dap_profile_music,
                               dap_feature_type_vsv, dap_feature_value_vsv_on)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_vsv, dap_feature_value_vsv_off)
    elif endpoint_id in (AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                         AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_hv, dap_feature_value_hv_on)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_hv, dap_feature_value_hv_off)

    # step 4 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def up_mix_and_sv_on_test_procedure(caller_name, endpoint_id, content_name, content_type,
                                    spk_tuning_device_name_id=dap_tuning_device_name_internal_speaker):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    # if content_type in content_type_dolby:
    #     if content_type in content_type_2_channel_dolby:
    #         logging.getLogger(endpoint_id).critical(
    #             "===== Verify up mix to 5.1 when sv on and playing {} channel Dolby content using {} ".format(
    #                 content_type, endpoint_id))
    #     else:
    #         logging.getLogger(endpoint_id).critical(
    #             "===== Verify up mix to 5.1.2 when sv on and playing {} Dolby content using {} ".format(
    #                 content_type, endpoint_id))
    # else:
    #     logging.getLogger(endpoint_id).critical(
    #         "===== Verify up mix to 5.1.2 when sv on and playing {} channel non Dolby content using {} ".format(
    #             content_type, endpoint_id))

    if endpoint_id == AUDIO_DEVICE_OUT_MONO_SPEAKER:
        logging.getLogger(endpoint_id).critical(
            "===== Verify for mono speaker endpoint")
        logging.getLogger(endpoint_id).critical(
            "=====        virtualization is always disable ")
        if content_type in content_type_dolby:
            logging.getLogger(endpoint_id).critical(
                "=====                       and UDC will do down mix task")
        logging.getLogger(endpoint_id).critical(
            "=====                              when playing {} channel content ".format(content_type))
    elif (endpoint_id == AUDIO_DEVICE_OUT_STEREO_SPEAKER) and \
            (dap_tuning_device_name_speaker_portrait == spk_tuning_device_name_id):
        logging.getLogger(endpoint_id).critical(
            "===== Verify for stereo speaker endpoint and tuning device name changed to portrait ")
        logging.getLogger(endpoint_id).critical(
            "=====        virtualization is always disable ")
        if content_type in content_type_dolby:
            logging.getLogger(endpoint_id).critical(
                "=====                       and DAP will do down mix task")
        logging.getLogger(endpoint_id).critical(
            "=====                              when playing {} channel content".format(content_type))
    else:
        if content_type in content_type_dolby:
            if content_type in content_type_2_channel_dolby:
                logging.getLogger(endpoint_id).critical(
                    "===== Verify virtualization could be turned on through calling API to turn virtual on ")
            else:
                logging.getLogger(endpoint_id).critical(
                    "===== Verify virtualization is always enabled even through call API to turn virtual on ")

            logging.getLogger(endpoint_id).critical(
                "=====       when playing {} channel Dolby content under {} ".format(content_type, endpoint_id))
        else:
            logging.getLogger(endpoint_id).critical(
                "===== Verify virtualization could be turned on through calling API to turn virtual on")
            logging.getLogger(endpoint_id).critical(
                "=====       when playing {} channel non Dolby content under {} ".format(content_type, endpoint_id))
        if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
            index = str(spk_tuning_device_name_id)
            logging.getLogger(endpoint_id).critical(
                "=====                          and {} mode".format(speaker_tuning_name[index]))
        if content_type in content_type_dolby:
            logging.getLogger(endpoint_id).critical(
                "===== and meanwhile DAP will do down mix task")

    # step 2 : change tuning device name for speaker port
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        if spk_tuning_device_name_id == dap_tuning_device_name_speaker_landscape:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                dap_tuning_port_internal_speaker,
                dap_tuning_device_name_speaker_landscape))
        elif spk_tuning_device_name_id == dap_tuning_device_name_speaker_portrait:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                dap_tuning_port_internal_speaker,
                dap_tuning_device_name_speaker_portrait))

    # step 3 : change dap feature
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        feature_test_procedure(content_name, dap_status_on, dap_profile_music,
                               dap_feature_type_vsv, dap_feature_value_vsv_on)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_vsv, dap_feature_value_vsv_on)
    elif endpoint_id in (AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                         AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_hv, dap_feature_value_hv_off)
        feature_test_procedure(content_name, dap_status_off)
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_hv, dap_feature_value_hv_on)

    # step 4 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def sv_always_enabled_in_music_profile_test_procedure(
        caller_name,
        endpoint_id,
        content_name,
        content_type,
        spk_tuning_device_name_id=dap_tuning_device_name_internal_speaker,
        sv_always_enabled=False):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_dolby:
        if content_type in content_type_2_channel_dolby:
            logging.getLogger(endpoint_id).critical(
                "===== Verify virtual could be changed in music profile ")
        else:
            logging.getLogger(endpoint_id).critical(
                "===== Verify virtual is always enabled in music profile ")

        logging.getLogger(endpoint_id).critical(
            "=====       when playing {} channel Dolby content under {} ".format(content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).critical(
            "===== Verify virtual could be changed in music profile ")
        logging.getLogger(endpoint_id).critical(
            "=====       when playing {} channel non Dolby content under {} ".format(content_type, endpoint_id))
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        index = str(spk_tuning_device_name_id)
        logging.getLogger(endpoint_id).critical(
            "=====                          and {} mode".format(speaker_tuning_name[index]))

    # step 2 : change tuning device name for speaker port
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        if spk_tuning_device_name_id == dap_tuning_device_name_speaker_landscape:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                dap_tuning_port_internal_speaker,
                dap_tuning_device_name_speaker_landscape))
        elif spk_tuning_device_name_id == dap_tuning_device_name_speaker_portrait:
            execute(adb_broadcast_intent + intent_change_dap_tuning_device.format(
                dap_tuning_port_internal_speaker,
                dap_tuning_device_name_speaker_portrait))

    # step 3 : change dap feature
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER):
        feature_test_procedure(content_name, dap_status_on, dap_profile_movie,
                               dap_feature_type_vsv, dap_feature_value_vsv_off)
        feature_test_procedure(content_name, dap_status_off)
        # even if turn off speaker virtual in music profile , for dolby content OMX would force turn on virtual again
        # and for non dolby content, virtual should be off
        feature_test_procedure(content_name, dap_status_on, dap_profile_music,
                               dap_feature_type_vsv, dap_feature_value_vsv_off)
    elif endpoint_id in (AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                         AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        feature_test_procedure(content_name, dap_status_on, dap_profile_movie,
                               dap_feature_type_hv, dap_feature_value_hv_off)
        feature_test_procedure(content_name, dap_status_off)
        # even if turn off headphone virtual in music profile , for dolby content OMX would force turn on virtual again
        # and for non dolby content, virtual should be off
        feature_test_procedure(content_name, dap_status_on, dap_profile_music,
                               dap_feature_type_hv, dap_feature_value_hv_off)

    # step 4 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def log_print_when_dap_off_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_non_dolby:
        logging.getLogger(endpoint_id).critical(
            "===== Verify no log print when dap off when playing {} channel content using {} ".format(
                content_type, endpoint_id))
    elif content_type in content_type_dolby:
        logging.getLogger(endpoint_id).critical(
            "===== Verify apply dap off profile values when dap off when playing {} channel content using {} ".format(
                content_type, endpoint_id))
    elif content_type in content_type_ac4:
        logging.getLogger(endpoint_id).critical(
            "===== Verify apply dap off profile values when dap off when playing ac4 content using {} ".format(
                endpoint_id))

    # step 2 : change dap feature
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER, AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_vsv, dap_feature_value_vsv_on)
        execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(dap_feature_type_vsv,
                                                                                   dap_feature_value_vsv_off))
    elif endpoint_id in (AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                         AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_hv, dap_feature_value_hv_on)
        execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(dap_feature_type_hv,
                                                                                   dap_feature_value_hv_off))
    time.sleep(2)
    # step 3 : clear log and turn off dap
    execute(adb_clear_log)
    time.sleep(2)
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status_off)

    # step 4 : check no log printing in stand output console
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def reference_level_when_dap_off_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    logging.getLogger(endpoint_id).critical(
        "===== Verify reference level of the output is correct when dap is disable ")
    logging.getLogger(endpoint_id).critical(
        "===== playing {} channel Dolby content using {} ".format(
            content_type, endpoint_id))

    # step 2 : turn off global dap
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                       AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                       AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        # play content
        execute(adb_broadcast_intent + intent_play_content + content_name)

        execute(adb_broadcast_intent + intent_change_dap_status + dap_status_on)

        # select a dap profile
        execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile_custom_dax3)

        # execute(adb_broadcast_intent +
        #         intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_off))
        # execute(adb_broadcast_intent +
        #         intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_on))

        execute(adb_broadcast_intent + intent_change_dap_status + dap_status_off)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def reference_level_when_dap_on_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    logging.getLogger(endpoint_id).critical(
        "===== Verify reference level of the output is correct when dap is enable")
    logging.getLogger(endpoint_id).critical(
        "===== playing {} channel Dolby content using {} ".format(
            content_type, endpoint_id))

    # step 2 : turn on global dap and volume level
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                       AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                       AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        # play content
        execute(adb_broadcast_intent + intent_play_content + content_name)

        execute(adb_broadcast_intent + intent_change_dap_status + dap_status_on)

        # select a dap profile
        execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile_custom_dax3)

        execute(adb_broadcast_intent +
                intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_off))
        execute(adb_broadcast_intent +
                intent_change_dap_high_level_feature.format(dap_feature_type_vl_dax3, dap_feature_value_vl_on))

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name, content_type)


def assert_no_log_print_when_dap_off_for_non_dolby_content(_endpoint_id):
    result = get_result_no_log_exist_when_dap_off
    if not result:
        logging.getLogger(_endpoint_id).critical("error!!! Found log relating to dap paras when dap off")
        pass
    assert result, "error!!! Found log relating to dap paras when dap off"


def assert_apply_dap_off_profile_values_when_dap_off_for_dolby_content(_endpoint_id):
    logging.getLogger(_endpoint_id).debug("===== verify apply dap off profile values for dolby content !")
    __comparison_result(_endpoint_id, content_type_51_dd, dap_off_four_cc_expected_dictionary_for_dolby_content_in_dax3)


def assert_apply_dap_off_profile_values_when_dap_off_for_ac4_content(_endpoint_id):
    logging.getLogger(_endpoint_id).debug("===== verify apply dap off profile values for ac4 content !")
    __comparison_ac4_result(
        _endpoint_id,
        content_type_ac4_ims,
        dap_off_four_cc_expected_dictionary_for_ac4_content_in_dax3)


def assert_decoding_drc_mode_related_feature_result(_content_type, _endpoint_id):
    if _content_type is None and _endpoint_id is None:
        pass


def assert_decoding_joc_down_mix_related_feature_result(_endpoint_id, _content_type, _down_mix=None):
    # the feature is related about joc content decoding
    # for non dolby content , down mix value should not exist
    # for dolby content , down mix mode settings depended on endpoint type
    # for mono speaker or blue booth , its value is 1
    # in DAX3.5, the value of force down mix with blue tooth endpoint should be changed to 0
    # always decode object for headphone, usb, stereo speaker endpoint and its value should be 0
    if _content_type in content_type_dolby:
        __assert_equal(_endpoint_id,
                       SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_JOC_FORCE_DOWN_MIX_INDEX],
                       _down_mix,
                       get_decoder_joc_force_down_mix_mode_value())
    pass


def assert_dap_mi_and_vl_related_feature_result(_endpoint_id, _content_type, _mi_expected_value,
                                                _vl_expected_value=None,
                                                _project_id=PROJECT_ID_DAX2):
    # verify mi related value is expected
    assert_dap_mi_related_feature_result(_endpoint_id, _content_type, _mi_expected_value)

    # verify volume level will always turn on for dolby content
    # assert_dap_reference_level_related_feature_result(_endpoint_id, _content_type, _vl_expected_value, _project_id)


def assert_dap_mi_related_feature_result(_endpoint_id, _content_type, _mi_expected_value):
    # verify no dap double processing
    __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)

    # verify mi related value is expected
    __comparison_result(_endpoint_id, _content_type, _mi_expected_value)


# to make decoding output level equals to -14db when dap on and -17db when dap off for dolby content ,
# volume level will always remain on even through end user click volume level button off
# But for non dolby content , the status of volume level is depending on end user settings
def assert_dap_vl_related_feature_result(_endpoint_id, _content_type, _vl_expected_value):
    # verify no dap double processing
    __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)

    if _content_type in content_type_dolby:
        vl_actual_value = get_feature_value_from_qmf_process("dvle")
        if '1' != vl_actual_value:
            logging.getLogger(_endpoint_id).critical(
                "!!!!!error: Volume leveler turned off unexpectedly when playing dolby content!")
        assert '1' == vl_actual_value, \
            "!!!!!error: Volume leveler turned off unexpectedly when playing dolby content!"
    else:
        vl_actual_value = get_feature_value_from_global_process("dvle")
        if _vl_expected_value != vl_actual_value:
            logging.getLogger(_endpoint_id).critical(
                "!!!!! error: Volume leveler should off but on when playing non dolby content!")
        assert _vl_expected_value == vl_actual_value, \
            "!!!!! error: Volume leveler should off but on when playing non dolby content!"


def assert_dap_reference_level_related_feature_result(_endpoint_id, _content_type, _ref_lvl_expected_dict,
                                                      _project_id=PROJECT_ID_DAX2):
    # __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)

    _temp_dict = _ref_lvl_expected_dict
    if _project_id == PROJECT_ID_DAX2:
        if _content_type in content_type_dolby:
            if 'vmb' in _ref_lvl_expected_dict.keys():
                _vmb_tmp_value = _ref_lvl_expected_dict['vmb']
                __comparison_vmb_result(_endpoint_id, _vmb_tmp_value)
                _temp_dict['vmb'] = '0'
                __comparison_result(_endpoint_id, _content_type, _temp_dict)
                _temp_dict['vmb'] = _vmb_tmp_value
            else:
                __comparison_result(_endpoint_id, _content_type, _ref_lvl_expected_dict)
                pass
        else:
            pass
    elif _project_id == PROJECT_ID_DAX3:
        if _content_type in content_type_dolby:
            __comparison_result(_endpoint_id, _content_type, _ref_lvl_expected_dict)
            pass
        else:
            __comparison_result(_endpoint_id, _content_type, _ref_lvl_expected_dict)
            pass


def assert_endpoint_type_in_dom_list(_endpoint_id, _dap_status):
    # for dax3 project , the second element of dom list represents the endpoint type when dap on
    #       but when dap off , the dom value is a single value for dolby content : dom = 0
    if _endpoint_id in (AUDIO_DEVICE_OUT_STEREO_SPEAKER, AUDIO_DEVICE_OUT_MONO_SPEAKER,
                        AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET,
                        AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
        if _dap_status == dap_status_on:
            if _endpoint_id in (AUDIO_DEVICE_OUT_STEREO_SPEAKER, AUDIO_DEVICE_OUT_MONO_SPEAKER):
                m_endpoint_type_expected_value = value_of_speaker_endpoint_type_in_dom
            elif _endpoint_id in (AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET, AUDIO_DEVICE_OUT_WIRED_HEADPHONE,
                                  AUDIO_DEVICE_OUT_BLUETOOTH_A2DP):
                m_endpoint_type_expected_value = value_of_headphone_endpoint_type_in_dom
            else:
                m_endpoint_type_expected_value = invalid_value_endpoint_type_in_dom

            dom_value_in_qmf_process = get_feature_value_from_qmf_process('dom')
            m_endpoint_type_actual_value = dom_value_in_qmf_process[index_endpoint_type_in_dom]
            __assert_equal(
                _endpoint_id, 'endpoint type ', m_endpoint_type_actual_value, m_endpoint_type_expected_value)
        elif _dap_status == dap_status_off:
            pass


def assert_dap_dom_related_feature_result(_endpoint_id, _content_type, _dap_dom):
    __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)
    __comparison_result(_endpoint_id, _content_type, _dap_dom)


def assert_up_mix_related_feature_result(
        _endpoint_id, _content_type, _dap_output_mode, _dap_mix_matrix, _dom,
        _down_mix=None, _tuning_device_name=dap_tuning_device_name_speaker_landscape):
    __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)

    if _content_type in content_type_dolby:
        assert_processing_mode_in_qmf_process(_endpoint_id, _dap_output_mode, _dap_mix_matrix, _dom)
        assert_processing_mode_in_global_process_for_dolby_content(_endpoint_id, _dom, _tuning_device_name)
        assert_decoding_joc_down_mix_related_feature_result(_endpoint_id, _content_type, _down_mix)
        pass
    elif _content_type in content_type_non_dolby:
        assert_processing_mode_in_global_process(_endpoint_id, _dap_output_mode, _dap_mix_matrix, _dom)
        pass


def assert_processing_mode_in_qmf_process(
        _endpoint_id,
        _dap_output_mode,
        _dap_mix_matrix,
        _dom):
    _temp_output_mode = get_dap_output_mode_set_value(content_type_51_dd)
    if _temp_output_mode is not None:
        __assert_equal(_endpoint_id,
                       SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX],
                       _dap_output_mode,
                       _temp_output_mode)

    _temp_dap_mix_matrix = get_mix_matrix_in_qmf_process()
    if _temp_dap_mix_matrix is not None:
        __assert_equal(_endpoint_id,
                       SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_MIX_MATRIX_INDEX],
                       _dap_mix_matrix,
                       _temp_dap_mix_matrix)

    # verify the dom value is correct
    __comparison_result(_endpoint_id, content_type_51_dd, _dom)


def assert_processing_mode_in_global_process_for_dolby_content(
        _endpoint_id,
        _dom,
        _tuning_device_name):
    if (_endpoint_id == AUDIO_DEVICE_OUT_STEREO_SPEAKER) and \
            (_tuning_device_name == dap_tuning_device_name_speaker_portrait):

        _temp_dom = '0' + _dom['dom'][1:]
        _temp_dom_dict = {'dom': _temp_dom}
        assert_processing_mode_in_global_process(_endpoint_id, '0', 'custom', _temp_dom_dict)
    else:
        _temp_dom = '0' + _dom['dom'][1:]
        _temp_dom_dict = {'dom': _temp_dom}
        assert_processing_mode_in_global_process(_endpoint_id, '1', 'null', _temp_dom_dict)


def assert_processing_mode_in_global_process(_endpoint_id, _dap_output_mode, _dap_mix_matrix, _dom):
    _temp_output_mode = get_output_mode_in_global_process()
    if _temp_output_mode is not None:
        __assert_equal(_endpoint_id,
                       SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX],
                       _dap_output_mode,
                       _temp_output_mode)

    _temp_dap_mix_matrix = get_mix_matrix_in_global_process()
    if _temp_dap_mix_matrix is not None:
        __assert_equal(_endpoint_id,
                       SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_MIX_MATRIX_INDEX],
                       _dap_mix_matrix,
                       _temp_dap_mix_matrix)

    # verify the dom value is correct
    actual_dom_value = get_feature_value_from_global_process('dom')
    if actual_dom_value is not None:
        __assert_equal(_endpoint_id, 'dom', _dom['dom'], actual_dom_value)


def assert_dom_value_in_global_process():
    pass


def __generate_and_parse_log_file(_caller_name, _endpoint_id, _content_name, _content_type):
    # generate log file
    temp_log_name = logFileNameFormat.format(functionName=_caller_name,
                                             endpoint_type=_endpoint_id,
                                             log_type=_content_name.replace('.', '_'))
    _current_directory = os.path.dirname(os.path.abspath(__file__))
    sv_log_file_name = abspath(join(_current_directory, 'log', _endpoint_id, temp_log_name))
    generate_log_file(sv_log_file_name)
    # parse log file
    if _content_type in content_type_2_channel_dolby:
        set_special_flag_for_specified_channel_num(flag_channel_num_equal_to_two=True)
    parse_dap_feature_value_from_log_file(sv_log_file_name)
    set_special_flag_for_specified_channel_num(flag_channel_num_equal_to_two=False)


# compare values in expected list to value pared from log
# the logic is stable for value comparison in global and qmf process
# But for value comparison in ac4 decoder, logic should be changed.
# you'd bether refer the following function
def __comparison_result(_endpoint_id, _content_type, _expected_list):
    for _four_cc_name in _expected_list.keys():
        expected_value = _expected_list[_four_cc_name]
        actual_value = get_feature_value_from_global_process(_four_cc_name)
        if _content_type in content_type_dolby:
            if _four_cc_name in CONTENT_PROCESSING_PARAM_LIST:
                actual_value = get_feature_value_from_qmf_process(_four_cc_name)
            if _four_cc_name in ['dvla', 'dvli', 'dvlo', 'vmb']:
                actual_value = get_feature_value_from_qmf_process(_four_cc_name)
        __assert_equal(_endpoint_id, _four_cc_name, expected_value, actual_value)
        assert expected_value == actual_value, \
            "{} expected value : {} but {}".format(_four_cc_name, expected_value, actual_value)


def __comparison_ac4_result(_endpoint_id, _content_type, _expected_list):
    if _content_type in content_type_ac4:
        assert isinstance(_expected_list, dict)
        for _ac4_decoder_para in _expected_list.keys():
            _expected_value = _expected_list[_ac4_decoder_para]
            _actual_value = get_feature_value_from_ac4_decoder(_ac4_decoder_para)
            if _ac4_decoder_para == "prei" and _actual_value is None:
                continue
            __assert_equal(_endpoint_id, _ac4_decoder_para, _expected_value, _actual_value)
            assert _expected_value == _actual_value, \
                "{} expected value : {} but {}".format(_ac4_decoder_para, _expected_value, _actual_value)


def __comparison_vmb_result(_endpoint_id, _vmb_expected_value):
    actual_value = get_feature_value_from_global_process('vmb')
    if _vmb_expected_value != actual_value:
        logging.getLogger(_endpoint_id).critical(
            "vmb in global process expected value : {} but {}".format(_vmb_expected_value, actual_value))
    assert _vmb_expected_value == actual_value, \
        "vmb in global process expected value : {} but {}".format(_vmb_expected_value, actual_value)


def __assert_equal(_endpoint_id, _key_word, _expected_value, _actual_value):
    # if _expected_value is None:
    #     __expected_value = 'null'
    if _expected_value != _actual_value:
        logging.getLogger(_endpoint_id).critical(
            "{} expected value : {} but {}".format(_key_word, _expected_value, _actual_value))
    assert _expected_value == _actual_value, \
        "{} expected value : {} but {}".format(_key_word, _expected_value, _actual_value)


def __assert_no_double_processing_by_content_type(_endpoint_id, _content_type):
    if _content_type in content_type_dolby:
        no_double_processing_result = verify_no_double_processing_dap_parameter(True)
        if not no_double_processing_result:
            logging.getLogger(_endpoint_id).critical("!!!!!! double processing error for dolby content !")
        assert no_double_processing_result, "!!!!!! double processing error for dolby content!"
    else:
        no_double_processing_result = verify_no_double_processing_dap_parameter(False)
        if not no_double_processing_result:
            logging.getLogger(_endpoint_id).critical("!!!!!! double processing error for non-dolby content !")
        assert no_double_processing_result, "!!!!!! double processing error for non-dolby content !"
