from connection import connection

async def create_sklad(creator , tg_id , name):
    try:
        con = await connection()
        await con.execute("""
        insert into sklad(creator , tg_id , name) values
        ($1 , $2 , $3);
        """ , creator , str(tg_id) , name)
        print("Sklad created!")
    except Exception as error:
        print(f"Erro in creating sklad: {error}")
    finally:
        await con.close()

async def see_my_sklads(tg_id):
    try:
        con = await connection()
        show_sklads = await con.fetch("""
        select * from sklad where tg_id = $1
        """ , str(tg_id))
        print("Sklad showed")
        return show_sklads
    except Exception as error:
        print(f"Error in showing sklad: {error}")

async def add_product(product_name , quantity , low_stock_threshold , tg_id , sklad_id):
    try:
        con = await connection()
        await con.execute("""
        insert into products (product_name , quantity , low_stock_threshold , tg_id , sklad_id) values
        ($1 , $2 , $3 , $4 , $5);
        """ , product_name , quantity , low_stock_threshold , str(tg_id) , int(sklad_id))
        print("Product Added")
    except Exception as error:
        print(f"Erro in adding product: {error}")
    finally:
        await con.close()

async def products(tg_id , sklad_name):
    try:
        con = await connection()
        show_pr = await con.fetch("""
        select product_name , quantity from products
        join sklad on sklad.tg_id = products.tg_id
        where products.tg_id = $1 and sklad.name = $2
        """ , str(tg_id) , sklad_name)
        print("Products shown")
        return show_pr
    except Exception as error:
        print(f"Error in products {error}")
    finally:
        await con.close()


async def restock(product_name , added_quantity , tg_id , sklad_id):
    try:
        con = await connection()
        await con.execute("""
        update products
        set quantity = quantity + $1
        where product_name = $2 and tg_id = $3 and sklad_id = $4
        """ , int(added_quantity) , product_name , str(tg_id) , int(sklad_id))
        print("""
        update products
        set quantity = quantity + $1
        where product_name = $2 and tg_id = $3 and sklad_id = $4
        """ , int(added_quantity) , product_name , str(tg_id) , int(sklad_id))

        print("Quantity added")
    except Exception as error:
        print(f"Error in adding quantity: {error}")
    finally:
        await con.close()

async def sell(product_name , removed_quantity , tg_id , sklad_id):
    try:
        con = await connection()
        await con.execute("""
        update products
        set quantity = quantity - $1
        where product_name = $2 and tg_id = $3 and sklad_id = $4
        """ , int(removed_quantity) , product_name , str(tg_id) , int(sklad_id))
        print("Quantity removed")
    except Exception as error:
        print(f"Error in removing quantity: {error}")
    finally:
        await con.close()

async def low_stock(tg_id , sklad_name):
    try:
        con = await connection()
        low_s = await con.fetch("""
        select products.* , sklad.name from products
        join sklad on sklad.sklad_id = products.sklad_id
        where quantity < low_stock_threshold and products.tg_id = $1 and sklad.name = $2
        """ , str(tg_id) , sklad_name)
        print("Low stock quantity showed")
        return low_s
    except Exception as error:
        print(f"Error in low stock: {error}")
    finally:
        await con.close()