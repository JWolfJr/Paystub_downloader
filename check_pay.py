from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
import os
import pandas as pd
import getpass
from time import sleep
import smtplib 

def get_pay_stub():
    username = input("Enter your username. ")
    password = getpass.getpass("Now enter your password. ")
    workpass = os.environ.get("WORK_PASSWORD")
    if password == workpass:
        print("Correct, you may enter!")
    else:
        print("Wrong, try again!")
    
    # create variable to hold date of wanted pay period
    pay_date = input("Enter pay period date to be emailed, with ##/##/#### format ")
    
    driver = webdriver.Chrome('/opt/google/chrome/chromedriver')
    
    print("Opening browser and navigating to Metras site")

    driver.get("https://ess.metrarr.com")

    username_field = (By.XPATH, "//input[@id='input_1']")
    password_field = (By.XPATH, "//input[@id='input_2']")

    submit_btn = (By.XPATH, "//input[@class='credentials_input_submit']")

    payments_link = (By.XPATH, "//a[@id='ctl00_ctl00_m_g_2bf8b5b7_c417_4fe8_ba8a_c8a00204ada8_ctl01_gvActivityPicker_ctl02_essShortcutLinkPicker_repeaterShortCutLinks_ctl00_hlkPlaces']")

    # now = datetime.now()
    # today = now.strftime("%m/%d/%Y")
    #print(today)
    select_newest_check = (By.XPATH, "//a[contains(text(),'%s')]"%pay_date)

    drop_down_tab = (By.XPATH, "//img[@id='ctl00_ctl00_m_g_9290a9e0_5625_48fe_a0eb_4ad1d316f93f_ctl01_MyReport_ctl02_ctl05_ctl04_ctl00_ButtonImg']")
    #csv_tab = (By.XPATH, "//a[contains(text(),'CSV (comma delimited)')]")
    excel_tab = (By.XPATH, "//a[contains(text(),'Excel')]")

    print("Entering username and password")
    
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(username_field)).send_keys(username)
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(password_field)).send_keys(password)

    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(submit_btn)).click()

    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(payments_link)).click()

    print("Finding most recent paystub")
    
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(select_newest_check)).click()

    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(drop_down_tab)).click()
    #WebDriverWait(driver, 20).until(ec.element_to_be_clickable(csv_tab)).click()

    print("Downloading paystub")
    
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable(excel_tab)).click()



def get_and_parse():
    file_path = os.environ.get("MACHINE_NAME")
    #Retrieve latest downloaded file
    files = os.listdir("/home/{}}/Downloads/".format(file_path))
    #Create variable to hold latest file
    newest_file = files[-1]

    print("Sending downloaded file to the parser")

    #pay = "PayrollPayStatementReport.Report_Metra.xlsx"
    col_names = ["Col 1", "Col 2"]
    df = pd.read_excel(newest_file, names=col_names, usecols=[1,3])

    print("Parsing data")

    hours = df.loc[[7,8,9], "Col 1"]
    money = df.loc[18, "Col 2"]
    total_hours= sum(hours)
    
    email_totals = "You made ${} this pay period, and worked {} hours.".format(money, total_hours)
    
    print(email_totals)

def mail_me():

    EMAIL_ADDRESS = os.environ.get("EMAIL_USERNAME")
    EMAIL_PASS = os.environ.get("EMAIL_PASSWORD")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)

        subject = "Recent paystub"
        body = email_totals
        msg = "Subject: {} \n\n {}".format(subject, body)
        
        print("Sending e-mail now")
        
        smtp.sendmail(EMAIL_ADDRESS, "mystinker08@gmail.com", msg)
    

get_pay_stub()
sleep(3)
get_and_parse()
sleep(3)
mail_me()