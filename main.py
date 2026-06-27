import time as t
import random

f=open("farm.txt", "r")
money = f.readline()
money = int(money.replace("\n",""))
stock = []
invent = []
logbk = []

temp = f.readline()
temp = temp.replace("\n","")
temp = temp.split(",")
for i in temp:
    stock.append(int(i))

temp = f.readline()
temp = temp.replace("\n","")
temp = temp.split(",")
for i in temp:
    invent.append(int(i))

temp = f.readline()
temp = temp.replace("\n","")
temp = temp.split(",")
for i in temp:
    logbk.append(int(i))

file = f.read()
slots = file.split("\n")
for i  in range(len(slots)):
    temp = slots[i].split(" ")
    slots[i] =temp

#time(s),min_price,max_price
potato_list=["Potato", "Good_potato", "Tri-potato"]
potato_dict={
    "Potato":[30,12,20],
    "Good_potato":[120,120,160],
    "Tri-potato":[1800,3000,4000]
}
#name,price,stock,type
slot_limit = 8
slot_price = 0
shop_list = []
slot_price = int(4000**(1+len(slots)*0.01))
shop_list=[
    ["Good_potato Seed",20,-1,"po"],
    ["Tri-potato Seed",300,-1,"po"],
    ["Extra slot",slot_price,slot_limit-len(slots),"slt"]
]



def save():
    global money
    global stock
    global slots
    global invent
    global logbk
    str_money = str(money)
    str_stock = ""
    str_invent = ""
    str_logbk = ""
    for i in range(len(stock)):
        str_stock += str(stock[i])
        if i != len(stock)-1:
            str_stock += ","

    for i in range(len(invent)):
        str_invent += str(invent[i])
        if i != len(invent)-1:
            str_invent += ","

    for i in range(len(logbk)):
        str_logbk += str(logbk[i])
        if i != len(logbk)-1:
            str_logbk += ","

    old = open("farm.txt", "w")
    old.write(str_money+"\n"+str_stock+"\n"+str_invent+"\n"+str_logbk+"\n")
    for j in range(len(slots)):
        temp = slots[j]
        for i in range(len(temp)):
            old.write(temp[i])
            if i != len(temp)-1:
                old.write(" ")
        if j != len(slots)-1:
            old.write("\n")
    
def int_ask(text):
    flag = True
    while flag:
        try:
            ans = int(input(text))
            flag = False
        except:
            print("Invalid input! Please input again.")
    return ans
    
def time_convert(time):
    mins = time//60
    secs = time%60
    if mins == 0:
        mins = ""
    else:
        mins = f"{mins} min(s) "
    if secs == 0:
        secs = ""
    else:
        secs = f"{secs} s"
    return mins+secs

def rate(slot_no):
    slot_no = int(slot_no)
    potato = slots[slot_no-1][1]
    if slots[slot_no-1][2] == "x":
        rate = "x"
    else:
        time = float(slots[slot_no-1][2])
        dif = round(t.time()-time,1)
        rate = dif/potato_dict[potato][0]
        if rate>=1:
            rate = "100%"
        else:
            rate = str(float("%0.1f" % (rate*100)))+"%"
    return  rate

def show_slots():
    headers = ["Slot", "Potato", "Progress"]
    print(f"{headers[0]:<4} {headers[1]:<15} {headers[2]:<5}")
    print("-" * 38) 
    
    for row in slots:
        temp_time = row[2]
        if temp_time != "x":
            temp_time = rate(row[0])
            
        print(f"{row[0]:<4} {row[1]:<15} {temp_time:<5}")

def menu(actions):
    global money    
    print(f"Welcome to Potato Farm!! Money: ${money}\n"+"="*38)
    for key, data in actions.items():
        print(f"{key}. {data['label']}")
    choice = input("Enter Choice: ")
    print("=" * 38)
    return choice

def farm():
    farm_actions = {
        "1": {"label": "Plant", "action": plant},
        "2": {"label": "Harvest ALL", "action": harvest}
    }
    while True:
        print("Here is your farm")
        show_slots()
        print("=" * 38)
        for key, data in farm_actions.items():
            print(f"{key}. {data['label']}")
        print("3. Return")
        
        choice = input("Enter Choice: ")
        print("=" * 38)
        
        if choice == "3":
            break 
        elif choice in farm_actions:
            farm_actions[choice]["action"]()
        else:
            print("Invalid choice!")


def plant():
    global logbk
    print("Which potato do you want to plant?")
    print(f"{"Potato_type":<17} {"Required time":<13} {"Stock"}")
    print("-" * 38) 
    for i in range(len(potato_list)):
        print(i+1, end=".")
        if stock[i] == -1:
            p_stock = "inf."
        else:
            p_stock = str(stock[i])
        potato = potato_list[i]
        print(f'{potato:<15} {time_convert(potato_dict[potato][0]):<13} ({p_stock})')
    choice = int_ask("Enter choice: ")-1
    if stock[choice] == 0:
        print("Sorry, you have no seed to plant this potato.")
    else:
        show_slots()
        farm_no = int_ask(f"Which slot do you want to plant {potato_list[choice]}? ")
        if slots[farm_no-1][1] == "x":
            print(f"You successfully plant {potato_list[choice]} in slot {farm_no}!")
            slots[farm_no-1][1] = potato_list[choice]
            slots[farm_no-1][2] = str(t.time())
            logbk[choice] += 1
            if stock[choice] != -1:
                stock[choice] -= 1
        else:
            print("Sorry, this slot is already occupied.")
        save()

