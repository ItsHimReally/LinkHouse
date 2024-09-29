from typing import Any, List, Optional
import os

from fastapi import FastAPI, Request, Response
from .models import UserData
import dotenv

import app.clickhouse as ch
import app.search as srch

from random import randrange

dotenv.load_dotenv(dotenv.find_dotenv())


app = FastAPI()


@app.get("/api/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello from FastAPI!"}


@app.get("/api/search")
async def search(q: Optional[str]=None, uid: Optional[str]=None, table: Optional[int]=None) -> List[UserData]:
    c = ch.client()
    if not uid:
        return [i for i in srch.search(c, f'%{q}%') if i.field_name in ['name', 'full_name']]
    else:
        res = [[], [], []]
        u1, u2, u3 = await srch.search_results(c, uid, table)
        for i in u1:
            res[0] += srch.search_uid(c, i, 'table_dataset1')
        for i in u2:
            res[1] += srch.search_uid(c, i, 'table_dataset2')
        for i in u3:
            res[2] += srch.search_uid(c, i, 'table_dataset3')
        return res[0] + res[1] + res[2]

    return [
        UserData(table_number=1, field_name='phone', field_value='8(800)555 35-35'),
        UserData(table_number=2, field_name='address', 
                 field_value='г. Урус-Мартан, пер. Шмидта, д. 233 к. 6/4, 635846'),
        UserData(table_number=3, field_name='last_name', field_value='БAЛKИБАEВ')
    ]

@app.get("/api/random")
async def random_client() -> Any:
    c = ch.client()
    num = randrange(1, 3)
    result = c.query(f'''
        SELECT id_is{num} FROM table_results WHERE length(id_is{num}) >= 1 ORDER BY rand() LIMIT 1
    ''')
    uid = str(result.result_rows[0][0][0])
    return {
        'uid': uid,
        'table': num
    }
