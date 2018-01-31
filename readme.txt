pre-con:
1. the image of test device must be release image ;
2. below build environment is required on host PC :  
		i) latest Android SDK (API version 26 or newer )and IDE Android Studio (version 2.3.3 or newer ) is installed ;
		ii) python Android pytest (version 3.x.x or newer ) library is also install ;



Step by step : 
1.install feature test apk on the target device located at apkSrc directory in python project  or download feature test source code from p4  , build the apk and then install it 
note : if first time launching the app on device under test  , you must allow  the permission 
request and then run test cases.

2.enable device wifi connection , connect device through usb cable to host pc , run the adbwifi.sh script to enable wifi connection and then disconnect usb cable ;

3.navigate to integrationAutorun project root directory in command line and run test case in python file ;
run all speaker endpoint test case : pytest -k "speaker" 
run all hesdphone endpoint test cases : pytest -k "headphone"
run all  bluetooth endpoint test case : pytest -k "bluetooth"
run all usb headphone endpoint test cases : pytest -k "usb"
run all test cases in current directory : pytest .
