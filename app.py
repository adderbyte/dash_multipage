import dash
import os
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_caching import Cache

import flask


server = flask.Flask(__name__, template_folder='assets')

app = dash.Dash(__name__, suppress_callback_exceptions=True, eager_loading=True,
                server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/bWLwgP.css"])
server = app.server

# CACHE_CONFIG={
#     'CACHE_TYPE':'redis',
#     'CACHE_REDIS_URL': os.environ.get('REDIS_URL','redis://localhost:6379')
# }
CACHE_CONFIG = {
    'CACHE_TYPE': 'simple'
    #     'CACHE_REDIS_URL': os.environ.get('REDIS_URL','redis://localhost:6379')
}


cache = Cache()
cache.init_app(server, config=CACHE_CONFIG)

#app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# @app.server.route('/assets/<path:path>')
# def static_file(path):
#     static_folder = os.path.join(os.getcwd(), 'assets')
#     return send_from_directory(assets, path)
#server.secret_key=os.environ.get('SECRET_KEY', 'ajiskkjsdkjasfjaffjhsfdkjsfd')
