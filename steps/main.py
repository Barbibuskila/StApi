from asyncio import get_event_loop

from fastapi import FastAPI
from uvicorn import Config, Server

from steps.config_reader import read_config
from steps.routers.basic import create_basic_router


class StepsApi:
    def __init__(self, database_config, host: str, port: int):
        """
        :param database_config: Database configuration to retrieve data from
        :param host: Host of the api
        :param port: Port of the api
        """
        self.app = FastAPI()
        self._database_config = database_config
        self._host = host
        self._port = port

    def run(self):
        """
        Starts the api.
        """
        self._add_routers()
        self._run_server()

    def _add_routers(self):
        """
        Add all routers to application.
        Each route contain business logic
        """
        self.app.include_router(router=create_basic_router(), tags=["Basic router"])

    def _run_server(self):
        """
        Runs fastapi async http server
        """
        loop = get_event_loop()
        config = Config(self.app, host=self._host, port=self._port)
        server = Server(config)
        loop.run_until_complete(server.serve())




def main():
    config = read_config("./resources/config.json")
    server = config["server"]
    mongodb = config["mongodb"]
    api = StepsApi(mongodb, server["host"], server["port"])
    api.run()


if __name__ == '__main__':
    main()
