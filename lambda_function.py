import json
import boto3
import os
import psycopg2

TABLES = os.getenv("TABLES_STRING").split(",")

def get_config():
    return {
      "DB_HOST": os.getenv("DB_HOST"),
      "DB_PORT": os.getenv("DB_PORT"),
      "DB_NAME": os.getenv("DB_NAME"),
      "DB_USER": os.getenv("DB_USER"),
      "DB_PASS": os.getenv("DB_PASS")
    }  


def get_db_connection(config):
    return psycopg2.connect(
      host=config["DB_HOST"],
      port=config["DB_PORT"],
      database=config["DB_NAME"],
      user=config["DB_USER"],
      password=config["DB_PASS"],
    )


def get_file_stream(bucket, s3_client, file_key):
    response = s3_client.get_object(Bucket=bucket, Key=file_key)
    return response['Body'].iter_lines()

def process_file(file_stream, cursor):
    for line in file_stream:
        line = line.decode("utf-8")
        print(f"linha: {line}")
        cliente_id, produto_id = line.strip().split(",")
        for table in TABLES:
          cursor.execute(f"UPDATE {table} SET product_id = %s WHERE client_id = %s;", (produto_id, cliente_id))

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        print(event)
        print(bucket)
        print(key)

        s3_client = boto3.client("s3")
        file_stream = get_file_stream(bucket, s3_client,key)

        config = get_config()
        connection = get_db_connection(config)
        cursor = connection.cursor()
        process_file(file_stream, cursor)
        connection.commit()
        cursor.close()
        connection.close()
        
      
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}
    
