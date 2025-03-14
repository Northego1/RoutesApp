from dependency_injector import containers, providers

from apps.auth import presentation as pres


class PresentationContainer(containers.DeclarativeContainer):
    usecases: providers.DependenciesContainer = providers.DependenciesContainer()

    get_user = providers.Factory(
        pres.GetUserController,
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
    )
    update = providers.Factory(
        pres.UpdateUserController,
    )
