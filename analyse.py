import pandas as pd
import plotly.express as px
import numpy as np

class DotaDataAnalysis:
    def __init__(self):
        self.df_top_heroes = pd.read_csv('data/precomputed_top_heroes.csv')
        self.df_chat_activity = pd.read_csv('data/precomputed_chat_activity.csv')
        self.df_bad_msg = pd.read_csv('data/precomputed_bad_msg_percentage.csv')
        self.df_matches_stats = pd.read_csv('data/precomputed_matches_stats.csv')
        self.df_boots_compare = pd.read_csv('data/precomputed_boots_compare.csv')
        self.df_hero_gpm = pd.read_csv('data/precomputed_hero_gpm.csv')
        
        self.df_hero_gpm['hero_id'] = 'Hero_' + self.df_hero_gpm['hero_id'].astype(str)

    def get_top_heroes(self, top_n=10):
        return self.df_top_heroes.head(top_n)

    def analyze_chat_activity(self):
        return self.df_chat_activity

    def calculate_bad_message_percentage(self):
        return self.df_bad_msg['bad_message_percentage'].iloc[0]

    def get_matches_stats(self):
        row = self.df_matches_stats.iloc[0].to_dict()
        return {
            "total_matches": int(row['total_matches']),
            "matches_with_chat": int(row['matches_with_chat']),
            "matches_without_chat": int(row['matches_without_chat'])
        }

    def get_boots_compare_data(self):
        return self.df_boots_compare

    def get_hero_gpm_data(self):
        return self.df_hero_gpm

    def plot_top_heroes(self, top_n=10):
        df = self.get_top_heroes(top_n)
        fig = px.bar(df, x="localized_name", y="count", title="Top Heroes")
        return fig

    def plot_chat_activity(self):
        df = self.analyze_chat_activity()
        fig = px.histogram(df, x="percent_players_in_chat", nbins=20, title="Distribution of % Players in Chat")
        return fig

    def plot_bad_message_pie(self):
        percentage = self.calculate_bad_message_percentage()
        values = [percentage, 100 - percentage]
        labels = ['Profane', 'Not Profane']
        fig = px.pie(values=values, names=labels, title='Profane vs Non-Profane Messages')
        return fig

    def plot_matches_stats_pie(self):
        stats = self.get_matches_stats()
        labels = ['Matches with chat', 'Matches without chat']
        sizes = [stats['matches_with_chat'], stats['matches_without_chat']]
        fig = px.pie(values=sizes, names=labels, title="Percentage of Matches with Chat")
        return fig

    def plot_first_boots_box(self):
        df = self.get_boots_compare_data()
        fig = px.box(df, x='category', y='time', points='all',
                     title='First Boots of Speed Purchase Time: Winners vs Losers')
        return fig
