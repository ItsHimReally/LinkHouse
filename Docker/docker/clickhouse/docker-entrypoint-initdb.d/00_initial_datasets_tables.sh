#!/bin/bash

set -e
clickhouse client -n <<-EOSQL
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
EOSQL

set -e 
clickhouse client -n <<-EOSQL
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
EOSQL

set -e 
clickhouse client -n <<-EOSQL
CREATE OR REPLACE TABLE table_dataset3 (
    uid UUID,
    name String,
    email String,
    birthdate String,
    sex String
) ENGINE = MergeTree()
PARTITION BY murmurHash3_32(uid) % 8
ORDER BY uid;
EOSQL

set -e 
clickhouse client -n <<-EOSQL
CREATE OR REPLACE TABLE table_results (
    id_is1 Array(UUID),
    id_is2 Array(UUID),
    id_is3 Array(UUID)
) ENGINE = MergeTree()
ORDER BY id_is1;
EOSQL

clickhouse-client --query="INSERT INTO table_dataset1 FORMAT CSV" < /csv_files/main1.csv
clickhouse-client --query="INSERT INTO table_dataset2 FORMAT CSV" < /csv_files/main2.csv
clickhouse-client --query="INSERT INTO table_dataset3 FORMAT CSV" < /csv_files/main3.csv
