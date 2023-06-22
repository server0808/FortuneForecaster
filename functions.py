from dataclasses import dataclass
from datetime import datetime, timedelta

import altair as alt
import numpy as np
import pandas as pd
import yfinance as yf
from numpy import ndarray

periodos_dictionary = {'7 dias': '7d',
                       '15 dias': '15d',
                       '1 mês': '30d',
                       '3 meses': '90d',
                       '6 meses': '180d',
                       '1 ano': '1y',
                       '2 anos': '2y',
                       '5 anos': '5y',
                       }


@dataclass
class Ativo:
    ticker: str
    period_before: str = '1y'
    days_ahead: int = 30
    iterations: int = 10000
    return_expected: float = 0.05

    def __post_init__(self):
        self.stock_hist = self.get_stock_prices()
        self.price_paths = self.simulate_prices(self.stock_hist)

    def get_stock_prices(self) -> 'DataFrame':
        """Pega os preços históricos do ativo usando a biblioteca yfinance."""
        stock = yf.Ticker(self.ticker)
        stock_hist = stock.history(period=self.period_before)
        stock_hist.reset_index(inplace=True)
        stock_hist = stock_hist.rename(columns={'Date': 'Data', 'Close': 'Preço no Fechamento'})
        return stock_hist

    def simulate_prices(self, stock_hist: 'DataFrame') -> np.array:
        """Simula os preços futuros do ativo usando o Movimento Browniano Geométrico e simulações de Monte Carlo."""
        log_returns = np.log(1 + stock_hist['Preço no Fechamento'].pct_change())
        mu = log_returns.mean()
        var = log_returns.var()
        drift = mu - (0.5 * var)
        stdev = log_returns.std()

        daily_returns = np.exp(drift + stdev * np.random.standard_normal(size=(self.days_ahead, self.iterations)))

        price_paths = np.zeros_like(daily_returns)
        price_paths[0] = stock_hist['Preço no Fechamento'].iloc[-1]

        for t in range(1, self.days_ahead):
            price_paths[t] = price_paths[t - 1] * daily_returns[t]

        return price_paths

    def calculate_p_return(self, price_paths: np.array) -> ndarray:
        """Calcula a probabilidade de retorno do ativo ser maior ou igual ao esperado."""
        actual = price_paths[0, 0]
        over = (price_paths[-1] / actual) >= self.return_expected + 1
        prob = np.mean(over)
        return prob

    def return_probability(self) -> ndarray:
        """Calcula a probabilidade de retorno do ativo"""
        return self.calculate_p_return(self.price_paths)

    def plot(self):
        """Plota o gráfico com os preços simulados."""
        df = self.create_dataframe_for_plot()
        return self.generate_chart(df)

    def plot_historic_prices(self):
        """Plota o gráfico com os preços históricos."""
        stock_hist = self.get_stock_prices()
        graph = alt.Chart(stock_hist).mark_line().encode(x='Data', y='Preço no Fechamento')
        nearest = alt.selection_point(nearest=True, on='mouseover',
                                      fields=['Data'], empty=False)
        selectors = alt.Chart(stock_hist).mark_point().encode(x='Data', opacity=alt.value(0)).add_params(nearest)
        points = graph.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))
        text = graph.mark_text(align='left', dx=5, dy=-5, size=14).encode(
            text=alt.condition(nearest, 'Preço no Fechamento', alt.value(' '), format='.2f'))
        rules = alt.Chart(stock_hist).mark_rule(color='gray').encode(x='Data').transform_filter(nearest)
        graph = alt.layer(graph, selectors, points, rules, text)
        return graph

    def create_dataframe_for_plot(self):
        """Cria um DataFrame com os preços simulados e os classifica em melhor, pior e média."""
        df = pd.DataFrame(self.price_paths.T)
        maximo = df.iloc[:, -1].max()
        minimo = df.iloc[:, -1].min()
        media = df.mean().reset_index(name='price').rename(columns={'index': 'time'})
        media['Categoria'] = 'Média'

        df = df[(df.iloc[:, -1] == maximo) | (df.iloc[:, -1] == minimo)]
        df['Categoria'] = np.where(df.iloc[:, -1] == maximo, 'Melhor cenário', 'Pior cenário')
        df = df.melt(id_vars='Categoria', var_name='time', value_name='price')
        df = pd.concat([df, media])
        df['Data'] = df['time'].apply(lambda x: datetime.today() + timedelta(days=x))

        return df

    @staticmethod
    def generate_chart(df):
        nearest = alt.selection_point(nearest=True, on='mouseover',
                                      fields=['time'], empty=False)

        chart = alt.Chart(df).mark_line().encode(
            x=alt.X('Data', axis=alt.Axis(title='Data')),
            y=alt.Y('price:Q', axis=alt.Axis(title='Preço Provável')),
            color='Categoria:N',
            tooltip=['Data', 'price', 'Categoria'])

        selectors = alt.Chart(df).mark_point().encode(
            x=alt.X('Data', axis=alt.Axis(title='Data')),
            opacity=alt.value(0)).add_params(nearest)

        points = chart.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

        text = chart.mark_text(align='left', dx=5, dy=-5, size=16).encode(
            text=alt.condition(nearest, 'price:Q', alt.value(' '), format='.2f'),
            color=alt.condition(nearest, 'Categoria:N', alt.value(' '),
                                legend=alt.Legend(title="Cenário", orient="bottom")))

        rules = alt.Chart(df).mark_rule(color='gray').encode(
            x=alt.X('Data', axis=alt.Axis(title='Data'))).transform_filter(nearest)

        return alt.layer(chart, selectors, points, rules, text)
