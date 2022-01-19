from sqlalchemy import select, and_, Table, Column, Integer, String, ForeignKey, MetaData, create_engine, DateTime, delete, insert, update
import datetime

metadata = MetaData()

engine = create_engine(
    "postgresql+psycopg2://vwkpsapgezatjo:0707b3f5b76e2dcc9cb997d24e99eaa3332d7b160736f6ae6f56456ec103aa0e@ec2-52-213-119-221.eu-west-1.compute.amazonaws.com:5432/dbfhqn219nh3ea")

# Ниже объекты для управления базой данных и каждый отвечает за свою таблицу

Accounts = Table("Accounts", metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('balance', Integer(), nullable=False), )

Users = Table("Users", metadata,
              Column('id', Integer(), primary_key=True),
              Column('login', String(100), unique=True, nullable=False),
              Column("password", String(100), nullable=False),
              Column("account_id", Integer(), ForeignKey('Accounts.id'),
                     nullable=False),
              )

Transactions = Table("Transactions", metadata,
                     Column("id", Integer(), primary_key=True),
                     Column("account_id_from", Integer(),
                            ForeignKey('Accounts.id'),
                            nullable=False),
                     Column("account_id_to", Integer(),
                            ForeignKey('Accounts.id'),
                            nullable=False),
                     Column("amount", Integer(),
                            nullable=False),
                     Column("comment", String(100)),
                     Column("time", DateTime(), default=datetime.datetime.utcnow)
                     )

Projects = Table("Projects", metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('name', String(100), unique=True, nullable=False),
                 Column("password", String(100), nullable=False),
                 Column("User", Integer(), ForeignKey('Users.id'), unique=True, nullable=False),
                 Column("account_id", Integer(), ForeignKey('Accounts.id'),
                        nullable=False),
                 )

Skins = Table("Skins", metadata,
              Column("id", Integer(), primary_key=True),
              Column("skin_Name", String(100), nullable=False),
              Column("user_id", Integer(), ForeignKey('Users.id'), nullable=False))

metadata.create_all(engine)

conn = engine.connect()
r = conn.execute(select([Skins.c.skin_Name]).where(Skins.c.user_id == 1))
print(*r.all(), sep="\n")
