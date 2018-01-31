#!/usr/bin/python
"""
Created on 1 20st, 2018
@author: Hongzhe Shi
"""

import sys, os
import logging
from collections import OrderedDict
from os.path import abspath, join, exists, isfile

#  "DAPv1 parameters name" to "DAPv2 parameters name"
help_content='''
Usage: runAutoTest.py [Mandatory parameters] [Optional parameters]

Mandatory parameters:
-t/--target\t\t: Followed by the build target id, to see a list of available targets and their corresponding IDs, execute: android list targets.

Optional parameters:
-p/--priority\t\t: Specify test priority, the value can be set to high, medium or low, by default, all auto cases will be executed.
-r/--revision\t\t: Specify the revision number of dev branch, otherwise, it will sync the latest code by default.
--offline\t\t: Execute auto test through offline mode, produce code will be synchronized automatically by script.
--uploadresult\t\t: Upload test result immediately once completing test execution.
--sendmail\t\t: Send out Auto test report by E-mail.

'''

DAP1_2_DAP2 = OrderedDict()
FILTER_TYPE_FLAG_GLOBAL = '1'
key_word_in_global_process = 'DlbDap2Process'

ARENDERER_PARAS_DIC = OrderedDict()
FILTER_TYPE_FLAG_QMF = '2'
key_word_in_qmf_process = 'DlbDap2QmfProcess'

DEVICE_PARAS_DIC = OrderedDict()
FILTER_TYPE_FLAG_DEVICE_PARA = '3'

#define global dap parameters 
#for non-dolby content , 
#for dolby content ,
def initilize_global_para_ordered_dict():
	DAP1_2_DAP2['dea'] = '0xffff'
	DAP1_2_DAP2['iea'] = '0xffff'
	DAP1_2_DAP2['dsa'] = '0xffff'
	DAP1_2_DAP2['beb'] = '0xffff'
	DAP1_2_DAP2['plb'] = '0xffff'
	DAP1_2_DAP2['vmb'] = '0xffff'
	DAP1_2_DAP2['dsb'] = '0xffff'
	DAP1_2_DAP2['ded'] = '0xffff'
	DAP1_2_DAP2['vbm'] = '0xffff'
	DAP1_2_DAP2['dom'] = '0xffff'
	DAP1_2_DAP2['bew'] = '0xffff'
	DAP1_2_DAP2['dvla'] = '0xffff'
	DAP1_2_DAP2['arra'] = '0xffff'
	DAP1_2_DAP2['dfsa'] = '0xffff'
	DAP1_2_DAP2['dhsa'] = '0xffff'
	DAP1_2_DAP2['dvmc'] = '0xffff'
	DAP1_2_DAP2['arod'] = '0xffff'
	DAP1_2_DAP2['msce'] = '0xffff'
	DAP1_2_DAP2['arde'] = '0xffff'
	DAP1_2_DAP2['mdee'] = '0xffff'
	DAP1_2_DAP2['miee'] = '0xffff'
	DAP1_2_DAP2['mdle'] = '0xffff'
	DAP1_2_DAP2['dvle'] = '0xffff'
	DAP1_2_DAP2['dvme'] = '0xffff'
	DAP1_2_DAP2['mave'] = '0xffff'
	DAP1_2_DAP2['vcbf'] = '0xffff'
	DAP1_2_DAP2['becf'] = '0xffff'
	DAP1_2_DAP2['vbmf'] = '0xffff'
	DAP1_2_DAP2['vbsf'] = '0xffff'
	DAP1_2_DAP2['preg'] = '0xffff'
	DAP1_2_DAP2['vbhg'] = '0xffff'
	DAP1_2_DAP2['vbog'] = '0xffff'
	DAP1_2_DAP2['vbsg'] = '0xffff'
	DAP1_2_DAP2['dvli'] = '0xffff'
	DAP1_2_DAP2['dhfm'] = '0xffff'
	DAP1_2_DAP2['vbon'] = '0xffff'
	DAP1_2_DAP2['beon'] = '0xffff'
	DAP1_2_DAP2['deon'] = '0xffff'
	DAP1_2_DAP2['geon'] = '0xffff'
	DAP1_2_DAP2['ieon'] = '0xffff'
	DAP1_2_DAP2['ngon'] = '0xffff'
	DAP1_2_DAP2['aoon'] = '0xffff'
	DAP1_2_DAP2['aron'] = '0xffff'
	DAP1_2_DAP2['dvlo'] = '0xffff'
	DAP1_2_DAP2['artp'] = '0xffff'
	DAP1_2_DAP2['pstg'] = '0xffff' # audio dump parameter does not include this
	DAP1_2_DAP2['gebs'] = '0xffff'
	DAP1_2_DAP2['iebs'] = '0xffff'
	DAP1_2_DAP2['aobs'] = '0xffff'
	DAP1_2_DAP2['arbs'] = '0xffff'

