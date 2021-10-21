import sys
from easysheet import cadence, orders
import pandas as pd
from alph import *
from flask import Flask, request, abort, Response
import smtplib
from email.message import EmailMessage
import base64
import hashlib
import datetime
import hmac
import json

app = Flask(__name__)


def send_email(rec, sub, message):
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
    sheet = orders()
    match = False
    for n in range(10, 300, 2):
        ln = sheet[f"D{n}"]
        if data[3] in ln:
            dd = datetime.datetime.strptime(data[4].split("T")[0], "%Y-%m-%d")

            dd = dd.strftime("%m/%d/%Y")
            for l in range(5, 1200, 4):
                d = sheet[f"{alph[l]}1"]
                if d == dd:
                    match = True
                    for item in data[-2]:
                        name = item["product"]["name"]
                        cases = int(item["quantity"].split(".")[0]) / int(item["unit_multiplier"])
                        if "Achieve 12oz Seltzer" in name:
                            sheet[f"{alph[l + 1]}{n}"] = cases
                        elif "Celebrate 12oz Seltzer" in name:
                            sheet[f"{alph[l]}{n}"] = cases
                        elif "Dream 12oz Seltzer" in name:
                            sheet[f"{alph[l + 2]}{n}"] = cases
                        elif "Seasonal" in name:
                            sheet[f"{alph[l + 3]}{n}"] = cases
                        elif "Celebrate" in name and "Tincture" in name:
                            sheet[f"{alph[l]}{n + 1}"] = cases
                        elif "Achieve" in name and "Tincture" in name:
                            sheet[f"{alph[l + 1]}{n + 1}"] = cases
                        elif "Dream" in name and "Tincture" in name:
                            sheet[f"{alph[l + 2]}{n + 1}"] = cases
                    break
    if match == True:
        sheet = cadence()
        match = False
        for n in range(6, 400, 2):
            ln = sheet[f"E{n}"]
            if data[3] in ln:
                dd = datetime.datetime.strptime(data[4].split("T")[0], "%Y-%m-%d")
                if dd.date().weekday() != 0:
                    for x in range(7):
                        dd = dd - datetime.timedelta(days=1)
                        if dd.date().weekday() == 0:
                            break

                d1 = dd.date().day
                m1 = dd.date().month
                for l in range(9, 600, 1):
                    d = sheet[f"{alph[l]}5"].split(" ")[1]
                    m2 = d.split("/")[0]
                    d2 = d.split("/")[1]
                    print(m1, d1, m2, d2)
                    print(int(d1) == int(d2), int(m1) == int(m2))
                    if int(d1) == int(d2) and int(m1) == int(m2):

                        match = True
                        seltzers = 0
                        tinctures = 0
                        for item in data[-2]:
                            name = item["product"]["name"]
                            cases = int(item["quantity"].split(".")[0]) / int(item["unit_multiplier"])
                            if "Seltzer" in name or "Seasonal" in name:
                                seltzers += cases
                            if "Tincture" in name:
                                tinctures += cases
                        sheet[f"{alph[l]}{n}"] = str(seltzers)
                        sheet[f"{alph[l]}{n + 1}"] = str(seltzers)
                        break
    return match


def del_order(lnn, ddd, items):
    sheet = orders()
    match = False
    for n in range(10, 300, 2):
        ln = sheet[f"D{n}"]
        if lnn in ln:
            dd = datetime.datetime.strptime(ddd.split("T")[0], "%Y-%m-%d")
            dd = dd.strftime("%m/%d/%Y")
            for l in range(5, 1200, 4):
                d = sheet[f"{alph[l]}1"]
                if d == dd:
                    match = True

                    sheet[f"{alph[l + 1]}{n}"] = ""

                    sheet[f"{alph[l]}{n}"] = ""

                    sheet[f"{alph[l + 2]}{n}"] = ""

                    sheet[f"{alph[l + 3]}{n}"] = ""

                    sheet[f"{alph[l]}{n + 1}"] = ""

                    sheet[f"{alph[l + 1]}{n + 1}"] = ""

                    sheet[f"{alph[l + 2]}{n + 1}"] = ""
                    break
    if match == True:
        sheet = cadence()
        match = False
        for n in range(6, 400, 2):
            ln = sheet[f"E{n}"]
            if lnn in ln:
                dd = datetime.datetime.strptime(ddd.split("T")[0], "%Y-%m-%d")
                if dd.date().weekday() != 0:
                    for x in range(7):
                        dd = dd - datetime.timedelta(days=1)
                        if dd.date().weekday() == 0:
                            break

                d1 = dd.date().day
                m1 = dd.date().month
                for l in range(9, 600, 1):
                    d = sheet[f"{alph[l]}5"].split(" ")[1]
                    m2 = d.split("/")[0]
                    d2 = d.split("/")[1]
                    if int(d1) == int(d2) and int(m1) == int(m2):
                        match = True

                        sheet[f"{alph[l]}{n}"] = ""
                        sheet[f"{alph[l]}{n + 1}"] = ""
                        break
    return match


