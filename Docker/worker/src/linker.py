from typing import Any
import pathlib

import polars as pl

from .db import Db


class Linker:
    def __init__(self, base_path: pathlib.Path) -> None:
        self._base_path = base_path

        self.db = Db(base_path=base_path)

    def load_pl(self) -> tuple[pl.LazyFrame, pl.LazyFrame, pl.LazyFrame]:
        self.import_path = self._base_path / "init"

        file1 = self.import_path / "data1"
        file2 = self.import_path / "data2"
        file3 = self.import_path / "data3"

        db1 = pl.scan_csv(file1).with_columns([
            pl.col("full_name")
                .str.to_lowercase()
                .str.replace_all(r"[^а-я ]", ""),

            pl.col("address")
                .str.to_lowercase()
                .str.replace_all(r"[^а-я0-9 ]", ""),

            pl.col("phone")
                .str.replace_all(r"[^0-9]", ""),
            pl.col("email").str.replace(r"@.*", "", literal=False).alias("email"),
            (pl.col("uid") + pl.lit("!db1")).alias("uid")
        ])

        db2 = pl.scan_csv(file2).with_columns([
            (pl.col("last_name") + " " + pl.col("first_name") + " " + pl.col("middle_name"))
                .str.to_lowercase()
                .str.replace_all(r"[^а-я\s]", "")
                .alias("full_name"),

            pl.col("address")
                .str.to_lowercase()
                .str.replace_all(r"[^а-я0-9 ]", ""),

            pl.col("phone")
                .str.replace_all(r"[^0-9]", ""),
            (pl.col("uid") + pl.lit("!db2")).alias("uid")
        ]).drop(["last_name", "middle_name", "first_name"])

        db3 = pl.scan_csv(file3).with_columns([
            pl.col("name")
                .str.to_lowercase()
                .str.replace_all(r"[^а-я ]", ""),

            pl.col("email").str.replace(r"@.*", "", literal=False).alias("email"),
            (pl.col("uid") + pl.lit("!db3")).alias("uid")
        ]).rename({"name": "full_name"})

        return (db1, db2, db3)

    def get_matches(self, pls: tuple[pl.LazyFrame, pl.LazyFrame, pl.LazyFrame]) -> pl.Series:
        db = pl.concat(*[pls], how="diagonal")

        address_matches = db.group_by("address").agg(
            [
                pl.col("uid").alias("uids"),
                pl.count("address").alias("count")
            ]
        ).filter(pl.col("count") > 1).select(["uids"]).collect()

        email_matches = db.group_by("email").agg(
            [
                pl.col("uid").alias("uids"),
                pl.count("email").alias("count")
            ]
        ).filter(pl.col("count") > 1).select(["uids"]).collect()

        db_filtered = db.filter(
            pl.col("phone").str.extract(r"(\d{11})", 1).is_not_null()
        )

        phone_matches = db_filtered.group_by("phone").agg(
            [
                pl.col("uid").alias("uids"),
                pl.count("phone").alias("count")
            ]
        ).filter(pl.col("count") > 1).select(["uids"]).collect()

        
        matches = pl.concat([email_matches, phone_matches, address_matches]).unique()["uids"]
        del email_matches, phone_matches, address_matches

        return matches

    def populate_data(self, linked_data: pl.Series) -> None:
        buffer = []
        for i, uids in enumerate(linked_data):
            ids1 = [uid[:-4] for uid in uids if uid.endswith("!db1")]
            ids2 = [uid[:-4] for uid in uids if uid.endswith("!db2")]
            ids3 = [uid[:-4] for uid in uids if uid.endswith("!db3")]
            
            row = (ids1, ids2, ids3)    
            buffer +=[row]

            if i % 10_000 == 0:
                self.db.insert_rows(buffer)
                buffer.clear()

        self.db.insert_rows(buffer)
        buffer.clear()
