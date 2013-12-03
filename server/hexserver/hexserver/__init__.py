from pyramid.config import Configurator
from pyramid.renderers import JSON

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('json', JSON(indent=4))

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('landing', '/')

    config.add_route('api_setup', '/api/setup')
    #config.add_route('api_backup', '/api/backup')

    config.add_route('api_create_user', '/api/users', request_method="POST")
    config.add_route('api_users', '/api/users')
    config.add_route('api_user_authenticate', 'api/users/authenticate', request_method="POST")
    config.add_route('api_user_show', '/api/users/{name}')
    config.add_route('api_create_spell', '/api/spells', request_method="POST")
    config.add_route('api_cast_spell', '/api/spells/run')
    config.add_route('show_spell', 'spells/{name}')
    config.add_route('api_spells', '/api/spells')
    config.add_route('test', '/test')

    config.scan()
    return config.make_wsgi_app()
