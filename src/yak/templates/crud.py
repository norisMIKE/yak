from aiohttp import web
from aiohttp_route import route
from datetime import datetime

from {{ project_name }} import db


def format_value(value):
    if type(value) == datetime:
        return value.isoformat()
    else:
        return value


def format_response(results):
    # TODO: Decide on having a list or dict for data
    return web.json_response({
        'data': [
            {
                k: format_value(v)
                for k, v in result.items()
            }
            for result in results
        ]
    })


@route('GET', '/crud/{table}/')
async def read(request):
    return format_response(
        await db.list_object(
            request.app['db'],
            request.match_info['table'],
        )
    )


@route('GET', '/crud/{table}/{id}/')
async def detail(request):
    return format_response(
        await db.detail_object(
            request.app['db'],
            request.match_info['table'],
            request.match_info['id']
        )
    )


@route('DELETE', '/crud/{table}/{id}/')
async def delete(request):
    await db.delete_object(
        request.app['db'],
        request.match_info['table'],
        request.match_info['id']
    )
    return web.HTTPNoContent()


@route('PATCH', '/crud/{table}/{id}/')
async def update(request):
    body = await request.json()
    await db.update_object(
        request.app['db'],
        request.match_info['table'],
        request.match_info['id'],
        body
    )
    return web.HTTPNoContent()


@route('POST', '/crud/{table}/')
async def create(request):
    body = await request.json()
    await db.create_object(
        request.app['db'],
        request.match_info['table'],
        body
    )
    return web.HTTPCreated(headers={'Location': 'uid'})
