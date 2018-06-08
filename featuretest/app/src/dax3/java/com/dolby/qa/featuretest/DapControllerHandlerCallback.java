package com.dolby.qa.featuretest;


import android.os.Handler;
import android.os.Message;
import android.util.Log;

import com.dolby.dax.DolbyAudioEffect;
import com.dolby.dax.DsParams;
import com.dolby.dax.DsTuning;

import java.io.UnsupportedEncodingException;
import java.util.Arrays;
import java.util.Locale;

import static com.dolby.qa.featuretest.ConstantdDax3.COMMAND_INDEX_MAPPING;
import static com.dolby.qa.featuretest.Constants.GLOBAL_SESSION_ID_NUM;
import static com.dolby.qa.featuretest.Constants.MIDDLE_PRIORITY_NUM;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_TUNING_DEVICE_NAME;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_DAP_FEATURE_TYPE_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_DAP_FEATURE_VALUE_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_DAP_PROFILE_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_DAP_STATUS_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_PLAY_CONTENT_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_RESET_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_UI_ARG1_DEFAULT;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_UI_ARG1_VISIBLE;
import static com.dolby.qa.featuretest.Constants.VOLUME_ADJUSTMENT_DIRECTION_LOWER;
import static com.dolby.qa.featuretest.Constants.VOLUME_ADJUSTMENT_DIRECTION_MAXIMUM;
import static com.dolby.qa.featuretest.Constants.VOLUME_ADJUSTMENT_DIRECTION_MUTE;
import static com.dolby.qa.featuretest.Constants.VOLUME_ADJUSTMENT_DIRECTION_RAISE;
import static com.dolby.qa.featuretest.Constants.VOLUME_ADJUSTMENT_DIRECTION_SAME;
import static com.dolby.qa.featuretest.MainActivity.mDAP;
import static com.dolby.qa.featuretest.MainActivity.mTrack;
import static com.dolby.qa.featuretest.MainActivity.playOrPause;
import static com.dolby.qa.featuretest.MainActivity.releaseResource;
import static com.dolby.qa.featuretest.MainActivity.restartPlayback;
import static com.dolby.qa.featuretest.MainActivity.setStreamVolume;
import static com.dolby.qa.featuretest.MainActivity.setTrackVolume;
import static com.dolby.qa.featuretest.MainActivity.stopPlayback;

public class DapControllerHandlerCallback implements Handler.Callback{
    private final String TAG = ConstantdDax3.TAG;
    private Handler mUpdateUIHandlerInMainUi;

    public DapControllerHandlerCallback(Handler mUpdateUIHandlerInMainUi) {
        this.mUpdateUIHandlerInMainUi = mUpdateUIHandlerInMainUi;
    }

