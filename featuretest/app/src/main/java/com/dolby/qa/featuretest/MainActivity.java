package com.dolby.qa.featuretest;

import android.content.BroadcastReceiver;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.dolby.dax.DolbyAudioEffect;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import static com.dolby.qa.featuretest.Constants.GLOBAL_SESSION_ID_NUM;
import static com.dolby.qa.featuretest.Constants.LOW_PRIORITY_NUM;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_DAP_FEATURE_VALUE_TV;
import static com.dolby.qa.featuretest.Constants.MSG_UPDATE_UI_ARG1_VISIBLE;

public class MainActivity extends AppCompatActivity {
    private final static String TAG="featureTest";
    private final static int SAMPLING_RATE=48000;

    private TextView show_play_content_tv;
    private TextView show_dap_status_tv;
    private TextView show_dap_profile_tv;
    private TextView show_dap_feature_type_tv;
    private TextView show_dap_feature_value_tv;

    static MediaPlayer mMediaPlayer=null;
    static int mSession;
    static String mFileName;
    static int current_position ;

    static DolbyAudioEffect mDAP = null;
    static AudioTrack mTrack=null;

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

    public Handler.Callback mUpdateUIHandlerCallback = new UpdateUIHandlerCallbackInMainUi() ;
    public Handler mUpdateUIHandlerInMainUi = new Handler(Looper.getMainLooper(), mUpdateUIHandlerCallback);

    public Handler.Callback mBroadcastReceiverParseHandlerCallback = new DapControllerHandlerCallback(mUpdateUIHandlerInMainUi);
    public Handler mBroadcastReceiverParseHandlerInMainUi = new Handler(Looper.getMainLooper(), mBroadcastReceiverParseHandlerCallback);



    private BroadcastReceiver mbr = new BroadcastReceiverParseFromHostClient(mBroadcastReceiverParseHandlerInMainUi){
        @Override
        public void configDAPWithDummyAudioTrack() {
            initializeDAPWithDummyAudioTrack();
        }
    };

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

        show_play_content_tv = findViewById(R.id.play_content_tv);
        show_dap_status_tv = findViewById(R.id.dap_status_tv);
        show_dap_profile_tv = findViewById(R.id.dap_profile_tv);
        show_dap_feature_type_tv =findViewById(R.id.dap_feature_type_tv);
        show_dap_feature_value_tv = findViewById(R.id.dap_feature_value_tv);

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
            mTrack= new AudioTrack.Builder()
                            .setAudioAttributes(new AudioAttributes.Builder()
                                    .setUsage(AudioAttributes.USAGE_MEDIA)
                                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                                    .build())
                            .setAudioFormat(new AudioFormat.Builder()
                                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                                    .setSampleRate(SAMPLING_RATE)
                                    .setChannelMask(AudioFormat.CHANNEL_OUT_STEREO)
                                    .build())
                            .setBufferSizeInBytes(AudioTrack.getMinBufferSize(SAMPLING_RATE, AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT))
                            .build();

            if (mTrack == null) {
                throw new AssertionError("create dummy audio track failed!");
            }
//            mDAP=new DolbyAudioEffect(0,mTrack.getAudioSessionId());
            mDAP=new DolbyAudioEffect(LOW_PRIORITY_NUM, GLOBAL_SESSION_ID_NUM);
        }
    }

    public static void playOrPause(String filename) {
        mFileName = filename;
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

    public static void stopPlayback(){
        if (mMediaPlayer != null){
            if (mMediaPlayer.isPlaying()){
                current_position = mMediaPlayer.getCurrentPosition();
                mMediaPlayer.stop();
            }
        }
    }

    public static void restartPlayback(){
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

    public static void releaseResource(){
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

    public class UpdateUIHandlerCallbackInMainUi implements Handler.Callback {
        @Override
        public boolean handleMessage(Message msg) {
            int messageType = msg.what;
            switch (messageType) {
                case Constants.MSG_UPDATE_PLAY_CONTENT_TV:
                    String mShowContent = (String) msg.obj;
                    show_play_content_tv.setText(mShowContent);
                    break;
                case Constants.MSG_UPDATE_DAP_STATUS_TV:
                    String mDapStatus = (String) msg.obj;
                    show_dap_status_tv.setText(mDapStatus);
                    break;
                case Constants.MSG_UPDATE_DAP_PROFILE_TV:
                    String mDapProfile = (String) msg.obj;
                    show_dap_profile_tv.setText(mDapProfile);
                    break;
                case Constants.MSG_UPDATE_DAP_FEATURE_TYPE_TV:
                    String mDapFeatureType = (String) msg.obj;
                    show_dap_feature_type_tv.setText(mDapFeatureType);
                    break;
                case MSG_UPDATE_DAP_FEATURE_VALUE_TV:
                    if (msg.arg1 == MSG_UPDATE_UI_ARG1_VISIBLE){
                        show_dap_feature_value_tv.setVisibility(View.VISIBLE);
                    }
                    String mDapFeatureValue = (String) msg.obj;
                    show_dap_feature_value_tv.setText(mDapFeatureValue);
                    break;
                case Constants.MSG_UPDATE_RESET_TV:
                    resetView();
                    break;
                default:
                    break;
            }
            return false;
        }
    }

}
