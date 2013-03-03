import os
import uuid
from flask import Flask, request, render_template, jsonify, abort, session
from flask.ext.assets import Environment, Bundle
from flask_sslify import SSLify

from bucketier import Bucketier

app = Flask(__name__)
app.debug = os.environ.get('ENV', 'development') == 'development'
app.secret_key = os.environ.get('SECRET_KEY') or "Set a secret key plz"

SSLify(app)

# Assets

assets = Environment(app)
assets.url = "/static/"
assets.manifest = "file"
assets.debug = app.debug
assets.config['compass_plugins'] = ['bootstrap-sass']

assets.register('js', 'http://cdnjs.cloudflare.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                'http://cdnjs.cloudflare.com/ajax/libs/jquery.form/3.24/jquery.form.js',
                'http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/2.3.0/js/bootstrap.min.js',
                Bundle('js/app.coffee', filters='coffeescript', output='gen/app.js'),
                filters='closure_js', output='gen/app-%(version)s.js')

assets.register('css', 'css/app.scss', filters='compass,cssmin',
                output='gen/app-%(version)s.css')


# Helpers

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = str(uuid.uuid1())
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


# Filters

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.get('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


# Routes

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/buckets/create', methods=['POST'])
def create():
    bucketier = Bucketier(request.form.get('bucket-name'),
                          request.form.get('aws-key'),
                          request.form.get('aws-secret'))

    if bucketier.validate():
        try:
            bucketier.run()
            return jsonify({'status': True, 'bucket': bucketier.to_json()})
        except Bucketier.BucketierException as ex:
            # this should really be a non-200 status code
            print ex
            return jsonify({
                'status': False,
                'message': ex.message,
            })
    else:
        # this should really be a non-200 status code
        return jsonify({
            'status': False,
            'message': "Enter stuff in all the fields."
        })

# GO

if __name__ == '__main__':
    if app.debug:
        print "Starting in development mode"
        app.run(debug=True)
    else:
        port = int(os.environ.get('PORT', 5000))
        print "Starting in production mode on port %s" % port
        app.run(host='0.0.0.0', port=port)
