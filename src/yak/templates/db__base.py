import sqlalchemy as sa


meta = sa.MetaData()


async def query_db(engine, query):
    async with engine.acquire() as conn:
        return await conn.execute(query)

async def list_object(engine, table):
    result = await query_db(engine, meta.tables[table].select())
    return await result.fetchall()


async def detail_object(engine, table, id):
    tbl = meta.tables[table]
    result =  await query_db(
        engine,
        tbl.select().where(tbl.c.id == id),
    )
    return await result.fetchall()


async def delete_object(engine, table, id):
    tbl = meta.tables[table]
    await query_db(engine, tbl.delete().where(tbl.c.id == id))


async def update_object(engine, table, id, values):
    tbl = meta.tables[table]
    return await query_db(
        engine,
        tbl.update()
        .where(tbl.c.id == id)
        .values(**values)
    )


async def create_object(engine, table, values):
    tbl = meta.tables[table]
    return await query_db(
        engine,
        tbl.insert()
        .values(**values)
    )
