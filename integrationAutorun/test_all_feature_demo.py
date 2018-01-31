# import os
# import inspect
# import pytest
# import time
# from common import *
#
# base_str = 'DapVLLDPProcess: setParam({0} = {1})'
# feature_test_data = [
#     ['stereo_channel_id.wav', dap_status_on, dap_profile_custom,
#      dap_feature_type_de, dap_feature_value_de_on, dap_feature_value_de_on],
#     ['silent5p1joc.mp4', dap_status_on, dap_profile_custom,
#      dap_feature_type_ieq, dap_feature_value_ieq_open, dap_feature_value_de_on],
#     ['stereo_dd_25fps_channel_id.m4a', dap_status_on, dap_profile_custom,
#      dap_feature_type_ieq, dap_feature_value_ieq_off, dap_feature_value_de_on],
#     ['stereo_channel_id.wav', dap_status_on, dap_profile_custom,
#      dap_feature_type_hv, dap_feature_value_hv_on, dap_feature_value_de_on],
#     ['silent5p1joc.mp4', dap_status_on, dap_profile_custom,
#      dap_feature_type_vsv, dap_feature_value_vsv_on, dap_feature_value_de_on],
#     ['stereo_dd_25fps_channel_id.m4a', dap_status_on, dap_profile_custom,
#      dap_feature_type_vl, dap_feature_value_vl_on, dap_feature_value_de_on],
#     ['stereo_channel_id.wav', dap_status_on, dap_profile_custom,
#      dap_feature_type_be, dap_feature_value_be_on, dap_feature_value_de_on],
#     ['silent5p1joc.mp4', dap_status_on, dap_profile_custom,
#      dap_feature_type_geq, dap_feature_value_geq_on, dap_feature_value_de_on],
#     ['stereo_dd_25fps_channel_id.m4a', dap_status_on, dap_profile_custom,
#      dap_feature_type_reset_universal_para, dap_feature_value_reset_universal_para, dap_feature_value_de_on],
#     ['stereo_channel_id.wav', dap_status_on, dap_profile_custom,
#      dap_feature_type_reset_profile, dap_profile_custom, dap_feature_value_de_on],
#     ['silent5p1joc.mp4', dap_status_on, dap_profile_custom,
#      dap_feature_type_reset_profile, dap_feature_value_reset_profile_all, dap_feature_value_de_on],
# ]
#
# gebg_test_data = [
#     ['silent5p1joc.mp4', dap_status_on, dap_profile_custom, dap_feature_type_gebg,
#      '3,3,3,3,13,13,13,13,23,23,15,15,15,15,5,5,5,5,25,25', '2'],
#     ['stereo_channel_id.wav', dap_status_on, dap_profile_custom, dap_feature_type_gebg,
#      '13,13,13,13,23,23,23,23,33,33,15,15,15,15,25,25,25,25,35,35', '1'],
#     ['stereo_dd_25fps_channel_id.m4a', dap_status_on, dap_profile_custom, dap_feature_type_gebg,
#      '113,113,113,113,103,103,103,103,123,123,115,115,115,115,105,105,105,105,125,125', '3'],
# ]
#
# de_speaker_test_data = [
#     ('stereo_channel_id.wav', dap_status_on, dap_profile_custom, 'dvle', '113', '113'),
# ]
#
# de_headphone_test_data = [
#     ('stereo_channel_id.wav', dap_status_on, dap_profile_custom, 'dvle', '0', '0'),
# ]
#
# de_bluetooth_test_data = [
#     ('stereo_channel_id.wav', dap_status_on, dap_profile_custom, 'dvle', '116', '116'),
# ]
#
#
# def feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str):
#     execute(adb_broadcast_intent + intent_play_content + content_name)
#     time.sleep(1)
#     execute(adb_broadcast_intent + intent_change_dap_status + dap_status)
#     time.sleep(1)
#     execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile)
#     time.sleep(1)
#     if dap_feature_type == dap_feature_type_gebg:
#         execute(adb_broadcast_intent + intent_change_dap_gebg_feature.format(dap_feature_type, dap_feature_value))
#     elif len(dap_feature_type) == 4:
#         execute(adb_broadcast_intent + intent_change_dap_low_level_feature.format(dap_feature_type, dap_feature_value))
#     else:
#         execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(dap_feature_type, dap_feature_value))
#     time.sleep(1)
#     execute(adb_broadcast_intent + "--es step record_log ")
#     time.sleep(1)
#     current_method_name = inspect.stack()[1][3]
#     log_file_name = logFileLocation + current_method_name + '_' + dap_feature_type + '_' + \
#                     dap_feature_value + '_' + content_name.replace('.', '_') + '.txt'
#     print log_file_name
#     print os.getcwd()
#     print __file__
#     time.sleep(SLEEP_TIME_BEFORE_RECORD_LOG)
#     execute(adb_record_log + log_file_name)
#     # assert isinstance(expected_str, object)
#     result = contain_string(log_file_name, base_str.format(dap_feature_type, expected_str))
#     print 'expected string is : ' + base_str.format(dap_feature_type, expected_str)
#     print 'expected string contain in log file :' + str(result)
#     if result is False:
#         assert 0
#
#
# @pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value, expected_str',
#                          feature_test_data)
# def test_not_gebg_feature_speaker(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value,
#                                   expected_str):
#     feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str)
#
#
# @pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value, expected_str',
#                          gebg_test_data)
# def test_gebg_feature_speaker(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str):
#     feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str)
#
#
# @pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value, expected_str',
#                          de_speaker_test_data)
# def test_de_feature_speaker(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str):
#     feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str)
#
#
# @pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value, expected_str',
#                          de_headphone_test_data)
# def test_de_feature_headphone(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str):
#     feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str)
#
#
# @pytest.mark.parametrize('content_name,dap_status,dap_profile,dap_feature_type,dap_feature_value, expected_str',
#                          de_bluetooth_test_data)
# def test_de_feature_bluetooth(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str):
#     feature_test_procedure(content_name, dap_status, dap_profile, dap_feature_type, dap_feature_value, expected_str)
