ARG TAG=22.8
FROM clickhouse/clickhouse-server:$TAG

COPY ./docker-entrypoint.sh /
COPY ./docker-entrypoint-initdb.d/* /docker-entrypoint-initdb.d/

EXPOSE 9000
EXPOSE 8123

ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]
