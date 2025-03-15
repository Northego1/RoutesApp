from dependency_injector import containers, providers

from apps.auth.application.usecases.get_me_usecase import GetMeUsecase
from apps.auth.application.usecases.login_usecase import LoginUsecase
from apps.auth.application.usecases.refresh_jwt_usecase import RefreshJwtUsecase
from apps.auth.application.usecases.register_usecase import RegisterUsecase
from apps.auth.infrastructure.utils.security import Security


class UsecaseContainer(containers.DeclarativeContainer):
    uow: providers.Dependency = providers.Dependency()

    security = providers.Singleton(Security)

    login_usecase = providers.Factory(
        LoginUsecase,
        uow=uow,
        security=security,
    )

    register_usecase = providers.Factory(
        RegisterUsecase,
        uow=uow,
        security=security,
    )

    refresh_jwt_usecase = providers.Factory(
        RefreshJwtUsecase,
        uow=uow,
        security=security,
    )

    get_me_usecase = providers.Factory(
        GetMeUsecase,
        uow=uow,
        security=security,
    )
