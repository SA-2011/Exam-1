import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
ps = os.getenv("password")

async def connection():
    try:
        con = await asyncpg.connect(
            database="Exam Bot 1",
            host="localhost",
            user="postgres",
            port=5432,
            password=ps
        )
        print("Conection OK")
        return con
    except Exception as error:
        print(f"Error in conection: {error}")

async def create_table():
    con = await connection()
    try:
        await con.execute("""

        create table if not exists sklad(
            sklad_id serial primary key,
            name varchar(100),
            creator varchar(100),
            created_at timestamp default now(),
            tg_id varchar
        );

        create table if not exists products(
            product_id serial primary key,
            product_name varchar(100),
            quantity int,
            tg_id varchar,
            sklad_id int references sklad(sklad_id),
            low_stock_threshold int
        );
        
        create table if not exists stock_movements(
            sm_id serial primary key,
            product_id int references products(product_id),
            change varchar(5) check(change = '+' or change = '-'),
            reason varchar(50) check(reason = 'restock' or reason = 'sell'),
            created_at timestamp default now()
        );
        """)
        print("Table created!")
    except Exception as error:
        print(f"Error in creating table: {error}")
    finally:
        await con.close()