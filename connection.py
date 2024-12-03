import pyodbc

def obtener_conexion():
    return pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=servidor-reservas-pedidos.database.windows.net;"
        "Database=ReservasPedidosDB;"
        "Uid=AdminReservas;"
        "Pwd=infraestructura_Anahuac7;"
    )
