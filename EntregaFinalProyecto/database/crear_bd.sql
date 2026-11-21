CREATE DATABASE DatosAbiertosDB;
GO

USE DatosAbiertosDB;
GO

CREATE TABLE RegistrosAPI (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_api NVARCHAR(100) NOT NULL UNIQUE,   -- código DIVIPOLA del municipio (cod_mpio)
    municipio NVARCHAR(150) NULL,           -- nom_mpio
    categoria NVARCHAR(150) NULL,           -- dpto (departamento)
    valor NVARCHAR(100) NULL,               -- tipo_municipio
    fecha_registro NVARCHAR(50) NULL,
    json_original NVARCHAR(MAX) NULL,
    fecha_captura DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);
GO
