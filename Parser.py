import sys
import xml.dom.minidom
import mysql.connector
#should extract the relevant data and insert the extracted data into a mySQL database
Ids=["current_conditions-summary","seven-day-forecast-body","detailed-forecast-body",'current-conditions','about_forecast']

file = sys.argv[1]
ipaddy = sys.argv[2]
state = sys.argv[3]
print(file,ipaddy,state)
document = xml.dom.minidom.parse(file)
divs = document.getElementsByTagName('div')

i = 0
id_num =[]
for div in divs:
    if div.getAttribute('id') == Ids[3]:
        id_num.append(i)
    if div.getAttribute('id') == Ids[0]:
        id_num.append(i)
    if div.getAttribute('id') == Ids[1]:
        id_num.append(i)
    if div.getAttribute('id') == Ids[2]:
        id_num.append(i)
    if div.getAttribute('id') == Ids[4]:
        id_num.append(i)
    
    i+=1
#searches for data
k = 0
for div in divs[id_num[4]].getElementsByTagName('div'):
    for grand_div in div.childNodes:
        for node in grand_div.childNodes:
            k+=1
            if k == 7:
                date =node.nodeValue
date= date[12:]
#extract the city name in the document
for div in divs[id_num[0]].getElementsByTagName('div'):
    for grand_div in div.getElementsByTagName('div'):
        for node in grand_div.childNodes:
            if node.nodeName == 'h2':
                city = node.childNodes[0].nodeValue
comma_pos=0
for char in city:
    if char == ',':
        city = city[:comma_pos]
    comma_pos+=1
#extract the current 
current_data=[]
for p in divs[id_num[1]].getElementsByTagName('p'):
    for node in p.childNodes:
        if node.nodeType == node.TEXT_NODE:
            current_data.append(node.nodeValue)
# print(current_data,len(current_data))

extend_summary = {}
for child_div in divs[id_num[3]].getElementsByTagName('div'):
    for grand_div in child_div.childNodes:
        for node in grand_div.childNodes:
            if node.nodeName == 'b':
                str = (node.childNodes[0].nodeValue)
            if node.nodeType == node.TEXT_NODE:
                if node.nodeValue in extend_summary:
                    continue
                extend_summary[str]=node.nodeValue

summary_data =[] ## contain the info of day day or night short_desc and temp respectively
for p in divs[id_num[2]].getElementsByTagName('p'):
    str = ''
    desc = ''
    for node in p.childNodes:
        if node.nodeType == node.ELEMENT_NODE and node.nodeName == 'img':
            desc = node.getAttribute('alt')
        if node.nodeType == node.TEXT_NODE:
            if node.nodeValue == 'Night':
                str =str +' '+node.nodeValue
            else:
                str = str +node.nodeValue
    if len(desc) != 0:
        summary_data.append(desc)
    if len(str) != 0:
        summary_data.append(str)
sum_dict={}
list=[]
for items in summary_data:
    if items in extend_summary:
        list=[]
        if 'Night'or 'night'in items:
            list.append(1)
        else:
            list.append(0)
        sum_dict[items]=list
    else:
        list.append(items)

##########
#Mini sql imporation starts
# ipaddy
# state_name
# city_name
# date
# day_or_night
# temp 
# short desc
# long desc 


def insert(cursor,day,d_n,temp,short_desc,long_desc):
    query = 'INSERT INTO '+state+'_T(ipaddy, state_name,city_name,date, day_or_night, temp, short_desc, long_desc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,(ipaddy,state,city,day,d_n,temp,short_desc,long_desc))


def update(cursor,ipaddy,day,temp,short_desc,long_desc):
    query = 'UPDATE '+state+'_T SET temp=%s,short_desc=%s,long_desc=%s WHERE ipaddy = \'%s\' AND date = \'%s\''
    cursor.execute(query, (temp,short_desc,long_desc,ipaddy,day))

def make_table(cursor):
    table_name = state + '_T'
    print(state,table_name)
    check_query = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s'
    cursor.execute(check_query, ('weather', table_name))
    count = cursor.fetchone()[0]
    if count > 0:
        return False
    else:
        create_query = f"CREATE TABLE {table_name} (ipaddy VARCHAR(16) not null, state_name CHAR(2) NOT NULL, city_name VARCHAR(100) not null, date varchar(50), day_or_night BOOLEAN NOT NULL, temp VARCHAR(50), short_desc TINYTEXT, long_desc LONGTEXT);"
        cursor.execute(create_query)
        return True
try:
    cnx = mysql.connector.connect(host='localhost', user='root', password='', database='weather')
    cursor = cnx.cursor()
    cnx.commit()
    if not make_table(cursor):
        for items in sum_dict:
            query = f"SELECT * FROM {state}_T WHERE date= '{items}'"
            cursor.execute(query)
            if cursor.fetchall:
                print(items)
                update(cursor,ipaddy,items,sum_dict[items][3],sum_dict[items][2],sum_dict[items][1])
            cursor.commit()

    for items in sum_dict:
        new_temp =''
        for chars in sum_dict[items][3]:
            if chars.isdigit():
                new_temp+=chars
        long_text =sum_dict[items][1]
        insert(cursor,items,sum_dict[items][0],new_temp,sum_dict[items][2],long_text)

    cnx.commit()

    cursor.close()
except mysql.connector.Error as err:
    print(err)
finally:
    try:
        cnx
    except NameError:
        pass
    else:
        cnx.close()
