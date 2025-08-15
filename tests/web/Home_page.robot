*** Settings ***
Library    ../../resource/library/common_web_andriod.py
Resource    ../../resource/library/common_web.robot



*** Test Cases ***
Search Udemy On YouTube
    [Tags]    smoke
    Open Web Browser And Go To URL
    
    