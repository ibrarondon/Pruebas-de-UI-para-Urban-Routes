# Pruebas automatizadas de UI para la aplicación web de Urban Routes

Urban Routes es una proveedora de movilidad con diversas opciones de transporte. Desarrollé pruebas automatizadas de UI para las características al solicitar un taxi de categoría "Comfort". 

### Descripción:

- El proyecto se desarrolló con Selenium WebDriver y POM, haciendo uso de Python como lenguaje de programación.
- Se crearon 9 pruebas para las funciones de: configuración de ruta, selección de tarifa "Comfort", agregar número de teléfono, agregar tarjeta de crédito, escribir un mensaje para el taxista, pedir manta y pañuelos, pedir 2 helados, verificación de solicitud de taxi y verificación de información del taxista.
- Para la prueba de información del conductor se llenaron todos los campos necesarios para la solicitud.
- El archivo data.py contiene la información que se envía a la solicitud: ruta, número de teléfono, datos de la tarjeta, mensaje al conductor y URL del servidor de Urban Routes.
- Se modificó el mensaje para el conductor a una longitud menor a 24 caracteres, que es la máxima adecuada para ese campo.


### Requisitos:
- Necesitas tener instalados el paquete pytest para ejecutar las pruebas.
- Para instalar el paquete usa el comando pip pytest
- Debes contar con los archivos data.py y main.py
- Antes de ejecutar las pruebas asegurarse de tener las configuraciones de pytest adecuadas.
- Ejecuta todas las pruebas con el comando pytest.
- Actualizar la URL del servidor antes de ejecutar alguna prueba.
- La URL del servidor debe tener el parámetro ?lng=es porque hay búsquedas y assert que utilizan palabras en español.
- Revisar los localizadores al hacerse actualizaciones 

### Herramientas utilizadas:
- Pycharm
- Selenium
- Postman
- Jira
- POM

### Instrucciones:

- Realizar una copia local del repositorio GitHub.
- Instalar el paquete pytest.
- Actualizar la URL del servidor contenida en la variable urban_routes_url del archivo data.py.
- Para realizar las pruebas de manera grupal: hacer click en el botón Run de la clase "TestUrbanRoutes" o hacer click en Run con la opción current file seleccionada.
- Para realizar pruebas individuales: desplegar la clase "TestUrbanRoutes" y hacer click en Run en la prueba de interés.

### Análisis de resultados y conclusiones

Probé las características de la interfaz de usuario para pedir un taxi de categoría "Comfort", haciendo uso de las APIs y pruebas automatizadas. Al realizar las pruebas encontré que existen discrepancias en los textos respecto a los requisitos, no se muestra el vehículo del viaje en el mapa, no se muestra adecuadamente la información del taxi reservado, las funcionalidades al borrar campos del formulario tienen comportamientos distintos a los requeridos, hay campos de entrada que no tienen el formato de dato adecuado, así como límites mínimo y máximos incorrectos. Se recomienda al equipo de desarrollo corregir con prioridad los errores reportados relacionados a métodos de pago y usabilidad del usuario, apegándose a las condiciones de diseño, limitando correctamente los formatos en los parámetros así como sus valores mínimos y máximos.

[Reporte de bugs en JIRA de UI para Urban Routes](https://drive.google.com/uc?id=1rqcf9nlp56UQTTyngQdeGd5wgGk_hPi-&export=download) 

*Desarrollado por: Ibrahim Rondón - c13 QA Engineer, TripleTen*
