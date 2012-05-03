client:
	./run_client.py

profile-client:
	python -m cProfile run_client.py -s

server:
	./run_server.py

test:
	./run_tests_with_coverage.sh