from os.path import abspath, join, dirname, exists
from common import run_command, register_logger_name
import logging
import xml.etree.ElementTree as Xml

logger_name = "test"


def get_test_apk_abs_path(__base_abs_path, __parent_directory, __apk_name):
    __test_apk_abs_location = abspath((join(__base_abs_path, __parent_directory, __apk_name)))
    return __test_apk_abs_location


def get_target_apk_abs_path(__base_abs_path, __parent_directory, __apk_name):
    return get_test_apk_abs_path(__base_abs_path, __parent_directory, __apk_name)


def get_test_method_file_parent_abs_path(__base_abs_path, __parent_directory):
    return abspath(join(__base_abs_path, __parent_directory))


def get_test_method_file_abs_path(__base_abs_path, __parent_directory, __file_name):
    return get_test_apk_abs_path(__base_abs_path, __parent_directory, __file_name)


def get_dex_test_parse_tool_abs_path():
    __current_directory = dirname(abspath(__file__))
    __dex_test_parse_abs_path = abspath(join(__current_directory, "3thtools", "parser-1.1.1-SNAPSHOT-all.jar"))
    if exists(__dex_test_parse_abs_path):
        logging.getLogger(logger_name).debug(
            "dex test parse tool exist in right folder: {}".format(__dex_test_parse_abs_path))
    else:
        logging.getLogger(logger_name).debug(
            "dex test parse tool did not exist in right folder: {}".format(__dex_test_parse_abs_path))
    return __dex_test_parse_abs_path


def get_spoon_tools_abs_path():
    __current_directory = dirname(abspath(__file__))
    __spoon_tool_abs_path = abspath(join(__current_directory, "3thtools", "parser-1.1.1-SNAPSHOT-all.jar"))
    if exists(__spoon_tool_abs_path):
        logging.getLogger(logger_name).debug(
            "spoon tool exist in right folder: {}".format(__spoon_tool_abs_path))
    else:
        logging.getLogger(logger_name).debug(
            "spoon tool did not exist in right folder: {}".format(__spoon_tool_abs_path))
    return __spoon_tool_abs_path


# the test method's file located in same folder of parsing apk
def generate_valid_test_method_from_apk(
        _base_abs_path,
        _parent_directory,
        _apk_name,
        _result_name="AllTests.txt",
        _logger_name="test"):
    # first step tp register the logger manager name
    global logger_name
    logger_name = _logger_name
    register_logger_name(_logger_name)

    _test_apk_location = get_test_apk_abs_path(_base_abs_path, _parent_directory, _apk_name)
    _test_method_list_parent_location = \
        get_test_method_file_parent_abs_path(_base_abs_path, _parent_directory)
    _file_name_path_containing_test_method = \
        get_test_method_file_abs_path(_base_abs_path, _parent_directory, _result_name)
    _dex_test_parse_tool_path = get_dex_test_parse_tool_abs_path()

    if exists(_test_apk_location):
        _parse_test_method_command = "java -jar {0} {1} {2}".format(
            _dex_test_parse_tool_path, _test_apk_location, _test_method_list_parent_location)

        std_output, err_output = run_command(_parse_test_method_command)

        if "Found 0" in std_output:
            err_output = ""
        else:
            err_output = None

        if err_output is None and exists(_file_name_path_containing_test_method):
            logging.getLogger(_logger_name).debug("stand output of dex test parse tool: " + std_output)
            # Read data from file
            try:
                with open(_file_name_path_containing_test_method, 'r') as fp_r:
                    lines = fp_r.readlines()
                    fp_r.close()
                _test_method_list = list()
                if lines is not None:
                    for line in lines:
                        line = line.strip('\n')
                        line = line.strip('\b')
                        _test_method_list.append(line)
                if len(_test_method_list) > 0:
                    for _one_items in _test_method_list:
                        logging.getLogger(_logger_name).debug("test method :" + str(_one_items))
                else:
                    logging.getLogger(_logger_name).critical("test methods is null parsing from " + _apk_name)
            except EnvironmentError, e:
                print("!!!!!failed to open file :" + e.message)
        else:
            _test_method_list = None
            logging.getLogger(_logger_name).critical("error output of dex test parse tool: " + std_output)
    else:
        _test_method_list = None
        logging.getLogger(_logger_name).critical("test apk did not exist: " + _test_apk_location)
    assert isinstance(_test_method_list, list), "test method list is null !!!!"
    return _test_method_list


