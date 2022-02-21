from app.src.extensions.database import Base, session


class BaseManager:
    model: Base

    @classmethod
    def create(cls, **kwargs) -> Base:
        with session() as db:
            obj = cls.model(**kwargs)
            db.add(obj)
            db.commit()
        return obj

    @classmethod
    def create_multiple_from_list(cls, list_of_kwargs: list[dict]) -> list[Base]:
        with session() as db:
            list_of_objects = []
            for data in list_of_kwargs:
                obj = cls.model(**data)
                list_of_objects.append(obj)
                db.add(obj)
            db.commit()
        return list_of_objects
