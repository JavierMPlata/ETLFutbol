class Config:
    """
    Clase de configuración para rutas y parámetros del ETL.
    """
    INPUT_PATH = r'Files\Futbol.csv'
    SQLITE_DB_PATH = r'Files\etl_data.db'
    SQLITE_TABLE = 'futbol_data_clean'