def harvest():
    global invent
    for i in range(len(slots)):
        if rate(str(i+1)) == "100%":
            potato = slots[i][1]
            invent[potato_list.index(potato)] += 1
            print(f"You harvest a(n) {potato} !")
            slots[i][1] = "x"
            slots[i][2] = "x"
    save()

def shop():
    global money
    global stock
    global slot_price
    print(f"Welcome to Shop!! Money: ${money}")
    print("="*38)
    print(f"          {"Items":<16} {"Price":<8} {"Stock"}")
    for i in range(len(shop_list)):
        if shop_list[i][2] == -1:
            amount = "inf."
        else:
            amount = str(shop_list[i][2])
        print(i+1, end=". ")
        print(f"{shop_list[i][0]:<25} ${shop_list[i][1]:<8} ({amount})")
    print(str(len(shop_list)+1)+". Exit shop")
    print("="*38)
    choice = int_ask("What do you want to buy? ")-1
    if choice == len(shop_list):
        print("Return to menu.")
        return
    else:
        if shop_list[choice][2] == 0:
            print("Sorry, this item is sold out.")
        else:
            if shop_list[choice][3] == "po":
                amount = int_ask("How many do you want to buy? ")
                while amount <= 0:
                    amount = int_ask("Sorry, please input again! ")
            else:
                amount = 1
            if money >= shop_list[choice][1]*amount:
                if shop_list[choice][3] == "po":
                    print(f"You bought {amount} {shop_list[choice][0]}(s) successfully!")
                    stock[choice+1] += amount
                    money -= shop_list[choice][1]*amount
                    save()
                elif shop_list[choice][3] == "slt":
                    print("You bought an extra slot!!")
                    num = str(len(slots)+1)
                    slots.append([num,"x","x"])
                    money -= shop_list[choice][1]*amount
                    shop_list[choice][2] -= 1
                    slot_price = int(4000**(1+len(slots)*0.01))
                    save()
            else:
                print("You don't have enough money to buy this. :(")

def market():
    global invent
    global money
    price_list = []
    print("Welcome to POTA-market!")
    print("="*38)
    for i in range(len(invent)):
        potato = potato_list[i]
        cur_price = int(random.uniform(potato_dict[potato][1],potato_dict[potato][2]))
        price_list.append(cur_price)

    while True:
        print(f"   {"Potato":<16} {"Price":<8} {"Inventory":}")
        for i in range(len(invent)):
            potato = potato_list[i]
            amount = str(invent[i])
            print(i+1, end=". ")
            print(f"{potato:<16} ${price_list[i]:<8} ({amount})")
        print(str(len(potato_list)+1)+". Exit Market")
        print("="*38)
        choice = int_ask("What do you want to sell? ")-1
        if choice == len(potato_list):
            print("Return to menu.")
            return 
        potato = potato_list[choice]
        if invent[choice] == 0:
            print(f"Sorry, you have no {potato} to sell.")
            continue
        else:
            profit = price_list[choice]*invent[choice]
            money += profit
            print(f"You sell all {potato} and earn ${profit} !")
            invent[choice] = 0
            save()


def show_logbk():
    print("Here is your logbook!")
    print("="*45)
    i=0
    while True:
        potato = potato_list[i]
        req_time = time_convert(potato_dict[potato][0])
        amount = logbk[i]
        print(
        fr"""    __________________   __________________
|||| Potato Name:      |                   ||||
||||  {potato:^15}  |     ~~Record~~    ||||
||||                   |                   ||||
|||| Required Time:    |   {amount:^13}   ||||
||||  {req_time:^15}  |      planted      ||||
||||                   |     --==*==--     ||||
||||                   |                   ||||
||||                   |                   ||||
||||                   |                   ||||
||||                   |                   ||||
||||__________________ | __________________||||
||/===================\|/===================\||
`--------------------~___~-------------------''
    """
        )
        print("="*45)
        print("1.Previous   2.Next  3.Exit logbook")
        choice = int_ask("Enter Choice: ")
        if choice == 1:
            if i != 0:
                i -= 1
        elif choice == 2:
            if i != len(logbk)-1:
                i += 1
        elif choice == 3:
            break 
def main():
    menu_actions = {
        "1": {"label": "Farm", "action": farm},
        "2": {"label": "Market", "action": market},
        "3": {"label": "Shop", "action": shop},
        "4": {"label": "Logbook", "action": show_logbk},
        "5": {"label": "Exit", "action": "exit"} 
    }
    while True:
        choice = menu(menu_actions)
        if menu_actions[choice]["action"] == "exit":
            save()
            print("See you next time!")
            t.sleep(1)
            f.close()
            break
        elif choice in menu_actions:
            menu_actions[choice]["action"]() 
        else:
            print("Invalid choice! Please try again.")
            
main()
