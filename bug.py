#!/usr/bin/python
# #-*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver                                  #在運行之前 這邊import所有東西都要先要在cmd裡面pip install 過喔!
import re
import time

if __name__ == '__main__':
    
    driver = webdriver.Chrome()                                 #開啟爬蟲版chrome

    driver.implicitly_wait(3)
    driver.get("https://wisdom.sfi.org.tw/account/index")       #發送請求到此網頁

    input_acc = driver.find_element_by_name('account')          #selenium基本指令 找到帳號欄然後輸入帳號
    input_acc.send_keys('C0054814')

    input_pass = driver.find_element_by_name('password')        #selenium基本指令 找到密碼欄然後輸入密碼
    time.sleep(1.5)
    input_pass.send_keys('c4bf75ca')
    
    log_in = driver.find_element_by_name('send')                #登入鍵
    log_in.click()                                              #按一下
                                                                #成功登入後會有視窗跳出來 關掉
    driver.switch_to_alert().accept()

    for i in range(1):                                          #迴圈次數range(x)隨便改 爽多少就多少

        try:
            time.sleep(3)
            driver.get("https://wisdom.sfi.org.tw/exam/videoList")  #發送請求到此網頁

            time.sleep(3)                               
            driver.get("https://wisdom.sfi.org.tw/exam/testStart")

            time.sleep(3)
            sub = driver.find_element_by_name('_action_testResult') #送出鍵 才有答案
            sub.click()                                             #按一下
    
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'html.parser') #到了答案的頁面之後

        
            f = open('result.txt','a+',encoding = 'utf8')                             #開檔準備寫檔 用a+開才可以一直往後寫 原來的檔案不會被刪除和覆寫
    
            for s in soup.find('div', 'main').find_all('tr'):       #找到soup裡面中的main的div裡面所有<tr>
            

                #print(s)                                           #雖然有文字了 但型態都是tag 不能做文字處裡
                #print(type(s))

                s = s.text.strip()                                  #轉成文字(Str)型態
                #print(type(s))

                re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)
                re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)
                re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)
                re_br=re.compile('<br\s*?/?>')
                re_h=re.compile('</?\w+[^>]*>')                     #re正規式刪掉html種種標籤
                re_comment=re.compile('<!--[^>]*-->')
                s=re_cdata.sub('',s)
                s=re_script.sub('',s)
                s=re_style.sub('',s)
                s=re_br.sub('\n',s)
                s=re_h.sub('',s)
                s=re_comment.sub('',s)
        
                f.write( s + '\n')
                #print(s)
        except :
                driver.get("https://wisdom.sfi.org.tw/")
                driver.get("https://wisdom.sfi.org.tw/account/index")       #發送請求到此網頁

                input_acc = driver.find_element_by_name('account')          #selenium基本指令 找到帳號欄然後輸入帳號
                input_acc.send_keys('C0054814')

                input_pass = driver.find_element_by_name('password')        #selenium基本指令 找到密碼欄然後輸入密碼
                input_pass.send_keys('c4bf75ca')

                log_in = driver.find_element_by_name('send')                #登入鍵
                log_in.click()                                              #按一下
                                                                #成功登入後會有視窗跳出來 關掉
                driver.switch_to_alert().accept()
    

    driver.close()