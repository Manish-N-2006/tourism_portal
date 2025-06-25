import mysql.connector as mc
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from datetime import date
from tabulate import tabulate as t
from dotenv import load_dotenv
import os
load_dotenv()

yl=''
de=''
distance_km=0
tcost=0
hcost=0
gcost=0



conn=mc.connect(user='root',host='localhost',password=os.getenv("DB_PASSWORD"),database='tourism_portal_fi')
cursor=conn.cursor()
pw='kmm'

user_database = dict()
admin_database=dict()

def register_admin():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name varchar(20) unique,
        password varchar(20),
        type varchar(10)
        )
    ''')
    username = input("Enter a new username: ")
    password = input("Enter a password: ")
    typ='admin'
    cursor.execute('''INSERT INTO users VALUES(%s,%s,%s)''',(username,password,typ))
    print(f"Admin {username} registered successfully!")
    conn.commit()


def register_user():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        name varchar(20) unique,
        password varchar(20),
        type varchar(10)
        )
    ''')
    username = input("Enter a new username: ")
    password = input("Enter a password: ")
    typ='user'
    cursor.execute('''INSERT INTO users VALUES(%s,%s,%s)''',(username,password,typ))
    print(f"User {username} registered successfully!")
    conn.commit()

def initialize_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name varchar(20) unique,
            password varchar(20),
            type varchar(10)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            location_id integer unique,
            location varchar(20) PRIMARY KEY
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transport (
            transport varchar(10),
            cost_per_km integer
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            location varchar(10),
            hotel varchar(20),
            Cost_per_night integer,
            foreign key (location) references locations(location)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spots(
            location varchar(10),
            spots varchar(100),
            foreign key (location) references locations(location)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS details(
            no int,
            cr varchar(15),
            des varchar(15),
            tp varchar(15),
            t_cost int,
            hotel varchar(15),
            h_cost int,
            gcost int,
            total_cost int
        )
    ''')
    conn.commit()




def login():
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    
    query = "SELECT * FROM users WHERE name = %s AND password = %s"
    cursor.execute(query, (name, password))
    result = cursor.fetchone()
    
    if result:
        print(f"Welcome {name}! Login successful as {result[2]}")
        if result[2].lower() == 'admin':
            admin_menu()
        elif result[2].lower() == 'user':
            user_menu()
    else:
        print("Error: Invalid username or password")
        login()


        

def addloca():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        location_id integer unique,
        location varchar(20) PRIMARY KEY
        )
    ''')
    while(1):
        try:
            nid=int(input("Enter location id:"))
            na=input('Enter the location:')
            cursor.execute('''INSERT INTO locations VALUES(%s,%s)''',(nid,na))
            conn.commit()
            ch=input('Enter do you want to add another record(y/n):')
            if ch in 'Nn':
                break
        except:
            print('error')
            conn.rollback()
            return


def tr():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transport (
        transport varchar(10),
        cost_per_km integer
        )
    ''')
    while(1):
        try:
            tra=input('Enter the transport:')
            c=int(input('Enter cost per km:'))
            cursor.execute('''INSERT INTO transport VALUES(%s,%s)''',(tra,c))
            conn.commit()
            ch=input('Enter do you want to add another record(y/n):')
            if ch in 'Nn':
                break
        except:
            print('error')
            conn.rollback()
            return


def hotels():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hotels (
        location varchar(10),
        hotel varchar(20),
        Cost_per_night integer,
        foreign key (location) references locations(location)
        )
    ''')
    while(1):
        try:
            loc=input('Enter the location:')
            hotel=input('Enter hotel name:')
            cpn=int(input('Enter Cost Per Night(in Rs):'))
            cursor.execute('''INSERT INTO hotels VALUES(%s,%s,%s)''',(loc,hotel,cpn))
            conn.commit()
            ch=input('Enter do you want to add another record(y/n):')
            if ch in 'Nn':
                break
        except:
            print('error')
            conn.rollback()
            return

