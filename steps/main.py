from asyncio import get_event_loop
from sys import exit as _exit
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from starlette_exporter import PrometheusMiddleware, handle_metrics
from uvicorn import Config, Server

from steps.config_reader import read_config
from steps.logic.posts import AsyncMongoPostsHandler
from steps.logic.statistics import AsyncMongoStatisticsHandler
from steps.routers.basic import create_basic_router
from steps.routers.posts import create_posts_router
from steps.routers.statistics import create_statistics_router


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
        self._database: Optional[AsyncIOMotorDatabase] = None

    def run(self):
        """
        Starts the api.
        """
        try:
            self._add_metrics()
            self._enable_cors()
            self._connect_to_database()
            self._add_routers()
            self._run_server()
        except:
            logger.critical("Cannot start steps api")
            _exit(1)

    def _add_metrics(self):
        """
        Adds Prometheus middleware for metrics
        :return:
        """
        self.app.add_middleware(PrometheusMiddleware)
        self.app.add_route("/metrics", handle_metrics)

    def _enable_cors(self):
        """
        Add cors middleware, allow all
        :return:
        """
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _connect_to_database(self):
        """
        Connect to mongodb.
        """
        try:
            client = AsyncIOMotorClient(self._database_config["connection_string"], uuidRepresentation="standard",
                                        ssl=True, ssl_cert_reqs='CERT_NONE')
            self._database = client[self._database_config["database"]]
        except Exception as err:
            logger.critical(
                f"Failed to {self._database_config['database']} mongo database"
                f" with {self._database_config['connection_string']} connection string - {err}")
            raise

    def _add_routers(self):
        """
        Add all routers to application.
        Each route contain business logic
        """
        try:
            self.app.include_router(router=create_basic_router(), tags=["Basic"])
            self.app.include_router(router=create_posts_router(AsyncMongoPostsHandler(self._database, "Posts"),
                                                               AsyncMongoStatisticsHandler(self._database, "Requests")),
                                    prefix="/posts",
                                    tags=["Posts"])
            self.app.include_router(router=create_statistics_router(AsyncMongoPostsHandler(self._database, "Posts"),
                                                                    AsyncMongoStatisticsHandler(self._database,
                                                                                                "Requests")),
                                    prefix="/stats",
                                    tags=["Statistics"])
        except Exception as err:
            logger.critical(f"Cannot add routers to api server - {err}")
            raise

    def _run_server(self):
        """
        Runs fastapi async http server
        """
        try:
            loop = get_event_loop()
            config = Config(self.app, host=self._host, port=self._port)
            server = Server(config)
            loop.run_until_complete(server.serve())
        except Exception as err:
            logger.critical(f"Cannot run fastapi async http server - {err}")
            raise


def main():
    """
    Reads configuration, create steps api and runs it.
    """
    config = read_config("./resources/config.json")
    server = config["server"]
    mongodb = config["mongodb"]
    api = StepsApi(mongodb, server["host"], server["port"])
    api.run()


if __name__ == '__main__':
    main()
