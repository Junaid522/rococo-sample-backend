from flask_restx import Namespace, Resource, fields
from app.helpers.decorators import login_required
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, \
    validate_required_fields
from flask import request
from common.app_config import config

from common.services import PersonService

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")

person_model = person_api.model('Person', {
    'first_name': fields.String(required=True, description='First name of person'),
    'last_name': fields.String(required=True, description='Last name of person'),
})


@person_api.route('/me')
class Me(Resource):

    @login_required()
    def get(self, person):
        return get_success_response(person=person)


@person_api.route('/me/<string:person_id>')  # This route is for updating a specific task
class PersonResource(Resource):
    @login_required()
    @person_api.expect(person_model)
    def put(self, person, person_id: str):
        """
        """
        data = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields({'first_name': data.get('first_name'), 'last_name': data.get('last_name')})

        person_service = PersonService(config)

        person = person_service.get_person_by_id(person.entity_id)

        if not person:
            return get_failure_response(message="User not found or not authorized.", status_code=404)

        person.first_name = data.get('first_name', person.first_name)
        person.last_name = data.get('last_name', person.last_name)
        person_service.save_person(person)
        return get_success_response(message="Personal Info updated successfully.", person=person)
