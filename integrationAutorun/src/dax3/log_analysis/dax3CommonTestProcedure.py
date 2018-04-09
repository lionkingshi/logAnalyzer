from tools.common import *
from tools.logger import *
from src.dax3.log_analysis.dax3XMLParser.XMLUpdater import *


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

    if content_type in content_type_dolby:
        index = int(_tuning_device_name)
        logging.getLogger(endpoint_id).info(
            "===== Verify {} profile default values when playing {} Dolby content using {} and {} mode".format(
                _profile_name, content_type, endpoint_id, tuning_endpoint_name[index]))
    else:
        index = int(_tuning_device_name)
        logging.getLogger(endpoint_id).info(
            "===== Verify {} profile default values when playing {} non Dolby content using {} and {} mode".format(
                _profile_name, content_type, endpoint_id, tuning_endpoint_name[index]))

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
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)


def assert_specified_profile_default_values_result(_profile_name, tuning_device_name,
                                                   _endpoint_type=AUDIO_DEVICE_OUT_STEREO_SPEAKER):
    post_para_dict_from_log = get_feature_value_from_global_process()
    if _endpoint_type == AUDIO_DEVICE_OUT_MONO_SPEAKER:
        default_xml_file_name = abspath(join('.', 'dax3XMLParser', 'mono', 'dax3-default-mono-speaker.xml'))
    else:
        default_xml_file_name = abspath(join('.', 'dax3XMLParser', 'stereo', 'dax3-default-stereo-speaker.xml'))
    xml_parser_class = TuningFileParser(default_xml_file_name)
    post_para_dict_from_xml = xml_parser_class.print_expect_value(_profile_name=_profile_name,
                                                                  tuning_device_name_endpoint=tuning_device_name)

    for __index in range(len(PARA_LIST_IN_GLOBAL_PROCESS)):
        four_cc_name = PARA_LIST_IN_GLOBAL_PROCESS[__index]
        assert isinstance(post_para_dict_from_xml[four_cc_name], str)
        assert isinstance(post_para_dict_from_log[four_cc_name], str)
        if four_cc_name not in ('vcbf', 'preg', 'pstg', 'vol'):
            if four_cc_name == 'ceqt':
                if len(post_para_dict_from_xml[four_cc_name]) == len(post_para_dict_from_log[four_cc_name]):
                    logging.getLogger(_endpoint_type).info("ceqt length from log and xml is equals : {} !".format(
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
                        post_para_dict_from_log[four_cc_name][:-1])
            else:
                # for custom profile , ieq status is off and iebs values remains as previous
                if _profile_name == profile_name[3]:
                    if four_cc_name == 'iebs':
                        continue

                __assert_equal(
                    _endpoint_type,
                    four_cc_name,
                    post_para_dict_from_xml[four_cc_name],
                    post_para_dict_from_log[four_cc_name])
        pass
    logging.getLogger(_endpoint_type).info(
        "====== {} profile default params are same as one parsing from xml !!!!!".format(_profile_name))


def be_test_procedure_dax3(caller_name, endpoint_id, content_name, content_type, dap_feature_value):
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
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_be_dax3, dap_feature_value_be_off)
    else:
        feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                               dap_feature_type_be_dax3, dap_feature_value_be_on)

    feature_test_procedure(content_name, dap_status_on, dap_profile_custom_dax3,
                           dap_feature_type_be_dax3, dap_feature_value)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)
    # print ("module name is :" + __name__)
    # step 4 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    # __assert_no_double_processing_by_content_type(content_type)
    #
    # if dap_feature_value == dap_feature_value_be_on:
    #     if (endpoint_id == AUDIO_DEVICE_OUT_MONO_SPEAKER) \
    #             or (endpoint_id == AUDIO_DEVICE_OUT_STEREO_SPEAKER):
    #         __comparison_result(content_type, be_on_expected_value_speaker_endpoint)
    #     else:
    #         __comparison_result(content_type, be_on_expected_value_except_speaker_endpoint)
    # elif dap_feature_value == dap_feature_value_be_off:
    #     __comparison_result(content_type, be_off_expected_value)


def assert_dap_be_related_feature_result(endpoint_id, _content_type, _be_value_dict):
    __assert_no_double_processing_by_content_type(endpoint_id, _content_type)
    __comparison_result(endpoint_id, _content_type, _be_value_dict)


