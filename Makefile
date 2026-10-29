PYTHON  = python3
VENV    = .venv
BIN     = $(VENV)/bin
REQS    = requirements.txt
APP     = app.py

# make / make install: create .venv and install the packages
# make run: start the website   make data: rebuild the csv/ tables from csv/osem_bike_data.csv
# make clean: remove cache files   make fclean: also remove .venv   make re: fresh install

all: install

$(BIN)/activate:
	$(PYTHON) -m venv $(VENV)

install: $(BIN)/activate $(REQS)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r $(REQS)

run: install
	$(BIN)/streamlit run $(APP)

data: install
	$(BIN)/python prepare_data.py

clean:
	find . -path ./$(VENV) -prune -o -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .streamlit/cache

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all install run data clean fclean re
