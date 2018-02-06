from constant import *

# define test data
# ************************************************************************************
# ************************************************************************************
# *****************     test data for be feature        ******************************
# ************************************************************************************
# ************************************************************************************
be_on_test_data = [
    ('stereo_channel_id.wav', False, dap_status_on, dap_profile_custom,
     dap_feature_type_be, dap_feature_value_be_on),
    ('stereo_dd_25fps_channel_id.m4a', True, dap_status_on, dap_profile_custom,
     dap_feature_type_be, dap_feature_value_be_on)
]
be_on_expected_value_speaker_endpoint = {'beon': '1', 'vbon': '1'}
be_on_expected_value_except_speaker_endpoint = {'beon': '1', 'vbon': '0'}
be_off_test_data = [
    ('stereo_dd_25fps_channel_id.m4a', True, dap_status_on, dap_profile_custom,
     dap_feature_type_be, dap_feature_value_be_off),
    ('stereo_channel_id.wav', False, dap_status_on, dap_profile_custom,
     dap_feature_type_be, dap_feature_value_be_off)
]
be_off_expected_value = {'beon': '0', 'vbon': '0'}

# ************************************************************************************
# ************************************************************************************
# *****************     test data for mi feature        ******************************
# ************************************************************************************
# ************************************************************************************
mi_on_2_channel_dolby_test_data = [
    ('stereo_dd_25fps_channel_id.m4a', '2', dap_status_on, dap_profile_dynamic, None, None)
]
mi_on_2_channel_expected_result = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}

mi_on_multi_channel_dolby_test_data = [
    ('7ch_ddp_25fps_diff_music_01.mp4', '3', dap_status_on, dap_profile_dynamic, None, None)
]
mi_on_multi_channel_expected_result = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}

mi_on_non_dolby_test_data = [
    ('2ch_channel_id.wav', '1', dap_status_on, dap_profile_dynamic, None, None)
]
mi_on_non_dolby_content_expected_result = {'msce': '1', 'mdee': '1', 'miee': '1', 'mdle': '1', 'mave': '1'}

mi_off_test_data = [
    ('stereo_dd_25fps_channel_id.m4a', True, dap_status_on, dap_profile_movie, None, None),
    ('2ch_channel_id.wav', False, dap_status_on, dap_profile_music, None, None),
    ('7ch_ddp_25fps_diff_music_01.mp4', True, dap_status_on, dap_profile_custom, None, None)
]
mi_off_expected_result = {'msce': '0', 'mdee': '0', 'miee': '0', 'mdle': '0', 'mave': '0'}
