import pyodbc
server = 'localhost'
bd = 'prueba12'
user = 'user_prueba12'
password = 'fer12345'

try:
    conexion = pyodbc.connect('DRIVER={SQL Server}; SERVER=' +
                              server + ';DATABASE=' + bd + ';UID=' + user+';PWD=' + password)
    # print('conexion exitosa')
except:
    print('Error al intentar conectarse')
