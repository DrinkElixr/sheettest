import ezsheets

from datetime import datetime

now = datetime.now()
sheet = ezsheets.Spreadsheet("1kqcS5reDtNToiWqSRw-X4Sjd_q2mImDNsn0Iwlkm0Iw")[0]

sheet["A1"]=now
