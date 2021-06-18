Limitações da implementação do grafo de funções:
    1)Não é permitido que o experimento do usuário utilize o comando from MODULO import * (necessário para que a classe que busca informações na AST realize sua análise corretamente)
        Ex.: Caso o usuário deseje utilizar a função random.random()
            É permitido: import random as rd
            É permitido: from random import random as rd
            Não é permitido: from random import *

A implementação do módulo function_graph pode ser melhorada mediante uma refatoração das estruturas de dados utilizadas (algumas vezes são utilizadas listas quando poderiam ser utilizados sets, outras vezes é possível melhorar a recuperação de informações alterando o modo como elas são armazenadas na estrutura de dados)
