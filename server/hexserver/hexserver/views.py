from pyramid.view import view_config, view_defaults
import pyramid.httpexceptions as exc
from models.db import create_db
from models.user import create_user, get_user, get_users, increment_user_score, spell_duration
from models.spell import get_current_spells, create_spell, mark_spell_complete, get_spell_by_time
import sqlite3
from hex_driver import HexDriver
import json
import logging
import pika

log = logging.getLogger(__name__)

@view_config(route_name='landing', renderer='templates/landing.jinja2')
def landing(request):
    return {}

def expect_json(view_callable):
    "A decorator which checks that the request came with json"
    def new_view_callable(self):
        if hasattr(self.request, 'json_body'):
            return view_callable(self)
        else:
            return {'result': 'ERROR', 
                    'message': 'The API expects json in the body and Content-Type: application/json'}
    new_view_callable.__name__ = view_callable.__name__
    return new_view_callable

@view_config(route_name='show_current_spell', renderer='templates/spell/view.jinja2')
def show_current_spell(request):
    currentSpell = get_current_spells(request).get('current')
    return {'request': request, 'spell': currentSpell}

@view_config(route_name='show_spell', renderer='templates/spell/view.jinja2')
def show_spell(request):
    spell = get_spell_by_time(request, request.matchdict['cast_time'])
    if spell:
        return {'request': request, 'spell': spell}
    else:
        raise exc.HTTPNotFound()

@view_defaults(renderer='json')
class ApiViews(object):

    def __init__(self, request):
        self.request = request
    
    @view_config(route_name='api_setup')
    @expect_json
    def api_setup(self):
        if self.request.json_body.get('password') == self.request.registry.settings['setup.password']:
            create_db(self.request)
            return self.ok()
        else:
            return self.error("Invalid setup password")

    @view_config(route_name='api_spells')
    def api_spells(self):
        return get_current_spells(self.request)
    
    @view_config(route_name='api_users')
    def api_users(self):
        users = get_users(self.request)
        return self.ok({'users': [self.format_user(user) for user in users]})

    @view_config(route_name='api_user_show')
    def api_user_show(self):
        user = get_user(self.request, self.request.matchdict['name'])
        if user:
            return self.ok({'user': self.format_user(user)})
        else:
            return self.error("No such user")
    
    @view_config(route_name='api_user_authenticate')
    @expect_json
    def api_user_authenticate(self):
        name = self.request.json_body.get('name', '')
        animal = self.request.json_body.get('spirit_animal', '')
        user = get_user(self.request, name, animal)
        if user:
            return self.ok({'user':self.format_user(user)})
        else:
            return self.error("Username or animal were not correct")
    
    @view_config(route_name='api_create_user')
    @expect_json
    def api_create_user(self):
        log.debug("IN CREATE USER")
        log.debug(self.request.json_body)
        newUser = create_user(self.request, self.request.json_body)
        log.debug(newUser)
        if newUser:
            return self.ok({'user': self.format_user(newUser)})
        else:
            return self.error("Invalid user")

    @view_config(route_name='api_create_spell')
    @expect_json
    def api_create_spell(self):
        newSpellRaw = create_spell(self.request, self.request.json_body)
        if newSpellRaw:
            newSpell = self.format_spell(newSpellRaw)
            connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='hex')
            channel.basic_publish(exchange='', routing_key='hex',
                      body=json.dumps(newSpell))
            connection.close()
            return self.ok({'spell': newSpell})
        else:
            return self.error("Invalid spell")

    @view_config(route_name='api_confirm_spell_cast')
    def api_confirm_spell_cast(self):
        log.info("Comfirming that spell %s ran" % self.request.matchdict['cast_time'])
        log.info(self.request.matchdict)
        castSpell = get_spell_by_time(self.request, self.request.matchdict['cast_time'])
        if castSpell:
            mark_spell_complete(self.request, castSpell[3])
            increment_user_score(self.request, castSpell[0])

    def ok(self, payload=None):
        response = {'result': 'OK'}
        if payload:
            response.update(payload)
        return response

    def error(self, message="Invalid request"):
        return {'result': 'ERROR', 'message': message}

    def format_user(self, user):
        return {'name': user[0], 'points': user[2], 'spell_duration': spell_duration(user[2])}
    
    def format_spell(self, spell):
        user = self.format_user(get_user(self.request, spell[0]))
        setup = json.loads(spell[4]) if spell[4] else None
        loop = json.loads(spell[5]) if spell[5] else None
        return {
            'user_name': spell[0],
            'name': spell[1],
            'priority': spell[2],
            'cast_time': spell[3],
            'setup': setup,
            'loop': loop,
            'complete': spell[6],
            'spell_duration': user['spell_duration']
        }

