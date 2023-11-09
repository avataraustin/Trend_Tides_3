import os, time
import yfinance as yf
import numpy as np
import pandas as pd
import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from send_emails import send_email
import pandas_ta as ta
from replit import db
import pandas_datareader as pdr
from reg_alerts import lrg_deg, lrg_alerts

# Idea for this app is to monitor financial market trends
# and give alerts as to status and turning points.


# set env variables for where/from to send emails in send_emails module
# send to email set here in env vars, additional sends can be passed into
# new function calls as a parameter.
receiver_email = os.environ['user_phones_email']

# Days you want to get a text report, regardless of new trend
# format of "Mon","Tue","Wed","Thu","Fri","Sat","Sun"
alert_days = ["Wed","Fri","Sat","Thu"]


# app runs in a loop at set UTC hour
while True:
  print ("Restarting...")
  print("current utc hour:", datetime.datetime.utcnow().strftime("%H"))
  #below code causes to execute between 7am-8am (13-14 utc) cent time
  if int(datetime.datetime.utcnow().strftime("%H")) >= 13 and int(datetime.datetime.utcnow().strftime("%H")) <= 18:
    

    # stores list of str messages to concatenate into final message
    msg_list = []
    
    
    # True if trend change detected, used for sending new alert
    send_new_alert = False

    ## Assets to track:
    '''
    1. Soybeans: 'ZS=F'
    2. Corn: 'ZC=F'
    3. Gold: 'GC=F'
    4. Silver: 'SI=F'
    5. S&P 500: 'SPY'
    6. Bitcoin: 'BTC-USD'
    7. Ethereum: 'ETH-USD'
    8. U.S. Dollar Index: 'DX-Y.NYB'
    9. Vix volatility: '^VIX'
    10. Fed Funds interest rate
    '''
    

    # Fetch U.S. Fed Funds Rate data & add to message
    fed_funds_data = pdr.get_data_fred('FEDFUNDS')
    val_fed = fed_funds_data.tail(1)['FEDFUNDS'].values[0]
    fedfundtxt = f"Latest Fed Funds Rate: {val_fed}"
    print(f"Latest Fed Funds Rate: {val_fed}")
    msg_list.append(fedfundtxt)

    ### Trend alerts ###
    
    # linreg slope calculation of USDX
    lrg_usdx = lrg_deg('DX-Y.NYB',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    usdx_msg = lrg_alerts(lrg_usdx,'USDX_trend','USDX Dollar Index')

    if usdx_msg.startswith("***"):
      msg_list.append(usdx_msg)
      send_new_alert = True
    else:
      msg_list.append(usdx_msg)

    # S&P 500 ('SPY') linreg trend calculation
    lrg_spy = lrg_deg('SPY',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    spy_msg = lrg_alerts(lrg_spy,'SPY_trend','S&P 500 (SPY)')

    if spy_msg.startswith("***"):
      msg_list.append(spy_msg)
      send_new_alert = True
    else:
      msg_list.append(spy_msg)

    # Bitcoin linreg slope calculation of 'BTC-USD'
    lrg_btc = lrg_deg('BTC-USD',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    btc_msg = lrg_alerts(lrg_btc,'BTC_trend','Bitcoin USD')

    if btc_msg.startswith("***"):
      msg_list.append(btc_msg)
      send_new_alert = True
    else:
      msg_list.append(btc_msg)

    # linreg slope calculation of Ethereum
    lrg_eth = lrg_deg('ETH-USD',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    eth_msg = lrg_alerts(lrg_eth,'ETH_trend','Ethereum USD')

    if eth_msg.startswith("***"):
      msg_list.append(eth_msg)
      send_new_alert = True
    else:
      msg_list.append(eth_msg)

    # linreg slope calculation of Gold
    lrg_gold = lrg_deg('GC=F',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    gold_msg = lrg_alerts(lrg_gold,'GOLD_trend','Gold')

    if gold_msg.startswith("***"):
      msg_list.append(gold_msg)
      send_new_alert = True
    else:
      msg_list.append(gold_msg)

    # linreg slope calculation of Silver
    lrg_slv = lrg_deg('SI=F',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    slv_msg = lrg_alerts(lrg_slv,'SILVER_trend','Silver')

    if slv_msg.startswith("***"):
      msg_list.append(slv_msg)
      send_new_alert = True
    else:
      msg_list.append(slv_msg)

    # linreg slope calculation of Corn
    lrg_corn = lrg_deg('ZC=F',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    corn_msg = lrg_alerts(lrg_corn,'CORN_trend','Corn')

    if corn_msg.startswith("***"):
      msg_list.append(corn_msg)
      send_new_alert = True
    else:
      msg_list.append(corn_msg)

    # linreg slope calculation of Soy Beans
    lrg_soy = lrg_deg('ZS=F',length=50) # pull the linreg data
    # calculate trend alert and return the alert message
    soy_msg = lrg_alerts(lrg_soy,'SOY_trend','Soy Beans')

    if soy_msg.startswith("***"):
      msg_list.append(soy_msg)
      send_new_alert = True
    else:
      msg_list.append(soy_msg)



    
    
    ## VIX Indicator ##
    # 12 or lower = Low volatility, 20 or higher = High volatility,
    # 30 or higher = markets unsettled & high volatility
    VIXdata = yf.Ticker('^VIX')
    VIX_df = VIXdata.history(period='6mo')['Close']
    
    currentvix = VIX_df.iloc[-1]
    prev_vix = VIX_df.iloc[-3] #used -3 rather than -2 away from current to avoid update errors
    currentvix_rounded = round(currentvix, 2)
    prev_vix_rounded = round(prev_vix, 2)
    print(f"The current VIX is {currentvix_rounded} ")
    print(f"The previous VIX was {prev_vix_rounded} ")
    str_prev_vix_rounded = f"The previous VIX was {prev_vix_rounded} "
    str_currentvix_rounded = f"The current VIX is {currentvix_rounded} "
  

    # logic for what to add to the text message sent. A string
    # that tells vix high,low,etc. and also numeric value.
    if VIX_df.iloc[-1] < 12:
      print("Vix Volatility LOW. ")
      VIX_low_txt = "Vix Volatility LOW. "
      VIX_low_val_msg = VIX_low_txt + str_prev_vix_rounded + str_currentvix_rounded
      msg_list.append(VIX_low_val_msg)
    elif (VIX_df.iloc[-1] > 20) and (VIX_df.iloc[-1] < 30):
      print("Vix Volatility HIGH. ")
      VIX_high_txt = "Vix Volatility HIGH. "
      VIX_high_val_msg = VIX_high_txt + str_prev_vix_rounded + str_currentvix_rounded
      msg_list.append(VIX_high_val_msg)
    elif VIX_df.iloc[-1] > 30:
      VIX_vhigh_txt = "Vix Volatility EXCEPTIONALLY HIGH. "
      VIX_vhigh_val_msg = VIX_vhigh_txt + str_prev_vix_rounded + str_currentvix_rounded
      print("Vix Volatility EXCEPTIONALLY HIGH. ")
      msg_list.append(VIX_vhigh_val_msg)
    elif (VIX_df.iloc[-1] > 12) and (VIX_df.iloc[-1] < 20):
      VIX_norm_txt = "Vix Volatility Normal Range. "
      VIX_norm_val_msg = VIX_norm_txt + str_prev_vix_rounded + str_currentvix_rounded
      print("Vix Volatility Normal Range. ")
      msg_list.append(VIX_norm_val_msg)
    
    # alert for new low on VIX
    if (VIX_df.iloc[-1] < 12) and (VIX_df.iloc[-3] > 12):
      print("VIX Volatility just became LOW.")
      new_vix_low = "**VIX Volatility just became LOW.**"
      
      # crosschecking dates to avoid duplicate notifications, keep in mind that
      # the VIX_df[-1] closing price fluctuates in price which can cause
      # alerts on subsequent days since the vix changes so much.
      last_VIX_trade_date = VIX_df.index[-1].strftime("%b-%d")
      todays_date = datetime.datetime.now().strftime("%b-%d")
      if last_VIX_trade_date == todays_date:
        msg_list.insert(0, new_vix_low)
        send_new_alert = True
      
    
    if (((VIX_df.iloc[-1] > 20) and (VIX_df.iloc[-1] < 30)) and (VIX_df.iloc[-3] < 20)):
      print("Vix Volatility just became HIGH.")
      new_vix_high = "**Vix Volatility just became HIGH.**"
      
      #crosschecking dates to avoid duplicate notifications,
      last_VIX_trade_date = VIX_df.index[-1].strftime("%b-%d")
      todays_date = datetime.datetime.now().strftime("%b-%d")
      if last_VIX_trade_date == todays_date:
        msg_list.insert(0, new_vix_high)
        send_new_alert = True

    if (VIX_df.iloc[-1] > 30) and (VIX_df.iloc[-3] < 30):
      print("Vix Volatility just became EXCEPTIONALLY HIGH.")
      new_vix_higher = "**Vix Volatility just became EXCEPTIONALLY HIGH.**"
      
      #crosschecking dates to avoid duplicate notifications,
      last_VIX_trade_date = VIX_df.index[-1].strftime("%b-%d")
      todays_date = datetime.datetime.now().strftime("%b-%d")
      if last_VIX_trade_date == todays_date:
        msg_list.insert(0, new_vix_higher)
        send_new_alert = True    
    
    # output what the VIX actually is right now  
    print(f"The current vix volatility is: {currentvix}")

    
    #################

    
    
    
    
    #the composite string of all the messages to then send:
    msg_str = '\n\n'.join(msg_list)
    print(msg_str)
    
    # code for checking when to send alerts, regular alert days are set at 
    # beginning of app. also cases where the send_new_alert variable gets set 
    # to True, such as when a new trend direction is detected.
    
    xday = datetime.datetime.now()
    print(xday.strftime("%a"))

    #todays date in m/d/y format to use to check the db to avoid duplicate sends
    xdaymdy = xday.strftime("%x")
    
    # day to send a regular update alert, checks list of alert_days to send on
    if xday.strftime("%a") in alert_days:
      send_new_alert = True
      
    
    # We use send_email module to send email to cellphone's carrier
    # text message address set in env variable for send_emails.py file
    # For example, 5551234567@txt.att.net for AT&T customers.

    # checking database 'status' key for today's date incase it ran already
    try:
      fetched = db['status']
    except KeyError:
      print("DB status entry may not yet exist, assigning initial value")
      db['status'] = "initial start value"
      fetched = db['status']

    # part of the send mail logic, checks db for date to avoid duplicate sends
    if send_new_alert and (fetched != xdaymdy):
      send_email(msg_str)
      time.sleep(10)
      #send_email(msg_str,"example@example.com") # <- to send to additonal people
      print('email(s) sent')
      db['status'] = xdaymdy

    else:
      print("send alert condition not triggered, sleeping...")

    # wait 2.5 hours until checking beginning of loop again
    time.sleep(9000) 
    #wait 1 hour until checking again (if loop never ran)
  else:
    print('Sleeping 1 hr...')
    time.sleep(3600) 
    

# Basically script checks every hour if it is the right time (7-8am central) 
# and then checks the data to see if an alert should be sent. If it is the 
# correct day set to send an email then it executes or if a new trend change 
# has just occured, it sends, otherwise it waits an hour. This structure was 
# chosen so that if a server restart occurs, it should still usually check 
# and execute properly unless the server is completely down between 7-8 am 
# but that seems unlikely enough that I am ok with this structure.

