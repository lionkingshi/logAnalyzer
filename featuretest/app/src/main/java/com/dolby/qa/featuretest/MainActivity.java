package com.dolby.qa.featuretest;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.dolby.dax.DolbyAudioEffect;
import com.dolby.dax.DsParams;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private final static String TAG="featureTest";
    private final static int SAMPLING_RATE=48000;

    TextView show_play_content_tv;
    TextView show_dap_status_tv;
    TextView show_dap_profile_tv;
    TextView show_dap_feature_type_tv;
    TextView show_dap_feature_value_tv;

    MediaPlayer mMediaPlayer=null;
    int mSession;
    String mFileName;
    int current_position ;

    DolbyAudioEffect mDAP = null;
    private AudioTrack mTrack=null;

    private static final String[] permissionArray=new String[]{
            android.Manifest.permission.MODIFY_AUDIO_SETTINGS,
            android.Manifest.permission.RECORD_AUDIO,
            android.Manifest.permission.READ_EXTERNAL_STORAGE
    };

    private static final List<String> permissionList = new ArrayList<String>();
    private static final int REQUEST_CODE_ASK_PERMISSION =1 ;
    private void checkRequiredPermission( ){
        for (String permission : permissionArray){
            if(this.checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED){
                permissionList.add(permission);
            }
        }
        if(!permissionList.isEmpty()){
            this.requestPermissions(permissionList.toArray(new String[permissionList.size()]),REQUEST_CODE_ASK_PERMISSION);
        }
    }

    private Handler mMainUiHandler;

    {
        mMainUiHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                int messageType = msg.what;
                switch (messageType) {
                    case Constants.MSG_PLAY_CONTENT:
                        show_play_content_tv.setText(String.format(Locale.getDefault(), "play content : %s", msg.obj));
                        mFileName = (String) msg.obj;
                        playOrPause();
                    /* create a dap instance every time app playback content */
                        if (mDAP != null) {
                            mDAP.release();
                            mDAP=null;
                        }
                        mDAP = new DolbyAudioEffect(5, mSession);
                        break;
                    case Constants.MSG_STOP_PLAYBACK:
                        stopPlayback();
                        break;
                    case Constants.MSG_RESTART_PLAYBACK:
                        restartPlayback();
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_STATUS:
                        show_dap_status_tv.setText(String.format(Locale.getDefault(), "set ds status : %b", msg.arg1 != 0));
                        mDAP.setDsOn(msg.arg1 != 0);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE:
                        show_dap_profile_tv.setText(String.format(Locale.getDefault(), "set profile id: %d", msg.arg1));
                        mDAP.setProfile(msg.arg1);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_RESET_PROFILE:
                        if (msg.arg1 == Constants.ID_RESET_ALL_PROFILE) {
                            show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "reset all profile : %d", msg.arg1));
                            for (int index = 0; index < Constants.PROFILE_NUM; index++) {
                                if (mDAP.isProfileSpecificSettingsModified(index)) {
                                    mDAP.resetProfileSpecificSettings(index);
                                }
                            }
                        } else {
                            show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "reset profile id: %d", msg.arg1));
                            mDAP.resetProfileSpecificSettings(msg.arg1);
                        }
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_RESET_UNIVERSAL:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "reset universal parameter %d", msg.arg1));
                        mDAP.resetUniversalSettings();
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_DE:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change de : %b", msg.arg1 != 0));
                        mDAP.setDialogEnhancementEnabled(msg.arg1 != 0);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_IEQ:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change ieq : %d", msg.arg1));
                        mDAP.setIeqPreset(msg.arg1);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_HV:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change headphone virtualizer : %b", msg.arg1 != 0));
                        mDAP.setDolbyHeadphoneVirtualizerEnabled(msg.arg1 != 0);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_PROFILE_VSV:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change speaker virtualizer : %b", msg.arg1 != 0));
                        mDAP.setDolbyVirtualSpeakerVirtualizerEnabled(msg.arg1 != 0);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_VL:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change vl : %b", msg.arg1 != 0));
                        int[] vlValue = {msg.arg1};
                        mDAP.setUniversalParameter(DsParams.DolbyVolumeLevelerEnable.toInt(), vlValue);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_BE:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change be : %b", msg.arg1 != 0));
                        int[] beValue = {msg.arg1};
                        mDAP.setUniversalParameter(DsParams.BassEnable.toInt(), beValue);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_GEQ:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change geq status : %b", msg.arg1 != 0));
                        int[] geqValue = {msg.arg1};
                        mDAP.setUniversalParameter(DsParams.GraphicEqualizerEnable.toInt(), geqValue);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_UNIVERSAL_GEBG:
                        show_dap_feature_type_tv.setText(String.format(Locale.getDefault(), "change geq band gain : %s", msg.arg1));
                        int[] geqbgValue = (int[]) msg.obj;
                        show_dap_feature_value_tv.setVisibility(View.VISIBLE);
                        show_dap_feature_value_tv.setText(String.format(Locale.getDefault(), "geq band gain : %s",Arrays.toString(geqbgValue)));
                        mDAP.setUniversalParameter(DsParams.GraphicEqualizerBandGains.toInt(), geqbgValue);
                        break;
                    case Constants.MSG_CHANGE_DAP_FEATURE_DAP_FEATURE_TYPE:
                        show_dap_feature_type_tv.setText("feature type :" + DsParams.FromInt(msg.arg1).toString());
                        int[] featureValue = (int[]) msg.obj;
                        for (int i = 0; i < featureValue.length; i++) {
                            show_dap_feature_value_tv.setVisibility(View.VISIBLE);
                            show_dap_feature_value_tv.setText(String.format(Locale.getDefault(), "feature value : %s",Arrays.toString(featureValue)));
                            //show_dap_feature_type_tv.setText("feature value :"+featureValue[i]);
                        }
                        mDAP.setParameter(msg.arg1, featureValue);
                        break;
                    case Constants.MSG_RECORD_LOG:
                        //show_dap_feature_type_tv.setText(String.format(Locale.getDefault(),"record log : %d",msg.arg1));
                        break;
                    case Constants.MSG_RELEASE_RESOURCE:
                        releaseResource();
                        resetView();
                        break;
                    default:
                        break;
                }
            }
        };
    }

    private BroadcastReceiver mbr=new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action=intent.getAction();
            if (action.equals(Constants.EXTRA_CMD_ACTION)){
                String type=intent.getStringExtra(Constants.EXTRA_CMD_STEP);
                if (type.equals(Constants.EXTRA_CMD_STEP_PLAY_CONTENT)){
                    parseIntentPlayContent(context,intent);
                }else if (type.equals(Constants.EXTRA_CMD_STEP_CHANGE_DAP_FEATURE)){
                    parseIntentChangeFeature(context, intent);
                }else if (type.equals(Constants.EXTRA_CMD_STEP_RECORD_LOG)){
                    parseIntentRecordLog(context, intent);
                }else if(type.equals(Constants.EXTRA_CMD_STEP_RELEASE_RESOURCE)){
                    parseIntentReleaseResource(context,intent);
                }else if(type.equals(Constants.EXTRA_CMD_STEP_STOP_PLAYBACK)){
                    parseIntentStopPlayback(context,intent);
                }else if(type.equals(Constants.EXTRA_CMD_STEP_RESTART_PLAYBACK)){
                    parseIntentRestartPlayback(context,intent);
                }else {
                    Log.d(TAG,"receive broadcast , not expected action !");
                }
            }
        }
    };

    /**
     * @param msgType
     * @param msgArg1
     * @param msgObj
     */
    public void handleIntentAndThenSendMessage(int msgType, int msgArg1, Object msgObj){
        Message msg=mMainUiHandler.obtainMessage();
        msg.what=msgType;
        msg.arg1= msgArg1;
        msg.obj=msgObj;
        mMainUiHandler.sendMessage(msg);
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
        initializeDAPWithDummyAudioTrack();
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
            int featureID=DsParams.FromString(featureType).toInt();
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

    public void registerReceiver(){
        IntentFilter commandFilter=new IntentFilter();
        //commandFilter.addCategory(Constants.EXTRA_CMD_CATEGORY);
        commandFilter.addAction(Constants.EXTRA_CMD_ACTION);
        this.registerReceiver(mbr,commandFilter);
    }

    public void unregisterReceiver(){
        this.unregisterReceiver(mbr);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d(TAG,"onCreate");


        TextView app_description = (TextView)findViewById(R.id.app_description_tv);
        show_play_content_tv = (TextView)findViewById(R.id.play_content_tv);
        show_dap_status_tv = (TextView)findViewById(R.id.dap_status_tv);
        show_dap_profile_tv = (TextView)findViewById(R.id.dap_profile_tv);
        show_dap_feature_type_tv =(TextView)findViewById(R.id.dap_feature_type_tv);
        show_dap_feature_value_tv = (TextView)findViewById(R.id.dap_feature_value_tv);

        // initialize the dap
        initializeDAPWithDummyAudioTrack();

        checkRequiredPermission();
        this.registerReceiver();
    }

    @Override
    protected void onResume() {
        super.onResume();
        Log.d(TAG,"onResume");
        restartPlayback();
    }

    @Override
    protected void onPause() {
        super.onPause();
        Log.d(TAG,"onPause");
        stopPlayback();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        Log.d(TAG,"onDestroy");
        this.unregisterReceiver();
        releaseResource();
    }

    public void initializeDAPWithDummyAudioTrack(){
        // create a dummy audio track to attach it to dolby audio processing
        if (mDAP == null){
            mTrack=
                    new AudioTrack(
                            AudioManager.STREAM_MUSIC,
                            SAMPLING_RATE,
                            AudioFormat.CHANNEL_OUT_MONO,
                            AudioFormat.ENCODING_PCM_16BIT,
                            AudioTrack.getMinBufferSize(
                                    SAMPLING_RATE,AudioFormat.CHANNEL_OUT_MONO,
                                    AudioFormat.ENCODING_PCM_16BIT),
                            AudioTrack.MODE_STREAM);
            if (mTrack == null) {
                throw new AssertionError("create dummy audio track failed!");
            }
            mDAP=new DolbyAudioEffect(0,mTrack.getAudioSessionId());
        }
    }

    public void playOrPause() {
        if (mMediaPlayer != null){
            mMediaPlayer.stop();
            mMediaPlayer.reset();
            mMediaPlayer.release();
            mMediaPlayer = null ;
        }
        if (mMediaPlayer == null || !mMediaPlayer.isPlaying()){
            if (mMediaPlayer == null) {
                try {
                    mMediaPlayer = new MediaPlayer();
                    mSession=mMediaPlayer.getAudioSessionId();
                    Log.d(TAG, "mMediaPlayer.getAudioSessionId(): "+mSession);
                    /*set playback content*/
                    Log.d(TAG, "Playing file: "+mFileName);
//                    File tempFile = new File(mFileName);
//                    FileInputStream fis = new FileInputStream(tempFile);
//                    mMediaPlayer.reset();
//                    mMediaPlayer.setDataSource(fis.getFD());
                    mMediaPlayer.setDataSource(mFileName);
                    mMediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
                    mMediaPlayer.prepare();
                    mMediaPlayer.setLooping(true);
                } catch (IOException ex1) {
                    Log.e(TAG, "mMediaPlayercreate failed:", ex1);
                    mMediaPlayer = null;
                } catch (IllegalArgumentException ex2) {
                    Log.e(TAG, "mMediaPlayercreate failed:", ex2);
                    mMediaPlayer = null;
                } catch (SecurityException ex3) {
                    Log.e(TAG, "mMediaPlayercreate failed:", ex3);
                    mMediaPlayer = null;
                }

                if (mMediaPlayer != null) {
                    //mMediaPlayer.setAuxEffectSendLevel(mSendLevel);
                    //mMediaPlayer.attachAuxEffect(mEffectId);
                    mMediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                        public void onCompletion(MediaPlayer mp) {
                            //updatePlayPauseButton();
                        }
                    });
                }
            }
            if (mMediaPlayer != null) {
                mMediaPlayer.start();
            }
        } else {
            //mMediaPlayer.pause();
        }
    }

    public void stopPlayback(){
        if (mMediaPlayer != null){
            if (mMediaPlayer.isPlaying()){
                current_position = mMediaPlayer.getCurrentPosition();
                mMediaPlayer.stop();
            }
        }
    }

    public void restartPlayback(){
        if (mMediaPlayer != null){
            if (!mMediaPlayer.isPlaying()){
                mMediaPlayer.reset();
                Log.d(TAG, "Playing from file");
                try {
                    mMediaPlayer.setDataSource(mFileName);
                    mMediaPlayer.prepare();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                mMediaPlayer.seekTo(current_position);
                mMediaPlayer.setLooping(true);
                mMediaPlayer.start();
            }
        }
    }

    public void releaseResource(){
        if (mMediaPlayer != null){
            mMediaPlayer.pause();
            mMediaPlayer.stop();
            mMediaPlayer.release();
            mMediaPlayer=null;
        }
        if (mDAP != null){
            mDAP.release();
            mDAP=null;
        }
        if (mTrack != null){
            mTrack.release();
            mTrack=null;
        }
    }

    public void resetView(){
        show_play_content_tv.setText(R.string.play_content_name);
        show_dap_status_tv.setText(R.string.dap_status);
        show_dap_profile_tv.setText(R.string.dap_profile);
        show_dap_feature_type_tv.setText(R.string.dap_feature_type);
        show_dap_feature_value_tv.setText(R.string.dap_feature_value);
        show_dap_feature_value_tv.setVisibility(View.INVISIBLE);
    }

}
