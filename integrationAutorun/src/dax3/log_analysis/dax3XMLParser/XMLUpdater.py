import os
import sys
from XMLConfigConstants import *
import csv
from os.path import abspath, exists, dirname
from getopt import getopt
# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
from collections import OrderedDict


# sort order for attributes
def _serialize_xml(write, elem, encoding, qnames, namespaces):
    tag = elem.tag
    text = elem.text
    if tag is ET.Comment:
        write("<!--%s-->" % ET._encode(text, encoding))
    elif tag is ET.ProcessingInstruction:
        write("<?%s?>" % ET._encode(text, encoding))
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(ET._escape_cdata(text, encoding))
            for _temp_element in elem:
                _serialize_xml(write, _temp_element, encoding, qnames, None)
        else:
            write("<" + tag)
            items = elem.items()
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(), key=lambda x: x[1]):  # sort on prefix
                        if k:
                            k = ":" + k
                        write(" xmlns%s=\"%s\"" % (
                            k.encode(encoding),
                            ET._escape_attrib(v, encoding)
                            ))
                for k, v in items: # Monkey patch
                    if isinstance(k, ET.QName):
                        k = k.text
                    if isinstance(v, ET.QName):
                        v = qnames[v.text]
                    else:
                        v = ET._escape_attrib(v, encoding)
                    write(" %s=\"%s\"" % (qnames[k], v))
            if text or len(elem):
                write(">")
                if text:
                    write(ET._escape_cdata(text, encoding))
                for e in elem:
                    _serialize_xml(write, e, encoding, qnames, None)
                write("</" + tag + ">")
            else:
                write(" />")
    if elem.tail:
        write(ET._escape_cdata(elem.tail, encoding))

ET._serialize_xml = _serialize_xml


class OrderedXMLTreeBuilder(ET.XMLTreeBuilder):
    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = OrderedDict()
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[fixname(attrib_in[i])] = self._fixtext(attrib_in[i+1])
        return self._target.start(tag, attrib)


