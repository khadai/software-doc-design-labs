from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conn_str = 'mssql+pyodbc://DESKTOP-41S4H8F/lab2_docs?' \
           'trusted_connection=yes;driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)

Base = declarative_base()

