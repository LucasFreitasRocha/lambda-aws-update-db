# lambda-aws-update-db

## Esse repositorio é um estudo sobre lamdba aws

Criei esse script em python para aprender sobre lambda aws e escrivei o passo para criar no [medium](https://medium.com/@devrocha/lambda-aws-update-base-postgresql-com-python-478689ffcb96)
nesse readme vou explicar do codigo em si

# funções

## lambda_handler
  Essa é a função chamada quando a lambda é iniciada
  recebe um evento que está em json 
  
      {
      "Records": [
          {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "us-east-1",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
              "principalId": "EXAMPLE"
            },
            "requestParameters": {
              "sourceIPAddress": "127.0.0.1"
            },
            "responseElements": {
              "x-amz-request-id": "EXAMPLE123456789",
              "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambda"
            },
            "s3": {
              "s3SchemaVersion": "1.0",
              "configurationId": "testConfigRule",
              "bucket": {
                "name": "example-bucket",
                "ownerIdentity": {
                  "principalId": "EXAMPLE"
                },
                "arn": "arn:aws:s3:::example-bucket"
              },
              "object": {
                "key": "test%2Fkey",
                "size": 1024,
                "eTag": "0123456789abcdef0123456789abcdef",
                "sequencer": "0A1B2C3D4E5F678901"
              }
            }
          }
      ]
    }

  então por isso que acessamos o nome do bucket e keyfile com o codigo da linha 41 e 42 do script

  na linha 43 instaciamos o client s3 que vamos utilizar mais a frente
  
## get_file_stream
  na linha 44 chamos a função que fica responsavel por acessar o conteudo do arquivo

    def get_file_stream(bucket, s3_client, file_key):
      response = s3_client.get_object(Bucket=bucket, Key=file_key)
      return response['Body'].iter_lines()
      
  chamamos o s3_client.get_object , com o retorno acessamos o body do conteudo e utilizamos o (iter_lines()), que lê o arquivo linha por linha, ideal para processamento de arquivos grandes sem carregá-los inteiramente na memória.

## get_config
  Pegamos as variaves de ambiente
  
    def get_config():
      return {
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME"),
        "DB_USER": os.getenv("DB_USER"),
        "DB_PASS": os.getenv("DB_PASS")
      }  

## get_db_connection
  Estabelece a conexão com o banco de dados com as variaveis de ambiente populada na função anterior

    def get_db_connection(config):
      return psycopg2.connect(
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        database=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASS"],
      )
## process_file
  com a conexão com o banco estabelecida e acesso ao arquivo txt está na hora de processar o arquivo, um adendo na linha 6 do script carregamos por variavel de ambiente quais tabelas vamoss fazer o update
  TABLES = os.getenv("TABLES_STRING").split(","), as tabelas estão em variavel de ambiente separdo por virgula

Parâmetros

    file_stream: Um iterador de linhas do arquivo (vem de iter_lines(), então cada linha está em bytes e precisa ser decodificada).
    cursor: Um cursor de banco de dados para executar comandos SQL.
O que a função faz

Percorre todas as linhas do arquivo, que devem estar no formato:

    cliente_id,produto_id
    123,456
    789,101
    
Decodifica a linha de bytes para string (decode("utf-8")).
Remove espaços em branco (strip()) e divide os valores (split(",")).
Faz um UPDATE para cada tabela em TABLES, atualizando product_id onde client_id corresponde ao valor lido.


# Conclusão

  obrigado por ter lido, estou aberto a feedBacks de como melhorar esse script
  

