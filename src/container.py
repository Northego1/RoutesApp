from dependency_injector import containers, providers

from core.container import InfrastructureContainer


class Container(containers.DeclarativeContainer):
    # wiring_config = containers.WiringConfiguration(packages=[".api"])

    infrastructure = providers.Container(InfrastructureContainer)

