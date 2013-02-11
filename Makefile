init:
	rm -rf venv
	virtualenv venv --distribute --no-site-packages
	. venv/bin/activate && pip install -r requirements.txt
	gem install foreman
	gem install bootstrap-sass
	npm install -g coffee-script

# :(
run:
	compass watch static/ &
	coffee -cw static/javascripts &
	. venv/bin/activate && python app.py &

# do this before deploying if stuff has not been compiled via run
build:
	compass compile static/
	coffee -c static/javascripts
