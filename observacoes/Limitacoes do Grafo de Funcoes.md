Limitações da implementação do grafo de funções:
    1) O grafo só analisa um script Python. Logo, o experimento do usuário deve ser totalmente escrito em um único arquivo .py

    2) Todas as funções definidas pelo usuário devem possuir nomes diferentes pois a comparação é feita pelo atributo __name__ do objeto que representa a função Python em tempo de execução e este só armazena o último nome da função

    3)Não é permitido que o experimento do usuário utilize o comando from MODULO import * (necessário para que a classe que busca informações na AST realize sua análise corretamente)
        Ex.: Caso o usuário deseje utilizar a função random.random()
            É permitido: import random as rd
            É permitido: from random import random as rd
            Não é permitido: from random import *
    