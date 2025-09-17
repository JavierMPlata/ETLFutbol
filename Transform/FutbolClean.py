import pandas as pd
import numpy as np

class futbolClean:
    def __init__(self, dataframe):
        """
        Inicializa la clase de limpieza con el DataFrame de resultados de partidos de fútbol

        Args:
            dataframe (pd.DataFrame): DataFrame con los datos de partidos de fútbol (fecha, equipos, marcadores, etc.)
        """
        self.data = dataframe.copy()
        self.original_data = dataframe.copy()
    
    def check_missing_values(self):
        """
        Verifica y reporta valores nulos y NA en el dataset
        
        Returns:
            dict: Diccionario con información sobre valores faltantes
        """
        missing_info = {
            'total_rows': len(self.data),
            'null_values': self.data.isnull().sum().to_dict(),
            'na_values': self.data.isna().sum().to_dict(),
            'rows_with_missing': len(self.data[self.data.isnull().any(axis=1)]),
            'missing_data_percentage': (self.data.isnull().sum() / len(self.data) * 100).to_dict()
        }
        
        return missing_info
    
    def display_missing_data_report(self):
        """
        Muestra un reporte detallado de los datos faltantes
        """
        missing_info = self.check_missing_values()
        
        print("=" * 50)
        print("REPORTE DE DATOS FALTANTES - PARTIDOS DE FÚTBOL")
        print("=" * 50)
        print(f"Total de filas: {missing_info['total_rows']}")
        print(f"Filas con datos faltantes: {missing_info['rows_with_missing']}")
        print()
        
        print("Valores nulos por columna:")
        print("-" * 30)
        for col, count in missing_info['null_values'].items():
            percentage = missing_info['missing_data_percentage'][col]
            if count > 0:
                print(f"{col}: {count} ({percentage:.2f}%)")
            else:
                print(f"{col}: {count}")
        
        print("\nPrimeras filas con valores faltantes:")
        print("-" * 30)
        missing_rows = self.data[self.data.isnull().any(axis=1)]
        if len(missing_rows) > 0:
            # Mostrar columnas más relevantes para este dataset de fútbol
            key_columns = ['date', 'home_team', 'away_team', 'home_score', 'away_score', 'tournament', 'city', 'country']
            available_columns = [col for col in key_columns if col in missing_rows.columns]
            print(missing_rows[available_columns].head(10))
        else:
            print("No hay filas con valores faltantes")
    
    def clean_missing_values(self):
        """
        Limpia los valores faltantes reemplazándolos con valores apropiados
        No elimina filas, solo reemplaza valores
        """
        print("Iniciando limpieza de datos para partidos de fútbol...")
        
        # Limpiar marcadores (scores)
        score_columns = ['home_score', 'away_score']
        for col in score_columns:
            if col in self.data.columns and self.data[col].isnull().any():
                print(f"Limpiando valores nulos en '{col}'...")
                # Para marcadores, usar 0 como valor por defecto
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce').fillna(0)
                print(f"Reemplazados valores nulos en {col} con 0")
        
        # Limpiar columna neutral (boolean)
        if 'neutral' in self.data.columns and self.data['neutral'].isnull().any():
            print("Limpiando valores nulos en 'neutral'...")
            # Para neutral, usar FALSE como valor por defecto (la mayoría de partidos no son en campo neutral)
            self.data['neutral'] = self.data['neutral'].fillna('FALSE')
            print("Reemplazados valores nulos en 'neutral' con 'FALSE'")
        
        # Limpiar columnas específicas con moda
        self._fill_with_mode(['away_team', 'home_team', 'tournament', 'country', 'city'])
        
        # Verificar si hay otros tipos de valores que podrían considerarse como faltantes
        self._clean_string_nulls()
        
        print("Limpieza completada!")
    
    def _fill_with_mode(self, columns):
        """
        Llena los valores nulos de las columnas especificadas con la moda (valor más frecuente)
        
        Args:
            columns (list): Lista de nombres de columnas a procesar
        """
        for col in columns:
            if col in self.data.columns:
                # Contar valores nulos incluyendo diferentes representaciones
                null_mask = (self.data[col].isnull() | 
                           self.data[col].isna() | 
                           self.data[col].isin(['', 'null', 'NULL', 'Null', 'nan', 'NaN', 'NAN', 'n/a', 'N/A', 'None', 'NONE']))
                
                if null_mask.any():
                    print(f"Procesando columna '{col}'...")
                    
                    # Obtener valores válidos (no nulos)
                    valid_values = self.data[col][~null_mask]
                    
                    if len(valid_values) > 0:
                        # Calcular la moda (valor más frecuente)
                        mode_series = valid_values.mode()
                        if len(mode_series) > 0:
                            mode_value = mode_series[0]
                            
                            # Reemplazar valores nulos con la moda
                            self.data.loc[null_mask, col] = mode_value
                            null_count = null_mask.sum()
                            print(f"  - Reemplazados {null_count} valores nulos en '{col}' con moda: '{mode_value}'")
                        else:
                            print(f"  - No se pudo calcular la moda para '{col}' (sin valores válidos)")
                    else:
                        print(f"  - No hay valores válidos en '{col}' para calcular la moda")
                else:
                    print(f"  - No hay valores nulos en '{col}'")
    
    def _clean_string_nulls(self):
        """
        Limpia valores que pueden estar representados como strings pero son efectivamente nulos
        Usa la moda (valor más frecuente) para reemplazar valores nulos en columnas de texto
        """
        null_representations = ['null', 'NULL', 'Null', 'nan', 'NaN', 'NAN', 'n/a', 'N/A', '', 'None', 'NONE']
        
        for col in self.data.columns:
            if self.data[col].dtype == 'object':  # Solo para columnas de texto
                # Reemplazar representaciones de null con valores apropiados
                mask = self.data[col].isin(null_representations)
                if mask.any():
                    # Calcular la moda (valor más frecuente) excluyendo los valores nulos
                    valid_values = self.data[col][~mask]
                    if len(valid_values) > 0:
                        mode_value = valid_values.mode()[0] if len(valid_values.mode()) > 0 else None
                    else:
                        mode_value = None
                    
                    # Si no hay moda válida, usar valores por defecto específicos por columna
                    if mode_value is None:
                        if col in ['home_team', 'away_team']:
                            mode_value = 'Unknown Team'
                        elif col == 'tournament':
                            mode_value = 'Friendly'
                        elif col in ['city', 'country']:
                            mode_value = 'Unknown'
                        elif col == 'neutral':
                            mode_value = 'FALSE'
                        else:
                            mode_value = 'Unknown'
                    
                    # Reemplazar valores nulos con la moda
                    self.data.loc[mask, col] = mode_value
                    print(f"Reemplazados {mask.sum()} valores nulos en {col} con moda: '{mode_value}'")
    
    def convert_data_types(self):
        """
        Convierte los tipos de datos a formatos más apropiados para el dataset de partidos de fútbol
        """
        # Convertir columnas numéricas (marcadores)
        numeric_columns = {
            'home_score': int,
            'away_score': int
        }
        
        for col, dtype in numeric_columns.items():
            if col in self.data.columns:
                try:
                    self.data[col] = pd.to_numeric(self.data[col], errors='coerce').fillna(0).astype(int)
                    print(f"Columna {col} convertida a tipo {dtype.__name__}")
                except Exception as e:
                    print(f"No se pudo convertir {col} a {dtype.__name__}: {e}")
        
        # Convertir fechas
        if 'date' in self.data.columns:
            try:
                # Parsear fechas en formato YYYY-MM-DD
                self.data['date'] = pd.to_datetime(self.data['date'], errors='coerce')
                print("Columna 'date' convertida a tipo datetime")
            except Exception as e:
                print(f"No se pudo convertir 'date' a datetime: {e}")
        
        # Convertir neutral a booleano
        if 'neutral' in self.data.columns:
            try:
                # Convertir TRUE/FALSE string a boolean
                self.data['neutral'] = self.data['neutral'].map({'TRUE': True, 'FALSE': False, True: True, False: False})
                print("Columna 'neutral' convertida a tipo boolean")
            except Exception as e:
                print(f"No se pudo convertir 'neutral' a boolean: {e}")
        
        # Limpiar y estandarizar columnas de texto
        text_columns = ['home_team', 'away_team', 'tournament', 'city', 'country']
        
        for col in text_columns:
            if col in self.data.columns:
                try:
                    # Limpiar caracteres especiales y estandarizar
                    self.data[col] = self.data[col].astype(str).str.strip()
                    # Reemplazar caracteres especiales comunes
                    self.data[col] = self.data[col].str.replace('Ã©', 'é', regex=False)
                    self.data[col] = self.data[col].str.replace('Ã¤', 'ä', regex=False)
                    self.data[col] = self.data[col].str.replace('Ã¶', 'ö', regex=False)
                    print(f"Columna {col} limpiada y estandarizada")
                except Exception as e:
                    print(f"Error al limpiar columna {col}: {e}")
    
    def get_cleaned_data(self):
        """
        Retorna el DataFrame limpio
        
        Returns:
            pd.DataFrame: DataFrame con los datos limpios
        """
        return self.data
    
    def get_cleaning_summary(self):
        """
        Retorna un resumen de las operaciones de limpieza realizadas
        
        Returns:
            dict: Resumen de la limpieza
        """
        original_missing = self.original_data.isnull().sum().sum()
        current_missing = self.data.isnull().sum().sum()
        
        summary = {
            'original_missing_values': original_missing,
            'current_missing_values': current_missing,
            'values_cleaned': original_missing - current_missing,
            'original_shape': self.original_data.shape,
            'current_shape': self.data.shape,
            'rows_preserved': self.original_data.shape[0] == self.data.shape[0],
            'columns_in_dataset': list(self.data.columns),
            'data_types': dict(self.data.dtypes)
        }
        
        return summary
    
    def full_cleaning_process(self):
        """
        Ejecuta el proceso completo de limpieza:
        1. Reporta datos faltantes
        2. Limpia valores faltantes
        3. Convierte tipos de datos
        4. Muestra resumen final
        
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        print("INICIANDO PROCESO COMPLETO DE LIMPIEZA")
        print("=" * 50)
        
        # 1. Mostrar reporte inicial
        self.display_missing_data_report()
        
        # 2. Limpiar valores faltantes
        print("\n" + "=" * 50)
        self.clean_missing_values()
        
        # 3. Convertir tipos de datos
        print("\n" + "=" * 50)
        print("Convirtiendo tipos de datos...")
        self.convert_data_types()
        
        # 4. Mostrar resumen final
        print("\n" + "=" * 50)
        print("RESUMEN FINAL DE LIMPIEZA")
        print("=" * 50)
        summary = self.get_cleaning_summary()
        print(f"Valores faltantes originales: {summary['original_missing_values']}")
        print(f"Valores faltantes actuales: {summary['current_missing_values']}")
        print(f"Valores limpiados: {summary['values_cleaned']}")
        print(f"Filas preservadas: {summary['rows_preserved']}")
        print(f"Shape original: {summary['original_shape']}")
        print(f"Shape actual: {summary['current_shape']}")
        
        # Verificación final
        final_missing = self.check_missing_values()
        print(f"\nVerificación final - Total valores nulos: {sum(final_missing['null_values'].values())}")
        
        return self.data
    
    def export_cleaned_data(self, file_path):
        """
        Exporta los datos limpios a un archivo CSV
        
        Args:
            file_path (str): Ruta donde guardar el archivo CSV limpio
        """
        try:
            self.data.to_csv(file_path, index=False)
            print(f"Datos limpios exportados exitosamente a: {file_path}")
        except Exception as e:
            print(f"Error al exportar los datos: {e}")