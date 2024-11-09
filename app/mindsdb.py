import mindsdb_sdk
import pandas as pd

# connects to the specified host and port
server = mindsdb_sdk.connect('http://127.0.0.1:47334')

# my_kb = server.knowledge_bases.create('my_kb')
my_kb = server.knowledge_bases.get('my_kb')

# insert data into a knowledge base from a file
my_kb.insert(pd.read_csv('file_name.csv'))

# insert data into a knowledge base from a database
my_kb.insert(server.databases.db_name.tables.table_name.filter(column_name='value'))

# insert data into a knowledge base
my_kb.insert({'column_name': 'value', 'column_name': 'value'})

kb_list = server.knowledge_bases.list()

# server.knowledge_bases.drop('my_kb')
