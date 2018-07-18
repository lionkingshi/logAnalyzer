from src.dax31.api.testconfig.full_api_config import *
from tools.common import *
from tools.logger import Logger
from tools.util import *

# register the logging configuration
test_type_in_module = "full-api"
_full_api_current_directory = dirname(realpath(__file__))
logging_file_name = abspath(join(_full_api_current_directory, 'log', test_type_in_module, __name__))
logger = Logger(log_name=logging_file_name + '.log', log_level='1',
                logger_name=test_type_in_module).get_log


# test_method_list = list()
test_method_list = generate_valid_test_method_from_apk(
    _full_api_current_directory,
    full_api_apk_folder_name,
    full_api_test_apk_file_name,
    _logger_name=test_type_in_module)


# @pytest.mark.parametrize('test_method', test_method_list)
# def test_full_api(test_method):
def test_full_api_by_class_filter():
    global test_method_list

    __full_api_setup()
    _test_class_list = [full_api_run_all_test_case]

    for _class_name_item in _test_class_list:
        _run_cnt = 0
        while _run_cnt < full_api_re_run_cnt:
            logger.critical("====== run class name : " + _class_name_item)
            std_output, err_output = run_test_case_by_class(_class_name_item, full_api_test_package_name)

            if err_output is not None:
                _result = False
                logger.critical("error output info : " + err_output)
                _temp_location_local = get_target_apk_abs_path(
                    _full_api_current_directory,
                    full_api_apk_folder_name,
                    str(_run_cnt) + "-" + _class_name_item + ".xml")
                # assert False, "test case execution failed !!!!!"
            else:
                _result = True
                _temp_location_local = get_target_apk_abs_path(
                    _full_api_current_directory,
                    full_api_apk_folder_name,
                    full_api_result_name)

            pull_test_result_from_device(full_api_xml_result_location_on_device, _temp_location_local)

            if _result:
                logger.critical("====== full api test finished and has no problem !")
                logger.critical("====== test result were saved : " + _temp_location_local)
                break
            else:
                logger.critical(
                    "====== full api test still failed after " + str(_run_cnt) + "times re-run")
                logger.critical("====== test result were saved : " + _temp_location_local)

            _run_cnt = _run_cnt + 1

        if (_run_cnt == full_api_re_run_cnt) or (_result is False):
            logger.critical(
                "====== " + str(_run_cnt) + "times re-run for full api test finished But test still failed !")
            assert False, "full api test failed and test class info :" + _class_name_item

    __full_api_tear_down()


def test_full_api_by_method_filter():
    global test_method_list

    __full_api_setup()

    _full_api_test_xml_file_list = list()
    _test_class_list = test_method_list
    _result = False

    for _class_name_item in _test_class_list:
        if "useAppContext" in _class_name_item or "UnitTest" in _class_name_item:
            continue

        _run_cnt = 0
        while _run_cnt < full_api_re_run_cnt:
            print("\n")
            print("\n")
            logger.critical("====== run method name : " + _class_name_item)
            std_output, err_output = run_test_case_by_class(_class_name_item, full_api_test_package_name)

            if err_output is not None:
                _result = False
                # assert False, "test case execution failed !!!!!"
            else:
                logger.debug("stand output info :  " + std_output)
                _result = True

            if _result:
                logger.critical("====== one full api test case finished execution and has no problem !")
                break
            else:
                logger.critical(
                    "====== full api test still failed after " + str(_run_cnt + 1) + "times re-run")

            _run_cnt = _run_cnt + 1

        _temp_location_local = get_target_apk_abs_path(
            _full_api_current_directory,
            full_api_apk_folder_name,
            str(_run_cnt) + "-" + _class_name_item.split("#")[1] + ".xml")
        _full_api_test_xml_file_list.append(_temp_location_local)
        pull_test_result_from_device(full_api_xml_result_location_on_device, _temp_location_local)

        if (_run_cnt == full_api_re_run_cnt) or (_result is False):
            logger.critical(
                "====== " + str(_run_cnt + 1) + "times re-run for full api test finished But test still failed !")
            __full_api_tear_down()
            assert False, "full api test failed and test class info :" + _class_name_item

    _new_xml_file_path = \
        get_target_apk_abs_path(_full_api_current_directory, full_api_apk_folder_name, full_api_result_name)
    assemble_xml_files_to_one(_full_api_test_xml_file_list, _new_xml_file_path)

    __full_api_tear_down()


def __full_api_setup():
    stop_target_activity("com.dolby.qa.featuretest")
    # logger.critical("read test method " + test_method)
    _target_apk_path = \
        get_target_apk_abs_path(
            _full_api_current_directory,
            full_api_apk_folder_name,
            full_api_target_apk_file_name)

    _test_apk_path = \
        get_target_apk_abs_path(
            _full_api_current_directory,
            full_api_apk_folder_name,
            full_api_test_apk_file_name)

    install_apk_on_device_under_test(_target_apk_path, full_api_target_apk_location_on_device)
    install_apk_on_device_under_test(_test_apk_path, full_api_test_apk_location_on_device)
    grant_apk_required_permission(full_api_target_package_name, permission_list)


def __full_api_tear_down():
    stop_target_activity(full_api_target_package_name)
    uninstall_apk_on_device_under_test(full_api_target_package_name)
    uninstall_apk_on_device_under_test(full_api_test_package_name)


if __name__ == "__main__":
    generate_valid_test_method_from_apk(
        _full_api_current_directory,
        full_api_apk_folder_name,
        full_api_test_apk_file_name,
        _logger_name=test_type_in_module)

    test_full_api_by_method_filter()
