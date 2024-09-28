import os
import pathlib

import clickhouse_connect


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
            and PASSWORD is not None), (
            "not all env variables are set"
        )
        
        self.client = clickhouse_connect.get_client(
            host=HOST,
            username=USER,
            password=PASSWORD,
            database=DB,
            port=int(PORT),
        )
    
    def reinit_data(self) -> None:
        export_path = self._base_path / "init"
        export_path.mkdir(parents=True, exist_ok=True)
        
        tables = ["table_dataset1", "table_dataset2", "table_dataset3"]
        
        for i, table in enumerate(tables):
            query = f"SELECT * FROM {table}"
            file_path = export_path / f"main{i+1}.csv"
            with (
                file_path.open("wb") as f, 
                self.client.raw_stream(query=query, fmt="CSVWithNames") as stream,
            ):
                for chunk in stream:
                    f.write(chunk)

    def insert_row(self, row: tuple[list[str], list[str], list[str]]) -> None:
        self.client.insert("table_results", [row])
