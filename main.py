import sys
import telnetlib
from datetime import datetime
import db




now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

conndb = db.DbConnection.dbconn("") 

            
            
def get_system(filename):
    system_details = []

    with open(filename, mode='r', encoding='utf-8') as system_file:
        for a_system in system_file:
            system_details.append(a_system)
    return system_details
 

def res_telnet(sysrem,host,portno,stype):
    try:
        conn = telnetlib.Telnet(host,portno)
        response = sysrem+' : ' +host+' ' + portno +' - Success'
        stat = 'SUCCESS'
    except:
        response = sysrem+' : ' +host+' ' + portno +' - Failed'
        stat = 'FAILED'
    finally:
        print(response)
        sql = "INSERT INTO OSSPRG.CONNECTIVITY_STATUS VALUES ( :SERVER,:SYSTEM,:IP,:PORT,:STATUS,:UPDATED_TIME,:STYPE)"
        with conndb.cursor() as cursor:
            cursor.execute(sql, ['172.25.36.45', sysrem, host, portno, stat, dt_string,stype])
            conndb.commit()
        
 
sqldel = "DELETE FROM OSSPRG.CONNECTIVITY_STATUS WHERE SERVER = '172.25.36.45'"
with conndb.cursor() as cursor:
    cursor.execute(sqldel)
    conndb.commit()
            
result = get_system('/opt/AvailabilityCheck/files/connectivitydetails.txt')    

for ret in result:
    sysrem =str(ret.split()[0])
    host =str(ret.split()[1])
    portno = str(ret.split()[2])
    
    res_telnet(sysrem,host,portno,'CONNECTIVITY')
    
resultapi = get_system('/opt/AvailabilityCheck/files/runningapi.txt')    

for ret in resultapi:
    sysrem =str(ret.split()[0])
    host =str(ret.split()[1])
    portno = str(ret.split()[2])
    
    res_telnet(sysrem,host,portno,'API')