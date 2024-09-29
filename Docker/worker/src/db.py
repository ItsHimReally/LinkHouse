import os
import pathlib
import time

import clickhouse_connect
import clickhouse_connect.driver.client
import loguru


class Db:
    def __init__(self, base_path: pathlib.Path) -> None:
        self._base_path = base_path

        HOST = os.getenv("CLICKHOUSE_HOST", None)
        PORT = os.getenv("CLICKHOUSE_PORT", None)
        DB = os.getenv("CLICKHOUSE_DB", None)
        USER = os.getenv("CLICKHOUSE_USER", None)
        PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", None)

        assert (
            HOST is not None
            and PORT is not None
            and DB is not None
            and USER is not None
            and PASSWORD is not None
        ), "not all env variables are set"

        self.client: clickhouse_connect.driver.client.Client
        for attempt in range(360):
            try:
                self.client = clickhouse_connect.get_client(
                    host=HOST,
                    username=USER,
                    password=PASSWORD,
                    database=DB,
                    port=int(PORT),
                )
            except:
                loguru.logger.info(f"Attempt #{attempt} to connect to ClickHouse...")
                time.sleep(10)
                continue
            break
        else:
            raise RuntimeError("Waited for too long")

    def reinit_data(self) -> None:
        export_path = self._base_path / "init"
        export_path.mkdir(parents=True, exist_ok=True)

        tables = {
            "table_dataset1": "uid full_name email address phone",
            "table_dataset2": "uid phone address last_name middle_name first_name",
            "table_dataset3": "uid name email",
        }

        PROCESSING_LIMIT = os.getenv("PROCESSING_LIMIT")
        assert PROCESSING_LIMIT, "PROCESSING_LIMIT is not set!"
        loguru.logger.debug(f"PROCESSING_LIMIT is set to {PROCESSING_LIMIT}")

        if int(PROCESSING_LIMIT) <= 0:
            raise RuntimeError(f"PROCESSING_LIMIT can't be <= 0, but set to {PROCESSING_LIMIT}")

        for i, table in enumerate(tables.keys()):
            query = f"SELECT COUNT(*) FROM {table}"
            out = self.client.query(query).result_rows
            count = out[0][0]

            cols = ",".join(tables[table].split(" "))
            query = f"SELECT {cols} FROM {table}"
            
            if count > int(PROCESSING_LIMIT):
                query += f" ORDER BY rand() LIMIT {PROCESSING_LIMIT}"

            file_path = export_path / f"data{i+1}"
            with (
                file_path.open("wb") as f,
                self.client.raw_stream(query=query, fmt="CSVWithNames") as stream,
            ):
                for chunk in stream:
                    f.write(chunk)

    def insert_rows(self, rows: list[tuple[list[str], list[str], list[str]]]) -> None:
        self.client.insert("table_results", rows)
