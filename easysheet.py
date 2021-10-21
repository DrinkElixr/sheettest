import ezsheets
def orders():
    ss=ezsheets.Spreadsheet("1iCK6KlaDOedlmoUnROZIzrjgcqKgIFTx9_dls5A5F1M")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Orders":
            return ss[i]
def picking():


    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Picking Chart":
            return ss[i]
def reference():

    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Reference":
            return ss[i]

def okay():
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Orders":
            return ss[i]
def delivery_skeet():
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Generated Delivery Plan":
            return ss[i]
def orders2():
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Orders2.0":
            return ss[i]
def tincture():
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Production (Tinctures)":
            return ss[i]
def oil():
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Cannabis Inventory":
            return ss[i]

def production():
    ss=ezsheets.Spreadsheet("1-Q8b5sb2Q6Tnk4VkBAcGyQFkbxXOOXnfHuGBImyIrKw")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Production (Seltzer)":
            return ss[i]
def cadence():
    ss=ezsheets.Spreadsheet("1T9LEoSqCg0Yg8C5qZMWGqoFZI1pPoF9VrrOQVzwTTvQ")
    sheets=ss.sheetTitles
    print(sheets)
    for i,sheet in enumerate(sheets):
        #print(sheet)
        if sheet=="Cadence":
            return ss[i]