def mi_off_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile, ):
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
    # __assert_no_double_processing_by_content_type(content_type)
    #
    # __comparison_result(content_type, mi_off_expected_result)


def mi_on_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile,
                         _project_id=PROJECT_ID_DAX2):
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

    # step 2 : change to dynamic profile
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file and parse dap parameter from log
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dynamic_' + content_name)

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
    __generate_and_parse_log_file(caller_name, endpoint_id, 'vl_off_' + content_name)

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
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dap_off_' + content_name)
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
    __generate_and_parse_log_file(caller_name, endpoint_id, 'dap_on_' + content_name)
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

    if content_type in content_type_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify no up mix when sv off and playing {} Dolby content using {} ".format(
                content_type, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify no up mix when sv off and playing {} channel non Dolby content using {} ".format(
                content_type, endpoint_id))

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
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)

    # step 5 : verify dap feature is correct or not , and include below step :
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct
    # __assert_no_double_processing_by_content_type(content_type)
    # __assert_dap_output_mode_setting(content_type, endpoint_id, dap_feature_value_vsv_off)
    #
    # __comparison_result(content_type, up_mix_and_sv_off_expected_value)


def up_mix_and_sv_on_test_procedure(caller_name, endpoint_id, content_name, content_type,
                                    spk_tuning_device_name_id=dap_tuning_device_name_internal_speaker):
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
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)

    # step 5 : verify dap feature is correct or not , and include below step
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


def log_print_when_dap_off_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if content_type in content_type_non_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify no log print when dap off when playing {} channel content using {} ".format(
                content_type, endpoint_id))
    elif content_type in content_type_non_dolby:
        logging.getLogger(endpoint_id).info(
            "===== Verify apply dap off profile values when dap off when playing {} channel content using {} ".format(
                content_type, endpoint_id))

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
    execute(adb_broadcast_intent + intent_change_dap_status + dap_status_off)

    # step 4 : check no log printing in stand output console
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)
    # assert_no_log_print_when_dap_off(endpoint_id)


def reference_level_when_dap_off_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    logging.getLogger(endpoint_id).info(
        "===== Verify the output reference level is correct when dap is disable ")
    logging.getLogger(endpoint_id).info(
        "===== playing {} channel Dolby content using {} ".format(
            content_type, endpoint_id))

    # step 2 : turn off global dap
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                       AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET):
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
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)


def reference_level_when_dap_on_test_procedure(caller_name, endpoint_id, content_name, content_type):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    logging.getLogger(endpoint_id).info(
        "===== Verify the output reference level is correct when dap is enable")
    logging.getLogger(endpoint_id).info(
        "===== playing {} channel Dolby content using {} ".format(
            content_type, endpoint_id))

    # step 2 : turn on global dap and volume level
    if endpoint_id in (AUDIO_DEVICE_OUT_MONO_SPEAKER, AUDIO_DEVICE_OUT_STEREO_SPEAKER,
                       AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET):
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
    __generate_and_parse_log_file(caller_name, endpoint_id, content_name)


def assert_no_log_print_when_dap_off_for_non_dolby_content(_endpoint_id):
    result = get_result_no_log_exist_when_dap_off
    if not result:
        logging.getLogger(_endpoint_id).critical("error!!! Found log relating to dap paras when dap off")
        pass
    assert result, "error!!! Found log relating to dap paras when dap off"


def assert_apply_dap_off_profile_values_when_dap_off_for_dolby_content(_endpoint_id):
    logging.getLogger(_endpoint_id).debug("===== verify apply dap off profile values for dolby content !")
    __comparison_result(_endpoint_id, content_type_51_dd, dap_off_four_cc_expected_dictionary_for_dolby_content_in_dax3)


def assert_decoding_drc_mode_related_feature_result(_content_type, _endpoint_id):
    pass


def assert_decoding_joc_down_mix_related_feature_result(_endpoint_id, _content_type, _down_mix=None):
    # the feature is related about joc content decoding
    # for non dolby content , down mix value should not exist
    # for dolby content , down mix mode settings depended on endpoint type
    # for mono speaker or blue booth , its value is 1
    # always decode object for headphone, usb, stereo speaker endpoint and its value should be 0
    if _content_type in content_type_dolby:
        __assert_equal(_endpoint_id,
                       SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_JOC_FORCE_DOWN_MIX_INDEX],
                       _down_mix,
                       get_decoder_joc_force_down_mix_mode_value())
    pass


