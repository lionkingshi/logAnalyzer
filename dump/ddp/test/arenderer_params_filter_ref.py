#!/usr/bin/python
'''
Created on Mar 21st, 2017
@author: twang
'''

import sys
from collections import OrderedDict



ARENDERER_PARAS_DIC = OrderedDict()

def initilizeOrderedDict():
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


#  "DAPv1 parameters name" to "DAPv2 parameters name"


def main():
    print('Welcome to DAP Parameters Converter!')

    # initial the order dictory to align with audio dump parameter list
    initilizeOrderedDict()

    # Read data from log file
    with open('arendered_qmfprocess.bak', 'r') as fp_r:
        lines = fp_r.readlines()
        fp_r.close()

    for line in lines:
        line = line.strip('\n')
        line = line.replace(' ','') # remove empty char
        # print("read string is :"+line)
        if (line != ""):
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
                    ARENDERER_PARAS_DIC[Fourcc] = FourccValue
                    # print('fourcc : {name}={value}'.format(name=Fourcc,value=FourccValue))
                    # print('fourcc 2: {name}={value}'.format(name=Fourcc,value=ARENDERER_PARAS_DIC[Fourcc]))
                    pass

    # for key,value in ARENDERER_PARAS_DIC.items():
    #     print key + " => " + value

        # print('length : {length}'.format(length=len(line)))
        # print('line content is {content}'.format(content=line))
        # keys = (line.split('=')[0])
        # values = (line.split('=')[1])
        # print('dap paramater name {dap_para} and its value :{dap_para_value}'.format(dap_para=keys,dap_para_value=values))


    with open('arenderer_params_from_log_parse.txt', 'w') as fp_w:
        for key,value in ARENDERER_PARAS_DIC.items():
            content = key+"="+value+'\n'
            # print("write content to file :"+content)
            fp_w.write(content)
        fp_w.close()

    print('Done! Refer to arenderer_params_from_log_parse.txt')

if __name__ == "__main__":
    sys.exit(main())





