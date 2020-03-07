# Dell Warranty Checker

Este script irá buscar na API da Dell por informações sobre determinados equipamentos, passados como argumento para o script, e imprimir na tela sobre.

#### Decorrer do script:
1. uma requisição para o Dell API Endpoint for Auth será realizada para pegar o token de acesso;
2. uma requisição para o Dell API Endpoint for Asset Waranty será realizada enviando as service tags para que a API retorne um JSON com os dados sobre estes equipamentos;
3. será impresso na tela as seguintes informações sobre cada equipamento: Service Tag, modelo do equipamento, garantia (pode ser OK, WARNING ou CRITICAL) e quantos dias ainda restam de garantia ou quantos dias se passaram desde o fim da garantia caso esteja vencida.

##### Exemplo de execução e saída:
    ./dell-warranty-checker.py 'BB3PKF2,B41JKF2,6W742V1,W433F67'

    W433F67 - ERROR - This tag may not exist
    BB3PKF2 - LATITUDE E7470 - Warranty OK - 561 days remaining.
    6W742V1 - VOSTRO 3550 - Warranty CRITICAL - 2476 days past.
    B41JKF2 - POWEREDGE R730XD - Warranty CRITICAL - 175 days past.
