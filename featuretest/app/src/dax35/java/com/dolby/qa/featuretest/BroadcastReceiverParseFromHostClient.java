package com.dolby.qa.featuretest;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.widget.Toast;

import com.dolby.dax.DsParams;

import static com.dolby.qa.featuretest.ConstantdDax35.TUNING_DEVICE_NAME_LIST;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_ACTION;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_CONTENT_LOCATION;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_FEATURE_TYPE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_FEATURE_VALUE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_BE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_DE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_DEA;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_GEBG;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_HV;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_IEQ;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_VL;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_VSV;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_RESET_PROFILE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_RESET_UNIVERSAL;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_STATUS;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_TUNING_DEVICE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_TUNING_PORT;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_BE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEBG;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEQ;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_VL;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_CHANGE_DAP_FEATURE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_PLAY_CONTENT;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_RECORD_LOG;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_RELEASE_RESOURCE;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_RESTART_PLAYBACK;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_STOP_PLAYBACK;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_STEP_VOLUME_CONTROL;
import static com.dolby.qa.featuretest.Constants.EXTRA_CMD_VOLUME_ADJUSTMENT_DIRECTION;
import static com.dolby.qa.featuretest.Constants.INVALID_DAP_PROFILE_ID;
import static com.dolby.qa.featuretest.Constants.MSG_ARG1_DEFAULT;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_FEATURE_TYPE;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_BE;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DE;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DEA;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_GEBG;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_HV;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_IEQ;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VL;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VSV;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_RESET_PROFILE;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_DAP_FEATURE_DAP_STATUS;
import static com.dolby.qa.featuretest.Constants.MSG_CHANGE_TUNING_DEVICE_NAME;
import static com.dolby.qa.featuretest.Constants.MSG_PLAY_CONTENT;
import static com.dolby.qa.featuretest.Constants.MSG_RECORD_LOG;
import static com.dolby.qa.featuretest.Constants.MSG_RELEASE_RESOURCE;
import static com.dolby.qa.featuretest.Constants.MSG_RESTART_PLAYBACK;
import static com.dolby.qa.featuretest.Constants.MSG_STOP_PLAYBACK;
import static com.dolby.qa.featuretest.Constants.MSG_VOLUME_CONTROL;
import static com.dolby.qa.featuretest.Constants.RESET_DAP_ALL_PROFILE_PARA;
import static com.dolby.qa.featuretest.Constants.VOLUME_ADJUSTMENT_DIRECTION_SAME;

public class BroadcastReceiverParseFromHostClient extends BroadcastReceiver {
    private static final String TAG = ConstantdDax35.TAG;
    private Handler mBroadcastReceiverParseHandlerInMainUi;

    public BroadcastReceiverParseFromHostClient(Handler mBroadcastReceiverParseHandlerInMainUi) {
        this.mBroadcastReceiverParseHandlerInMainUi = mBroadcastReceiverParseHandlerInMainUi;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        String action=intent.getAction();
        if (action.equals(EXTRA_CMD_ACTION)){
            String type=intent.getStringExtra(EXTRA_CMD_STEP);
            switch (type) {
                case EXTRA_CMD_STEP_PLAY_CONTENT:
                    parseIntentPlayContent(context, intent);
                    break;
                case EXTRA_CMD_STEP_CHANGE_DAP_FEATURE:
                    parseIntentChangeFeature(context, intent);
                    break;
                case EXTRA_CMD_STEP_RECORD_LOG:
                    parseIntentRecordLog(context, intent);
                    break;
                case EXTRA_CMD_STEP_RELEASE_RESOURCE:
                    parseIntentReleaseResource(context, intent);
                    break;
                case EXTRA_CMD_STEP_STOP_PLAYBACK:
                    parseIntentStopPlayback(context, intent);
                    break;
                case EXTRA_CMD_STEP_RESTART_PLAYBACK:
                    parseIntentRestartPlayback(context, intent);
                    break;
                case EXTRA_CMD_STEP_VOLUME_CONTROL:
                    parseIntentVolumeControl(context,intent);
                    break;
                default:
                    Log.d(TAG, "receive broadcast , not expected action !");
                    break;
            }
        }
    }

    public void handleIntentAndThenSendMessage(int msgType, int msgArg1, Object msgObj){
        Message msg= mBroadcastReceiverParseHandlerInMainUi.obtainMessage();
        msg.what=msgType;
        msg.arg1= msgArg1;
        msg.obj=msgObj;
        mBroadcastReceiverParseHandlerInMainUi.sendMessage(msg);
    }

