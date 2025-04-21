from models.short_url import ShortURL as ShortURLModel
from schemas.short_url import ShortURLCreate, ShortURLUpdate

from .base import RepositoryDB


class RepositoryShortURL(RepositoryDB[ShortURLModel, ShortURLCreate, ShortURLUpdate]):
    pass


short_url_crud = RepositoryShortURL(ShortURLModel)
