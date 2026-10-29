PYTHON  = python3
VENV    = .venv
BIN     = $(VENV)/bin
REQS    = requirements.txt
APP     = app.py
# made after a successful install, so the packages are installed again only when requirements.txt changes
STAMP   = $(VENV)/.installed
RAW    = csv/osem_bike_data.csv

# Files the website needs (make check lists the missing ones)
FILES   = $(APP) $(REQS) prepare_data.py \
          tabs/__init__.py tabs/translation.py tabs/real_data.py tabs/routing.py \
          tabs/livability.py tabs/periods.py tabs/community_examples.py \
          tabs/home_tab.py tabs/map_tab.py tabs/community_tab.py tabs/rate_report_tab.py tabs/dashboard_tab.py \
          csv/area_centers.csv csv/heilbronn_area_ranking.csv csv/area_months.csv \
          csv/tracks.csv csv/data_info.json csv/bike_road_network_heilbronn.csv

# make / make install: check the files, create .venv and install the packages
# make run: start the website   make data: rebuild the csv/ tables from csv/osem_bike_data.csv
# make check: list missing files
# make clean: remove cache files   make fclean: also remove .venv   make re: fresh install

all: install

check:
	@missing=""; \
	for f in $(FILES); do [ -f "$$f" ] || missing="$$missing $$f"; done; \
	if [ -n "$$missing" ]; then echo "Missing in this folder:$$missing"; exit 1; fi; \
	echo "All project files are here."

$(STAMP): $(REQS)
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r $(REQS)
	touch $(STAMP)

install: check $(STAMP)

run: install
	$(BIN)/streamlit run $(APP)

data: $(STAMP)
	@[ -f $(RAW) ] || { echo "Missing $(RAW): download the openSenseMap export first"; exit 1; }
	$(BIN)/python prepare_data.py

clean:
	find . -path ./$(VENV) -prune -o -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .streamlit/cache

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all check install run data clean fclean re
