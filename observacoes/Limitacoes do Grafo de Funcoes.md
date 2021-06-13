Limitações da implementação do grafo de funções:
    1) Todas as funções definidas pelo usuário devem possuir nomes diferentes pois a comparação é feita pelo atributo __name__ do objeto que representa a função Python em tempo de execução e este só armazena o último nome da função

    2)Não é permitido que o experimento do usuário utilize o comando from MODULO import * (necessário para que a classe que busca informações na AST realize sua análise corretamente)
        Ex.: Caso o usuário deseje utilizar a função random.random()
            É permitido: import random as rd
            É permitido: from random import random as rd
            Não é permitido: from random import *
    
    3)Analisar casos em que o import realizado é feito em uma pasta que contém o arquivo __init__.py