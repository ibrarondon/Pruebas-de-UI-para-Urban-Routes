# Pruebas automatizadas de UI para la aplicación web de Urban Routes
Pruebas automatizadas de UI para las características de Urban Routes al solicitar un taxi de categoría "Comfort". 

### Requisitos:
- Necesitas tener instalados el paquete pytest para ejecutar las pruebas.
- Para instalar el paquete usa el comando pip pytest
- Debes contar con los archivos data.py y main.py
- Antes de ejecutar las pruebas asegurarse de tener las configuraciones de pytest adecuadas.
- Ejecuta todas las pruebas con el comando pytest.
- Actualizar la URL del servidor antes de ejecutar alguna prueba.
- La URL del servidor debe tener el parámetro ?lng=es porque hay búsquedas y assert que utilizan palabras en español.
- Revisar los localizadores al hacerse actualizaciones 

### Descripción:

- El proyecto se desarrolló con Selenium WebDriver y POM, haciendo uso de Python como lenguaje de programación.
- Se crearon 9 pruebas para las funciones de: configuración de ruta, selección de tarifa "Comfort", agregar número de teléfono, agregar tarjeta de crédito, escribir un mensaje para el taxista, pedir manta y pañuelos, pedir 2 helados, verificación de solicitud de taxi y verificación de información del taxista.
- Para la prueba de información del conductor se llenaron todos los campos necesarios para la solicitud.
- El archivo data.py contiene la información que se envía a la solicitud: ruta, número de teléfono, datos de la tarjeta, mensaje al conductor y URL del servidor de Urban Routes.
- Se modificó el mensaje para el conductor a una longitud menor a 24 caracteres, que es la máxima adecuada para ese campo.

### Instrucciones:

- Realizar una copia local del repositorio GitHub.
- Instalar el paquete pytest.
- Actualizar la URL del servidor contenida en la variable urban_routes_url del archivo data.py.
- Para realizar las pruebas de manera grupal: hacer click en el botón Run de la clase "TestUrbanRoutes" o hacer click en Run con la opción current file seleccionada.
- Para realizar pruebas individuales: desplegar la clase "TestUrbanRoutes" y hacer click en Run en la prueba de interés.


*Desarrollado por: Ibrahim Rondón - c13 QA Engineer, TripleTen*