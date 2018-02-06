from tools.common import *
from tools.logger import *


def be_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_feature_value):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)

    if dap_feature_value == dap_feature_value_be_on:
        tmp_status = 'on'
    else:
        tmp_status = 'off'
    if content_type:
        logging.getLogger(endpoint_id).info(
            "===== Verify VB & BE are {} when playing Dolby content using {} ".format(tmp_status, endpoint_id))
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify VB & BE are {} when playing non Dolby content using {} ".format(tmp_status, endpoint_id))

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status_on, dap_profile_custom,
                           dap_feature_type_be, dap_feature_value)

    # step 3 : capture adb log to a file
    # print ("module name is :" + __name__)
    # print ("function name is :" + test_log_bass_on_verify.__name__)
    # temp_log_type = dap_feature_type + '_' + dap_feature_value + '_' + content_name.replace('.', '_')
    temp_log_name = logFileNameFormat.format(functionName=caller_name,
                                             endpoint_type=endpoint_id,
                                             log_type=content_name.replace('.', '_'))
    be_log_file_name = abspath(join('.', 'log', endpoint_id, temp_log_name))
    generate_log_file(be_log_file_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    parse_dap_feature_value_from_log_file(be_log_file_name)

    verify_no_double_processing_dap_parameter(content_type)

    if dap_feature_value == dap_feature_value_be_on:
        if (endpoint_id == 'mono_speaker') or (endpoint_id == 'stereo_speaker'):
            for be_four_cc_name in be_on_expected_value_speaker_endpoint.keys():
                expected_value = be_on_expected_value_speaker_endpoint[be_four_cc_name]
                actual_data = get_feature_value_from_global_process(be_four_cc_name)
                assert expected_value == actual_data, \
                    "{} expected value : {} but {}".format(be_four_cc_name, expected_value, actual_data)
        else:
            for be_four_cc_name in be_on_expected_value_except_speaker_endpoint.keys():
                expected_value = be_on_expected_value_except_speaker_endpoint[be_four_cc_name]
                actual_data = get_feature_value_from_global_process(be_four_cc_name)
                assert expected_value == actual_data, \
                    "{} expected value : {} but {}".format(be_four_cc_name, expected_value, actual_data)
    elif dap_feature_value == dap_feature_value_be_off:
        for be_four_cc_name in be_off_expected_value.keys():
            expected_value = be_off_expected_value[be_four_cc_name]
            actual_data = get_feature_value_from_global_process(be_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(be_four_cc_name, expected_value, actual_data)


def mi_off_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)
    if content_type:
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is off when playing Dolby content using %s " % endpoint_id)
    else:
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is off when playing non Dolby content using {} ".format(endpoint_id))

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file
    temp_log_name = logFileNameFormat.format(functionName=caller_name,
                                             endpoint_type=endpoint_id,
                                             log_type=content_name.replace('.', '_'))
    be_log_file_name = abspath(join('.', 'log', endpoint_id, temp_log_name))
    generate_log_file(be_log_file_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    parse_dap_feature_value_from_log_file(be_log_file_name)

    verify_no_double_processing_dap_parameter(content_type)

    for mi_four_cc_name in mi_off_expected_result.keys():
        temp_data = get_feature_value_from_global_process(mi_four_cc_name)
        assert mi_off_expected_result[mi_four_cc_name] == temp_data, \
            "{} expected value : 0 but {}".format(mi_four_cc_name, temp_data)


def mi_on_dolby_content_test_procedure(caller_name, endpoint_id, content_name, content_type, dap_status, dap_profile):
    # step 1 :register logger name to record all command to logger file except session setup() function
    register_logger_name(endpoint_id)
    # 2 is treated as 2 channel dolby content
    if content_type == '2':
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is on when playing 2 channel Dolby content using %s " % endpoint_id)
    elif content_type == '3':
        # 3 is treated as multiple channel dolby content
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is on when playing multi channel Dolby content using {} ".format(endpoint_id))
    elif content_type == '1':
        # 1 is treated as non dolby content
        logging.getLogger(endpoint_id).info(
            "===== Verify mi steer is on when playing non Dolby content using {} ".format(endpoint_id))

    # step 2 : change dap feature
    feature_test_procedure(content_name, dap_status, dap_profile)

    # step 3 : capture adb log to a file
    temp_log_name = logFileNameFormat.format(functionName=caller_name,
                                             endpoint_type=endpoint_id,
                                             log_type=content_name.replace('.', '_'))
    temp_log_file_name = abspath(join('.', 'log', endpoint_id, temp_log_name))
    generate_log_file(temp_log_file_name)

    # step 4 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    parse_dap_feature_value_from_log_file(temp_log_file_name)

    if content_type != '1':
        verify_no_double_processing_dap_parameter(True)
    else:
        verify_no_double_processing_dap_parameter(False)

    if content_type == '2':
        for mi_four_cc_name in mi_on_2_channel_expected_result.keys():
            expected_value = mi_on_2_channel_expected_result[mi_four_cc_name]
            actual_data = get_feature_value_from_qmf_process(mi_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(mi_four_cc_name, expected_value, actual_data)
    elif content_type == '3':
        for mi_four_cc_name in mi_on_multi_channel_expected_result.keys():
            expected_value = mi_on_multi_channel_expected_result[mi_four_cc_name]
            actual_data = get_feature_value_from_qmf_process(mi_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(mi_four_cc_name, expected_value, actual_data)
    elif content_type == '1':
        for mi_four_cc_name in mi_on_non_dolby_content_expected_result.keys():
            expected_value = mi_on_non_dolby_content_expected_result[mi_four_cc_name]
            actual_data = get_feature_value_from_global_process(mi_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(mi_four_cc_name, expected_value, actual_data)

    if content_type != '1':
        vl_actual_value = get_feature_value_from_qmf_process("dvle")
        assert '1' == vl_actual_value, "Volume leveler change to turn off for dolby content !"

    # step 5 : even through changing volume level , values should always be true
    # to make qmf output level from line-mode -31db to portable mode -14db
    execute(adb_broadcast_intent +
            intent_change_dap_high_level_feature.format(dap_feature_type_vl, dap_feature_value_vl_off))

    # step 6 : capture adb log to a file
    generate_log_file(temp_log_file_name)

    # step 7 : verify dap feature is correct or not , and include below step :
    # parse dap parameter from log
    #                     -->check no double processing for dolby content
    #                     -->check no qmf processing for non dolby content
    #                            --> check specified dap feature value is correct

    parse_dap_feature_value_from_log_file(temp_log_file_name)

    if content_type != '1':
        verify_no_double_processing_dap_parameter(True)
    else:
        verify_no_double_processing_dap_parameter(False)

    if content_type == '2':
        for mi_four_cc_name in mi_on_2_channel_expected_result.keys():
            expected_value = mi_on_2_channel_expected_result[mi_four_cc_name]
            actual_data = get_feature_value_from_qmf_process(mi_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(mi_four_cc_name, expected_value, actual_data)
    elif content_type == '3':
        for mi_four_cc_name in mi_on_multi_channel_expected_result.keys():
            expected_value = mi_on_multi_channel_expected_result[mi_four_cc_name]
            actual_data = get_feature_value_from_qmf_process(mi_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(mi_four_cc_name, expected_value, actual_data)
    elif content_type == '1':
        for mi_four_cc_name in mi_on_non_dolby_content_expected_result.keys():
            expected_value = mi_on_non_dolby_content_expected_result[mi_four_cc_name]
            actual_data = get_feature_value_from_global_process(mi_four_cc_name)
            assert expected_value == actual_data, \
                "{} expected value : {} but {}".format(mi_four_cc_name, expected_value, actual_data)

    if content_type != '1':
        vl_actual_value = get_feature_value_from_qmf_process("dvle")
        assert '1' == vl_actual_value, "Volume leveler change to turn off for dolby content !"
    else :
        vl_actual_value = get_feature_value_from_global_process("dvle")
        assert '0' == vl_actual_value, "Volume leveler should off but on for non dolby content !"


# def mi_on_non_dolby_content_test_procedure():