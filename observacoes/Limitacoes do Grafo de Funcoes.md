Limitações da implementação do grafo de funções:
    1) O grafo só analisa um script Python. Logo, o experimento do usuário deve ser totalmente escrito em um único arquivo .py

    2) Todas as funções definidas pelo usuário devem possuir nomes diferentes pois a comparação é feita pelo atributo __name__ do objeto que representa a função Python em tempo de execução e este só armazena o último nome da função

    3)O experimento do usuário deve seguir às seguintes regras de escrita para que a classe que busca informações na AST realize sua análise corretamente:
        a)Sempre que um objeto chamar um método de instância, isso deve ser feito por nome_do_objeto.metodo_instancia()
            Ex.: Se existe a classe Teste() e uma instância t dessa classe,
                É permitido: t.metodo_instancia()
                Não é permitido: Teste().metodo_instancia()

        b)Sempre que deseje-se executar um método de classe, isso deve ser feito por nome_da_classe.metodo_da_classe()
            Ex.: Se existe a classe Teste() e uma instância t dessa classe,
                É permitido: Teste.metodo_da_classe()
                Não é permitido: t.metodo_da_classe()

        c)Sempre que deseje-se declara um método de classe, isso deve ser feito utilizando a marcação @staticmethod
            Ex.: class Teste():
                    @staticmethod
                    def metodo_estatico():
                        return 1

        d)Todos os imports feitos pelo usuário devem ser realizados através do comando import ...
            Ex.: Caso o usuário deseje utilizar a função random.random()
                É permitido: import random
                Não é permitido: import random as rd
                Não é permitido: from random import random
                Não é permitido: from random import *
    