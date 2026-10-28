PYTHON  = python3
VENV    = .venv
BIN     = $(VENV)/bin
REQS    = requirements.txt
APP     = app.py

all: install

$(BIN)/activate:
	$(PYTHON) -m venv $(VENV)

install: $(BIN)/activate $(REQS)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r $(REQS)

run: install
	$(BIN)/streamlit run $(APP)

clean:
	rm -rf __pycache__ .streamlit/cache

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all install run clean fclean re
