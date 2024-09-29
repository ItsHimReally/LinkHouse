import asyncio
import pathlib

import dotenv

from src import Worker


async def main() -> None:
    dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv())
    
    base_path = pathlib.Path("./.data/")
    
    worker = Worker(base_path=base_path)
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