    public void handleIntentAndThenSendMessage(int msgType, int msgArg1, int msgArg2){
        Message msg= mBroadcastReceiverParseHandlerInMainUi.obtainMessage();
        msg.what=msgType;
        msg.arg1= msgArg1;
        msg.arg2 = msgArg2;
        mBroadcastReceiverParseHandlerInMainUi.sendMessage(msg);
    }


    public void parseIntentPlayContent(Context context,Intent intent){
        String mContentLocation=intent.getStringExtra(EXTRA_CMD_CONTENT_LOCATION);
        Log.d(TAG,"receive broadcast , playing content location :"+mContentLocation);
        //Toast.makeText(context,mContentLocation,Toast.LENGTH_SHORT).show();
        handleIntentAndThenSendMessage(MSG_PLAY_CONTENT,MSG_ARG1_DEFAULT,mContentLocation);
    }

    public void parseIntentStopPlayback(Context context,Intent intent){
        Log.d(TAG,"receive broadcast , stop music player audio track playback .......");
        handleIntentAndThenSendMessage(MSG_STOP_PLAYBACK,MSG_ARG1_DEFAULT,null);
    }

    public void parseIntentRestartPlayback(Context context,Intent intent){
        Log.d(TAG,"receive broadcast , restart music player audio track playback .......");
        handleIntentAndThenSendMessage(MSG_RESTART_PLAYBACK,MSG_ARG1_DEFAULT,null);
    }

    public void parseIntentVolumeControl(Context context,Intent intent){
        int adjust_direction = intent.getIntExtra(
                EXTRA_CMD_VOLUME_ADJUSTMENT_DIRECTION,VOLUME_ADJUSTMENT_DIRECTION_SAME);
        Log.d(TAG,"receive broadcast , adjust stream volume for media player : " +
                adjust_direction);

        handleIntentAndThenSendMessage(MSG_VOLUME_CONTROL,adjust_direction,null);
    }


