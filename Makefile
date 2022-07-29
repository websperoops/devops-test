stop-all-docker:
	docker stop $$(docker ps -a -q)