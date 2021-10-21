import sys

import pandas as pd
from flask import Flask, request, abort, Response
import smtplib
from email.message import EmailMessage
import base64
import hashlib
import datetime
import hmac
import ezgmail
import json
app= Flask(__name__)
def parse_json(json):
    action=json["action"]
    ln=json["data"]["buyer"]["number"]
    name=ln=json["data"]["buyer"]["name"]
    items=json["data"]['orderedproduct_set']
    rep=json['data']['sales_reps'][0]["email"]
    dd=json['data']['ship_date']
    id=json['data']['number']
    df=pd.read_csv("LL_Rec.csv",index_col=0)
    pd.concat([df,pd.DataFrame([[datetime.now(),id,action,ln,dd,rep,items,False]],columns=df.columns,index=[len(df)])]).to_csv("LL_Rec.csv")
    return [datetime.now(),id,action,ln,dd,rep,items,name]

def send_email(rec, sub,message):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = sub
    msg['From'] = "mikeb@levia.buzz"
    msg['To'] = "mikeb@levia.buzz"

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("mikeb@levia.buzz", "bobgjkisuczynaze")
    server.send_message(msg)
    server.quit()

def new_order(data):
    return True
def del_order(ln,dd,items):
    return True
@app.route("/",methods=["POST"])
def welcome():
    #ezgmail.send("mikeb@levia.buzz", "Order", request.json)
    data=parse_json(request.json)
    success=None
    successd=None
    if data[2]=="edit":
        if data[4]=="None":
            send_email(data[5],f"{data[-1]} Sheet Push Failure",f"Order for {data[-1]} was not entered into Google Sheets because there was no Shipping Date entered. Please edit the order to include Shipping Date to push order to Google Sheets.")
        else:
            df=pd.read_csv("LL_Rec.csv",index_col=0)
            dff=df[df["Id"]==data[1]]
            dff=dff[dff["Pushed"]==True]
            i_list=dff.index.to_list()
            i=i_list[-1]
            if len(dff)==0:
                success=new_order(data)
            else:

                successd=del_order(dff["License"][i],dff["DD"][i],dff["Items"][i])
                success=new_order(data)
    else:
        success=new_order(data)

    if success==True:
        send_email(data[5], f"{data[-1]} Sheet Push Success",f"Order for {data[-1]} was successfully entered into Google Sheets.")
        df = pd.read_csv("LL_Rec.csv", index_col=0)
        df["Pushed"][len(df)]=True
        df.to_csv("LL_Rec.csv")

    if success==False:
        send_email(data[5],f"{data[-1]} Sheet Push Success",f"Order for {data[-1]} was unsuccessfully entered into Google Sheets.")
    return "A simple webhook listener"

@app.route("/webhook",methods=["POST"])
def webhook():
    print("Recieved Webhook")
    #sys.stdout.flush()
    key = bytes('7d84c4926c8133acdb9b64e6cf8a22f65badefb0', 'utf-8')
    request_body = '{"foo": "bar"}'

    signature = base64.b64encode(hmac.new(key, request_body, digestmod=hashlib.sha256).digest())

    # compare the calculated signature to the signature provided in the request header
    success = signature == request.headers['LL-Signature']
    print(success)
    if request.method=="POST" and success:
        print(request.get_json())
        send_email("mikeb@levia.buzz","WH")
        return Response(status=200)
    else:
        abort(400)
if __name__ == '__main__':
    app.run(debug=True)