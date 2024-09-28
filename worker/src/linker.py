from typing import Any
import pathlib

import polars as pl

from .db import Db


class Linker:
    def __init__(self, base_path: pathlib.Path) -> None:
        self._base_path = base_path

        self.db = Db(base_path=base_path)

        self.lf_db1: pl.LazyFrame
        self.lf_db2: pl.LazyFrame
        self.lf_db3: pl.LazyFrame

    def load_pl(self) -> None:
        self.import_path = self._base_path / "init"

        self.lf_db1 = (
            pl.scan_csv(self.import_path / "main1.csv")
            .with_columns(
                [
                    pl.col("full_name")
                    .str.to_lowercase()
                    .str.replace_all(r"[^а-я ]", ""),
                    pl.col("address")
                    .str.to_lowercase()
                    .str.replace_all(r"[^а-я0-9 ]", ""),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_0")
                    .alias("year"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_1")
                    .alias("month"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_2")
                    .alias("day"),
                    pl.when(pl.col("sex") == "m")
                    .then(0)
                    .when(pl.col("sex") == "f")
                    .then(1)
                    .otherwise(pl.col("sex"))
                    .cast(pl.Int64)
                    .alias("sex"),
                    pl.col("phone").str.replace_all(r"[^0-9]", ""),
                    pl.col("email")
                    .str.replace(r"@.*", "", literal=False)
                    .alias("email"),
                    (pl.col("uid") + pl.lit("!db1")).alias("uid"),
                ]
            )
            .drop("birthdate")
        )

        self.lf_db2 = (
            pl.scan_csv(self.import_path / "main2.csv")
            .with_columns(
                [
                    (
                        pl.col("first_name")
                        + " "
                        + pl.col("middle_name")
                        + " "
                        + pl.col("last_name")
                    )
                    .str.to_lowercase()
                    .str.replace_all(r"[^а-я\s]", "")
                    .alias("full_name"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_0")
                    .alias("year"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_1")
                    .alias("month"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_2")
                    .alias("day"),
                    pl.col("address")
                    .str.to_lowercase()
                    .str.replace_all(r"[^а-я0-9 ]", ""),
                    pl.col("phone").str.replace_all(r"[^0-9]", ""),
                    (pl.col("uid") + pl.lit("!db2")).alias("uid"),
                ]
            )
            .drop(["birthdate", "last_name", "middle_name", "first_name"])
        )

        self.lf_db3 = (
            pl.scan_csv(self.import_path / "main3.csv")
            .with_columns(
                [
                    pl.col("name").str.to_lowercase().str.replace_all(r"[^а-я ]", ""),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_0")
                    .alias("year"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_1")
                    .alias("month"),
                    pl.col("birthdate")
                    .str.split_exact("-", 2)
                    .struct.field("field_2")
                    .alias("day"),
                    pl.when(pl.col("sex") == "m")
                    .then(0)
                    .when(pl.col("sex") == "f")
                    .then(1)
                    .otherwise(pl.col("sex"))
                    .cast(pl.Int64)
                    .alias("sex"),
                    pl.col("email")
                    .str.replace(r"@.*", "", literal=False)
                    .alias("email"),
                    (pl.col("uid") + pl.lit("!db3")).alias("uid"),
                ]
            )
            .drop("birthdate")
            .rename({"name": "full_name"})
        )

    def get_matches(self) -> list[Any]:
        merged_lazy_df = pl.concat(
            (
                self.lf_db1,
                self.lf_db2,
                self.lf_db3,
            ),
            how="diagonal",
        )

        db_filtered_lazy = merged_lazy_df.filter(
            pl.col("phone").str.extract(r"(\d{11})", 1).is_not_null()
        )

        email_matches = (
            db_filtered_lazy.group_by("email")
            .agg([pl.col("uid").alias("uids"), pl.count().alias("count")])
            .filter(pl.col("count") > 1)
            .select(["uids"])
            .collect()
        )

        phone_matches = (
            db_filtered_lazy.group_by("phone")
            .agg([pl.col("uid").alias("uids"), pl.count().alias("count")])
            .filter(pl.col("count") > 1)
            .select(["uids"])
            .collect()
        )

        matches = list(email_matches["uids"]) + list(phone_matches["uids"])
        return matches

    def populate_data(self, linked_data: list[Any]) -> None:
        for uids in linked_data:
            ids1 = [uid[:-4] for uid in uids if uid.endswith("!db1")]
            ids2 = [uid[:-4] for uid in uids if uid.endswith("!db2")]
            ids3 = [uid[:-4] for uid in uids if uid.endswith("!db3")]
            
            row = (ids1, ids2, ids3)    

            self.db.insert_row(row)