class TuningFileParser:
    POST_PROCESSING_PARAS_DICT = OrderedDict()

    def __init__(self, xml_file_path='dax3-default-stereo-speaker.xml'):
        if not exists(xml_file_path):
            raise Exception("Input file '%s' doesn't exist." % xml_file_path)
        self.__input = xml_file_path

        self.__tree = ET.parse(xml_file_path, OrderedXMLTreeBuilder())
        self.__root = self.__tree.getroot()
        self.__initialize_parameters_value_to_non_exist()

    # initial the parameters dictionary
    @staticmethod
    def __initialize_parameters_value_to_non_exist():
        for index in range(len(POST_PROCESSING_PARAS_LIST)):
            TuningFileParser.POST_PROCESSING_PARAS_DICT[POST_PROCESSING_PARAS_LIST[index]] = 'non-exist'
        pass

    # check profile if valid
    @staticmethod
    def check_ifvalid(self, profile, endpoint):
        flag = 1
        if profile not in profile_name:
            print ("valid profile name shall be : ")
            print (profile_name)
            flag = 0
        if endpoint not in tuning_endpoint_name:
            print ("valid tuning endpoint name shall be : ")
            print (tuning_endpoint_name)
            flag = 0
        return flag

    '''
    get dap feature item element for tuning ,here for gain left/right ,dap feature shall be aobs
    for threshold_low/high of AR, dap feature shall be arbs
    '''

    def get_dapE_tuning(self, dap_feature, endpoint):
        # patten for specific endpoint
        tuning_patten = ".//tuning[@name='%s']" % endpoint
        dap_feature_patten = ".//%s" % (dap_feature)
        try:
            e_tuning = self.__root.find(tuning_patten)
            if dap_feature in ["band_optimizer", "band_regulator"]:
                e_dap_feature = e_tuning.findall(dap_feature_patten)
                # print e_dap_feature[0].tag
            else:
                e_dap_feature = e_tuning.find(dap_feature_patten)
                # print e_dap_feature.tag
            return e_dap_feature
        except Exception, e:
            print (e)

    # get dap feature item element for profile
    def get_dapE_profile(self, dap_feature, profile, endpoint_type):
        # patten for finding specific profile
        profile_patten = ".//profile[@name='%s']" % profile
        # patten for find specific child of endpoint type of profile
        if endpoint_type != "":
            dap_feature_patten = ".//endpoint_type[@id='%s']/%s" % (endpoint_type, dap_feature)
        else:
            dap_feature_patten = ".//%s" % (dap_feature)
        try:
            profile = self.__root.find(profile_patten)
            e_dap_feature = profile.find(dap_feature_patten)
            return e_dap_feature
        except Exception, e:
            print (e)

    # change default dict to Order dict,for aobs, the channel order , for arbs, threshold low/high
    def order_attribs(self, e_band, order_list):
        attribs_order_dict = OrderedDict()
        attrib_dict = e_band.attrib
        # if e_band.tag=="band_optimizer":
        for a in order_list:
            attribs_order_dict[a] = attrib_dict[a]
        # print attribs_order_dict.keys()
        return attribs_order_dict

    # unit function for get attrib value of 20 bands
    def get_value_of_bands(self, e_bands):
        frequency_s = "20,"
        first_band = e_bands[0]
        # get the attrib num, this is used by aobs
        attrib_dict = first_band.attrib
        attribs = attrib_dict.keys()
        attrib_num = len(attribs)
        # for aobs, shall add 10 in front of the actual value
        if first_band.tag == "band_optimizer":
            band_order = band_optimizer_order
            channel_count = attrib_num - 1
            frequency_s += str(channel_count) + ","
        elif first_band.tag == "band_regulator":
            band_order = band_regulator_order
        elif first_band.tag == "band_ieq":
            band_order = iebs_order
        elif first_band.tag == "band_geq":
            band_order = gebs_order
        bands_list = []
        try:
            for each_band in e_bands:
                # get the order dict according to the band order
                attribs_order_dict = self.order_attribs(each_band, band_order)
                # order_keys=attribs_order_dict.keys()
                order_values = attribs_order_dict.values()
                # bands_list.append(order_keys)
                bands_list.append(order_values)
            # get the final values, gain_left(20 bands)+gain_right(20 bands)+...
            values = ""
            for j in range(0, attrib_num):
                temp = ""
                for i in range(0, 20):
                    temp = bands_list[i][j]
                    if temp == "false":
                        temp = '0'
                    elif temp == "true":
                        temp = '1'
                    values += temp + ","
            values = frequency_s + values
            return values[:-1]
        except Exception as e:
            raise e
            # get value of aobs_arbs for specific endpoint

    def get_feature_aobs_arbs(self, dap_feature, endpoint):
        if dap_feature not in ["aobs", "arbs"]:
            print ("input error for aobs(arbs)")
            return -1
        try:
            dap_feature = dap_tuning_dict[dap_feature]
            e_dap_feature = self.get_dapE_tuning(dap_feature, endpoint)
            return self.get_value_of_bands(e_dap_feature)
        except Exception, e:
            print (e)

    # get iebs for profile
    def get_iebs_gebs(self, ie_ge, profile):
        profile_patten = ".//profile[@name='%s']" % profile
        profile = self.__root.find(profile_patten)
        e_includes = profile.findall(".//include")
        if ie_ge == "iebs":
            e_iebs = e_includes[0]
            band_name = "band_ieq"
        if ie_ge == "gebs":
            e_iebs = e_includes[1]
            band_name = "band_geq"
        iebs_preset = e_iebs.get("preset")
        # print "iebs_preset " + iebs_preset
        ieq_preset_patten = ".//preset[@id='%s']" % iebs_preset
        e_ieq_preset = self.__root.find(ieq_preset_patten)
        # print "e_ieq_preset.tag "+e_ieq_preset.get("id")
        e_ieq_bands = e_ieq_preset.findall(".//" + band_name)
        return self.get_value_of_bands(e_ieq_bands)

    # get iebs for profile
    def get_iebs_profile_only_discarded(self, profile):
        profile_patten = ".//profile[@name='%s']" % profile
        profile = self.__root.find(profile_patten)
        e_iebs = profile.find(".//include")
        iebs_preset = e_iebs.get("preset")
        # print "iebs_preset " + iebs_preset
        ieq_preset_patten = ".//preset[@id='%s']" % iebs_preset
        e_ieq_preset = self.__root.find(ieq_preset_patten)
        # print "e_ieq_preset.tag"+e_ieq_preset.get("id")
        e_ieq_bands = e_ieq_preset.findall(".//band_ieq")
        frequency_s = "20,"
        value_s = ""
        for each_band in e_ieq_bands:
            frequency_s += each_band.get("frequency") + ","
            value_s += each_band.get("target") + ","
        return frequency_s + value_s

    # get features for profile except aobs,arbs,dom,beon,vbon
    def get_feature_profile_only(self, dap_feature, profile):
        # get value for profile only feature
        dap_feature = dap_profile_dict[dap_feature]
        e_dap_feature_profile = self.get_dapE_profile(dap_feature, profile, "")
        value = e_dap_feature_profile.get('value')
        return value
        # get features for profile except aobs,arbs,dom,beon,vbon

    def get_feature_profile_endpoint(self, dap_feature, profile, endpoint):
        dap_feature_s = dap_feature
        dap_feature = dap_profile_dict[dap_feature_s]
        tuning_patten = ".//tuning[@name='%s']" % endpoint
        try:
            tuning = self.__root.find(tuning_patten)
            endpoint_type = tuning.get('endpoint_type')
            e_dap_feature_profile = self.get_dapE_profile(dap_feature, profile, endpoint_type)
            value = e_dap_feature_profile.get('value')
            if dap_feature_s == "dea":
                temp = float(int(value) * 10)
                temp = temp / 16
                value = int(round(temp))
            # if it's dea, the value shall be (round(received_DEA * 10 / 16))
            # print profile_value
            return value
        except Exception as e:
            raise e

    # get features for tuning except aobs,arbs,dom,beon,vbon
    def get_feature_tuning(self, dap_feature, endpoint):
        dap_feature_s = dap_feature
        tuning_patten = ".//tuning[@name='%s']" % endpoint
        tuning = self.__root.find(tuning_patten)
        if dap_feature_s == "ceqt":
            value = "2,155,"
            for each in dap_tuning_dict[dap_feature_s]:
                e_dap_feature_tuning = self.get_dapE_tuning(each, endpoint)
                temp = e_dap_feature_tuning.get('value')
                value = value + temp + ','
            # omit the last string ','
            value = value[:-1]
        else:
            try:
                dap_feature = dap_tuning_dict[dap_feature_s]
            except Exception as e:
                return "non-exist"

            e_dap_feature_tuning = self.get_dapE_tuning(dap_feature, endpoint)
            value = e_dap_feature_tuning.get('value')
        # print profile_value
        return value

    # get feature for vbmf,vbsf and vbhg
    def get_feature_vb(self, dap_feature, endpoint):
        dap_feature_s = dap_feature
        dap_feature = dap_tuning_dict[dap_feature_s]
        e_dap = self.get_dapE_tuning(dap_feature, endpoint)
        if dap_feature_s in ["vbmf", "vbsf"]:
            value = e_dap.get("frequency_low") + "," + e_dap.get("frequency_high")
        if dap_feature_s == "vbhg":
            value = e_dap.get('harmonic_2') + "," + e_dap.get('harmonic_3') + "," + e_dap.get('harmonic_4')
        return value

    # get orientation of endpoint
    def get_orientation_endpoint(self, endpoint):
        tuning_patten = ".//tuning[@name='%s']" % endpoint
        orientation_patten = ".//orientation"
        try:
            # get the endpoint type for the endpoint
            tuning = self.__root.find(tuning_patten)
            e_oritenation = tuning.find(orientation_patten)
            orientation_value = e_oritenation.get('value')
            return orientation_value
        except Exception, e:
            print (e)

    # get matrix of endpoint
    def get_matrix_endpoint(self, endpoint):
        tuning_patten = ".//tuning[@name='%s']" % endpoint
        matrix_patten = ".//mix_matrix"
        try:
            # get the endpoint type for the endpoint
            tuning = self.__root.find(tuning_patten)
            e_matrix = tuning.find(matrix_patten)
            e_matrix_element = e_matrix.findall(".//element")
            value = ""
            if e_matrix_element is None:
                return ""
            for each_ele in e_matrix_element:
                value += each_ele.get('value') + ","
            return value[:-1]
        except Exception, e:
            print (e)

    # get feature value for dom,vbon and beon, these three ones are special ones
    def get_feture_dom_bass(self, dap_feature, profile, endpoint):
        if not self.check_ifvalid(profile, endpoint):
            return 0
        flag = 0
        tuning_patten = ".//tuning[@name='%s']" % endpoint
        try:
            # get the endpoint type for the endpoint
            tuning = self.__root.find(tuning_patten)
            endpoint_type = tuning.get('endpoint_type')
            # print endpoint_type
            # for dom,beon/vbon, the [0] is for profile, the [1] is for tuning
            # get the value of profile
            dap_feature_s = dap_feature
            dap_feature = dap_profile_dict[dap_feature_s][0]
            e_dap_feature_profile = self.get_dapE_profile(dap_feature, profile, endpoint_type)
            profile_value = e_dap_feature_profile.get('value')
            # print dap_feature_s+ " value in profile "+profile+ " "+profile_value
            # get the value of tuning
            dap_feature = dap_profile_dict[dap_feature_s][1]
            e_dap_feature_tuning = self.get_dapE_tuning(dap_feature, endpoint)
            tuning_value = e_dap_feature_tuning.get('value')
            # print dap_feature_s+" value in endpoint "+endpoint+" "+tuning_value
            # profile value multiple tuning value is the final value
            if profile_value == "true" and tuning_value == "true":
                flag = 1
            if dap_feature_s == "dom":
                endp = dom_endp_dict[endpoint_type]
                orientation = self.get_orientation_endpoint(endpoint)
                matrix = self.get_matrix_endpoint(endpoint)
                # print endp
                # print orientation
                # print matrix

                if matrix == "":
                    dom_str = str(flag) + "," + str(endp) + "," + orientation
                    pass
                else:
                    dom_str = str(flag) + "," + str(endp) + "," + orientation + "," + matrix
                return dom_str

            return flag
        except Exception, e:
            print (e)
            print ("Cannot get the value of  " + dap_feature + " for " + profile + "," + endpoint)

    ''' 
    set features for tuning part
    dap feature, the specific feature, except gain_left/right and threshold_high/low, others use the short name
    feature value, the value you want to the feature
    ao_or_ar, please specified as aobs or arbs, if want to set gain_left/right threshold_low/high
    others, ignore it
    endpoint, the endpoint name in tuning part
    '''

    def set_feature_tuning(self, dap_feature, feature_value, endpoint, ao_or_ar=""):
        try:
            if dap_feature in ["gain_left", "gain_right", "threshold_high", "threshold_low"]:
                pass
            elif dap_feature in ["dom", "beon", "vbon"]:
                dap_feature = dap_profile_dict[dap_feature][1]
            else:
                dap_feature = dap_tuning_dict[dap_feature]
                # print "dap_feature "+dap_feature
        except Exception, e:
            print (e)
        try:
            if ao_or_ar != "":
                ao_or_ar = dap_tuning_dict[ao_or_ar]
                e_dap_feature = self.get_dapE_tuning(ao_or_ar, endpoint)
                # it has 20 band for ao and ar
                for each_band in e_dap_feature:
                    each_band.set(dap_feature, feature_value)
                print ("Set parameters succeed: " + e_dap_feature[0].tag)
            else:
                e_dap_feature = self.get_dapE_tuning(dap_feature, endpoint)
                e_dap_feature.set('value', feature_value)
                print ("Set parameters succeed: " + e_dap_feature.tag)
        except Exception, e:
            print (e)

    '''
    set parameters for profile part
    dap feature, the short ones can be found in log, e,g ieon,iebs,deon,ded, please refer to XMLConfigConstants.py file
    feature value, the value you want set to the feature
    endpoint type, the endpoint type of each profile,it the feature not related to endpoint, leave it alone
    profile, the specific profile name
    '''

    def set_feature_profile(self, dap_feature, feature_value, profile, endpoint_type=""):
        try:
            if dap_feature in ["dom", "beon", "vbon"]:
                dap_feature = dap_profile_dict[dap_feature][0]
            else:
                dap_feature = dap_profile_dict[dap_feature]
            e_dap_feature = self.get_dapE_profile(dap_feature, profile, endpoint_type)
            e_dap_feature.set('value', feature_value)
            print ("Set parameters succeed: " + e_dap_feature.tag)
        except Exception, e:
            print (e)

    # print expect value for all supported features
    def print_expect_value(self, _profile_name="Movie", tuning_device_name_endpoint="Speaker_landscape"):
        self.__initialize_parameters_value_to_non_exist()
        profile_only_feature = ["ieon", "iea", "mdee", "mdle", "miee", "msce", "mave", "dvme"]
        profile_endpoint_feature = ["plb", "deon", "dea", "ded", "ngon", "dsb", "vmb",
                                    "dvle", "dvla", "dvli", "dvlo", "geon"]
        input_file_path = os.path.abspath(self.__input)
        input_dirname=os.path.dirname(input_file_path)
        out_file_name= _profile_name + "_" + tuning_device_name_endpoint + ".txt"
        out_file=os.path.join(input_dirname,out_file_name)

        fo = open(out_file, "w")
        for feature in POST_PROCESSING_PARAS_LIST:
            # print feature
            _value = ""
            if feature in ["dom", "beon", "vbon"]:
                _value = self.get_feture_dom_bass(feature, _profile_name, tuning_device_name_endpoint)
            elif feature in ["aobs", "arbs"]:
                _value = self.get_feature_aobs_arbs(feature, tuning_device_name_endpoint)
            elif feature in ["vbmf", "vbsf", "vbhg"]:
                _value = self.get_feature_vb(feature, tuning_device_name_endpoint)
            elif feature in ["iebs", "gebs"]:
                _value = self.get_iebs_gebs(feature, _profile_name)
            elif feature in profile_only_feature:
                _value = self.get_feature_profile_only(feature, _profile_name)
            elif feature in profile_endpoint_feature:
                _value = self.get_feature_profile_endpoint(feature, _profile_name, tuning_device_name_endpoint)
            else:
                _value = self.get_feature_tuning(feature, tuning_device_name_endpoint)
            if _value == "true":
                _value = 1
            if _value == "false":
                _value = 0
            # save all post processing params to order dictionary
            TuningFileParser.POST_PROCESSING_PARAS_DICT[feature] = str(_value)
            fo.write(feature + "=" + str(_value) + "\n")
        fo.close()
        print ("Succeed read :" + out_file_name)
        return TuningFileParser.POST_PROCESSING_PARAS_DICT

    # print values for all profiles and endpoints
    def print_value_for_all(self):
        for _profile in profile_name:
            for _endpoint in tuning_endpoint_name:
                self.print_expect_value(_profile, _endpoint)

    # for save xml
    def save(self, output_file):
        input_file_path = os.path.abspath(self.__input)
        input_dirname = os.path.dirname(input_file_path)
        _output_file = os.path.join(input_dirname, output_file)
        self.__root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        self.__root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
        self.__tree.write(_output_file, encoding='utf-8', xml_declaration=True)