    @Override
    public boolean handleMessage(Message msg) {
        int messageType = msg.what;
        switch (messageType) {
            case Constants.MSG_PLAY_CONTENT:
                String mContentShowInPlayContentTV = String.format(Locale.getDefault(), "play content : %s", msg.obj);
                packageIntentForUIUpdate(MSG_UPDATE_PLAY_CONTENT_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mContentShowInPlayContentTV);
                String mFileName = (String) msg.obj;
                playOrPause(mFileName);
                /* create a dap instance every time app playback content */
                if (mDAP != null) {
                    mDAP.release();
                    mDAP=null;
                }
                if (mTrack != null){
                    mTrack.release();
                    mTrack = null;
                }
//                        mDAP = new DolbyAudioEffect(5, mSession);
                mDAP = new DolbyAudioEffect(MIDDLE_PRIORITY_NUM, GLOBAL_SESSION_ID_NUM);
                break;
            case Constants.MSG_STOP_PLAYBACK:
                stopPlayback();
                break;
            case Constants.MSG_RESTART_PLAYBACK:
                restartPlayback();
                break;
            case Constants.MSG_VOLUME_CONTROL:
                int m_adjustment_direction = msg.arg1;
                switch (m_adjustment_direction){
                    case VOLUME_ADJUSTMENT_DIRECTION_MUTE:
                        setStreamVolume(m_adjustment_direction,true,false);
                        break;
                    case VOLUME_ADJUSTMENT_DIRECTION_MAXIMUM:
                        setStreamVolume(m_adjustment_direction,false,true);
                        break;
                    case VOLUME_ADJUSTMENT_DIRECTION_LOWER:
                    case VOLUME_ADJUSTMENT_DIRECTION_SAME:
                    case VOLUME_ADJUSTMENT_DIRECTION_RAISE:
                        setStreamVolume(m_adjustment_direction,false,false);
                        break;
                }
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_STATUS:
                String mContentShowInDapStatusTV = String.format(Locale.getDefault(), "set ds status : %b", msg.arg1 != 0);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_STATUS_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mContentShowInDapStatusTV);
                mDAP.setDsOn(msg.arg1 != 0);
                break;

            case MSG_CHANGE_TUNING_DEVICE_NAME:
                int mPortId = msg.arg1;
                int mTuningDeviceNameIndex = msg.arg2;

                try {
                    if ((msg.arg1 >= DsTuning.internal_speaker.toInt()) &&
                            (msg.arg1 <= DsTuning.usb.toInt())){

                        String[] mTuningDeviceNameList = mDAP.getTuningDevicesList(mPortId);

                        int m_tuning_device_list_length = mTuningDeviceNameList.length;

                        for(int index=0;index<m_tuning_device_list_length;index++){
                            Log.d(TAG,"tuning device name list : " + index +
                                    "==" + mTuningDeviceNameList[index]);
                        }

                        if (mTuningDeviceNameIndex >= mTuningDeviceNameList.length){
                            Log.d(TAG,"tuning device name index invalid: "+
                                    mTuningDeviceNameIndex + " not in range [0:" +
                                    mTuningDeviceNameList.length+")");
                        }else {
                            for (int index=0;index<m_tuning_device_list_length;index++){
                                if (mTuningDeviceNameList[index].contains(
                                        COMMAND_INDEX_MAPPING[mTuningDeviceNameIndex])){
                                    String mTuningInfoShowInTV =
                                            String.format(
                                                    Locale.getDefault(),
                                                    "change tuning device name to : %s",
                                                    mTuningDeviceNameList[index]);

                                    packageIntentForUIUpdate(
                                            MSG_UPDATE_DAP_FEATURE_TYPE_TV,
                                            MSG_UPDATE_UI_ARG1_DEFAULT,
                                            mTuningInfoShowInTV);

                                    Log.d(TAG, "change tuning port :" + msg.arg1);
                                    Log.d(TAG, "change tuning device name :" +
                                            mTuningDeviceNameList[index]);

                                    mDAP.setSelectedTuningDevice(
                                            mPortId,
                                            mTuningDeviceNameList[index]);
                                }
                            }

//                            String mTuningInfoShowInTV =
//                                    String.format(
//                                            Locale.getDefault(),
//                                            "change tuning device name to : %s",
//                                            mTuningDeviceNameList[mTuningDeviceNameIndex]);
//
//                            packageIntentForUIUpdate(
//                                    MSG_UPDATE_DAP_FEATURE_TYPE_TV,
//                                    MSG_UPDATE_UI_ARG1_DEFAULT,
//                                    mTuningInfoShowInTV);
//
//                            Log.d(TAG, "change tuning port :" + msg.arg1);
//                            Log.d(TAG, "change tuning device name :" +
//                                    mTuningDeviceNameList[mTuningDeviceNameIndex]);
//
//                            mDAP.setSelectedTuningDevice(
//                                    mPortId,
//                                    mTuningDeviceNameList[mTuningDeviceNameIndex]);
                        }
                    }else {
                        Log.d(TAG,"tuning port index invalid: " +
                                msg.arg1 + "not in range [" +
                                DsTuning.internal_speaker.toInt() +
                                ":" +
                                DsTuning.usb.toInt()+"]");
                    }
                }catch (UnsupportedEncodingException e1){
                    e1.printStackTrace();
                    Log.d(TAG,"fail to change to tuning device name : port-tuning = "+
                            msg.arg1+"-"+msg.arg2);
                }
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE:
                String mContentShowInDapProfileTV = String.format(Locale.getDefault(), "set profile id: %d", msg.arg1);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_PROFILE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mContentShowInDapProfileTV);
                mDAP.setProfile(msg.arg1);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_RESET_PROFILE:
                if (msg.arg1 == Constants.ID_RESET_ALL_PROFILE) {
                    String mContentShowInDapFeatureTypeTV = String.format(Locale.getDefault(), "reset all profile : %d", msg.arg1);
                    packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mContentShowInDapFeatureTypeTV);

