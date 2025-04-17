from common.repositories.factory import RepositoryFactory, RepoType
from common.models.todo import Todo


class TodoService:

    def __init__(self, config):
        self.config = config
        self.repository_factory = RepositoryFactory(config)
        self.todo_repo = self.repository_factory.get_repository(RepoType.TODO)

    def save_todo(self, todo: Todo):
        todo = self.todo_repo.save(todo)
        return todo

    def get_user_todos(self, person_id:str, filters: dict):
        filters = filters or {}
        filters['person_id'] = person_id
        return self.todo_repo.get_many(filters)

    def get_todo_by_id_and_person(self, todo_id: str, person_id: str):
        return self.todo_repo.get_one({"entity_id": todo_id, "person_id": person_id})

    def delete_todo(self, todo: Todo):
        return self.todo_repo.delete(todo)