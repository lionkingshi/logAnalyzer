package com.dolby.qa.featuretest;


public class Constants {
    public static final String EXTRA_CMD_ACTION = "feature_test";

    //common key
    public static final String EXTRA_CMD_STEP = "step";
    public static final String EXTRA_CMD_STEP_PLAY_CONTENT = "play_content";
    public static final String EXTRA_CMD_STEP_STOP_PLAYBACK = "stop_playback";
    public static final String EXTRA_CMD_STEP_RESTART_PLAYBACK = "restart_playback";
    public static final String EXTRA_CMD_STEP_CHANGE_DAP_FEATURE = "change_dap_feature";
    public static final String EXTRA_CMD_STEP_RECORD_LOG = "record_log";
    public static final String EXTRA_CMD_STEP_RELEASE_RESOURCE = "release_resource";
    //public static final String EXTRA_CMD_STEP_RESET_DAP = "reset_dap";

    //playing content key
    public static final String EXTRA_CMD_CONTENT_LOCATION = "content_location";

    //key matched by first class api
    public static final String EXTRA_CMD_FEATURE_DAP_STATUS = "dap_status";
    public static final String EXTRA_CMD_FEATURE_DAP_PROFILE = "dap_profile";
    public static final String EXTRA_CMD_FEATURE_DAP_RESET_PROFILE = "dap_reset_profile";
    public static final String EXTRA_CMD_FEATURE_DAP_RESET_UNIVERSAL = "dap_reset_universal";
    public static final String EXTRA_CMD_FEATURE_DAP_PROFILE_DE = "dap_profile_de";
    public static final String EXTRA_CMD_FEATURE_DAP_PROFILE_IEQ = "dap_profile_ieq";
    public static final String EXTRA_CMD_FEATURE_DAP_PROFILE_HV = "dap_profile_hv";
    public static final String EXTRA_CMD_FEATURE_DAP_PROFILE_VSV = "dap_profile_vsv";
    public static final String EXTRA_CMD_FEATURE_DAP_UNIVERSAL_VL = "dap_universal_vl";
    public static final String EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEQ = "dap_universal_geq";
    public static final String EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEBG = "dap_universal_gebg";
    public static final String EXTRA_CMD_FEATURE_DAP_UNIVERSAL_BE = "dap_universal_be";
    //key matched by low level api
    public static final String EXTRA_CMD_FEATURE_DAP_FEATURE_TYPE = "dap_feature_type";
    public static final String EXTRA_CMD_FEATURE_DAP_FEATURE_VALUE = "dap_feature_value";


    //message type
    public static final int MSG_WHAT_DEFAULT = 0;
    //play content
    public static final int MSG_PLAY_CONTENT=0X100;
    //stop and restart playback
    public static final int MSG_STOP_PLAYBACK=0X101;
    public static final int MSG_RESTART_PLAYBACK=0X102;
    //change dap
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_STATUS=0X111;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_PROFILE=0X112;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_RESET_PROFILE=0X113;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_RESET_UNIVERSAL=0X114;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DE=0X115;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_IEQ=0X116;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_HV =0X117;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VSV =0X118;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_VL=0X119;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_GEQ=0X120;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_GEBG =0X121;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_BE=0X122;
    public static final int MSG_CHANGE_DAP_FEATURE_DAP_FEATURE_TYPE=0X123;
    //record log
    public static final int MSG_RECORD_LOG=0X130;
    //release all resource : dap ,audio track instance
    public static final int MSG_RELEASE_RESOURCE=0X140;

    //invalid num definition
    public static final int INVALID_DAP_PROFILE_ID = 8 ;
    public static final int RESET_DAP_ALL_PROFILE_PARA = 10 ;
    public static final int MSG_ARG1_DEFAULT = 0 ;
    public static final int ID_RESET_ALL_PROFILE = 10 ;
    public static final int PROFILE_NUM = 6 ;
}
