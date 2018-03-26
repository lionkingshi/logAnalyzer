package com.dolby.qa.featuretest;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.widget.Toast;

import com.dolby.dax.DsParams;

public class BroadcastReceiverParseFromHostClient extends BroadcastReceiver {
    private static final String TAG = ConstantdDax2.TAG;
    private Handler mBroadcastReceiverParseHandlerInMainUi;

    public BroadcastReceiverParseFromHostClient(Handler mBroadcastReceiverParseHandlerInMainUi) {
        this.mBroadcastReceiverParseHandlerInMainUi = mBroadcastReceiverParseHandlerInMainUi;
    }

    @Override
    public void onReceive(Context context, Intent intent) {
        String action=intent.getAction();
        if (action.equals(Constants.EXTRA_CMD_ACTION)){
            String type=intent.getStringExtra(Constants.EXTRA_CMD_STEP);
            switch (type) {
                case Constants.EXTRA_CMD_STEP_PLAY_CONTENT:
                    parseIntentPlayContent(context, intent);
                    break;
                case Constants.EXTRA_CMD_STEP_CHANGE_DAP_FEATURE:
                    parseIntentChangeFeature(context, intent);
                    break;
                case Constants.EXTRA_CMD_STEP_RECORD_LOG:
                    parseIntentRecordLog(context, intent);
                    break;
                case Constants.EXTRA_CMD_STEP_RELEASE_RESOURCE:
                    parseIntentReleaseResource(context, intent);
                    break;
                case Constants.EXTRA_CMD_STEP_STOP_PLAYBACK:
                    parseIntentStopPlayback(context, intent);
                    break;
                case Constants.EXTRA_CMD_STEP_RESTART_PLAYBACK:
                    parseIntentRestartPlayback(context, intent);
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

    public void parseIntentPlayContent(Context context,Intent intent){
        String mContentLocation=intent.getStringExtra(Constants.EXTRA_CMD_CONTENT_LOCATION);
        Log.d(TAG,"receive broadcast , playing content location :"+mContentLocation);
        //Toast.makeText(context,mContentLocation,Toast.LENGTH_SHORT).show();
        handleIntentAndThenSendMessage(Constants.MSG_PLAY_CONTENT,Constants.MSG_ARG1_DEFAULT,mContentLocation);
    }

    public void parseIntentStopPlayback(Context context,Intent intent){
        Log.d(TAG,"receive broadcast , stop music player audio track playback .......");
        handleIntentAndThenSendMessage(Constants.MSG_STOP_PLAYBACK,Constants.MSG_ARG1_DEFAULT,null);
    }

    public void parseIntentRestartPlayback(Context context,Intent intent){
        Log.d(TAG,"receive broadcast , restart music player audio track playback .......");
        handleIntentAndThenSendMessage(Constants.MSG_RESTART_PLAYBACK,Constants.MSG_ARG1_DEFAULT,null);
    }

    public void parseIntentChangeFeature(Context context,Intent intent){
        // create a dummy audio track if no playing content intent was received
        // create a dummy audio track to attach it to dolby audio processing
        configDAPWithDummyAudioTrack();
        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_STATUS)){
            int dsStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_STATUS,2);
            Log.d(TAG,"receive broadcast , change ds status :"+dsStatus);
            Toast.makeText(context,Integer.toString(dsStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_STATUS,dsStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE)){
            int profileID=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE,Constants.INVALID_DAP_PROFILE_ID);
            Log.d(TAG,"receive broadcast , change ds profile id :"+profileID);
            Toast.makeText(context,Integer.toString(profileID),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE,profileID,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_RESET_PROFILE)){
            int profileID=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_RESET_PROFILE,Constants.INVALID_DAP_PROFILE_ID);
            if (profileID == Constants.RESET_DAP_ALL_PROFILE_PARA){
                Log.d(TAG,"receive broadcast , reset all profile para !");
            }else {
                Log.d(TAG,"receive broadcast , reset one profile para : "+profileID);
            }

            Toast.makeText(context,Integer.toString(profileID),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_RESET_PROFILE,profileID,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_RESET_UNIVERSAL)){
            Log.d(TAG,"receive broadcast , reset universal parameters !");
            Toast.makeText(context,"reset universal para",Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_RESET_UNIVERSAL,Constants.MSG_ARG1_DEFAULT,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_DE)){
            int deStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_DE,2);
            Log.d(TAG,"receive broadcast , change dialog enhancement :"+deStatus);
            Toast.makeText(context,Integer.toString(deStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DE,deStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_IEQ)){
            int ieqID=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_IEQ,10);
            Log.d(TAG,"receive broadcast , change intelligent equalizer :"+ieqID);
            Toast.makeText(context,Integer.toString(ieqID),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_IEQ,ieqID,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_HV)){
            int hsvStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_HV,2);
            Log.d(TAG,"receive broadcast , change headphone sound virtualizer :"+hsvStatus);
            Toast.makeText(context,Integer.toString(hsvStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_HV,hsvStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_VSV)){
            int ssvStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_PROFILE_VSV,2);
            Log.d(TAG,"receive broadcast , change virtual speaker  virtualizer :"+ssvStatus);
            Toast.makeText(context,Integer.toString(ssvStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VSV,ssvStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_VL)){
            int vlStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_VL,2);
            Log.d(TAG,"receive broadcast , change volume leveler :"+vlStatus);
            Toast.makeText(context,Integer.toString(vlStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_VL,vlStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEQ)){
            int geqStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEQ,2);
            Log.d(TAG,"receive broadcast , change graphic equalizer enable status :"+geqStatus);
            Toast.makeText(context,Integer.toString(geqStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_GEQ,geqStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEBG)){
            int[] geqbgValue=intent.getIntArrayExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_GEBG);
            Log.d(TAG,"receive broadcast , change graphic equalizer band gain !"+geqbgValue.length);
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_GEBG,Constants.MSG_ARG1_DEFAULT,geqbgValue);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_BE)){
            int beStatus=intent.getIntExtra(Constants.EXTRA_CMD_FEATURE_DAP_UNIVERSAL_BE,2);
            Log.d(TAG,"receive broadcast , change bass enable :"+beStatus);
            Toast.makeText(context,Integer.toString(beStatus),Toast.LENGTH_SHORT).show();
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_BE,beStatus,null);
        }

        if (intent.hasExtra(Constants.EXTRA_CMD_FEATURE_DAP_FEATURE_TYPE)){
            String featureType=intent.getStringExtra(Constants.EXTRA_CMD_FEATURE_DAP_FEATURE_TYPE);
            int featureID= DsParams.FromString(featureType).toInt();
            Log.d(TAG,"receive broadcast , change ds feature type :"+featureType+" and id :"+featureID);
            Toast.makeText(context,featureType,Toast.LENGTH_SHORT).show();
            int[] featureValue=intent.getIntArrayExtra(Constants.EXTRA_CMD_FEATURE_DAP_FEATURE_VALUE);
            Log.d(TAG,"receive broadcast , change ds feature values size :"+featureValue.length);
            for (int i=0;i<featureValue.length;i++){
                Log.d(TAG,"receive broadcast , change ds feature values :"+featureValue[i]);
                Toast.makeText(context,Integer.toString(featureValue[i]),Toast.LENGTH_SHORT).show();
            }
            handleIntentAndThenSendMessage(Constants.MSG_CHANGE_DAP_FEATURE_DAP_FEATURE_TYPE,featureID,featureValue);
        }
    }

    public void parseIntentRecordLog(Context context,Intent intent){
        int temp=intent.getIntExtra(Constants.EXTRA_CMD_STEP_RECORD_LOG,0);
        Log.d(TAG,"receive broadcast , record log :"+temp);
        handleIntentAndThenSendMessage(Constants.MSG_RECORD_LOG,Constants.MSG_ARG1_DEFAULT,null);
    }

    public void parseIntentReleaseResource(Context context,Intent intent){
        Log.d(TAG,"receive broadcast , release resource : dap and audio track instance .......");
        handleIntentAndThenSendMessage(Constants.MSG_RELEASE_RESOURCE,Constants.MSG_ARG1_DEFAULT,null);
    }

    public interface initialDapInstance{
        public boolean configDAPWithDummyAudioTrack();
    }

    public void configDAPWithDummyAudioTrack(){

    }
}
