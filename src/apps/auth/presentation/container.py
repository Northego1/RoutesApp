from dependency_injector import containers, providers

from apps.auth import presentation as pres


class PresentationContainer(containers.DeclarativeContainer):
    usecases: providers.DependenciesContainer = providers.DependenciesContainer()

    get_me = providers.Factory(
        pres.GetMeController,
        usecases.get_me_usecase,
    )
    login = providers.Factory(
        pres.LoginController,
        usecases.login_usecase,
    )
    logout = providers.Factory(
        pres.LogoutController,
    )
    register = providers.Factory(
        pres.RegisterController,
        usecases.register_usecase,
    )
    refresh_jwt = providers.Factory(
        pres.RefreshController,
        usecases.refresh_jwt_usecase,
    )
    update = providers.Factory(
        pres.UpdateUserController,
    )
