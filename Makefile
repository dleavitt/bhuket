init:
	rm -rf venv
	virtualenv venv --distribute --no-site-packages
	. venv/bin/activate && pip install -r requirements.txt
	gem install foreman
	gem install compass
	gem install bootstrap-sass
	npm install -g coffee-script

# :(
run:
	. venv/bin/activate && python app.py