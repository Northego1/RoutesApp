from dependency_injector import containers, providers

from apps.auth.application.container import UsecaseContainer
from apps.auth.presentation.container import PresentationContainer
from core.container import InfrastructureContainer


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["api.v1", "core.middlewares"])

    infrastructure = providers.Container(InfrastructureContainer)

    usecases = providers.Container(
        UsecaseContainer,
        uow=infrastructure.uow,
    )

    presentation = providers.Container(
        PresentationContainer,
        usecases=usecases,
    )

