import cx_Oracle

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe') # if needed, place an 'r' before any parameter in order to address special characters such as ''.
conn = cx_Oracle.connect(user='project', password='project', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as ''. For example, if your user name contains '', you'll need to place 'r' before the user name: user=r'User Name'

cur = conn.cursor()
cur.execute("select * from dept")
print(cur.description)
# res = cur.fetchone()
# print(res)
# for deptno, dname, loc in res:
#     print("Department number: ", deptno)
#     print("Department name: ", dname)
    
conn.close()