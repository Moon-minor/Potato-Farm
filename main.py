import time as t

f=open("farm.txt", "r")
money = f.readline()
money = int(money.replace("\n",""))
stock = []
temp = f.readline()
temp = temp.replace("\n","")
temp = temp.split(",")
for i in temp:
    stock.append(int(i))

file = f.read()
slots = file.split("\n")
for i  in range(len(slots)):
    temp = slots[i].split(" ")
    slots [i] =temp

#time(s),price
potato_list=["Potato", "Good_potato", "Tri-potato"]
potato_dict={
    "Potato":[30,15],
    "Good_potato":[120,120],
    "Tri-potato":[1800,3000]
}
#name,price,stock,type
slot_limit = 8
slot_price = 0
shop_list = []
def update_shop():
    global slot_price
    global shop_list
    slot_price = int(4000**(1+len(slots)*0.01))
    shop_list=[["Good_potato Seed",20,-1,"po"],["Tri-potato Seed",300,-1,"po"],["Extra slot",slot_price,slot_limit-len(slots),"slt"]]
update_shop()

def save():
    global money
    global stock
    global slots
    str_money = str(money)
    str_stock = ""
    for i in range(len(stock)):
        str_stock += str(stock[i])
        if i != len(stock)-1:
            str_stock += ","
    old = open("farm.txt", "w")
    old.write(str_money+"\n"+str_stock+"\n")
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

def menu():
    global money    
    print(f"Welcome to Potato Farm!! Money: ${money}\n"+"="*38)
    print("1.Farm\n2.Shop\n3.Exit")
    choice = input("Enter Choice: ")
    print("=" * 38)
    return choice

def farm():
    print("Here is your farm")
    show_slots()
    print("=" * 38)
    print("1.Plant\n2.Harvest ALL\n3.Return")
    choice = input("Enter Choice: ")
    print("=" * 38)
    return choice


def plant():
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
            if stock[choice] != -1:
                stock[choice] -= 1
        else:
            print("Sorry, this slot is already occupied.")
        save()

def harvest():
    global money
    for i in range(len(slots)):
        if rate(str(i+1)) == "100%":
            profit = potato_dict[slots[i][1]][1]
            money += profit
            print(f"You sell {slots[i][1]} and earn ${profit} !")
            slots[i][1] = "x"
            slots[i][2] = "x"
    save()
def shop():
    global money
    global stock
    print(f"Welcome to Shop!! Money: ${money}")
    print("="*38)
    print(f"          {"Items":<16} {"Price":<8} {"Stock"}")
    for i in range(len(shop_list)):
        if shop_list[i][2] == -1:
            amount = "inf."
        else:
            amount = str(shop_list[i][2])
        print(i+1, end=".")
        print(f"{shop_list[i][0]:<25} ${shop_list[i][1]:<8} ({amount})")
    print("="*38)
    choice = int_ask("What do you want to buy? ")-1
    amount = shop_list[choice][2]
    if amount == 0:
        print("Sorry, this item is sold out.")
    else:
        if money >= shop_list[choice][1]:
            if shop_list[choice][3] == "po":
                print(f"You bought {shop_list[choice][0]} successfully!")
                stock[choice+1] += 1
                money -= shop_list[choice][1]
                save()
            elif shop_list[choice][3] == "slt":
                print("You bought an extra slot!!")
                num = str(len(slots)+1)
                slots.append([num,"x","x"])
                money -= shop_list[choice][1]
                update_shop()
                save()
        else:
            print("You don't have enough money to buy this. :(")


def main():
    farm_flag = False
    end = False
    while not end:
        choice = menu()
        if choice == "1":
            farm_flag = True
            while farm_flag:
                choice = farm()
                if choice == "1":
                    plant()
                elif choice == "2":
                    harvest()
                elif choice == "3":
                    farm_flag = False
        elif choice == "2":
            shop()
        elif choice == "3":
            save()
            print("See you next time!")
            end = True
            f.close()
main()
