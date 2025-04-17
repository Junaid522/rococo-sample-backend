from flask_restx import Namespace, Resource, fields
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.models.todo import Todo
from common.services import TodoService

todo_api = Namespace('todo', description="Todo related APIs")

todo_model = todo_api.model('Todo', {
    'title': fields.String(required=True, description='The title of the Todo task'),
    'description': fields.String(description='Description of the Todo task'),
    'is_completed': fields.Boolean(description='Todo task completed status'),
})


@todo_api.route('/task')
class Todos(Resource):
    @login_required()
    @todo_api.expect(todo_model)
    def post(self, person):
        todo_body = parse_request_body(request, ['title', 'description', 'is_completed'])
        validate_required_fields({'title': todo_body.get('title')})

        todo_service = TodoService(config)
        todo = Todo(
            title=todo_body['title'],
            description=todo_body.get('description', None),
            person_id=person.entity_id
        )

        todo_service.save_todo(todo)
        return get_success_response(message="Todo task Created.", todo=todo)

    @login_required()
    def get(self, person):
        filter_type = request.args.get('filter_type', type=str)

        todo_service = TodoService(config)
        filters = {'person_id': person.entity_id}

        if filter_type is not None:
            if filter_type.lower() == 'incomplete':
                filters['is_completed'] = False
            elif filter_type.lower() == 'completed':
                filters['is_completed'] = True
            elif filter_type.lower() == 'all':
                pass
            else:
                return get_failure_response(message="'filter_type' must be 'all', 'incomplete', or 'completed'.",
                                            status_code=400)

        todos = todo_service.get_user_todos(person.entity_id, filters)
        return get_success_response(message="Fetched filtered Todo tasks.", data=todos)

@todo_api.route('/task/<string:todo_id>')
class TodoResource(Resource):
    @login_required()
    @todo_api.expect(todo_model)
    def put(self, person, todo_id: str):

        todo_body = parse_request_body(request, ['title', 'description', 'is_completed'])
        validate_required_fields({'title': todo_body.get('title'), 'is_completed': todo_body.get('is_completed')})

        todo_service = TodoService(config)

        todo = todo_service.get_todo_by_id_and_person(todo_id, person.entity_id)

        if not todo:
            return get_failure_response(message="Todo task not found or not authorized.", status_code=404)

        todo.title = todo_body.get('title', todo.title)
        todo.description = todo_body.get('description', todo.description)
        todo.is_completed = todo_body.get('is_completed', todo.is_completed)

        todo_service.save_todo(todo)

        return get_success_response(message="Todo task updated successfully.", todo=todo)

    @login_required()
    def delete(self, person, todo_id: str):

        todo_service = TodoService(config)

        todo = todo_service.get_todo_by_id_and_person(todo_id, person.entity_id)

        if not todo:
            return get_failure_response(message="Todo task not found or not authorized.", status_code=404)

        todo_service.delete_todo(todo)

        return get_success_response(message="Todo task deleted successfully.")