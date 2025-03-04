from dependency_injector import containers, providers

from core.config import settings
from core.database import DataBase
from core.uow import UnitOfWork


class InfrastructureContainer(containers.DeclarativeContainer):
    db = providers.Singleton(DataBase, settings.db.dsn)

    uow = providers.Factory(UnitOfWork, db)
