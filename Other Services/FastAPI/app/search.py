try:
    from .models import UserData
except:
    from models import UserData

from typing import List

SEARCH_COLUMNS = {
    'table_dataset1': ['full_name', 'email', 'phone'],
    'table_dataset3': ['name', 'email'],
    'table_dataset2': ['first_name', 'middle_name', 'last_name', 'phone'],
}
ALL_COLUMNS = {
    'table_dataset1': ['uid', 'full_name', 'email', 'address', 'sex', 'birthdate', 'phone'],
    'table_dataset2': ['uid', 'first_name', 'middle_name', 'last_name', 'birthdate', 'phone', 'address'],
    'table_dataset3': ['uid', 'name', 'email', 'birthdate', 'sex']
}

def search_table(client, table, pattern):
    res = []
    columns = SEARCH_COLUMNS[table]
    columns_str = ','.join(['uid'] + columns)
    like_expr = ' OR '.join(f'{i} LIKE \'{pattern}\'' for i in columns)
    with client.query_row_block_stream(f'''
            SELECT * FROM {table} WHERE {like_expr} LIMIT 30
        ''') as stream:
        for block in stream:
            for row in block:
                for col,val in zip(ALL_COLUMNS[table], row):
                    res.append(UserData(
                        table_number=int(table[-1]), 
                        field_name=col,
                        field_value=str(val), 
                        uid=str(row[0])))
    return res

def search(client, pattern) -> List[UserData]:
    res = []
    res += search_table(client, 'table_dataset1', pattern)
    res += search_table(client, 'table_dataset2', pattern)
    res += search_table(client, 'table_dataset3', pattern)
    return res

def search_uid(client, uid, table) -> List[UserData]:
    columns = ALL_COLUMNS[table]
    result = client.query(f"SELECT * FROM {table} WHERE uid=toUUID('{uid}')")
    row = result.result_rows[0]
    res = []
    for col,val in zip(columns, row):
        res.append(UserData(
            table_number=int(table[-1]),
            field_name=col,
            field_value=str(val),
            uid=str(uid)
        ))
    return res

async def search_results(client, uid, table) -> List[UserData]:
    uids = [[], [], []]
    with client.query_row_block_stream(
        f"SELECT * FROM table_results where arrayExists(x -> x = toUUID('{uid}'), id_is{table})"
    ) as stream:
        for block in stream:
            for t1,t2,t3 in block:
                uids[0] += t1
                uids[1] += t2
                uids[2] += t3
    uids[table-1].append(uid)
    return uids
