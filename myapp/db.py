import cx_Oracle

def oraconnect():
	dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='xe')
	connection = cx_Oracle.connect(user='project', password='project', dsn=dsn_tns)
	return connection

def exec_query(query):
	connection = oraconnect()
	cursor = connection.cursor()
	cursor.execute(query)
	connection.commit()
	return cursor

def get_table(query):
	# print(query)
	table = exec_query(query).fetchall()
	# print(table)
	return table

def update_table(query):
	exec_query(query)