def spots():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS spots(
        location varchar(10),
        spots varchar(100),
        foreign key (location) references locations(location)
        )
    ''')
    while(1):
        try:
            loc=input('Enter the location:')
            spots=input('Enter places to visit:')
            cursor.execute('''INSERT INTO spots VALUES(%s,%s)''',(loc,spots))
            conn.commit()
            ch=input('Enter do you want to add another record(y/n):')
            if ch in 'Nn':
                break
        except:
            print('error')
            conn.rollback()
            return


def shspots(loc):
    cursor.execute('''SELECT * from spots''')
    row = cursor.fetchall()
    print("%-12s%-100s"%("Location","spots"))
    for c in row:
        if c[0].lower()==loc.lower():
            print('%-12s%-100s'%(c[0],c[1]))
        
            
    
    



def admin_menu():
    print('Welcome, Admin! \nwhat do you want to do')
    while(1):
        print('''
                ADMINISTRATOR MENU
               ====================
        1. Add location
        2. Add transport
        3. Add hotels
        4. Add Tourist spots
        5. Show locations
        6. Show Tourist spots
        7. Show hotels
        8. Show transport 
        9. Exit
        ''')
        ch=int(input('Enter choice:'))
        if ch==1:
            addloca()
        elif ch==2:
            tr()
        elif ch==3:
            hotels()
        elif ch==4:
            spots()
        elif ch==5:
            cursor.execute('''select * from locations''')
            row = cursor.fetchall()
            print("%-12s%-12s"%("Id",'Place'))
            for c in row:
                print("%-12s%-12s"%(c[0],c[1]))
        elif ch==6:
            cursor.execute('''SELECT * from spots''')
            row = cursor.fetchall()
            print("%-12s%-100s"%("Location","spots"))
            for c in row:
                print('%-12s%-100s'%(c[0],c[1]))
        elif ch==7:
            cursor.execute('''select * from hotels''')
            row = cursor.fetchall()
            print("%-12s%-12s%-12s"%("Location","Hotel","Cost"))
            for c in row:
                print("%-12s%-12s%-12s"%(c[0],c[1],c[2]))
        elif ch==8:
            cursor.execute('''select * from transport''')
            row = cursor.fetchall()
            print("%-12s%-25s"%("Transport",'Cost(per Km (in Rs))'))
            for c in row:
                print("%-12s%-25s"%(c[0],c[1]))
        elif ch==9:
            break
    
        else:
            print('Invalid input')


def user_menu():
    print("Welcome, User!")
    while True:
        print('''
                    CUSTOMER MENU
                   ===============
                1. Available locations
                2. Book packages
                3. Exit''')
        ch=int(input('Enter Choice:'))
        if ch==1:
            cursor.execute('''select * from locations''')
            row = cursor.fetchall()
            print("%-12s%-12s"%("Id",'Place'))
            for c in row:
                print("%-12s%-12s"%(c[0],c[1]))
        elif ch==2:
            print('\n\nNOTE : Please only Enter the available locations ')
            yl=input('\n\nEnter your current location :')
            
            de=input('Enter the location you want to travel:')
            

            #distance
            
            
            geolocator = Nominatim(user_agent="distance_calculator") # Initialize the geocoder
            
            # Get user input for the two locations
            location1 = yl
            location2 = de
            
            # Geocode the locations to get latitude and longitude
            location1_coords = geolocator.geocode(location1)
            location2_coords = geolocator.geocode(location2)
            if location1_coords is None or location2_coords is None:
                print("One or both of the locations could not be geocoded.")
            else:
                # Calculate the distance using geodesic distance
                distance_km = geodesic((location1_coords.latitude, location1_coords.longitude),(location2_coords.latitude, location2_coords.longitude)).kilometers
            print(f"The distance between {location1} and {location2} is approximately {distance_km:.2f} kilometers.")

            



            #spots

            print('\n\nSome tourist spots to visit')
            shspots(de)



            #transport

            print('\n\nAvailable transports to travel and thier cost per kilometer')
            print('\n')
            cursor.execute('''select * from transport''')
            row = cursor.fetchall()
            print("%-12s%-25s"%("Transport",'Cost(per Km (in Rs))'))
            for c in row:
                print("%-12s%-25s"%(c[0],c[1]))
            print('\n')
            tr = input('Enter the transport you wish to travel with:')
            cursor.execute('''select * from transport''')
            row = cursor.fetchall()
            for z in row:
                if z[0].lower() == tr.lower():
                    tcost = distance_km * int(z[1])
                    print('The cost for transport:', int(tcost),'Rs')
            


            #hotels

            print('\n\nAvailable Hotels for your location to stay and thier cost per night')
            print('\n')
            cursor.execute('''select * from hotels''')
            row = cursor.fetchall()
            print("%-12s%-12s%-12s"%("Location","Hotel","Cost"))
            for c in row:
                print("%-12s%-12s%-12s"%(c[0],c[1],c[2]))
            print('\n')
            ht=input('Enter the Hotel you wish to stay:')
            nc=int(input('Enter how many nights you want to stay:'))
            cursor.execute('''select * from hotels''')
            row = cursor.fetchall()
            for z in row:
                if z[1].lower() == ht.lower():
                    hcost = nc * int(z[2])
                    print('The cost for hotel',int(hcost),'Rs')


            #guide

            print('\n\nCost of a tourist guide for one night is 400')
            ch=input('Enter do you want a guide(y/n):')
            
            if ch.lower()=='y':
                co=int(input('How many days do you want a guide:'))
                gcost=400*co
                print('Cost of guide for your trip:',gcost)
            else:
                gcost=0


            ctr=1
            tu=(ctr,yl,de,tr,tcost,ht,hcost,gcost)

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS details(
                    no int,
                    cr varchar(15),
                    des varchar(15),
                    tp varchar(15),
                    t_cost int,
                    hotel varchar(15),
                    h_cost int,
                    gcost int,
                    total_cost int
                )
                ''')
    
            a,b,c,d,e,f,g,h=tu
            bill=[e,g,h]
            formatted_bill = [item if isinstance(item, list) else [item] for item in bill]
            tamt=sum(bill)
            cursor.execute('''INSERT INTO details values(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(a,b,c,d,e,f,g,h,tamt))
            conn.commit()
            print('\n')
            print('Successfully Booked the package')
            print('\n')
            d1=date.today().strftime('%d/%m/%y')
            print('BILL:')
            print(t(formatted_bill, headers=['Transport,Hotel,Guide Costs', 'Hotel Cost', 'Guide Cost'], tablefmt='grid'))
            #print(t(bill,['Transport Cost','Hotel Cost','Guide Cost'],tablefmt='grid'))
            print('Total Amount=',int(tamt),'Rs')
            conn.commit()
            print('''


                                            Thank You for Booking.
                                                Enjoy your trip''')
            
            
        elif ch==3:
            break
        else:
            print('Invalid input')

            
 
   

initialize_tables()
while(1):
    print('''
            WELCOME TO THE_EXPLORER TOURISM PORTAL
           ========================================
                1.Register user or admin
                2.Login
                3.Exit''')
    ch=int(input('Enter choice:'))
    if ch==1:
        ty=input('Admin or user:')
        if ty.lower()=='admin':
            ps=input('Enter the main password to register admin:')
            if ps==pw:
                register_admin()
            else:
                print('Enter correct password to register admin')
        elif ty.lower()=='user':
            an=input('Enter admin name to register user:')
            ap=input('Enter password:')
            cursor.execute('''Select * from users''')
            row=cursor.fetchall()
            for c in row:
                if c[0].lower()==an.lower() and c[1]==ap:
                    register_user()
                    
            
                else:
                    print('you have to enter correct admin name and password to register user')
        else:
            print('Invalid input')
    elif ch==2:
        login()
    elif ch==3:
        break
    else:
        print('invalid input')
        
input()                
