Unificação do acesso ao banco de dados + inserção de novos dados do cache em dicionário e, ao fim da execução no banco de dados:

Em "environment.py", mantive uma abertura e fechamento de conexão com o banco de dados diferente da conexão utilizada para recuperar dados do banco. Mantive assim separação entre criação do ambiente e manipulação do banco de dados. Entretanto adpatei a forma de criar a conexão para que fosse utilizada uma instância da classe Banco.

A função "init_env()" definida em "environment.py" foi alterada. Ela não recebe mais parâmetros pois passou a ser executada apenas uma vez ao se importar o módulo intpy (arquivo "__init__.py"). Isso foi necessário para que logo em seguida pudesse ser aberta a conexão única com o banco de dados (constante "CONN_DB").

No arquivo "data_access.py" foram removidas as funções: "_create_conn()", "_close_conn(conn)", "_exec_stmt(stmt)", "_exec_stmt_return(stmt)". As funções "_save(file_name)", "_get(id)" e "_remove(id)" foram alteradas para utilizar a constante "CONN_DB".

No arquivo "intpy.py" alterei as quatro chamadas à função time.time() que não é mais suportada por chamdas à função time.perf_counter().

Criação da função "salvarCache()" no arquivo "intpy.py" que deve ser chamada ao final do script para que a conexão com o banco possa ser fechada e os dados em "DICT_NEW_DATA" possam ser salvos no banco.

==============================================================
Implementação de Threads com a biblioteca threading:

i)Conexão com o banco de dados
    A conexão com o banco de dados passou a ser thread local. Assim, sempre que uma consulta ao banco necessita ser feita é necessário abrir uma nova conexão com o banco de dados.

    Talvez não valha a pena continuar abrindo uma conexão no início do programa pois ela só será utilizada na inserção dos dados ao fim da execução e estávamos pensando em fazer essa etapa em outro processo

ii)Execução das Threads
    Sempre que a função do usuário termina sua execução antes que a consulta ao banco seja concluída, o retorno da função é adicionado ao dicionário DICT_NEW_DATA

    Consequentemente, na hora de inserir os dados no banco é necessário verificar antes da inserção se os dados estão ou não no cache. Essa abordagem possui duas vantagens e uma desvantagem.
    
    Vantagem: Ganhamos velocidade na execução do script pois antes que o select termine de executar continuamos a execução do script do usuário.

    Como o dado será adicionado ao dicionário e, quando a busca no banco é feita, antes de executar o select no banco é verificado se o valor se encontra no dicionário, recuperar esse dado no futuro será mais rápido pois não será necessário acessar o banco

    Desvantagem: No momento da inserção de novos dados ao banco, será necessário verificar se o dado já está no cache o que aumentará o tempo de execução dessa etapa. Entretanto como pensamos em executar essa etapa em outro processo esse tempo adicional talvez seja tolerável

iii)Término das threads
    As threads iniciadas durante a execução do decorador deterministic ainda não são destruídas. Isso significa que tanto a consulta ao banco como a execução da função do usuário são executadas até o final.

iv)Mensagens de DEBUG
    O código ainda possui mensagens de DEBUG

v)Mensagens 
    Há várias mensagens que o intpy utilizava como DEBUG que talvez tenham perdido o seu sentido e devessem ser removidas
