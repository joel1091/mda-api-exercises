```bash

openapi: 3.0.0
info:
  title: API de Ejemplo
  version: 1.0.0
  description: Una API simple para entender la estructura básica

servers:
  - url: http://api.ejemplo.com/v1
    description: Servidor de producción
  - url: http://staging.ejemplo.com/v1
    description: Servidor de staging

paths:
  /hello:
    get:
      summary: Saludo básico
      description: Retorna un mensaje de saludo
      responses:
        '200':
          description: Saludo exitoso
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "¡Hola, mundo!"
  /books:
    post:
      summary: Crear un libro
      description: Agrega un libro nuevo al sistema
      requestBody:
        description: Datos del libro a crear
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
                  example: "El Principito"
                author:
                  type: string
                  example: "Antoine de Saint-Exupéry"
      responses:
        '201':
          description: Libro creado exitosamente
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Libro creado con éxito"
```