*** Settings ***
Library    resource/keywords/sign_in.py
Resource   ../../resource/library/common_web.robot


*** Keywords ***
Sign In
    Open Web Browser And Go To URL
    perform_login
    