def filter_test_class_name(_test_method_list):
    assert isinstance(_test_method_list, list)
    assert len(_test_method_list) > 0, "length of the input argument is equals to 0 !!!!"

    _class_name_list = list()

    for _item in _test_method_list:
        _temp_class_name = _item.split("#")[0]
        if _temp_class_name not in _class_name_list:
            _class_name_list.append(_temp_class_name)

    return _class_name_list


def start_target_activity(_package_name, _package_main_activity_name="com.dolby.qa.dolbyeffecttest.DAXApiActivity"):
    run_command("adb shell am start -n {0}/{1}".format(_package_name, _package_main_activity_name))


def stop_target_activity(_package_name):
    run_command("adb shell am force-stop {0}".format(_package_name))


def install_apk_on_device_under_test(_apk_abs_path, _location_on_device):
    run_command("adb push {0} {1}".format(_apk_abs_path, _location_on_device))
    run_command("adb shell pm install -t -r {0}".format(_location_on_device))


def uninstall_apk_on_device_under_test(_package_name):
    run_command("adb shell pm uninstall {0}".format(_package_name))


def grant_apk_required_permission(_package_name, _permission_list):
    # print(type(_permission_list))
    assert isinstance(_package_name, str)
    assert isinstance(_permission_list, list)
    if len(_permission_list) > 0:
        for _item in _permission_list:
            run_command("adb shell pm grant {} {}".format(_package_name, _item))


def run_test_case_by_class(
        _class_name,
        _test_package_name,
        _run_listener="com.dolby.qa.util.XMLRunListener.XmlRunListener"):
    _stdout, _stderr = run_command(
        "adb shell am instrument -w -r " +
        "-e listener {0} -e class {1} {2}/android.support.test.runner.AndroidJUnitRunner".format(
            _run_listener,
            _class_name,
            _test_package_name))

    if "Failures" in _stdout or "FAILURES!!!" in _stdout:
        _stderr = "Failures"
    elif "OK" in _stdout:
        _stderr = None
    else:
        _stderr = None
    return _stdout, _stderr


def pull_test_result_from_device(_result_location_on_device, _file_location_local):
    import os
    if exists(_file_location_local):
        os.remove(_file_location_local)
    std_output, err_output = run_command("adb pull {0} {1}".format(_result_location_on_device, _file_location_local))
    run_command("adb shell rm -rf {0}".format(_result_location_on_device))
    return std_output, err_output


def detect_foreground_activity(_package_name):
    std_output, err_output = run_command("adb shell dumpsys window windows | grep mCurrentFocus")
    if _package_name in std_output:
        return True
    else:
        return False


def assemble_xml_files_to_one(__xml_file_list, __new_xml_file_path):
    assert isinstance(__xml_file_list, list)
    for __xml_file_path in __xml_file_list:
        if not exists(__xml_file_path):
            assert False, "xml file does not exist : " + __xml_file_path

    if len(__xml_file_list) == 0:
        logging.getLogger(logger_name).critical("has no xml files to assemble to one file !")
        return None

    _local_first_tree = Xml.parse(__xml_file_list[0])
    _local_first_root = _local_first_tree.getroot()
    for __index in xrange(1, len(__xml_file_list), 1):
        _local_other_tree = Xml.parse(__xml_file_list[__index])
        _local_other_root = _local_other_tree.getroot()
        __update_summary_info(_local_first_root, _local_other_root)
        __test_case_list = _local_other_root.findall("testcase")
        for _test_case in __test_case_list:
            _local_first_root.append(_test_case)
            # _local_first_root.insert(2, _test_case)

    _local_first_tree.write(__new_xml_file_path)
    logging.getLogger(logger_name).critical("===== test result were save: " + __new_xml_file_path)

    # remove unused xml file
    for __xml_file_path in __xml_file_list:
        import os
        os.remove(__xml_file_path)


def __update_summary_info(_a, _b):
    __current_info = _a.attrib
    assert isinstance(__current_info, dict), "the attrib of the first argument is not a dict"
    __new_info = _b.attrib
    assert isinstance(__current_info, dict), "the attrib of the second argument is not a dict"

    for __key in __current_info.keys():
        __update_value = __new_info.get(__key, None)
        if __update_value is not None:
            if __key == "timestamp":
                continue
            if __key == "time":
                _total_time = float(__current_info[__key])
                _total_time = _total_time + float(__new_info[__key])
                __current_info[__key] = str(_total_time)
            if __key in ("errors", "failures", "skipped", "tests"):
                _test_case_num = int(__current_info[__key])
                _test_case_num = _test_case_num + int(__new_info[__key])
                __current_info[__key] = str(_test_case_num)
