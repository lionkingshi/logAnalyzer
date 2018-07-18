import xml.etree.ElementTree as xml
import copy
import inspect
from os.path import dirname, join, abspath
from shutil import copyfile

filename2 = "/home/emediaqa/selfstudy/101-python/parseXML/dax3-default-stereo-speaker.xml"
geq_frequency_list = ['47', '141', '234', '328', '469', '656', '844', '1031', '1313', '1688',
                      '2250', '3000', '3750', '4688', '5813', '7125', '9000', '11250', '13875', '19688']
total_added_profile_number = 0


def get_speaker_endpoint_type(_xml_file_abs_path):
    _flag_speaker_is_mono = True
    _lang = xml.parse(_xml_file_abs_path)
    _root = _lang.getroot()

    for _tuning_tag_element in _root.iter("tuning"):
        if _tuning_tag_element.attrib["mono_device"] == "true":
            _flag_speaker_is_mono = True
            break
        elif _tuning_tag_element.attrib["mono_device"] == "false":
            _flag_speaker_is_mono = False
            break
        else:
            _flag_speaker_is_mono = True

    import os
    os.remove(_xml_file_abs_path)
    return _flag_speaker_is_mono


def get_profile_name_by_id(_xml_file_path, _profile_id):
    assert isinstance(_profile_id, int)

    _profile_name_ = "unknowed"
    _lang = xml.parse(_xml_file_path)
    _root = _lang.getroot()

    for _profile in _root.findall('profile'):
        _temp_id = int(_profile.attrib['id'])
        assert isinstance(_temp_id, int)
        if _temp_id == _profile_id:
            _profile_name_ = _profile.attrib['name']

    return _profile_name_


def get_profile_name(_xml_file_path):
    _lang = xml.parse(_xml_file_path)
    _root = _lang.getroot()
    _profile_name_list = list()

    for _profile in _root.findall('profile'):
        _profile_name_list.append(_profile.attrib['name'])

    if len(_profile_name_list) == 0:
        _profile_name_list = None

    return _profile_name_list


def copy_specified_profile_and_then_crate_a_new_profile(_xml_real_path, _copied_profile_name, _new_profile_num):
    assert isinstance(_new_profile_num, int)
    assert isinstance(_copied_profile_name, str)
    assert _copied_profile_name in ("Dynamic", 'Movie', 'Music', 'Custom'), "wrong specified profile name!"
    assert _new_profile_num > 0, "the number of added profile should be bigger than 0!"

    _lang = xml.parse(_xml_real_path)
    _root = _lang.getroot()

    global total_added_profile_number
    total_added_profile_number = _new_profile_num
    for x in range(1, total_added_profile_number+1, 1):
        # print(str(x))
        # print (_temp_profile_name)
        insert_profile_paras_copy_from_a_existing_profile(_root, _copied_profile_name, x)
    save_xml_file(_lang, "dax-default-copy-from-{}.xml".format(_copied_profile_name))


def create_new_profiles_in_sequence(_xml_real_path, _new_profile_num, output_file_name):
    assert isinstance(_new_profile_num, int)
    assert _new_profile_num >= 0, "the number of added profile should be bigger than 0!"
    _lang = xml.parse(_xml_real_path)
    _root = _lang.getroot()
    _existing_profile_name = ["Dynamic", 'Movie', 'Music', 'Custom']

    global total_added_profile_number
    total_added_profile_number = _new_profile_num
    for x in range(0, total_added_profile_number, 1):
        _temp_profile_name_index = x % 4
        # _temp_profile_x = x / 4 + 1
        _temp_profile_x = x
        insert_profile_paras_copy_from_a_existing_profile(_root,
                                                          _existing_profile_name[_temp_profile_name_index],
                                                          _temp_profile_x)

    input_file_directory = dirname(_xml_real_path)
    output_real_path = abspath(join(input_file_directory, output_file_name))
    if _new_profile_num == 4:
        copyfile(_xml_real_path, output_real_path)
    else:
        save_xml_file(_lang, output_real_path)


def save_xml_file(_lang, _output_file):
    assert inspect.isclass(type(_lang))
    _lang.write(_output_file)


