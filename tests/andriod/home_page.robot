*** Settings ***
Library    ../../resource/library/common_web_andriod.py
Resource    ../../resource/library/common_andriod.robot


*** Test Cases ***
Search Udemy On YouTube
    [Tags]    smoke
    verify andriod is open or not
    quit driver in andriod
