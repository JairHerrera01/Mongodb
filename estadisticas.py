from pymongo import MongoClient
import matplotlib.pyplot as plt
import re

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bases_datos"]
coleccion = db["Datos"]

# Recuperar los datos de la colección
datos = list(coleccion.find({}))

# Mostrar una muestra de los datos para verificar
for i, dato in enumerate(datos[:5]):  # Mostrar los primeros 5 documentos para revisar
    print(f"Documento {i + 1}: {dato}")

# Limitar el número de datos para la gráfica
datos_seleccionados = datos[:20]

# Extraer los datos para graficar, asegurando que existan los campos requeridos
nombres = [dato.get("NOMBRE CUENTA", "Sin nombre") for dato in datos_seleccionados]

valores = []
for dato in datos_seleccionados:
    valor = dato.get("VALOR EN PESOS", "0")  # Asignar "0" si no existe el campo
    if isinstance(valor, str):
        # Eliminar el símbolo de moneda y las comas, luego convertir a número
        valor_numero = re.sub(r"[^\d]", "", valor)  # Remueve todo excepto dígitos
        valores.append(int(valor_numero) if valor_numero else 0)
    elif isinstance(valor, (int, float)):  # Si es número, usarlo tal cual
        valores.append(valor)
    else:  # Otros casos, asignar 0 como valor predeterminado
        valores.append(0)

# Cerrar la conexión
client.close()

# Mostrar los nombres y valores extraídos para verificar
print("Nombres:", nombres)
print("Valores:", valores)

# Crear el gráfico de barras
plt.figure(figsize=(12, 6))
plt.bar(nombres, valores, color="skyblue")
plt.xlabel("Nombres")
plt.ylabel("Valores")
plt.title("Gráfico de valores desde MongoDB")

# Ajustar las etiquetas del eje x
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()

# Mostrar el gráfico
plt.show()