# assume that the id of custom profile is the biggest in current existing profile
def insert_profile_paras_copy_from_a_existing_profile(_root, _copied_profile_name, current_added_profile_index):
    global total_added_profile_number
    assert isinstance(_copied_profile_name, str)
    assert isinstance(current_added_profile_index, int)

    _increase_profile_number_step = 1
    if current_added_profile_index >= total_added_profile_number/2:
        _increase_profile_number_step = 1

    # step 1 : find a profile element which has a biggest id and its position order in parent sub element
    _biggest_profile_id_element = get_biggest_profile_id_element(_root)
    _biggest_profile_id = int(_biggest_profile_id_element.attrib['id'])
    _position_index = get_position_index_by_tag_and_id(_root, "profile", _biggest_profile_id)

    # step 2 :insert the element and increase the id
    _existing_profile_element = get_specified_profile_name_element(_root, _copied_profile_name)
    _new_id_profile = copy.deepcopy(_existing_profile_element)
    _new_id_profile.attrib['id'] = str(_biggest_profile_id + _increase_profile_number_step)
    _new_id_profile.attrib['name'] = str(_copied_profile_name) + str(current_added_profile_index/4 + 1)
    insert_sub_element_at_given_position(_root, _new_id_profile, _position_index + 1)

    # step 3: find the position of geq element to insert a new one
    _biggest_geq_preset_id_element = get_biggest_geq_preset_id_element(_root)
    _biggest_geq_preset_id = _biggest_geq_preset_id_element.attrib['id']
    _geq_position_index = get_position_index_by_tag_and_id(_root, "preset", _biggest_geq_preset_id)

    # step 4: the id of geq should be equal to id of profile
    #         insert a new geq element and its value is -576 or 576
    _new_id_geq_preset = copy.deepcopy(_biggest_geq_preset_id_element)
    _new_id_geq_preset.attrib['id'] = str(_biggest_profile_id + _increase_profile_number_step)
    _geq_band_gain_element_list = _new_id_geq_preset.findall("*/*/band_geq")
    # print(_geq_band_gain_element_list)
    assert len(_geq_band_gain_element_list) == 20, "the length of geq band gain obtained from xml should be 20 !"
    _geqbg_value_list = \
        produce_geq_band_gain_by_custom_profile_id(total_added_profile_number, current_added_profile_index)
    for index in range(len(_geq_band_gain_element_list)):
        assert _geq_band_gain_element_list[index].attrib['frequency'] == geq_frequency_list[index], \
            "dis-ordered list !"
        _geq_band_gain_element_list[index].attrib['gain'] = str(_geqbg_value_list[index])

    insert_sub_element_at_given_position(_root, _new_id_geq_preset, _geq_position_index + 1)


def insert_geq(_xml_real_path):
    _lang = xml.parse(_xml_real_path)
    _root = _lang.getroot()

    _biggest_profile_id_element = get_biggest_profile_id_element(_root)
    _biggest_profile_id = int(_biggest_profile_id_element.attrib['id'])
    _profile_name = _biggest_profile_id_element.attrib['name']
    _position_index = get_position_index_by_tag_and_id(_root, "profile", _biggest_profile_id)

    _new_id_profile = copy.deepcopy(_biggest_profile_id_element)
    _new_id_profile.attrib['id'] = str(_biggest_profile_id + 1)
    _new_id_profile.attrib['name'] = str(_profile_name + '1')
    insert_sub_element_at_given_position(_root, _new_id_profile, _position_index + 1)

    _lang.write('2.xml')


def get_last_geq_position_element():
    pass


def get_last_profile_position_element():
    pass


def get_biggest_profile_id_element(_parent_element):
    # assert isinstance(_parent_element, Element)
    # randomly find a profile element and then do the initialization
    _random_profile = find_a_arbitrary_profile_element(_parent_element)
    _maximum_id = int(_random_profile.attrib['id'])
    _maximum_id_element = _random_profile

    # find profile element by the biggest id
    for _profile in _parent_element.findall('profile'):
        _temp_id = int(_profile.attrib['id'])
        assert isinstance(_temp_id, int)
        if _temp_id > _maximum_id:
            _maximum_id = _temp_id
            _maximum_id_element = _profile
            pass
    return _maximum_id_element


def get_specified_profile_name_element(_parent_element, _profile_name):
    assert isinstance(_profile_name, str)
    # print(".//profile[@name='%s']" % _profile_name)
    _random_profile = _parent_element.find(".//profile[@name='%s']" % _profile_name)
    if _random_profile is not None and _random_profile.attrib['name'] == _profile_name:
        return _random_profile
    else:
        assert False, "current xml file has no profile element whose name is " + _profile_name
    pass


