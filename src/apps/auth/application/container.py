from dependency_injector import providers, containers


class AuthUsecaseContainer(containers.DeclarativeContainer):
    uow: providers.Dependency = providers.Dependency()


