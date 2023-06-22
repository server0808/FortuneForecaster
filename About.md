# FortuneForecaster
Desenvolvido por [Matheus C. Pestana](https://www.linkedin.com/in/matheus-pestana/)

## Descrição
O FortuneForecaster é um projeto de um sistema de previsão de preços de ativos, baseando-se no GBM (*Geometric Brownian Motion*) e em simulações de Monte Carlo. 
O projeto é todo realizado em Streamlit, usando majoritariamente as bibliotecas Pandas, Numpy e Altair.

## Como funciona
O *Geometric Brownian Motion* (GBM) e as simulações de Monte Carlo são métodos usados ​​extensivamente na modelagem financeira, particularmente na precificação de derivativos, como opções. A relação entre os dois é que as simulações de Monte Carlo são frequentemente usadas para gerar caminhos da Geometric Brownian Motion.

O *Geometric Brownian Motion8 é um modelo usado para descrever os prováveis caminhos que o preço de uma ação ou outra métrica financeira pode seguir ao longo do tempo. É um processo estocástico de tempo contínuo onde o logaritmo da quantidade variando aleatoriamente segue um movimento browniano. Suas suposições incluem constante deriva (*drift*) e volatilidade, __o que pode ser uma limitação nas aplicações do mundo real__.

As simulações de Monte Carlo, por outro lado, são uma ampla classe de algoritmos computacionais que dependem de amostragem aleatória repetida para obter resultados numéricos. Estes métodos são usados para modelar a probabilidade de diferentes resultados em um processo que não pode ser facilmente previsto devido à intervenção de variáveis aleatórias.

No contexto da modelagem financeira:

- __GBM é o modelo teórico__ - Ele fornece uma fórmula matemática para modelar a evolução dos preços das ações ou outras variáveis ao longo do tempo. O GBM incorpora aleatoriedade, o que lhe permite gerar uma gama de possíveis caminhos para a variável em questão.
- __As simulações de Monte Carlo são a implementação prática deste modelo__ - Ao gerar um grande número de potenciais caminhos, as simulações de Monte Carlo permitem que você calcule uma variedade de resultados potenciais e calcule coisas como o valor esperado de um derivativo, medições de risco, etc.

Em resumo, as simulações de Monte Carlo podem usar *Geometric Brownian Motion* como o processo estocástico subjacente para simular diferentes caminhos de um preço de ação, por exemplo. Esta abordagem é amplamente usada na engenharia financeira para precificar vários derivativos financeiros e gerenciar riscos financeiros.