import streamlit as st

from functions import Ativo, periodos_dictionary

st.set_page_config(layout='wide', page_title='FortuneForecaster - Simulador de Probabilidade de Retorno',
                   page_icon=':moneybag:', initial_sidebar_state='auto',
                   menu_items={'Get Help': None, 'Report a bug': None, 'About': None})
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('🔮 FortuneForecaster')
st.header('Simulador de Probabilidade de Retorno')
st.subheader('Calcula a probabilidade de retorno de um ativo ser maior ou igual ao esperado, usando simulações de Monte Carlo a partir do Movimento Geométrico Browniano')

def main():
    with st.form(key='ativo_ticker'):
        coluna1, coluna2, coluna3 = st.columns(3)
        ticker = coluna1.text_input('Digite o ticker do ativo:', value='MGLU3.SA')
        st.caption('Para o ticker, usar o formato do YahooFinance. Exemplo: PETR4.SA, VALE3.SA, ITUB4.SA, etc.')
        periodo = coluna2.selectbox('Considerar dados dos últimos:', options=periodos_dictionary.keys(), index=5)
        previsao = coluna3.number_input('Prever o preço daqui a quantos dias?', min_value=5, max_value=365, value=30)
        iteracoes = coluna1.number_input('Quantas iterações?', min_value=1000, max_value=1000000, value=10000)
        retorno = coluna2.number_input('Qual o retorno esperado, em %?', min_value=0.5, max_value=99.5, value=5.0, step=0.5)
        analisar = st.form_submit_button('Analisar')

    if analisar:
        with st.spinner('Baixando e processando dados...'):
            try:
                ativo = Ativo(ticker=ticker, period_before=periodos_dictionary[periodo], days_ahead=previsao,
                              iterations=iteracoes, return_expected=retorno / 100)
                prob = ativo.return_probability()
                st.success(f'Probabilidade de retorno maior ou igual a {retorno}% em {previsao} dias: {prob:.2%}')
                coluna_graph1, coluna_graph2 = st.columns([1, 2])
                coluna_graph1.subheader('Preço histórico do ativo:')
                coluna_graph1.altair_chart(ativo.plot_historic_prices(), use_container_width=True)
                coluna_graph2.subheader('Simulação de preços futuros:')
                coluna_graph2.altair_chart(ativo.plot(), use_container_width=True)
            except Exception as e:
                st.error(f'Erro: verifique o Ticker. Detalhes: {e}')

    with open('About.md', 'r') as f:
        about = f.read()

    with st.sidebar:
        st.markdown(about)

ft = """
<style>
a:link , a:visited{
color: #BFBFBF;  /* theme's text color hex code at 75 percent brightness*/
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: #0283C3; /* theme's primary color*/
background-color: transparent;
text-decoration: underline;
}

#page-container {
  position: relative;
  min-height: 10vh;
}

footer{
    visibility:hidden;
}

.footer {
position: relative;
left: 0;
top:230px;
bottom: 0;
width: 100%;
background-color: transparent;
color: #808080; /* theme's text color hex code at 50 percent brightness*/
text-align: left; /* you can replace 'left' with 'center' or 'right' if you want*/
}
</style>

<div id="page-container">

<div class="footer">
<p style='font-size: 0.875em;'>Made with <a style='display: inline; text-align: left;' href="https://streamlit.io/" target="_blank">Streamlit</a>, 
<a style='display: inline; text-align: left;' href="https://altair-viz.github.io" target="_blank">Altair</a>, 
<a style='display: inline; text-align: left;' href="https://pandas.pydata.org/" target="_blank">Pandas</a>,
<a style='display: inline; text-align: left;' href="https://numpy.org/" target="_blank">Numpy</a>,
on 
<a style='display: inline; text-align: left;' href="https://www.python.org" target="_blank">Python</a>.
<br 'style= top:3px;'>
with <img src="https://em-content.zobj.net/source/skype/289/red-heart_2764-fe0f.png" alt="heart" height= "10"/><a style='display: inline; text-align: left;' href="https://github.com/mateuspestana" target="_blank"> by Matheus C. Pestana</a></p>
</div>

</div>
"""
if __name__ == '__main__':
    main()
    st.markdown(ft, unsafe_allow_html=True)