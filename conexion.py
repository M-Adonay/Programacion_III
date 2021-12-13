import mysql.connector

class conex():
    def __init__(self):
        self.conn = mysql.connector.connect(host = 'localhost', user = 'root', port = '3307', password = '', database = 'book_store')
        self.cursor = self.conn.cursor()
        if self.conn.is_connected():
            print('Conectado')
        else:
            print('No conectado')

    def generar_id(self, tabla):
        print(tabla)
        if tabla == 'libros':
            sql = 'SELECT MAX(idLibro) AS id FROM libros'
        elif tabla == 'tipocuenta':
            sql = 'SELECT MAX(idTipo) AS id FROM tipocuenta'
        elif tabla == 'generos':
            sql = 'SELECT MAX(idGenero) AS id FROM generos'
        elif tabla == 'usuarios':
            sql = 'SELECT MAX(idUsuario) AS id FROM usuarios'
        elif tabla == 'librosprestados':
            sql = 'SELECT MAX(idPrestado) AS id FROM librosprestados'
        resultado = self.ejecutar_mostrar_sql(sql)
        print(resultado)
        if resultado[0] == True:
            id = resultado[1][0]['id']
            if id == None:
                id = 0
            id = int(id) + 1
            return id
        else:
            return False

    def ejecutar_sql(self, sql, valores):
        try:
            print(sql, valores)
            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            print('Se ejecuto la consulta')
            return True
        except Exception as e:
            print(e)
            return False

    def ejecutar_mostrar_sql(self, sql):
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql)
            resultado = cursor.fetchall()
            if len(resultado) == 0:
                return False, resultado
            else:
                return True, resultado
        except Exception as e:
            print(e)
            return False

    def ejecutar_select_datos(self, sql, datos):
        try:
            print(sql, datos)
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, datos)
            resultado = cursor.fetchall()
            if len(resultado) == 0:
                return False, resultado
            else:
                return True, resultado
        except Exception as e:
            print(e)
            return False