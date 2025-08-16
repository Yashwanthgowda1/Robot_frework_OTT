*** Settings ***

Library    resource/library/common_web_andriod.py


*** Keywords ***
verify andriod is open or not
    ${driver}=    Initialize Driver    emulator

quit driver in andriod
    quit_driver
   