    public void parseIntentChangeFeature(Context context,Intent intent){
        // create a dummy audio track if no playing content intent was received
        // create a dummy audio track to attach it to dolby audio processing
        configDAPWithDummyAudioTrack();
        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_STATUS)){
            int dsStatus=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_STATUS,2);
            Log.d(TAG,"receive broadcast , change ds status :"+dsStatus);
            Toast.makeText(context,Integer.toString(dsStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_STATUS,dsStatus,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE)){
            int profileID=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE,INVALID_DAP_PROFILE_ID);
            Log.d(TAG,"receive broadcast , change ds profile id :"+profileID);
            Toast.makeText(context,Integer.toString(profileID),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE,profileID,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_RESET_PROFILE)){
            int profileID=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_RESET_PROFILE,INVALID_DAP_PROFILE_ID);
            if (profileID == RESET_DAP_ALL_PROFILE_PARA){
                Log.d(TAG,"receive broadcast , reset all profile para !");
            }else {
                Log.d(TAG,"receive broadcast , reset one profile para : "+profileID);
            }

            Toast.makeText(context,Integer.toString(profileID),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_RESET_PROFILE,profileID,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_RESET_UNIVERSAL)){
            errorLog();
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_DE)){
            int deStatus=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_DE,2);
            Log.d(TAG,"receive broadcast , change dialog enhancement :"+deStatus);
            Toast.makeText(context,Integer.toString(deStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DE,deStatus,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_DEA)){
            int deaNum=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_DEA,20);
            Log.d(TAG,"receive broadcast , change dialogue enhancer amount value  :"+deaNum);
            Toast.makeText(context,Integer.toString(deaNum),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DEA,deaNum,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_IEQ)){
            int ieqID=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_IEQ,10);
            Log.d(TAG,"receive broadcast , change intelligent equalizer :"+ieqID);
            Toast.makeText(context,Integer.toString(ieqID),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_IEQ,ieqID,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_HV)){
            int hsvStatus=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_HV,2);
            Log.d(TAG,"receive broadcast , change headphone sound virtualizer :"+hsvStatus);
            Toast.makeText(context,Integer.toString(hsvStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_HV,hsvStatus,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_VSV)){
            int ssvStatus=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_VSV,2);
            Log.d(TAG,"receive broadcast , change virtual speaker  virtualizer :"+ssvStatus);
            Toast.makeText(context,Integer.toString(ssvStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VSV,ssvStatus,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_UNIVERSAL_VL)){
            errorLog();
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_VL)){
            int vlStatus=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_VL,2);
            Log.d(TAG,"receive broadcast , change volume leveler :"+vlStatus);
            Toast.makeText(context,Integer.toString(vlStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VL,vlStatus,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEQ)){
            errorLog();
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEBG)){
            errorLog();
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_GEBG)){
            int[] geqbgValue=intent.getIntArrayExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_GEBG);
            Log.d(TAG,"receive broadcast , change graphic equalizer band gain !"+geqbgValue.length);
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_GEBG,MSG_ARG1_DEFAULT,geqbgValue);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_UNIVERSAL_BE)){
            errorLog();
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_BE)){
            int beStatus=intent.getIntExtra(EXTRA_CMD_FEATURE_DAP_PROFILE_BE,2);
            Log.d(TAG,"receive broadcast , change bass enable :"+beStatus);
            Toast.makeText(context,Integer.toString(beStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_BE,beStatus,null);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_FEATURE_TYPE)){
            String featureType=intent.getStringExtra(EXTRA_CMD_FEATURE_DAP_FEATURE_TYPE);
            int featureID= DsParams.FromString(featureType).toInt();
            Log.d(TAG,"receive broadcast , change ds feature type :"+featureType+" and id :"+featureID);
            Toast.makeText(context,featureType,Toast.LENGTH_SHORT).show();
            int[] featureValue=intent.getIntArrayExtra(EXTRA_CMD_FEATURE_DAP_FEATURE_VALUE);
            Log.d(TAG,"receive broadcast , change ds feature values size :"+featureValue.length);
            for (int i=0;i<featureValue.length;i++){
                Log.d(TAG,"receive broadcast , change ds feature values :"+featureValue[i]);
                Toast.makeText(context,Integer.toString(featureValue[i]),Toast.LENGTH_SHORT).show();
            }
            handleIntentAndThenSendMessage(MSG_CHANGE_DAP_FEATURE_DAP_FEATURE_TYPE,featureID,featureValue);
        }

        if (intent.hasExtra(EXTRA_CMD_FEATURE_DAP_TUNING_PORT)){
            int mPortId =
                    intent.getIntExtra(
                            EXTRA_CMD_FEATURE_DAP_TUNING_PORT,
                            INVALID_DAP_PROFILE_ID);
            int mDeviceNameId =
                    intent.getIntExtra(
                            EXTRA_CMD_FEATURE_DAP_TUNING_DEVICE,
                            INVALID_DAP_PROFILE_ID);

            try{
                Log.d(TAG,"receive broadcast , tuning port index:" + mPortId );
                Log.d(TAG,"receive broadcast , tuning device name index:" + mDeviceNameId);

                Toast.makeText(
                        context,
                        TUNING_DEVICE_NAME_LIST[mPortId][mDeviceNameId],
                        Toast.LENGTH_SHORT).show();
            }catch (IndexOutOfBoundsException e){
                e.printStackTrace();
            }

            handleIntentAndThenSendMessage(MSG_CHANGE_TUNING_DEVICE_NAME,mPortId,mDeviceNameId);
        }

    }

    public void parseIntentRecordLog(Context context,Intent intent){
        int temp=intent.getIntExtra(EXTRA_CMD_STEP_RECORD_LOG,0);
        Log.d(TAG,"receive broadcast , record log :"+temp);
        handleIntentAndThenSendMessage(MSG_RECORD_LOG,MSG_ARG1_DEFAULT,null);
    }

    public void parseIntentReleaseResource(Context context,Intent intent){
        Log.d(TAG,"receive broadcast , release resource : dap and audio track instance .......");
        handleIntentAndThenSendMessage(MSG_RELEASE_RESOURCE,MSG_ARG1_DEFAULT,null);
    }

    public void errorLog(){
        Log.e(TAG,"for dax3, dismiss the universal mode parameters and change to profile based parameters!");
        Log.e(TAG,"please check your commands from the python script !");
    }

    public interface initialDapInstance{
        public boolean configDAPWithDummyAudioTrack();
    }

    public void configDAPWithDummyAudioTrack(){

    }
}