#define content-processing dap parameters 
#for non-dolby content , 
#for dolby content ,
def initilizeQMFParaOrderedDict():
    ARENDERER_PARAS_DIC['dea'] = '0xffff'
    ARENDERER_PARAS_DIC['iea'] = '0xffff'
    ARENDERER_PARAS_DIC['dsa'] = '0xffff'
    ARENDERER_PARAS_DIC['beb'] = '0xffff'
    ARENDERER_PARAS_DIC['plb'] = '0xffff'
    ARENDERER_PARAS_DIC['vmb'] = '0xffff'
    ARENDERER_PARAS_DIC['dsb'] = '0xffff'
    ARENDERER_PARAS_DIC['ded'] = '0xffff'
    # ARENDERER_PARAS_DIC['vbm'] = '0xffff'
    ARENDERER_PARAS_DIC['vol'] = '0xffff'   # add this line 
    ARENDERER_PARAS_DIC['dom'] = '0xffff'
    ARENDERER_PARAS_DIC['bew'] = '0xffff'
    ARENDERER_PARAS_DIC['dvla'] = '0xffff'
    # ARENDERER_PARAS_DIC['arra'] = '0xffff'
    ARENDERER_PARAS_DIC['dfsa'] = '0xffff'
    ARENDERER_PARAS_DIC['dhsa'] = '0xffff'
    ARENDERER_PARAS_DIC['dvmc'] = '0xffff'
    # ARENDERER_PARAS_DIC['arod'] = '0xffff'
    ARENDERER_PARAS_DIC['msce'] = '0xffff'
    # ARENDERER_PARAS_DIC['arde'] = '0xffff'
    ARENDERER_PARAS_DIC['mdee'] = '0xffff'
    ARENDERER_PARAS_DIC['miee'] = '0xffff'
    ARENDERER_PARAS_DIC['mdle'] = '0xffff'
    ARENDERER_PARAS_DIC['dvle'] = '0xffff'
    ARENDERER_PARAS_DIC['dvme'] = '0xffff'
    ARENDERER_PARAS_DIC['mave'] = '0xffff'
    ARENDERER_PARAS_DIC['vcbf'] = '0xffff'
    ARENDERER_PARAS_DIC['becf'] = '0xffff'
    ARENDERER_PARAS_DIC['vbmf'] = '0xffff'
    ARENDERER_PARAS_DIC['vbsf'] = '0xffff'
    ARENDERER_PARAS_DIC['preg'] = '0xffff'
    ARENDERER_PARAS_DIC['vbhg'] = '0xffff'
    ARENDERER_PARAS_DIC['vbog'] = '0xffff'
    ARENDERER_PARAS_DIC['vbsg'] = '0xffff'
    ARENDERER_PARAS_DIC['dvli'] = '0xffff'
    ARENDERER_PARAS_DIC['dhfm'] = '0xffff'
    # ARENDERER_PARAS_DIC['vbon'] = '0xffff'
    # ARENDERER_PARAS_DIC['beon'] = '0xffff'
    ARENDERER_PARAS_DIC['deon'] = '0xffff'
    # ARENDERER_PARAS_DIC['geon'] = '0xffff'
    ARENDERER_PARAS_DIC['ieon'] = '0xffff'
    ARENDERER_PARAS_DIC['ngon'] = '0xffff'
    # ARENDERER_PARAS_DIC['aoon'] = '0xffff'
    # ARENDERER_PARAS_DIC['aron'] = '0xffff'
    ARENDERER_PARAS_DIC['dvlo'] = '0xffff'
    # ARENDERER_PARAS_DIC['artp'] = '0xffff'
    # ARENDERER_PARAS_DIC['pstg'] = '0xffff' # audio dump parameter does not include this
    ARENDERER_PARAS_DIC['gebs'] = '0xffff'
    ARENDERER_PARAS_DIC['iebs'] = '0xffff'
    ARENDERER_PARAS_DIC['aobs'] = '0xffff'
    # ARENDERER_PARAS_DIC['arbs'] = '0xffff'

#define 12 device parameters 
def initilizeDeviceParaOrderedDict():
	DEVICE_PARAS_DIC['aoon'] = '0xfffe'
	DEVICE_PARAS_DIC['beon'] = '0xfffe'
	DEVICE_PARAS_DIC['vbon'] = '0xfffe'
	DEVICE_PARAS_DIC['vbm'] = '0xfffe'
	DEVICE_PARAS_DIC['bexe'] = '0xfffe'
	DEVICE_PARAS_DIC['geon'] = '0xfffe'
	DEVICE_PARAS_DIC['aron'] = '0xfffe'
	DEVICE_PARAS_DIC['arde'] = '0xfffe'
	DEVICE_PARAS_DIC['arra'] = '0xfffe'
	DEVICE_PARAS_DIC['arod'] = '0xfffe'
	DEVICE_PARAS_DIC['artp'] = '0xfffe'
	DEVICE_PARAS_DIC['arbs'] = '0xfffe'

