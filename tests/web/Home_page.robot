*** Settings ***
Library    ../../resource/keywords/common_web_andriod
Library    SeleniumLibrary


*** Test Cases ***
Search Udemy On YouTube
    ${search_box}=    Wait For Element    search_box    10    web    Home_page.json
    Input Text    ${search_box}    udemy
    Press Keys    ${search_box}    ENTER
    Sleep    5s