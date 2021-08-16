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
    
    4)É importante observar que assim que o processamento do script do usuário se encerra, o IntPy inicializa um processo separado para realizar o salvamento dos dados no cache. Esse processo não pode ser visto pelo usuário, que tem seu terminal liberado para executar outros programas, enquanto esse procedimento ocorre. Assim, surgem as seguintes limitações:
        i)Caso o usuário desligue o computador logo após o fim do processamento do usuário, é possível que os dados não sejam salvos no cache. Isso impediria que o IntPy acelerasse a execução do experimento da próxima vez que este fosse executado.
        
        ii)Caso o usuário execute duas vezes consecutivas o mesmo experimento, é possível que os dados coletados pelo IntPy durante a primeira execução do experimento ainda não tenham sido salvos. Isso faria com que a execução do segundo experimento não fosse acelerada, podendo inclusive demorar mais que o normal, devido a concomitantemente estar sendo executado um outro processo no sistema.
