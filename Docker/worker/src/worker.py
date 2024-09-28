import pathlib

import loguru

from .linker import Linker


class Worker:
    def __init__(self, base_path: pathlib.Path) -> None:
        self._base_path = base_path

        self.linker = Linker(base_path=base_path)

    @loguru.logger.catch()
    async def run(self) -> None:
        loguru.logger.info("Data reiniting in progress...")
        self.linker.db.reinit_data()
        loguru.logger.info("Data reiniting completed")

        loguru.logger.info("Data is loading...")
        self.linker.load_pl()
        loguru.logger.info("Data was loaded")

        loguru.logger.info("Linking data...")
        linked_data = self.linker.get_matches()
        loguru.logger.info("Data linkage completed")
        
        loguru.logger.info("Populating DB...")
        self.linker.populate_data(linked_data)
        loguru.logger.info("DB population completed")
