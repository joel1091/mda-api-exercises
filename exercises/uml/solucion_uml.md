
** Ejercicio 1

```bash
Inicio --> Validar datos ingresados --> [alt]
  [Datos válidos] --> Crear cuenta --> Mostrar mensaje de éxito --> Fin
  [Datos no válidos] --> Mostrar mensaje de error --> Fin
```


** Ejercicio 2
```bash
Inicio --> Usuario ingresa criterio de búsqueda --> Consultar base de datos --> [alt]
  [Producto encontrado] --> Mostrar información del producto --> Fin
  [Producto no encontrado] --> Mostrar mensaje de error --> Fin
```

** Ejercicio 3

```bash
Inicio --> Validar carrito --> [alt]
  [Carrito válido] --> Validar información del usuario --> [alt]
    [Información válida] --> Procesar pago --> [alt]
      [Pago exitoso] --> Confirmar pedido --> Fin
      [Pago fallido] --> Mostrar error de pago --> Fin
    [Información inválida] --> Mostrar mensaje de error (datos incorrectos) --> Fin
  [Carrito inválido] --> Mostrar error (carrito vacío o no disponible) --> Fin
```

** Ejercicio 4

```bash
Inicio --> Preparar notificación --> [par]
  --> Enviar por correo electrónico
  --> Enviar por SMS
  --> Enviar por notificación push
[Fin de par] --> [alt]
  [Todos los envíos exitosos] --> Mostrar confirmación al usuario --> Fin
  [Fallos en algún canal] --> Registrar errores --> Notificar problemas al usuario --> Fin
```