                    for (int index = 0; index < ConstantdDax3.PROFILE_NUM; index++) {
                        if (mDAP.isProfileSpecificSettingsModified(index)) {
                            mDAP.resetProfileSpecificSettings(index);
                        }
                    }
                } else {
                    String mContentShowInDapFeatureTypeTV = String.format(Locale.getDefault(), "reset profile id: %d", msg.arg1);
                    packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mContentShowInDapFeatureTypeTV);
                    mDAP.resetProfileSpecificSettings(msg.arg1);
                }
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DE:
                String mdeTV = String.format(Locale.getDefault(), "change de : %b", msg.arg1 != 0);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mdeTV);
                mDAP.setDialogEnhancerEnabled(msg.arg1 != 0);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DEA:
                String mdeaTV = String.format(Locale.getDefault(), "change dea : %d", msg.arg1);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mdeaTV);
                mDAP.setDialogEnhancerAmount(msg.arg1);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_IEQ:
                String mieqTV = String.format(Locale.getDefault(), "change ieq : %d", msg.arg1);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mieqTV);
                mDAP.setIeqPreset(msg.arg1);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_HV:
                String mhvTV = String.format(Locale.getDefault(), "change headphone virtualizer : %b", msg.arg1 != 0);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mhvTV);
                mDAP.setHeadphoneVirtualizerEnabled(msg.arg1 != 0);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VSV:
                String mvsvTV = String.format(Locale.getDefault(), "change speaker virtualizer : %b", msg.arg1 != 0);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mvsvTV);
                if (!mDAP.isMonoSpeaker()){
                    mDAP.setSpeakerVirtualizerEnabled(msg.arg1 != 0);
                }else{
                    try{
                        mDAP.setSpeakerVirtualizerEnabled(msg.arg1 != 0);
                    }catch (UnsupportedOperationException e){
                        e.printStackTrace();
                        Log.d(TAG,"virtual speaker virtualizer can not be operated for mono speaker endpoint!");
                    }
                }
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VL:
                String mvlTV = String.format(Locale.getDefault(), "change vl : %b", msg.arg1 != 0);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mvlTV);
                mDAP.setVolumeLevelerEnabled(msg.arg1!=0);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_BE:
                String mbeTV = String.format(Locale.getDefault(), "change be : %b", msg.arg1 != 0);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mbeTV);
                mDAP.setBassEnhancerEnabled(msg.arg1 != 0);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_GEBG:
                String mgeqbgTV = String.format(Locale.getDefault(), "change geq band gain : %s", msg.arg1);
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mgeqbgTV);
                int[] geqbgValue = (int[]) msg.obj;
                String mgeqbgValueTV = String.format(Locale.getDefault(), "geq band gain : %s", Arrays.toString(geqbgValue));
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_VALUE_TV,MSG_UPDATE_UI_ARG1_VISIBLE,mgeqbgValueTV);
                mDAP.setGeqBandGains(geqbgValue);
                break;
            case Constants.MSG_CHANGE_DAP_FEATURE_DAP_FEATURE_TYPE:
                String mTypeTV = "feature type :" + DsParams.FromInt(msg.arg1).toString();
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_TYPE_TV,MSG_UPDATE_UI_ARG1_DEFAULT,mTypeTV);
                int[] featureValue = (int[]) msg.obj;
                String mValueTV = String.format(Locale.getDefault(), "feature value : %s",Arrays.toString(featureValue));
                packageIntentForUIUpdate(MSG_UPDATE_DAP_FEATURE_VALUE_TV,MSG_UPDATE_UI_ARG1_VISIBLE,mValueTV);
                mDAP.setDapParameter(msg.arg1, featureValue);
                break;
            case Constants.MSG_RECORD_LOG:
                //show_dap_feature_type_tv.setText(String.format(Locale.getDefault(),"record log : %d",msg.arg1));
                break;
            case Constants.MSG_RELEASE_RESOURCE:
                releaseResource();
                packageIntentForUIUpdate(MSG_UPDATE_RESET_TV,MSG_UPDATE_UI_ARG1_DEFAULT,null);
                break;
            default:
                break;
        }
        return false;
    }

    private void packageIntentForUIUpdate(int msgType, int msgArg1, Object msgObj){
        Message msg= mUpdateUIHandlerInMainUi.obtainMessage();
        msg.what=msgType;
        msg.arg1= msgArg1;
        msg.obj=msgObj;
        mUpdateUIHandlerInMainUi.sendMessage(msg);
    }
}