#define content processing parameters
CONTENT_PROCESSING_PARAM_LIST = ['deon', 'dvle', 'ieon', 'dvme', 'dom', 'msce', 'miee', 'mdle', 'mdee', 'mave', 'ngon']
DEVICE_PROCESSING_PARAM_LIST = ['aoon', 'beon', 'vbon', 'vbm', 'bexe', 'geon', 'aron', 'arde', 'arra', 'arod', 'artp', 'arbs']


def filterParamter(filter_type,input_file_name):
	print('Welcome to DAP Parameters Converter!')
	print("==="+filter_type)
	# initial the order dictory to align with audio dump parameter list
    # key_word = 'unknown'
	if FILTER_TYPE_FLAG_GLOBAL == filter_type:
		initilize_global_para_ordered_dict()
        key_word = key_word_in_global_process
	elif filter_type == FILTER_TYPE_FLAG_QMF:

		initilizeQMFParaOrderedDict()


	else :
		initilizeDeviceParaOrderedDict()

	# Read data from log file
	with open(input_file_name, 'r') as fp_r:
		lines = fp_r.readlines()
		fp_r.close()

	for line in lines:
		line = line.strip('\n')
		line = line.replace(' ','') # remove empty char
		# print("read string is :"+line)
		if line != "":
            if line
			FourccStartIndex = line.find('(') # dap parameter begin with '(' and end with '=''
			FourccEndIndex = line.find('=')
			# print("para name rang : {start}:{end}".format(start=FourccStartIndex,end=FourccEndIndex))
			if (FourccStartIndex >= 0 ) and (FourccEndIndex >= 0 ):
				FourccValueStartIndex = line.find('[') # dap parameter value begin with '[' and end with ']'
				FourccValueEndIndex = line.find(']')
				# print("para value rang : {start}:{end}".format(start=FourccValueStartIndex,end=FourccValueEndIndex))
				if (FourccValueStartIndex >= 0) and (FourccValueEndIndex >= 0):
					Fourcc = line[(FourccStartIndex+1):FourccEndIndex]
					FourccValue= line[(FourccValueStartIndex+1):FourccValueEndIndex]
					if filter_type == FILTER_TYPE_FLAG_GLOBAL:
						DAP1_2_DAP2[Fourcc] = FourccValue
					elif filter_type == FILTER_TYPE_FLAG_QMF:
						ARENDERER_PARAS_DIC[Fourcc] = FourccValue
					else:
						DEVICE_PARAS_DIC[Fourcc] = FourccValue
	# for key,value in DAP1_2_DAP2.items():
	#     print key + " => " + value

		# print('length : {length}'.format(length=len(line)))
		# print('line content is {content}'.format(content=line))
		# keys = (line.split('=')[0])
		# values = (line.split('=')[1])
		# print('dap paramater name {dap_para} and its value :{dap_para_value}'.format(dap_para=keys,dap_para_value=values))
	print('Done! Refer to dap_cpdp.txt')


def parseGlobalParamter(input_file_name):
	filterParamter(FILTER_TYPE_FLAG_GLOBAL,input_file_name)

def parseQMFParameter(input_file_name):
	filterParamter(FILTER_TYPE_FLAG_QMF,input_file_name)

def parseDeviceParameterFromQMFProcess(input_file_name):
	filterParamter(FILTER_TYPE_FLAG_DEVICE_PARA,input_file_name)

def writeParameterToFile(input_order_diction,output_file_name):
	with open(output_file_name, 'w') as fp_w:
		for key,value in input_order_diction.items():
			content = key+"="+value+'\n'
			# print("write content to file :"+content)
			fp_w.write(content)
		fp_w.close()

def writeGlobalParameterToFile(output_file_name):
	writeParameterToFile(DAP1_2_DAP2,output_file_name)

def writeQMFParameterToFile(output_file_name):
	writeParameterToFile(ARENDERER_PARAS_DIC,output_file_name)

def writeDeviceParameterFromQMFProcessToFile(output_file_name):
	writeParameterToFile(DEVICE_PARAS_DIC,output_file_name)

def checkAllGlobalParameterIsSet():
	result = False
	for key,value in DAP1_2_DAP2.items():
	    # print key + " => " + value
		keys = (line.split('=')[0])
		values = (line.split('=')[1])
		if values == '0xffff':
			result = True
	return result


