*** Settings ***

Library    resource/library/common_web_andriod.py


*** Variables ***
${BROWSER}    chrome
${URL}        https://www.youtube.com

*** Keywords ***
Open Web Browser And Go To URL
    ${driver}=    Initialize Driver    device_type=web    browser=${BROWSER}
    go_to_url    ${URL}

Close Web Browser
    close_browser
   