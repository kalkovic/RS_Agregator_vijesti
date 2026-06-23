import os
import time
import boto3
from botocore.exceptions import ClientError
from web3 import Web3

DYNAMODB_URL = os.getenv("DYNAMODB_URL", "http://dynamodb-local:8000")
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://ganache-cli:8545")

def wait_for_services():
    print("Čekam povezivanje s Ganache blockchainom...")
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
    while not w3.is_connected():
        time.sleep(2)
    print("Ganache je spreman!")

    print(f"Čekam povezivanje s DynamoDB Local na adresi: {DYNAMODB_URL}...")
    db_client = boto3.client(
        'dynamodb',
        endpoint_url=DYNAMODB_URL,
        region_name=os.getenv("AWS_DEFAULT_REGION", "eu-central-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "akiahubnews2026local"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "secretaccesskeyhubnews2026local"),
        aws_session_token=None # Eksplicitno onemogućavamo sesijske tokene
    )
    
    while True:
        try:
            db_client.list_tables()
            print("✅ DynamoDB je spreman!")
            return db_client
        except Exception as e:
            print(f"Pokušavam ponovno... Detalji greške: {e}")
            time.sleep(2)

def create_table_safely(db_client, table_name, key_schema, attribute_definitions):
    try:
        db_client.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"Tablica '{table_name}' uspješno kreirana!")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"ℹ Tablica '{table_name}' već postoji. Preskačem kreiranje.")
        else:
            print(f"❌ Greška pri kreiranju tablice {table_name}: {e}")

def main():
    db_client = wait_for_services()

    create_table_safely(
        db_client,
        table_name="Users",
        key_schema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'email', 'AttributeType': 'S'}]
    )

    create_table_safely(
        db_client,
        table_name="News",
        key_schema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'id', 'AttributeType': 'S'}]
    )

    create_table_safely(
        db_client,
        table_name="Analytics",
        key_schema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'id', 'AttributeType': 'S'}]
    )

    print("\nSve inicijalizacijske skripte su uspješno izvršene! Kontejner se gasi...")

if __name__ == "__main__":
    main()