As seguintes limitações foram identificadas no IntPy:
    1)O IntPy não funciona corretamente com objetos. Portanto, não é recomendável que usuários marquem com o decorador "@deterministic" funções que recebem por parâmetros, retornam ou utilizam em seu processamento objetos.

    2)O IntPy não funciona corretamente com funções que retornam None. Caso uma função possa retorne None, mesmo que seja para apenas um conjunto restrito de entradas, não é recomendável marcá-la com o decorador @deterministic.

    Ex.: A função abaixo não deveria ser marcada com o decorador @deterministic
                            def funcao(arg):
                                if(arg > 10):
                                    return None
                                else:
                                    return 1

    3)O IntPy não funciona corretamente com funções que não recebem parâmetros. Caso uma função possa em algum caso não receber parâmetros (ex.: funções que possuem valores default ou argumentos opcionais), não é recomendável marcá-la com o decorador @deterministic.

    Ex.: A função abaixo não deveria ser marcada com o decorador @deterministic
                            def funcao(argumento=1):
                                return 10