def checkGlobalParameterEqualToExpected(para_name,para_value):
	result = False 
	for key,value in DAP1_2_DAP2.items():
	    # print key + " => " + value
		keys = (line.split('=')[0])
		values = (line.split('=')[1])
		if keys == para_name:
			if para_value == value:
				result = True
	return result



def checkDeviceProcessingParameterInQMFProcessIsNotSet():
	result = True
	for key,value in DEVICE_PARAS_DIC.items():
		# print key + " => " + value
		keys = (line.split('=')[0])
		values = (line.split('=')[1])
		if values == '0xffff':
			result = True
		else:
			result = False
	return result


def checkContentProcessingParameterInGlobalProcessIsNotSet():
	result = False 
	for key in CONTENT_PROCESSING_PARAM_LIST.items():
		if DAP1_2_DAP2[key] == '0':
			print("no double processing!")
		else:
			result = True
			print("double processing! key = "+key)
			print("double processing! value = "+DAP1_2_DAP2[key])
	return result



#Create a temporary folder
def createFolder(folderName):
	# logging.getLogger.info('Create a temporary folder : {name}'.format(name=folderName))
	# print("======="+folderName)
	import shutil
	try:
		folder = folderName
		if exists(folder):
			shutil.rmtree(folder)
		os.mkdir(folder)
		# print("folder created!")
	except Exception, e:
		print(e)
		raise e 

#Delete a folder


def deleteFolder(folderName):
	print("delete a folder "+folderName)



def main(argvs):
	import getopt 
	try:
		opts, args = getopt.getopt(argvs, 'hf:i:o:e:',['isdolbycontent','input','output', 'expectedresult'])
	except Exception,e:
		print e
		sys.exit(0)
	if len(opts) == 0:
		print("please specify the effect process name , input file name and output file name ....")
		sys.exit(0)

	flag_is_dolby_content = False #'dap2'
	input_file_name = None #'effect_params_from_log.txt'
	output_file_name = None #'effect_params_from_log_parse.txt'
	expected_fourcc_para = None
	expected_fourcc_value = None
	print(" opts :"+str(opts))

	try:
		for op, value in opts:
			if op in ('-h', '--help'):
				print help_content
				sys.exit(0)
			if op in ('-f', '--isdolbycontent'):
				print ("is dolby content :"+value)
				flag_is_dolby_content=value
				# if value.lower() in ('qmf', 'dap2'):
				# 	process_name = value.lower()
				# else:
				# 	print('Please set the process name where you want to parse the dap parameters !')
				# 	sys.exit(0)
			if op in ('-i', '--input'):
				print("input file name :"+value)
				input_file_name = value
				if input_file_name is None:
					print 'Please set the log file name which is filted from logcat !'
					sys.exit(0)
			if op in ('-o', '--output'):
				output_file_name = value
				print("output file name :"+value)
				if output_file_name is None:
					print 'Better to set the output file name which would be parsed from input file ! '
					print 'If not specified , use default value : effect_params_from_log_parse.txt !'
			if op in ('-e', '--expectedresult'):
				expected_fourcc_para=value.split('=')[0]
				expected_fourcc_value=value.split('=')[1]
				if expected_fourcc_para is None:
					print 'expected result format is wrong. use this format : dom=0 .'
					sys.exit(0)
				if expected_fourcc_value is None:
					print 'expected result format is wrong. use this format : dom=0 .'
					sys.exit(0)
			parseGlobalParamter(input_file_name)
			writeGlobalParameterToFile(input_file_name+"effect_para.txt")

			parseQMFParameter(input_file_name)
			writeQMFParameterToFile(input_file_name+"arendered_para.txt")

			parseDeviceParameterFromQMFProcess(input_file_name)
			writeDeviceParameterFromQMFProcessToFile(input_file_name+"device_para_qmf.txt")

			if flag_is_dolby_content :
				print()
			else:


		# input_file_abs_path = abspath(input_file_name)
		# output_file_abs_path = abspath(output_file_name)
		# print (input_file_abs_path+"----"+output_file_abs_path)

		# input_file_abs_path = abspath(join('.','log','monospk'))
		# output_file_abs_path = abspath(output_file_name)
		# print (input_file_abs_path+"----"+output_file_abs_path)

		# # parseDAPParamter(process_name,input_file_name,output_file_name)
		# if process_name == 'dap2':
		# 	parseGlobalParamter(input_file_name)
		# 	writeGlobalParameterToFile(output_file_name)
		# elif process_name == 'qmf':
		# 	parseQMFParameter(input_file_name)
		# 	writeQMFParameterToFile(output_file_name)

		# new_folder=abspath(join('.','log1'))
		# print(new_folder)
		# createFolder(new_folder)
	except Exception, e:
		logging.getLogger().error('Encounter an exception : %s' %e)

if __name__ == "__main__":
	main(sys.argv[1:])





