ALICE = python main.py alice
BOB = python main.py bob
LOCAL = python main.py local

default:
	@echo Hi, you can execute make bob in order to start the server.
	@echo Then open another terminal and execute make alice.

clean:
	rm -rf __pycache__

alice:
	${ALICE} -c circuit/add.json

bob:
	${BOB}

local:
	${LOCAL} -c circuit/add.json
