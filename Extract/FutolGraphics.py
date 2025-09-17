import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class FutbolGraphics:
    def __init__(self, dataframe):
        """
        Inicializa la clase de gráficas con el DataFrame de datos de fútbol limpios
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos limpios de partidos de fútbol
        """
        self.data = dataframe.copy()
        
        # Configurar estilo de matplotlib
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Crear directorio para guardar gráficas si no existe
        import os
        self.output_dir = "Graphics"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Directorio '{self.output_dir}' creado para guardar las gráficas")
    
    def goals_distribution(self):
        """
        Crea gráficas de distribución de goles
        """
        print("Generando gráficas de distribución de goles...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análisis de Distribución de Goles', fontsize=16, fontweight='bold')
        
        # Gráfica 1: Distribución de goles locales
        axes[0, 0].hist(self.data['home_score'], bins=range(0, max(self.data['home_score'])+2), 
                       alpha=0.7, color='blue', edgecolor='black')
        axes[0, 0].set_title('Distribución de Goles de Equipos Locales')
        axes[0, 0].set_xlabel('Goles')
        axes[0, 0].set_ylabel('Frecuencia')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfica 2: Distribución de goles visitantes
        axes[0, 1].hist(self.data['away_score'], bins=range(0, max(self.data['away_score'])+2), 
                       alpha=0.7, color='red', edgecolor='black')
        axes[0, 1].set_title('Distribución de Goles de Equipos Visitantes')
        axes[0, 1].set_xlabel('Goles')
        axes[0, 1].set_ylabel('Frecuencia')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfica 3: Total de goles por partido
        total_goals = self.data['home_score'] + self.data['away_score']
        axes[1, 0].hist(total_goals, bins=range(0, max(total_goals)+2), 
                       alpha=0.7, color='green', edgecolor='black')
        axes[1, 0].set_title('Distribución de Total de Goles por Partido')
        axes[1, 0].set_xlabel('Total de Goles')
        axes[1, 0].set_ylabel('Frecuencia')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Gráfica 4: Comparación de promedios
        promedio_local = self.data['home_score'].mean()
        promedio_visitante = self.data['away_score'].mean()
        
        axes[1, 1].bar(['Equipos Locales', 'Equipos Visitantes'], 
                      [promedio_local, promedio_visitante], 
                      color=['blue', 'red'], alpha=0.7)
        axes[1, 1].set_title('Promedio de Goles por Tipo de Equipo')
        axes[1, 1].set_ylabel('Promedio de Goles')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Añadir valores en las barras
        for i, v in enumerate([promedio_local, promedio_visitante]):
            axes[1, 1].text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/distribucion_goles.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Gráfica guardada en {self.output_dir}/distribucion_goles.png")
    
    def temporal_analysis(self):
        """
        Crea gráficas de análisis temporal
        """
        print("Generando gráficas de análisis temporal...")
        
        # Preparar datos temporales
        self.data['year'] = pd.to_datetime(self.data['date']).dt.year
        self.data['decade'] = (self.data['year'] // 10) * 10
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis Temporal del Fútbol', fontsize=16, fontweight='bold')
        
        # Gráfica 1: Partidos por década
        decade_counts = self.data['decade'].value_counts().sort_index()
        axes[0, 0].plot(decade_counts.index, decade_counts.values, marker='o', linewidth=2, markersize=6)
        axes[0, 0].set_title('Número de Partidos por Década')
        axes[0, 0].set_xlabel('Década')
        axes[0, 0].set_ylabel('Número de Partidos')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfica 2: Evolución de goles promedio por década
        goals_by_decade = self.data.groupby('decade').agg({
            'home_score': 'mean',
            'away_score': 'mean'
        })
        goals_by_decade['total_avg'] = goals_by_decade['home_score'] + goals_by_decade['away_score']
        
        axes[0, 1].plot(goals_by_decade.index, goals_by_decade['total_avg'], 
                       marker='s', color='purple', linewidth=2, markersize=6)
        axes[0, 1].set_title('Evolución del Promedio de Goles por Partido')
        axes[0, 1].set_xlabel('Década')
        axes[0, 1].set_ylabel('Promedio de Goles por Partido')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfica 3: Tendencia de goles locales vs visitantes por década
        axes[1, 0].plot(goals_by_decade.index, goals_by_decade['home_score'], 
                       marker='o', label='Goles Locales', linewidth=2)
        axes[1, 0].plot(goals_by_decade.index, goals_by_decade['away_score'], 
                       marker='s', label='Goles Visitantes', linewidth=2)
        axes[1, 0].set_title('Tendencia de Goles: Locales vs Visitantes')
        axes[1, 0].set_xlabel('Década')
        axes[1, 0].set_ylabel('Promedio de Goles')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Gráfica 4: Distribución de partidos por años recientes (últimos 50 años)
        recent_years = self.data[self.data['year'] >= (datetime.now().year - 50)]
        if not recent_years.empty:
            year_counts = recent_years['year'].value_counts().sort_index()
            axes[1, 1].plot(year_counts.index, year_counts.values, alpha=0.7, color='orange')
            axes[1, 1].fill_between(year_counts.index, year_counts.values, alpha=0.3, color='orange')
            axes[1, 1].set_title('Partidos por Año (Últimos 50 años)')
            axes[1, 1].set_xlabel('Año')
            axes[1, 1].set_ylabel('Número de Partidos')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/analisis_temporal.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Gráfica guardada en {self.output_dir}/analisis_temporal.png")
    
    def top_teams_analysis(self):
        """
        Analiza y grafica los equipos más exitosos
        """
        print("Generando análisis de equipos más exitosos...")
        
        # Calcular estadísticas por equipo
        teams_stats = {}
        
        # Obtener todos los equipos únicos
        all_teams = set(self.data['home_team'].unique()) | set(self.data['away_team'].unique())
        all_teams.discard('Unknown Team')  # Remover equipos desconocidos si existen
        
        for team in all_teams:
            home_games = self.data[self.data['home_team'] == team]
            away_games = self.data[self.data['away_team'] == team]
            
            # Estadísticas básicas
            total_games = len(home_games) + len(away_games)
            goals_scored = home_games['home_score'].sum() + away_games['away_score'].sum()
            goals_conceded = home_games['away_score'].sum() + away_games['home_score'].sum()
            
            # Victorias
            home_wins = len(home_games[home_games['home_score'] > home_games['away_score']])
            away_wins = len(away_games[away_games['away_score'] > away_games['home_score']])
            total_wins = home_wins + away_wins
            
            teams_stats[team] = {
                'games': total_games,
                'goals_scored': goals_scored,
                'goals_conceded': goals_conceded,
                'wins': total_wins,
                'win_rate': total_wins / total_games if total_games > 0 else 0,
                'goal_difference': goals_scored - goals_conceded
            }
        
        # Convertir a DataFrame para facilitar el análisis
        teams_df = pd.DataFrame.from_dict(teams_stats, orient='index')
        teams_df = teams_df[teams_df['games'] >= 10]  # Solo equipos con al menos 10 partidos
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis de Equipos Más Exitosos', fontsize=16, fontweight='bold')
        
        # Top 15 equipos por número de partidos
        top_games = teams_df.nlargest(15, 'games')
        axes[0, 0].barh(range(len(top_games)), top_games['games'], color='skyblue')
        axes[0, 0].set_yticks(range(len(top_games)))
        axes[0, 0].set_yticklabels(top_games.index, fontsize=8)
        axes[0, 0].set_title('Top 15 Equipos por Número de Partidos')
        axes[0, 0].set_xlabel('Número de Partidos')
        
        # Top 15 equipos por diferencia de goles
        top_goal_diff = teams_df.nlargest(15, 'goal_difference')
        bars = axes[0, 1].barh(range(len(top_goal_diff)), top_goal_diff['goal_difference'], 
                              color='lightgreen')
        axes[0, 1].set_yticks(range(len(top_goal_diff)))
        axes[0, 1].set_yticklabels(top_goal_diff.index, fontsize=8)
        axes[0, 1].set_title('Top 15 Equipos por Diferencia de Goles')
        axes[0, 1].set_xlabel('Diferencia de Goles')
        
        # Top 15 equipos por tasa de victorias (mínimo 20 partidos)
        teams_min_games = teams_df[teams_df['games'] >= 20]
        if not teams_min_games.empty:
            top_win_rate = teams_min_games.nlargest(15, 'win_rate')
            axes[1, 0].barh(range(len(top_win_rate)), top_win_rate['win_rate'] * 100, 
                           color='gold')
            axes[1, 0].set_yticks(range(len(top_win_rate)))
            axes[1, 0].set_yticklabels(top_win_rate.index, fontsize=8)
            axes[1, 0].set_title('Top 15 Equipos por Tasa de Victorias (≥20 partidos)')
            axes[1, 0].set_xlabel('Tasa de Victorias (%)')
        
        # Top 15 equipos por goles anotados
        top_goals = teams_df.nlargest(15, 'goals_scored')
        axes[1, 1].barh(range(len(top_goals)), top_goals['goals_scored'], color='salmon')
        axes[1, 1].set_yticks(range(len(top_goals)))
        axes[1, 1].set_yticklabels(top_goals.index, fontsize=8)
        axes[1, 1].set_title('Top 15 Equipos por Goles Anotados')
        axes[1, 1].set_xlabel('Goles Anotados')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/top_equipos.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Gráfica guardada en {self.output_dir}/top_equipos.png")
    
    def tournaments_analysis(self):
        """
        Analiza los torneos y competiciones
        """
        print("Generando análisis de torneos...")
        
        # Análisis de torneos
        tournament_stats = self.data['tournament'].value_counts()
        tournament_goals = self.data.groupby('tournament').agg({
            'home_score': 'sum',
            'away_score': 'sum'
        })
        tournament_goals['total_goals'] = tournament_goals['home_score'] + tournament_goals['away_score']
        tournament_goals['avg_goals_per_match'] = tournament_goals['total_goals'] / tournament_stats
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis de Torneos y Competiciones', fontsize=16, fontweight='bold')
        
        # Top 15 torneos por número de partidos
        top_tournaments = tournament_stats.head(15)
        axes[0, 0].barh(range(len(top_tournaments)), top_tournaments.values, color='lightblue')
        axes[0, 0].set_yticks(range(len(top_tournaments)))
        axes[0, 0].set_yticklabels(top_tournaments.index, fontsize=8)
        axes[0, 0].set_title('Top 15 Torneos por Número de Partidos')
        axes[0, 0].set_xlabel('Número de Partidos')
        
        # Gráfica circular de torneos principales (top 10)
        top_10_tournaments = tournament_stats.head(10)
        others_sum = tournament_stats.iloc[10:].sum()
        
        pie_data = list(top_10_tournaments.values) + [others_sum]
        pie_labels = list(top_10_tournaments.index) + ['Otros']
        
        axes[0, 1].pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Distribución de Partidos por Torneo (Top 10)')
        
        # Promedio de goles por torneo (top 15)
        top_goals_tournaments = tournament_goals['avg_goals_per_match'].sort_values(ascending=False).head(15)
        axes[1, 0].barh(range(len(top_goals_tournaments)), top_goals_tournaments.values, color='orange')
        axes[1, 0].set_yticks(range(len(top_goals_tournaments)))
        axes[1, 0].set_yticklabels(top_goals_tournaments.index, fontsize=8)
        axes[1, 0].set_title('Top 15 Torneos por Promedio de Goles por Partido')
        axes[1, 0].set_xlabel('Promedio de Goles por Partido')
        
        # Evolución temporal de los principales torneos
        main_tournaments = tournament_stats.head(5).index
        tournament_temporal = self.data[self.data['tournament'].isin(main_tournaments)]
        tournament_temporal['year'] = pd.to_datetime(tournament_temporal['date']).dt.year
        
        for tournament in main_tournaments:
            tournament_data = tournament_temporal[tournament_temporal['tournament'] == tournament]
            yearly_counts = tournament_data['year'].value_counts().sort_index()
            if len(yearly_counts) > 1:  # Solo si hay datos de múltiples años
                axes[1, 1].plot(yearly_counts.index, yearly_counts.values, 
                               marker='o', label=tournament, alpha=0.7, linewidth=2)
        
        axes[1, 1].set_title('Evolución Temporal de Principales Torneos')
        axes[1, 1].set_xlabel('Año')
        axes[1, 1].set_ylabel('Número de Partidos')
        axes[1, 1].legend(fontsize=8)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/analisis_torneos.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Gráfica guardada en {self.output_dir}/analisis_torneos.png")
    
    def countries_analysis(self):
        """
        Analiza los países en el fútbol internacional
        """
        print("Generando análisis de países...")
        
        # Estadísticas por país
        country_stats = self.data['country'].value_counts()
        country_goals = self.data.groupby('country').agg({
            'home_score': 'sum',
            'away_score': 'sum'
        })
        country_goals['total_goals'] = country_goals['home_score'] + country_goals['away_score']
        country_goals['avg_goals_per_match'] = country_goals['total_goals'] / country_stats
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis por Países', fontsize=16, fontweight='bold')
        
        # Top 20 países por número de partidos
        top_countries = country_stats.head(20)
        axes[0, 0].barh(range(len(top_countries)), top_countries.values, color='mediumseagreen')
        axes[0, 0].set_yticks(range(len(top_countries)))
        axes[0, 0].set_yticklabels(top_countries.index, fontsize=8)
        axes[0, 0].set_title('Top 20 Países por Número de Partidos')
        axes[0, 0].set_xlabel('Número de Partidos')
        
        # Gráfica circular de países principales (top 12)
        top_12_countries = country_stats.head(12)
        others_sum = country_stats.iloc[12:].sum()
        
        pie_data = list(top_12_countries.values) + [others_sum]
        pie_labels = list(top_12_countries.index) + ['Otros']
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(pie_data)))
        axes[0, 1].pie(pie_data, labels=pie_labels, autopct='%1.1f%%', 
                      startangle=90, colors=colors)
        axes[0, 1].set_title('Distribución de Partidos por País (Top 12)')
        
        # Promedio de goles por país (países con al menos 50 partidos)
        countries_min_games = country_goals[country_stats >= 50]['avg_goals_per_match'].sort_values(ascending=False).head(15)
        if not countries_min_games.empty:
            axes[1, 0].barh(range(len(countries_min_games)), countries_min_games.values, color='coral')
            axes[1, 0].set_yticks(range(len(countries_min_games)))
            axes[1, 0].set_yticklabels(countries_min_games.index, fontsize=8)
            axes[1, 0].set_title('Top 15 Países por Promedio de Goles (≥50 partidos)')
            axes[1, 0].set_xlabel('Promedio de Goles por Partido')
        
        # Análisis de partidos neutrales
        neutral_analysis = self.data.groupby('country')['neutral'].agg(['sum', 'count'])
        neutral_analysis['neutral_percentage'] = (neutral_analysis['sum'] / neutral_analysis['count']) * 100
        neutral_top = neutral_analysis[neutral_analysis['count'] >= 20]['neutral_percentage'].sort_values(ascending=False).head(15)
        
        if not neutral_top.empty:
            axes[1, 1].barh(range(len(neutral_top)), neutral_top.values, color='plum')
            axes[1, 1].set_yticks(range(len(neutral_top)))
            axes[1, 1].set_yticklabels(neutral_top.index, fontsize=8)
            axes[1, 1].set_title('Top 15 Países por % Partidos en Campo Neutral (≥20 partidos)')
            axes[1, 1].set_xlabel('Porcentaje de Partidos en Campo Neutral')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/analisis_paises.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Gráfica guardada en {self.output_dir}/analisis_paises.png")
    
    def summary_dashboard(self):
        """
        Crea un dashboard resumen con las estadísticas más importantes
        """
        print("Generando dashboard resumen...")
        
        fig, axes = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Dashboard Resumen - Análisis Completo del Fútbol', fontsize=20, fontweight='bold')
        
        # Estadísticas generales
        total_matches = len(self.data)
        total_goals = self.data['home_score'].sum() + self.data['away_score'].sum()
        avg_goals_per_match = total_goals / total_matches
        date_range = f"{self.data['date'].min().strftime('%Y')} - {self.data['date'].max().strftime('%Y')}"
        
        # 1. Información general (texto)
        axes[0, 0].text(0.5, 0.8, f'Total de Partidos: {total_matches:,}', 
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       transform=axes[0, 0].transAxes)
        axes[0, 0].text(0.5, 0.6, f'Total de Goles: {total_goals:,}', 
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       transform=axes[0, 0].transAxes)
        axes[0, 0].text(0.5, 0.4, f'Promedio Goles/Partido: {avg_goals_per_match:.2f}', 
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       transform=axes[0, 0].transAxes)
        axes[0, 0].text(0.5, 0.2, f'Período: {date_range}', 
                       ha='center', va='center', fontsize=14, fontweight='bold',
                       transform=axes[0, 0].transAxes)
        axes[0, 0].set_title('Estadísticas Generales')
        axes[0, 0].axis('off')
        
        # 2. Distribución de goles totales
        total_goals_per_match = self.data['home_score'] + self.data['away_score']
        axes[0, 1].hist(total_goals_per_match, bins=range(0, 16), alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 1].set_title('Distribución de Goles por Partido')
        axes[0, 1].set_xlabel('Goles Totales')
        axes[0, 1].set_ylabel('Frecuencia')
        
        # 3. Ventaja de local vs visitante
        home_avg = self.data['home_score'].mean()
        away_avg = self.data['away_score'].mean()
        axes[0, 2].bar(['Local', 'Visitante'], [home_avg, away_avg], color=['blue', 'red'], alpha=0.7)
        axes[0, 2].set_title('Promedio de Goles: Local vs Visitante')
        axes[0, 2].set_ylabel('Promedio de Goles')
        for i, v in enumerate([home_avg, away_avg]):
            axes[0, 2].text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Top 10 equipos por partidos
        team_counts = pd.concat([self.data['home_team'], self.data['away_team']]).value_counts().head(10)
        axes[1, 0].barh(range(len(team_counts)), team_counts.values, color='lightgreen')
        axes[1, 0].set_yticks(range(len(team_counts)))
        axes[1, 0].set_yticklabels([team[:15] + '...' if len(team) > 15 else team for team in team_counts.index], fontsize=8)
        axes[1, 0].set_title('Top 10 Equipos por Partidos')
        axes[1, 0].set_xlabel('Número de Partidos')
        
        # 5. Top 10 torneos
        tournament_counts = self.data['tournament'].value_counts().head(10)
        axes[1, 1].pie(tournament_counts.values, labels=[t[:10] + '...' if len(t) > 10 else t for t in tournament_counts.index], 
                      autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Top 10 Torneos')
        
        # 6. Top 10 países
        country_counts = self.data['country'].value_counts().head(10)
        axes[1, 2].barh(range(len(country_counts)), country_counts.values, color='orange')
        axes[1, 2].set_yticks(range(len(country_counts)))
        axes[1, 2].set_yticklabels(country_counts.index, fontsize=8)
        axes[1, 2].set_title('Top 10 Países por Partidos')
        axes[1, 2].set_xlabel('Número de Partidos')
        
        # 7. Evolución temporal (por década)
        self.data['decade'] = (pd.to_datetime(self.data['date']).dt.year // 10) * 10
        decade_counts = self.data['decade'].value_counts().sort_index()
        axes[2, 0].plot(decade_counts.index, decade_counts.values, marker='o', linewidth=3, markersize=8, color='purple')
        axes[2, 0].fill_between(decade_counts.index, decade_counts.values, alpha=0.3, color='purple')
        axes[2, 0].set_title('Evolución del Fútbol por Década')
        axes[2, 0].set_xlabel('Década')
        axes[2, 0].set_ylabel('Número de Partidos')
        axes[2, 0].grid(True, alpha=0.3)
        
        # 8. Análisis de resultados (victorias locales, empates, victorias visitantes)
        home_wins = len(self.data[self.data['home_score'] > self.data['away_score']])
        draws = len(self.data[self.data['home_score'] == self.data['away_score']])
        away_wins = len(self.data[self.data['home_score'] < self.data['away_score']])
        
        result_labels = ['Victorias Locales', 'Empates', 'Victorias Visitantes']
        result_values = [home_wins, draws, away_wins]
        colors = ['blue', 'yellow', 'red']
        
        axes[2, 1].pie(result_values, labels=result_labels, autopct='%1.1f%%', 
                      colors=colors, startangle=90)
        axes[2, 1].set_title('Distribución de Resultados')
        
        # 9. Partidos por tipo (neutral vs no neutral)
        neutral_counts = self.data['neutral'].value_counts()
        axes[2, 2].bar(neutral_counts.index.map({True: 'Campo Neutral', False: 'Campo Propio'}), 
                      neutral_counts.values, color=['gray', 'green'], alpha=0.7)
        axes[2, 2].set_title('Distribución por Tipo de Campo')
        axes[2, 2].set_ylabel('Número de Partidos')
        for i, v in enumerate(neutral_counts.values):
            axes[2, 2].text(i, v + max(neutral_counts.values) * 0.01, f'{v:,}', 
                           ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/dashboard_resumen.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✓ Dashboard guardado en {self.output_dir}/dashboard_resumen.png")
    
    def generate_all_graphics(self):
        """
        Genera las 3 gráficas principales más importantes para el análisis de fútbol
        """
        print("=" * 60)
        print("GENERANDO GRÁFICAS PRINCIPALES DE ANÁLISIS DE FÚTBOL")
        print("=" * 60)
        
        # Verificar que tenemos datos
        if self.data.empty:
            print("❌ Error: No hay datos para generar gráficas")
            return
        
        print(f"📊 Datos disponibles: {len(self.data):,} partidos")
        print(f"📅 Rango de fechas: {self.data['date'].min()} a {self.data['date'].max()}")
        
        # Generar solo las 3 gráficas principales
        try:
            print("\n🎯 Generando Gráfica 1 de 3...")
            self.goals_distribution()
            print()
            
            print("🎯 Generando Gráfica 2 de 3...")
            self.temporal_analysis()
            print()
            
            print("🎯 Generando Gráfica 3 de 3...")
            self.top_teams_analysis()
            print()
            
            print("=" * 60)
            print("✅ LAS 3 GRÁFICAS PRINCIPALES HAN SIDO GENERADAS EXITOSAMENTE")
            print("📁 Gráficas generadas:")
            print("   1. distribucion_goles.png - Análisis de patrones de goles")
            print("   2. analisis_temporal.png - Evolución del fútbol en el tiempo")
            print("   3. top_equipos.png - Equipos más exitosos")
            print(f"📂 Ubicación: {self.output_dir}/")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Error al generar las gráficas: {e}")
            import traceback
            traceback.print_exc()