def parse_json(json):
    action = json["action"]
    ln = json["data"]["customer"]["license_number"]
    name = json["data"]["buyer"]["name"]
    items = json["data"]['orderedproduct_set']
    rep = json['data']['sales_reps'][0]["email"]
    dd = json['data']['ship_date']
    id = json['data']['number']
    df = pd.read_csv("LL_Rec.csv", index_col=0)
    pd.concat([df, pd.DataFrame([[datetime.datetime.now(), id, action, ln, dd, rep, items, False]], columns=df.columns,
                                index=[len(df)])]).to_csv("LL_Rec.csv")
    return [datetime.datetime.now(), id, action, ln, dd, rep, items, name]


@app.route("/", methods=["POST"])
def welcome():
    # ezgmail.send("mikeb@levia.buzz", "Order", request.json)
    data = parse_json(request.json)
    print(data)
    success = None
    successd = None
    if request.json["data"]["status"] == "Rejected":
        df = pd.read_csv("LL_Rec.csv", index_col=0)
        dff = df[df["Id"] == data[1]]
        print(dff["Pushed"])
        dff = dff[dff["Pushed"] != False]
        dff=dff.dropna()
        i_list = dff.index.to_list()
        print((dff["DD"]))
        ddd = dff["DD"][i_list[-1]]
        del_order(data[3], ddd, data[6])
    elif data[2] == "edit":
        if data[4] == "null":
            send_email(data[5], f"{data[-1]} Sheet Push Failure",
                       f"Order for {data[-1]} was not entered into Google Sheets because there was no Shipping Date entered. Please edit the order to include Shipping Date to push order to Google Sheets.")
        else:
            df = pd.read_csv("LL_Rec.csv", index_col=0)
            dff = df[df["Id"] == data[1]]
            dff = dff[dff["Pushed"] == True]
            i_list = dff.index.to_list()

            if len(dff) == 0:
                success = new_order(data)
            else:
                i = i_list[-1]
                successd = del_order(dff["License"][i], dff["DD"][i], dff["Items"][i])
                success = new_order(data)
    else:
        send_email(data[5], f"{data[-1]} Sheet Push Failure",
                   f"Order for {data[-1]} was not entered into Google Sheets because there was no Shipping Date entered. Please edit the order to include Shipping Date to push order to Google Sheets.")

    if success == True:
        send_email(data[5], f"{data[-1]} Sheet Push Success",
                   f"Order for {data[-1]} was successfully entered into Google Sheets.")
        df = pd.read_csv("LL_Rec.csv", index_col=0)
        df["Pushed"][len(df) - 1] = True
        df.to_csv("LL_Rec.csv")

    if success == False:
        send_email(data[5], f"{data[-1]} Sheet Push Failure",
                   f"Order for {data[-1]} was unsuccessfully entered into Google Sheets.")
    return "A simple webhook listener"


@app.route("/webhook", methods=["POST"])
def webhook():
    print("Recieved Webhook")
    # sys.stdout.flush()
    key = bytes('7d84c4926c8133acdb9b64e6cf8a22f65badefb0', 'utf-8')
    request_body = '{"foo": "bar"}'

    signature = base64.b64encode(hmac.new(key, request_body, digestmod=hashlib.sha256).digest())

    # compare the calculated signature to the signature provided in the request header
    success = signature == request.headers['LL-Signature']
    print(success)
    if request.method == "POST" and success:
        print(request.get_json())
        send_email("mikeb@levia.buzz", "WH")
        return Response(status=200)
    else:
        abort(400)


if __name__ == '__main__':
    app.run(debug=True,threaded=True,host="0.0.0.0",port=8080)
