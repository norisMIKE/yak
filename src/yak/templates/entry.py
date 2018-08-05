import asyncio
{% if rest %}import aiohttp_cors
{% endif %}
from aiohttp import web
from aiohttp_route import router
from {{ database }}.sa import create_engine

from {{ project_name }} import crud, db
from {{ project_name }}.middleware import error_middleware
from {{ project_name }}.settings import get_settings


async def get_app():

    middleware = [
        error_middleware
    ]

    settings = get_settings()
    app = web.Application(middlewares=middleware)
    app['settings'] = settings
    app['db'] = await create_engine(**settings['db'])

    routes = router(app, [crud])

    {% if rest %}cors = aiohttp_cors.setup(app, defaults={
        domain: aiohttp_cors.ResourceOptions(**options)
        for domain, options in settings['cors'].items()
    })

    for route in routes:
        cors.add(route){% endif %}

    return app


APP = get_app()
if __name__ == '__main__':
    web.run_app(APP, port=8080, host='127.0.0.1')