help_content = '''This is used to :
1.Read xml to display in the same format with log dumps
2.Update dap feature value in xml

Usage: 
read xml:xmlUpdater.py -i dax-default.xml -e Speaker_landscape -p Movie --option=read
write xml:xmlUpdater.py -i dax-default.xml -pf parameters.csv -o changed_dax-default.xml --option=write

Mandatory Parameters:
-i/--input:   Tuning XML to be parsed.specify the path

Optional Parameters:   
-p/--profile=           Profile name,default value is "Movie".
-e/--endpoint=          Endpoint name,default value is "Speaker_landscape".
-o/--output=            Saved xml after changed,default value is "changed_dax-default.xml".
                        No need to specify path, it will be in the same path as input xml file.
--option=               option can be read and write, the two usage of the script, default is "read"
--parameters_file=  Paramter file which list the paramters and values want to change,
                        default value is "parameters.csv". The format shall be:
                        The first colume is feature, 2nd colume is value, 3rd is Profile or endpoint name
                        4th colume: endpoint type if it's profile feature, can be blank
                        aobs if it's gain_left/right,arbs if it's threshold_low/high, other blank
                        e.g
                        dom             false   Movie               speaker
                        ieon            false   Movie               
                        dom             true    Speaker_portrait    
                        gain_left       -240    Speaker_portrait    aobs
                        threshold_low   -2080   Headphone           arbs
                        aoon            true    Headphone   
--readAll=              If this parameter is true, it will read all profiles and endpoints
'''
if __name__ == "__main__":
    try:
        opts, args = getopt(sys.argv[1:], 'hi:p:e:o:pf',
                            ['help', 'input=', 'profile=', 'endpoint=', 'output=', 'parameters_file=', 'option=',
                             'readAll='])
    except Exception, e:
        print (e)
        sys.exit(1)

    if len(opts) == 0:
        print ("Please specify the mandatory parameters. Use '-h' or '--help' to see how to use this tool")
        sys.exit(0)

        # Assgin default values to the parameters
    input_file = None
    output_file = "Changed_dax-default.xml"
    endpoint = 'Speaker_landscape'
    parameters_file = "parameters.csv"
    profile = 'Movie'
    option = 'read'
    readAll = 'true'
    try:
        for op, value in opts:
            if op in ('--help', '-h'):
                print (help_content)
                sys.exit(0)
            if op in ('-i', '--input'):
                input_file = value
            if op in ('-p', '--profile'):
                profile = value
                if profile not in profile_name:
                    print ("profile name shall be the following:")
                    print (profile_name)
                    sys.exit(1)
            if op in ('-e', '--endpoint'):
                endpoint = value
                if endpoint not in tuning_endpoint_name:
                    print ("endpoint name shall be the following:")
                    print (tuning_endpoint_name)
                    sys.exit(1)
            if op in ('-o', '--output'):
                output_file = value
            if op in ('-pf', '--parameters_file'):
                parameters_file = value
            if op in ('--option',):
                option = value
                if option not in ('read', 'write'):
                    print ("Option must be 'read' or 'write'.Use '-h' or '--help' to see how to use this tool")
                    sys.exit(1)
            if op in ('--readAll',):
                readAll = value
                if readAll not in ('true', 'false'):
                    print ("ReadAll must be 'true' or 'false'.Use '-h' or '--help' to see how to use this tool")
                    sys.exit(1)
        if input_file is None:
            print ("Missing Input File Name. Use '-h' or '--help' to see how to use this tool")
            sys.exit(1)
    except Exception, e:
        print (e)
    tuningFileUpdater = TuningFileParser(input_file)
    # read values of all profile and all endpoint
    if readAll == 'true':
        for profile in profile_name:
            tuningFileUpdater.print_value_for_all()
    elif option == 'read':
        tuningFileUpdater.print_expect_value(profile, endpoint)
    # change parameters according to the csv file
    if option == "write":
        with open(parameters_file, 'rb') as csvfile:
            pramreader = csv.reader(csvfile)
            for row in pramreader:
                dap_feature = row[0]
                feature_value = row[1]
                temp = row[2]
                if temp in profile_name:
                    profile = temp
                    endpoint_type = row[3]
                    tuningFileUpdater.set_feature_profile(dap_feature, feature_value, profile, endpoint_type)
                if temp in tuning_endpoint_name:
                    endpoint = temp
                    ao_or_ar = row[3]
                    tuningFileUpdater.set_feature_tuning(dap_feature, feature_value, endpoint, ao_or_ar)
        tuningFileUpdater.save(output_file)
