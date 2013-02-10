import os
import uuid
from redis import StrictRedis
from flask import Flask, request, render_template, g, jsonify, abort, session

from bucketier import Bucketier

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or "Set a secret key plz"


redis_uri = os.environ.get('REDISTOGO_URL')
if redis_uri:
    r = StrictRedis.from_url(redis_uri)
else:
    r = StrictRedis()

Bucketier.redis = r


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


@app.route('/buckets/create', methods=['POST', 'GET'])
def create():
    bucketier = Bucketier(request.form.get('bucket-name'),
        request.form.get('aws-key'), request.form.get('aws-secret'))

    if bucketier.validate():
        try:
            bucketier.run()
            return jsonify({'status': True, 'job': bucketier.to_json()})
        except StandardError as ex:
            return jsonify({
                'status': False,
                'message': "There was an error. Bad AWS Creds?",
                'error': ex.message
            })

    else:
        # this should really be a non-200 status code
        return jsonify({
            'status': False,
            'message': "Enter stuff in all the fields."
        })

# GO

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
