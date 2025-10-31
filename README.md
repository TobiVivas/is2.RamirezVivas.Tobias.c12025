TRABAJO: IMPLEMENTACIÓN DE UN SISTEMA DE GESTIÓN DE BIBLIOTECA

Este documento presenta el diseño y desarrollo de un sistema de software para la gestión de una biblioteca, implementado en lenguaje Python. El objetivo principal es demostrar la aplicación práctica de los principios fundamentales de la ingeniería de software, como la arquitectura en capas y los patrones de diseño, para construir un sistema mantenible, escalable y fácil de probar.

El sistema simula las operaciones básicas de una biblioteca, incluyendo el préstamo de libros, el registro de devoluciones y la gestión de socios.

Para lograr una correcta separación de responsabilidades, el sistema se ha estructurado siguiendo una arquitectura de 3 capas (o 3 niveles):

Capa de Presentación: Una interfaz de usuario de terminal (consola) que interactúa con el usuario, captura sus solicitudes y muestra los resultados.

Capa de Lógica de Negocio: El "cerebro" del sistema. Contiene todas las reglas de negocio (ej. "un socio con multas no puede pedir préstamos") y coordina las operaciones.

Capa de Datos: La única capa responsable de la persistencia. Se comunica con una base de datos SQLite para almacenar y recuperar información de libros y socios.

Para resolver problemas comunes de diseño, como el desacoplamiento entre la lógica de negocio y la base de datos, se han implementado varios patrones de diseño:

Patrón Repositorio (Capa de Datos): La clase 'BibliotecaDB' actúa como un repositorio, abstrayendo toda la lógica SQL y permitiendo que la capa de negocio trabaje con objetos sin saber cómo se almacenan.

Patrón Fachada (Capa de Negocio): La clase 'GestorBiblioteca' actúa como una fachada, proporcionando una interfaz simple a la capa de presentación para ejecutar operaciones complejas (como 'realizar_prestamo').

Inyección de Dependencias (DI): En lugar de patrones rígidos como el Singleton, el sistema utiliza la Inyección de Dependencias para "conectar" las capas al inicio, lo que centraliza la configuración y facilita enormemente las pruebas unitarias (testing).

Finalmente, el proyecto incluye un conjunto de pruebas unitarias (usando el módulo 'unittest') que validan la lógica de negocio de forma aislada, demostrando la robustez y correctitud del código.
