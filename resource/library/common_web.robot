*** Settings ***
<<<<<<< refs/remotes/origin/new_web
Library    resource/library/common_web_andriod.py
Library   resource/library/initialize_browser.py

*** Variables ***
${BROWSER}    chrome
${URL}        https://www.youtube.com

*** Keywords ***
Open Web Browser And Go To URL
    ${driver}=    Initialize Driver    device_type=web    browser=${BROWSER}
    go_to_url    ${URL}

Close Web Browser
    close_browser
    
=======
Library    ../../resource/library/common_web_andriod.py

*** Variables ***
${BROWSER}     chrome
${URL}         https://www.youtube.com


*** Keywords ***
Initialize Web Driver
    [Documentation]    Initialize the web browser using common_web_andriod.py
    ${driver}=    Initialize Driver    web    ${BROWSER}
    
Go To URL
    [Arguments]    ${url}
    ${driver}.get(${url})

Open YouTube and Search Box
    [Documentation]    Launch YouTube and wait for the search box
    Initialize Web Driver
    Go To URL    ${URL}
>>>>>>> local
