# Pruebas para comprobar la funcionalidad de Urban Routes
Pruebas automatizadas para las características de Urban Routes al solicitar un taxi de categoría "Comfort" 

### Requisitos:
- Necesitas tener instalados el paquete pytest para ejecutar las pruebas.
- Para instalar el paquete usa el comando pip pytest
- Debes contar con los archivos data.py y main.py
- Antes de ejecutar las pruebas asegurarse de tener las configuraciones de pytest adecuadas.
- Ejecuta todas las pruebas con el comando pytest.
- Actualizar la URL del servidor antes de ejecutar alguna prueba.
- La URL del servidor debe tener el parámetro ?lng=es porque hay búsquedas y assert que utilizan palabras en español.

### Descripción:
- Se crearon 9 pruebas para las funciones de: configuración de ruta, selección de tarifa "Comfort", agregar número de teléfono, agregar tarjeta de crédito, escribir un mensaje para el taxista, pedir manta y pañuelos, pedir 2 helados, verificación de solicitud de taxi y verificación de información del taxista.
- Para la prueba de información del taxi se llenaron los campos de ruta, número de teléfono y tarjeta.
- El archivo data.py contiene la información que se envía a la solicitud: ruta, número de teléfono, datos de la tarjeta, mensaje al conductor y URL del servidor de Urban Routes.