# ColombiaData – Sistema Web de Consulta y Análisis de Datos Abiertos de Colombia

**Proyecto integrador – Desarrollo de Aplicaciones con Acceso a Datos**

**Institución:** Corporación Universitaria Americana

## 1. Descripción del proyecto

ColombiaData es una aplicación web desarrollada en Python utilizando Flask, SQL Server y el patrón de arquitectura MVC (Modelo, Vista y Controlador).

Su finalidad es consultar información pública de los municipios y departamentos de Colombia mediante una API de datos.gov.co, almacenar los registros en una base de datos y permitir que los usuarios consulten esta información desde una interfaz web.

El sistema también muestra estadísticas generales y evita almacenar registros duplicados.

## 2. Objetivo general

Desarrollar una aplicación web que permita consumir información de una API pública, almacenarla en SQL Server y consultarla mediante una interfaz web, aplicando el patrón MVC.

## 3. Objetivos específicos

- Consultar información pública mediante una API REST.
- Establecer una conexión entre Python y SQL Server.
- Almacenar los registros obtenidos de la API.
- Evitar la duplicación de información en la base de datos.
- Implementar búsquedas por municipio o departamento.
- Mostrar estadísticas generales de los registros almacenados.
- Desarrollar una interfaz web organizada y fácil de utilizar.

## 4. Dataset utilizado

**Nombre:** DIVIPOLA – Códigos de municipios de Colombia.

**Fuente:** Portal de Datos Abiertos de Colombia.

**Identificador:** gdxc-w37w

**Ficha del dataset:** https://www.datos.gov.co/d/gdxc-w37w

**Endpoint de la API:**

`https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=1200`

Este conjunto de datos contiene información sobre los municipios y departamentos de Colombia, incluyendo sus códigos y clasificaciones territoriales.

## 5. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje principal de programación |
| Flask | Framework para desarrollar la aplicación web |
| SQL Server | Almacenamiento de información |
| SSMS | Administración de la base de datos |
| pyodbc | Conexión entre Python y SQL Server |
| HTML | Estructura de la página web |
| CSS | Diseño visual de la aplicación |
| API REST | Obtención de información externa |
| Visual Studio Code | Entorno de desarrollo |

## 6. Arquitectura MVC

El proyecto utiliza el patrón Modelo, Vista y Controlador para organizar sus componentes.

**Modelo – `models/datos_model.py`**

Se encarga de establecer la conexión con SQL Server, guardar los registros, consultar información y obtener estadísticas.

**Vista – `templates/index.html` y `static/estilos.css`**

Se encarga de mostrar la información mediante una interfaz web moderna, incluyendo el buscador, las tablas y las tarjetas de estadísticas.

**Controlador – `app.py`**

Recibe las solicitudes de los usuarios, coordina las consultas y conecta el modelo con las vistas.

**Cliente de API – `api/api_client.py`**

Se encarga de obtener los datos desde el servicio externo de datos.gov.co.

## 7. Base de datos

La base de datos utilizada se llama `DatosAbiertosDB`.

La tabla principal es `RegistrosAPI`, que almacena la información obtenida de la API.

| Campo | Descripción |
|---|---|
| id | Identificador interno |
| id_api | Código del registro en la API |
| municipio | Nombre del municipio |
| categoria | Departamento |
| valor | Clasificación territorial |
| fecha_registro | Fecha del registro, si está disponible |
| json_original | Información original recibida de la API |
| fecha_captura | Fecha de almacenamiento |

El campo `id_api` tiene una restricción `UNIQUE` para evitar códigos duplicados.

## 8. Funcionalidades principales

**Consulta de API:** permite obtener información pública sobre los municipios de Colombia.

**Almacenamiento:** guarda los registros obtenidos en SQL Server.

**Control de duplicados:** verifica si un registro ya existe antes de insertarlo.

**Buscador:** permite encontrar registros mediante el nombre de un municipio o departamento.

**Resumen estadístico:** muestra la cantidad de registros almacenados, nombres de municipios distintos y departamentos o territorios.

**Interfaz web:** presenta los resultados mediante el diseño ColombiaData.

## 9. Resultados obtenidos

Durante las pruebas realizadas, el sistema obtuvo los siguientes resultados:

| Indicador | Resultado |
|---|---:|
| Registros almacenados | 1.122 |
| Nombres de municipios distintos | 1.037 |
| Departamentos y territorios distintos | 33 |

También se comprobó que, al realizar nuevamente la sincronización con los mismos datos, el sistema obtuvo:

- Registros recibidos: 1.122.
- Nuevos registros guardados: 0.
- Registros omitidos: 1.122.

Esto demuestra que el sistema reconoce los registros existentes y evita insertarlos nuevamente.

Se realizaron búsquedas por departamento, incluyendo ATLÁNTICO, y se visualizaron correctamente los resultados.

## 10. Requisitos para ejecutar el proyecto

- Python compatible con las dependencias del proyecto.
- SQL Server.
- SQL Server Management Studio.
- ODBC Driver 18 for SQL Server.
- Visual Studio Code o un editor de código.
- Conexión a internet para consultar la API.

## 11. Instalación y ejecución

**Paso 1.** Abrir la carpeta del proyecto en Visual Studio Code.

**Paso 2.** Crear un entorno virtual, si todavía no existe:

```powershell
python -m venv .venv
```

**Paso 3.** Activar el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

**Paso 4.** Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

**Paso 5.** Ejecutar el script `database/crear_bd.sql` en SQL Server Management Studio para preparar la base de datos.

**Paso 6.** Copiar `.env.example` como `.env` y configurar los datos de conexión a SQL Server.

**Paso 7.** Ejecutar la aplicación:

```powershell
python app.py
```

**Paso 8.** Abrir en el navegador:

http://127.0.0.1:5000

**Paso 9.** Presionar el botón **Consultar API y actualizar datos** para sincronizar la información.

## 12. Pruebas realizadas

Se realizaron las siguientes pruebas:

1. Conexión entre Python y SQL Server.
2. Consulta de información mediante la API REST.
3. Almacenamiento de registros en la base de datos.
4. Visualización de registros en la interfaz web.
5. Búsqueda de información por departamento.
6. Verificación de registros duplicados.
7. Segunda sincronización para comprobar que no se insertan registros existentes.

Las pruebas realizadas mostraron resultados satisfactorios.

## 13. Evidencias

Las capturas del funcionamiento del proyecto se organizarán en la carpeta `evidencias/`.

Se incluirán:

- Página principal de ColombiaData.
- Resultados de la sincronización.
- Búsqueda filtrada por departamento.
- Registros almacenados en SQL Server.
- Consulta SQL para comprobar los duplicados.
- Ejemplo de la respuesta JSON de la API.

## 14. Integrantes y responsabilidades
Jesus David Suarez Melendres
Juan David Alvarez  Fontalvo


## 15. Conclusiones

Con el desarrollo de ColombiaData se logró integrar una API pública con una base de datos SQL Server y una aplicación web creada con Flask.

El proyecto permitió aplicar conocimientos sobre conexión a bases de datos, consultas SQL, consumo de servicios REST y arquitectura MVC.

Además, se implementaron funciones para buscar información, mostrar estadísticas y evitar registros duplicados.

Esta experiencia permitió comprender cómo diferentes tecnologías pueden trabajar juntas para desarrollar una aplicación que consulta, almacena y presenta información real.