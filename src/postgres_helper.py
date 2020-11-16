import contextlib
import datetime as dt
import psycopg2
# import logging
from psycopg2.extras import NamedTupleCursor

from src import file_utils


table_name = 'sitemon'
table_schema = [
    ('id', 'serial PRIMARY KEY'),
    ('request_start_time', 'timestamp'),
    ('url', 'varchar(256)'),
    ('status_code', 'smallint'),
    ('response_time', 'integer'),  # probably, interval type may be better here, but i am not sure
    ('regexp', 'varchar(256)'),
    ('regexp_found', 'boolean'),
]
table_names = [i[0] for i in table_schema]


def _get_config(pgconfig_file_path):
    return file_utils.load_json(pgconfig_file_path)


def _execute_query(pgconfig_file_path, query):
    with contextlib.closing(psycopg2.connect(**_get_config(pgconfig_file_path))) as conn:
        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            print('executing query', query)
            cursor.execute(query)
            conn.commit()
            result = cursor.statusmessage
            print(f'Query "{query}" executed with result: {result}')
    return result


def prepare_db(pgconfig_file_path):
    schema = ', '.join(' '.join(i) for i in table_schema)
    _execute_query(pgconfig_file_path, f'DROP TABLE IF EXISTS {table_name};')
    return _execute_query(pgconfig_file_path, f'CREATE TABLE {table_name} ({schema});')


def store_batch_data(pgconfig_file_path, batch):
    batch_str = ', '.join(_convert_data(i) for i in batch)
    query = [
        f'INSERT INTO {table_name} ({", ".join(table_names[1:])}) VALUES {batch_str};',
    ]
    return _execute_query(pgconfig_file_path, ' '.join(query))


def _convert_data(data):
    ts = dt.datetime.fromtimestamp(data['request_start_time']).strftime("%Y-%m-%d %H:%M:%S.%f")
    mus = int(data['response_time'] * 1000000)
    regexp = 'NULL' if data.get('regexp') is None else f"'{data['regexp']}'"  # todo: extract helper func for this
    found = 'NULL' if data.get('regexp_found') is None else data['regexp_found']
    return f"(TIMESTAMP '{ts}', '{data['url']}', {data['status_code']}, {mus}, {regexp}, {found})"