def get_biggest_geq_preset_id_element(_parent_element):
    # assert isinstance(_parent_element, Element)
    # randomly find a profile element and then do the initialization
    _random_profile = find_a_arbitrary_geq_preset_element(_parent_element)
    _maximum_id = int(_random_profile.attrib['id'])
    _maximum_id_element = _random_profile

    # find profile element by the biggest id
    for _profile in _parent_element.findall(".//preset[@type='geq']"):
        _temp_id = int(_profile.attrib['id'])
        assert isinstance(_temp_id, int)
        if _temp_id > _maximum_id:
            _maximum_id = _temp_id
            _maximum_id_element = _profile
            pass
    return _maximum_id_element


def find_a_arbitrary_profile_element(_parent_element):
    _random_profile = _parent_element.find('profile')
    if _random_profile is not None:
        return _random_profile
    else:
        assert False, "current xml file has no profile element!"
    pass


def find_a_arbitrary_geq_preset_element(_parent_element):
    _random_geq_preset = _parent_element.find(".//preset[@type='geq']")
    if _random_geq_preset is not None:
        return _random_geq_preset
    else:
        assert False, "current xml file has no geq preset element!"
    pass


def get_position_index_by_tag_and_id(_parent_element, _tag, _id):
    _sub_element_list = _parent_element.getchildren()
    assert isinstance(_sub_element_list, list)
    assert len(_sub_element_list) > 0, "length of sub elements is 0!"

    _position_index = None
    for _temp_index in range(len(_sub_element_list)):
        if _sub_element_list[_temp_index].tag == _tag:
            if _sub_element_list[_temp_index].attrib['id'] == str(_id):
                _position_index = _temp_index
                break
    return _position_index


def get_total_element_number_by_tag(_parent_element, _tag):
    _sub_element_list = _parent_element.findall(str(_tag))
    return len(_sub_element_list)


def get_total_number_of_profile(_parent_element):
    return get_total_element_number_by_tag(_parent_element, 'profile')


def get_total_number_of_geq(_parent_element):
    _sub_element_list = _parent_element.findall(".//preset[@type='geq']")
    return len(_sub_element_list)


def get_total_number_sub_element(_parent_element):
    return len(_parent_element.getchildren())


def get_geq_id_list(_parent_element):
    _sub_element_list = _parent_element.findall(".//preset[@type='geq']")
    _id_list = None
    for x in range(len(_sub_element_list)):
        _id_list.append(int(_sub_element_list[x].attrib['id']))
    return _id_list


def get_profile_id_list(_parent_element):
    _sub_element_list = _parent_element.findall("profile")
    _id_list = None
    for x in range(len(_sub_element_list)):
        _id_list.append(int(_sub_element_list[x].attrib['id']))
    return _id_list


def remove_additional_geq_element():
    pass


def verify_geq_id_in_profile_id_list():
    pass


def insert_sub_element_at_given_position(_parent_element, _new_sub_element, _position_index):
    _total_num = get_total_number_sub_element(_parent_element)
    _parent_element.insert(_position_index, _new_sub_element)
    _new_total_num = get_total_number_sub_element(_parent_element)
    assert _new_total_num == (_total_num + 1), "fail to insert element !"


def produce_geq_band_gain_by_custom_profile_id(_maximum_id, _current_id, _maximum_geqbg=576, _minimum_geqbg=-576):
    assert isinstance(_maximum_id, int)
    assert isinstance(_current_id, int)
    assert _current_id <= _maximum_id, "please make sure the input arguments!"

    if (_current_id % 2) == 0:
        _first_element = _maximum_geqbg
    else:
        _first_element = _minimum_geqbg
    return_value = [_first_element]

    for index in range(1, 20, 1):
        if (index % 2) == 1:
            return_value.append(_first_element*(-1))
        else:
            return_value.append(_first_element)

    assert len(return_value) == 20, "the length of geq band gain array is not equals to 20 !"
    return return_value


if __name__ == "__main__":
    copy_specified_profile_and_then_crate_a_new_profile(filename2, 'Custom', 12)
    copy_specified_profile_and_then_crate_a_new_profile(filename2, 'Music', 1)
    copy_specified_profile_and_then_crate_a_new_profile(filename2, 'Movie', 20)
    copy_specified_profile_and_then_crate_a_new_profile(filename2, 'Dynamic', 8)
    create_new_profiles_in_sequence(filename2, 12, "dax-default-copy-in-sequence.xml")
