BIN = $(PWD)/.venv3/bin
MANAGE = $(BIN)/python3 manage.py

debug: install
	$(MANAGE) runserver
	
install: .venv3
	$(MANAGE) migrate

test: install
	$(MANAGE) test fingerprints

.venv3: requirements.txt
	[ -d $@ ] || python3 -m venv $@
	$(BIN)/python3 -m pip install -U pip
	$(BIN)/pip3 install -r $<
	touch $@

clean:
	-find . -name \*.pyc -delete
	-find . -name __pycache__ -delete
