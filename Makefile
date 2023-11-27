get_data:
	rm -f database.db
	touch database.db
	python3 load_data/create_tables.py
	python3 load_data/load_data.py
	python3 load_data/visualization.py

get_parameters:
	python3 load_data/MLE.py
	python3 load_data/simulation.py

simul:
	rm -f *.json
	python3 simulation/generate_initial_data.py
	python3 simulation/get_simulation_data.py
	python3 simulation/us_map.py
