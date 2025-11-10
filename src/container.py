from typing import ClassVar
from dependency_injector import containers, providers
from src.config import Config


class AppContainer(containers.DeclarativeContainer):
    wiring_config: containers.WiringConfiguration = containers.WiringConfiguration(
        packages=["src"]
    )
    config: ClassVar[providers.Singleton[Config]] = providers.Singleton(Config)
