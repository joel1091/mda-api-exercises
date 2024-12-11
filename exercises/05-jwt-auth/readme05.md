# Ejercicio 5: Autenticación con JSON Web Tokens (JWT)

## Objetivo
Implementar autenticación utilizando JSON Web Tokens (JWT) en una API REST desarrollada con Python y Flask.

## Descripción
En este ejercicio, ampliarás la API desarrollada en los ejercicios anteriores para incluir autenticación mediante JWT. Implementarás endpoints para que los usuarios puedan iniciar sesión y obtener un token JWT, el cual deberán incluir en las solicitudes a rutas protegidas para acceder a recursos seguros.

## Requisitos
1. **Instalación de Dependencias Adicionales:**
   - Instala las bibliotecas necesarias para manejar JWT (`Flask-JWT-Extended`).
   
2. **Estructura de la API:**
   - Crea una ruta para que los usuarios inicien sesión (`POST /login`) y obtengan un token JWT.
   - Crea una ruta protegida (`GET /perfil`) que solo pueda ser accedida con un token JWT válido.

3. **Implementación de JWT:**
   - Configura `Flask-JWT-Extended` en tu aplicación.
   - Al autenticar a un usuario en el endpoint de login, genera y retorna un token JWT.
   - Protege las rutas sensibles utilizando decoradores que verifiquen la presencia y validez del token JWT.

4. **Pruebas:**
   - Utiliza herramientas como Postman o `curl` para probar el flujo de autenticación y el acceso a rutas protegidas con y sin un token válido.

## Pasos Sugeridos

1. **Instala Dependencias Adicionales:**
   ```bash
   pip install Flask-JWT-Extended
