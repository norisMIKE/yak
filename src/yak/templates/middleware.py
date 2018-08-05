from aiohttp import web
from json.decoder import JSONDecodeError
from {{ database }} import IntegrityError


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except (IntegrityError, JSONDecodeError) as err:
        raise web.HTTPBadRequest(str(err))
    return response
