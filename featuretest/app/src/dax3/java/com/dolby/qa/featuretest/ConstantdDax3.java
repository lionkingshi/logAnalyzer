package com.dolby.qa.featuretest;

public class ConstantdDax3 {
    public static final int PROFILE_NUM = 4 ;
    public static final String TAG = "<<<< Dax3FeatureTest: " ;

    // following tuning device name list must sync up with dax-default.xml
    public static final String[][] TUNING_DEVICE_NAME_LIST =
            {
                    {"Speaker_landscape", "internal_speaker", "Speaker_portrait"},
                    {"hdmi"},
                    {"miracast"},
                    {"headphone_port"},
                    {"bluetooth","headphone_bluetooth","speaker_bluetooth"},
                    {"usb","headphone_usb","speaker_usb"},
                    {"other"}
            };
}
