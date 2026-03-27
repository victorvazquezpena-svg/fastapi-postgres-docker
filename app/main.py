from fastapi import FastAPI
import psycopg2

app = FastAPI()

def obtener_conexion():
    return psycopg2.connect(
        host="host.docker.internal",
        database="liga",
        user="victor",
        password="2002",
        port="5432"
    )

@app.get("/")
def inicio():
    return {"mensaje": "API FastAPI conectada al entorno de base de datos"}

@app.get("/clasificacion")
def clasificacion():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        consulta = """
        SELECT e.nombre, c.puntos
        FROM equipos e
        JOIN clasificacion c ON e.id = c.equipo_id
        ORDER BY c.puntos DESC;
        """

        cursor.execute(consulta)
        resultados = cursor.fetchall()

        datos = []
        for fila in resultados:
            datos.append({
                "equipo": fila[0],
                "puntos": fila[1]
            })

        cursor.close()
        conexion.close()

        return datos

    except Exception as e:
        return {"error": str(e)}
