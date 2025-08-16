*** Settings ***
Resource  ../../resource/keywords/sigin.robot


*** Test Cases ***
signin to orangeHRM
    [Tags]  56754   smoke
    Sign In
    [Teardown]  Close Web Browser
    


    
    