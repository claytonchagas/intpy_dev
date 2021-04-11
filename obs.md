Unificação do acesso ao banco de dados + inserção de novos dados do cache em dicionário e, ao fim da execução no banco de dados:

Em "environment.py", mantive uma abertura e fechamento de conexão com o banco de dados diferente da conexão utilizada para recuperar dados do banco. Mantive assim separação entre criação do ambiente e manipulação do banco de dados. Entretanto adpatei a forma de criar a conexão para que fosse utilizada uma instância da classe Banco.

A função "init_env()" definida em "environment.py" foi alterada. Ela não recebe mais parâmetros pois passou a ser executada apenas uma vez ao se importar o módulo intpy (arquivo "__init__.py"). Isso foi necessário para que logo em seguida pudesse ser aberta a conexão única com o banco de dados (constante "CONEXAO_BANCO").

No arquivo "data_access.py" foram removidas as funções: "_create_conn()", "_close_conn(conn)", "_exec_stmt(stmt)", "_exec_stmt_return(stmt)". As funções "_save(file_name)", "_get(id)" e "_remove(id)" foram alteradas para utilizar a constante "CONEXAO_BANCO".

No arquivo "intpy.py" alterei as quatro chamadas à função time.time() que não é mais suportada por chamdas à função time.perf_counter().

Criação da função "salvarCache()" no arquivo "intpy.py" que deve ser chamada ao final do script para que a conexão com o banco possa ser fechada e os dados em "DICIO_NOVOS_DADOS" possam ser salvos no banco.

==============================================================
Implementação de Threads com a biblioteca threading:

CONEXÃO COM BANCO É THREAD-LOCAL

CRIEI UMA CONEXÃO SEMPRE QUE UMA THREAD DE CONSULTA AO BANCO É ATIVADA

NÃO SEI SE VALE A PENA CONTINUAR ABRINDO A CONEXÃO COM O BANCO NO INÍCIO DO PROGRAMA POIS ELA SÓ SERÁ UTILIZADA NA INSERÇÃO DOS DADOS AO FIM DA EXECUÇÃO (QUERIAMOS FAZER ISSO EM OUTRO PROCESSO)


FIZ COM QUE SEMPRE QUE A FUNÇÃO SEJA PROCESSADA ANTES DO BANCO ASSUMA QUE HOUVE CACHE MISS

NA HORA DA INSERÇÃO DOS DADOS VERIFICAMOS SE HOUVE DE FATO O DADO ESTÁ OU NÃO NO CACHE

PRÓ: GANHA VELOCIDADE NA EXECUÇÃO DO SCRIPT (NÃO ESPERAMOS O SELECT DO BANCO TERMINAR)

COM O NOVO VALOR NO DICIONÁRIO ELE SERÁ VERIFICADO ANTES DE PESQUISAR NO BANCO NOVAMENTE
CONTRA: NA HORA DE INSERÇÃO HÁ NECESSIDADE DE VERIFICAR SE OS VALORES ESTÃO NO CACHE SENÃO OCORRE RUPTURA DA CONSTRAINT UNIQUE

MAS SE A EXECUÇÃO OCORRER EM UM PROCESSO A PARTE O TEMPO ADICIONAL PODE SER TOLERÁVEL, TALVEZ


IMPLEMENTAÇÃO PARA FUNÇÕES ITERATIVAS (_function_call(f))
SEM DESTRUIR THREADS
AINDA COM MENSAGENS DE DEBUG