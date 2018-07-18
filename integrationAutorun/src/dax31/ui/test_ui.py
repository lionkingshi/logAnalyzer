from src.dax31.ui.testconfig.ui_config import *
from tools.common import *
from tools.logger import Logger
from tools.util import *

# register the logging configuration
test_type_in_module = "ui"
_ui_current_directory = dirname(realpath(__file__))
logging_file_name = abspath(join(_ui_current_directory, 'log', test_type_in_module, __name__))
logger = Logger(log_name=logging_file_name + '.log', log_level='1',
                logger_name=test_type_in_module).get_log

# test_method_list = list()
test_method_list = generate_valid_test_method_from_apk(
    _ui_current_directory,
    ui_apk_folder_name,
    ui_test_apk_file_name,
    _logger_name=test_type_in_module)


# @pytest.mark.parametrize('test_method', test_method_list)
# def test_ui(test_method):
def test_ui_by_method_filter():
    global test_method_list

    __ui_setup()

    _test_class_list = test_method_list
    _xml_file_list = list()

    for _class_name_item in _test_class_list:
        if "useAppContext" in _class_name_item or "UnitTest" in _class_name_item:
            continue

        _run_cnt = 0
        while _run_cnt < ui_re_run_cnt:
            print("\n")
            print("\n")
            logger.critical("====== test method name : " + _class_name_item)
            std_output, err_output = \
                run_test_case_by_class(_class_name_item, ui_test_package_name, _run_listener=ui_run_listener_name)
            # std_output, err_output = "test", None

            if err_output is not None:
                _result = False
                # logger.critical("error output info : " + std_output)
            else:
                logger.debug("stand output info : " + std_output)
                _result = True

            if _result:
                logger.critical("====== one ui test case finished execution and has no problem !")
                break
            else:
                logger.critical(
                    "====== ui test still failed after " + str(_run_cnt + 1) + "times re-run")

            _run_cnt = _run_cnt + 1

        _temp_location_local = get_target_apk_abs_path(
            _ui_current_directory,
            ui_apk_folder_name,
            str(_run_cnt) + "-" + _class_name_item.split("#")[1] + ".xml")
        _xml_file_list.append(_temp_location_local)
        pull_test_result_from_device(ui_xml_result_location_on_device, _temp_location_local)
        # logger.critical("====== test result were saved : " + _temp_location_local)

        if (_run_cnt == ui_re_run_cnt) or (_result is False):
            logger.critical(
                "====== " + str(_run_cnt + 1) + "times re-run for ui test finished But test still failed !")
            __ui_tear_down()
            assert False, "ui test failed and test class info :" + _class_name_item

    _new_xml_file_path = get_target_apk_abs_path(_ui_current_directory, ui_apk_folder_name, ui_result_name)
    assemble_xml_files_to_one(_xml_file_list, _new_xml_file_path)

    __ui_tear_down()


def __ui_setup():
    stop_target_activity("com.dolby.qa.featuretest")
    # logger.critical("read test method " + test_method)
    _target_apk_path = \
        get_target_apk_abs_path(
            _ui_current_directory,
            ui_apk_folder_name,
            ui_target_apk_file_name)

    _test_apk_path = \
        get_target_apk_abs_path(
            _ui_current_directory,
            ui_apk_folder_name,
            ui_test_apk_file_name)

    install_apk_on_device_under_test(_target_apk_path, ui_target_apk_location_on_device)
    install_apk_on_device_under_test(_test_apk_path, ui_test_apk_location_on_device)
    grant_apk_required_permission(ui_target_package_name, permission_list)


def __ui_tear_down():
    stop_target_activity(ui_stop_package_name)
    uninstall_apk_on_device_under_test(ui_target_package_name)
    uninstall_apk_on_device_under_test(ui_test_package_name)


def launch_ui():
    start_target_activity(ui_start_activity_name, _package_main_activity_name=ui_start_activity_name)


if __name__ == "__main__":
    test_ui_by_method_filter()
