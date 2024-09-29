import clickhouse_connect
import dotenv
from os import getenv
from clickhouse_connect.driver.tools import insert_file

dotenv.load_dotenv(dotenv.find_dotenv())


def client(database="default"):
    host = getenv("CLICKHOUSE_HOST")
    username = getenv("CLICKHOUSE_UNAME")
    password = getenv("CLICKHOUSE_PWD")

    assert username != None
    assert password != None

    return clickhouse_connect.get_client(
        host=getenv("CLICKHOUSE_HOST") or "localhost",
        username=username,
        password=password,
        database=database,
    )


def create_tables(client):
    client.command(
        """
        CREATE OR REPLACE TABLE table_dataset1 (
            uid UUID,
            full_name String,
            email String,
            address String,
            sex String,
            birthdate String,
            phone String
        ) ENGINE = MergeTree()
        PARTITION BY murmurHash3_32(uid) % 8
        ORDER BY uid;
    """
    )

    client.command(
        """
        CREATE OR REPLACE TABLE table_dataset2 (
            uid UUID,
            first_name String,
            middle_name String,
            last_name String,
            birthdate String,
            phone String,
            address String
        ) ENGINE = MergeTree()
        PARTITION BY murmurHash3_32(uid) % 8
        ORDER BY uid;
    """
    )

    client.command(
        """
        CREATE OR REPLACE TABLE table_dataset3 (
            uid UUID,
            name String,
            email String,
            birthdate String,
            sex String
        ) ENGINE = MergeTree()
        PARTITION BY murmurHash3_32(uid) % 8
        ORDER BY uid;
    """
    )


def load_data(client):
    create_tables(client)

    insert_file(client, "table_dataset1", "../public/main1.csv")
    insert_file(client, "table_dataset2", "../public/main2.csv")
    insert_file(client, "table_dataset3", "../public/main3.csv")