def assert_dap_mi_and_vl_related_feature_result(_endpoint_id, _content_type, _mi_expected_value, _vl_expected_value,
                                                _project_id=PROJECT_ID_DAX2):
    # verify mi related value is expected
    assert_dap_mi_related_feature_result(_endpoint_id, _content_type, _mi_expected_value)

    # verify volume level will always turn on for dolby content
    assert_dap_reference_level_related_feature_result(_endpoint_id, _content_type, _vl_expected_value, _project_id)


def assert_dap_mi_related_feature_result(_endpoint_id, _content_type, _mi_expected_value):
    # verify no dap double processing
    __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)

    # verify mi related value is expected
    __comparison_result(_endpoint_id, _content_type, _mi_expected_value)

    # if _mi_expected_value:
    #     if _content_type in content_type_2_channel_dolby:
    #         __comparison_result(_content_type, mi_on_2_channel_expected_result)
    #     elif _content_type in content_type_dolby:
    #         __comparison_result(_content_type, mi_on_multi_channel_expected_result)
    #     else:
    #         __comparison_result(_content_type, mi_on_non_dolby_content_expected_result)
    # else:
    #     __comparison_result(_content_type, mi_off_expected_result)


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
    __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)

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
                        AUDIO_DEVICE_OUT_WIRED_HEADPHONE, AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET):
        if _dap_status == dap_status_on:
            if _endpoint_id in (AUDIO_DEVICE_OUT_STEREO_SPEAKER, AUDIO_DEVICE_OUT_MONO_SPEAKER):
                m_endpoint_type_expected_value = endpoint_type_speaker_in_dom
            elif _endpoint_id in (AUDIO_DEVICE_OUT_DGTL_DOCK_HEADSET, AUDIO_DEVICE_OUT_WIRED_HEADPHONE):
                m_endpoint_type_expected_value = endpoint_type_headphone_in_dom
            dom_value_in_qmf_process = get_feature_value_from_qmf_process('dom')
            m_endpoint_type_actual_value = dom_value_in_qmf_process[endpoint_type_index_in_dom]
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


# def assert_up_mix_related_feature_result(
#         _endpoint_id, _content_type, _dap_output_mode, _dap_mix_matrix, _dom, _down_mix=None):
#     __assert_no_double_processing_by_content_type(_endpoint_id, _content_type)
#
#     if _content_type in content_type_dolby:
#         # for dolby content , output mode value should print in qmf process
#         _output_mode_in_process = DAP_OUT_PUT_MODE_FOR_DOLBY_CONTENT_INDEX
#         temp_down_mix = _down_mix
#     else:
#         # for non dolby content , output mode value should print in global process
#         _output_mode_in_process = DAP_OUT_PUT_MODE_FOR_NON_DOLBY_CONTENT_INDEX
#         # for non dolby content , down mix value should not exist
#         temp_down_mix = None
#
#     _temp_output_mode = get_dap_output_mode_set_value(_content_type)
#
#     if _temp_output_mode is not None or _content_type in content_type_dolby:
#         __assert_equal(_endpoint_id,
#                        SPECIFIED_FEATURE_KEY_WORDS_LIST[_output_mode_in_process],
#                        _dap_output_mode,
#                        _temp_output_mode)
#         __assert_equal(_endpoint_id,
#                        SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_MIX_MATRIX_INDEX],
#                        _dap_mix_matrix,
#                        get_dap_output_mode_mix_matrix())
#         __assert_equal(_endpoint_id,
#                        SPECIFIED_FEATURE_KEY_WORDS_LIST[DAP_JOC_FORCE_DOWN_MIX_INDEX],
#                        temp_down_mix,
#                        get_decoder_joc_force_down_mix_mode_value())
#
#     # verify the dom value is correct
#     __comparison_result(_endpoint_id, _content_type, _dom)


def assert_dom_value_in_global_process():
    pass


def __generate_and_parse_log_file(_caller_name, _endpoint_id, _content_name):
    # generate log file
    temp_log_name = logFileNameFormat.format(functionName=_caller_name,
                                             endpoint_type=_endpoint_id,
                                             log_type=_content_name.replace('.', '_'))
    sv_log_file_name = abspath(join('.', 'log', _endpoint_id, temp_log_name))
    generate_log_file(sv_log_file_name)
    # parse log file
    parse_dap_feature_value_from_log_file(sv_log_file_name)


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
