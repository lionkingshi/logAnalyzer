import subprocess
from constant import *
import time
from filter_para import *

logger_name = ''
endpoint_type = 'unknown'
log_analysis_instance = LogComparison()


# register a logging manager name
def register_logger_name(_logger_name):
    global logger_name
    logger_name = _logger_name
    global endpoint_type
    endpoint_type = _logger_name
    log_analysis_instance.set_logger_name(_logger_name)


# common serial action : play content -> change dap parameter -> save log to a specified file for later analysis
def feature_test_procedure(content_name, dap_status, dap_profile=None, dap_feature_type=None, dap_feature_value=None):
    # play content
    execute(adb_broadcast_intent + intent_play_content + content_name)
    # time.sleep(1)
    # change dap status
    if dap_status == dap_status_on:
        execute(adb_broadcast_intent + intent_change_dap_status + dap_status)
        # time.sleep(1)
        # select a dap profile
        execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile)
        # time.sleep(1)
        # change dap parameter
        if dap_feature_type is not None:
            if dap_feature_type == dap_feature_type_gebg:
                execute(
                    adb_broadcast_intent + intent_change_dap_gebg_feature.format(dap_feature_type, dap_feature_value))
            elif len(dap_feature_type) == 4:
                execute(adb_broadcast_intent + intent_change_dap_low_level_feature.format(dap_feature_type,
                                                                                          dap_feature_value))
            else:
                execute(adb_broadcast_intent + intent_change_dap_high_level_feature.format(dap_feature_type,
                                                                                           dap_feature_value))
                # time.sleep(1)
        # do nothing
        execute(adb_broadcast_intent + "--es step record_log ")
        # time.sleep(1)
    else:
        # turn off dap and no need to update parameters again
        execute(adb_broadcast_intent + intent_change_dap_status + dap_status)
        # time.sleep(1)
        # select a dap profile
        # execute(adb_broadcast_intent + intent_change_dap_profile + dap_profile_music)


# capture the adb log cat stand output to a specified file
def generate_log_file(output_file_name):
    # wait for log flush
    time.sleep(SLEEP_TIME_BEFORE_RECORD_LOG)
    # save log to a file
    execute(adb_record_log + output_file_name)
    #
    if not exists(output_file_name):
        logging.getLogger(logger_name).error("!!!!! failed to capture output from adb logcat to a file")
    else:
        logging.getLogger(logger_name).info("===== Succeed to capture output from adb logcat to a file")
        pass


# parse dap feature value from log file
def parse_dap_feature_value_from_log_file(log_file_name):
    # first specified the log file we want to filter effect parameters
    log_file_abs_path_except_extension = log_file_name[:-4]
    logging.getLogger(logger_name).info("specified log file : %s" % log_file_name)
    # specified the output file name , and default it will be saved at current location
    effect_paras_output_file_abs_path = abspath(log_file_abs_path_except_extension + "_effect_params_from_log.txt")
    arendered_param_output_file_abs_path = abspath(
        log_file_abs_path_except_extension + "_arendered_params_from_log.txt")
    dap_global_cp_dp_param_output_file_abs_path = \
        abspath(log_file_abs_path_except_extension + "_dap_global_cp_dp_from_log.txt")
    dap_qmf_cp_dp_param_output_file_abs_path = abspath(
        log_file_abs_path_except_extension + "_dap_qmf_cp_dp_from_log.txt")
    logging.getLogger(logger_name).debug(
        "effect para in global process saved at : %s" % effect_paras_output_file_abs_path)
    logging.getLogger(logger_name).debug(
        "effect para in qmf process saved at : %s" % arendered_param_output_file_abs_path)
    logging.getLogger(logger_name).debug(
        "dap global cp and dp para saved at : %s" % dap_global_cp_dp_param_output_file_abs_path)
    logging.getLogger(logger_name).debug(
        "dap qmf cp and dp para saved at : %s" % dap_qmf_cp_dp_param_output_file_abs_path)
    # global log_analysis_instance
    # log_analysis_instance = LogComparison(endpoint_type)
    log_analysis_instance.filter_para_from_log(log_file_name,
                                               effect_paras_output_file_abs_path,
                                               arendered_param_output_file_abs_path,
                                               dap_global_cp_dp_param_output_file_abs_path,
                                               dap_qmf_cp_dp_param_output_file_abs_path)


# special handle for 2 channel content when creating binary command line
def set_special_flag_for_specified_channel_num(flag_channel_num_equal_to_two=False):
    log_analysis_instance.set_special_flag_for_specified_channel_num(flag_channel_num_equal_to_two)


def get_result_no_log_exist_when_dap_off():
    return verify_all_dap_parameters_equals_to_non_exist()


# check no double processing for dolby content and no qmf processing for non dolby content
def verify_no_double_processing_dap_parameter(content_type):
    no_double_process_result = False
    # True will be treated as dolby content
    if content_type:
        no_double_process_result = log_analysis_instance.verify_no_double_processing_effect_for_dolby_content()
    else:
        # False will be treated as non dolby content
        no_double_process_result = log_analysis_instance.verify_no_double_processing_effect_for_non_dolby_content()

    return no_double_process_result


# return a specified feature value from global process
def get_feature_value_from_global_process(effect_fourcc_name=None):
    return log_analysis_instance.get_parameter_value_in_global_process(effect_fourcc_name)


# return a specified feature value from qmf process
def get_feature_value_from_qmf_process(effect_fourcc_name=None):
    return log_analysis_instance.get_parameter_value_in_qmf_process(effect_fourcc_name)


#
def get_decoder_joc_force_down_mix_mode_value():
    return log_analysis_instance.get_decoder_joc_force_down_mix_mode_value_in_ddp_joc_decoder()


#
def get_dap_output_mode_set_value(_content_type):
    if _content_type in content_type_dolby:
        # for dolby content decoded by udc decoder , dap2qmf instance will be created
        return log_analysis_instance.get_dap_output_mode_set_value_in_qmf_process()
    else:
        # for non dolby content , global processing will process up mix and down mix
        return log_analysis_instance.get_dap_output_mode_set_value_in_global_process()


def get_output_mode_in_qmf_process():
    return log_analysis_instance.get_dap_output_mode_set_value_in_qmf_process()


def get_output_mode_in_global_process():
    return log_analysis_instance.get_dap_output_mode_set_value_in_global_process()


#
def get_dap_output_mode_mix_matrix():
    return log_analysis_instance.get_dap_output_mode_mix_matrix()


def get_mix_matrix_in_qmf_process():
    return log_analysis_instance.get_mix_matrix_in_qmf_process()


def get_mix_matrix_in_global_process():
    return log_analysis_instance.get_mix_matrix_in_global_process()


def contain_string(files, string):
    rtn = False
    try:
        f = open(files, 'r')
        try:
            lines = f.readlines()
            for line in lines:
                if string in line:
                    rtn = True
        finally:
            f.close()
    except Exception as e:
        print(files, e)

    return rtn


def execute(cmd):
    # prc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # return prc.communicate()[0]
    return_code = subprocess.call(cmd, shell=True)
    logging.getLogger(logger_name).info("===== run command : %s " % cmd)
    # print cmd + ' return result : ' + str(return_code)
    return return_code
