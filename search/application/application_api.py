from flask import Blueprint
from flask_restful import reqparse
from common.common import from_view_dict, json_response
from application.application import new_application
from application.application import all_applications
from application.application import application_detail
from application.application import delete_application
from application.application import patch_application
from application.application import entities_list
from application.application import delete_entity
from application.upload import upload
from application.search import search


application = Blueprint("application", __name__)


@application.route("/")
@json_response
def application_list_api():
    return all_applications()


@application.route("/<name>")
@json_response
def application_detail_api(name):
    return application_detail(name)


@application.route("/<name>", methods=['POST'])
@json_response
def new_application_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict, required=True). \
        add_argument("s3Buckets", type=str, required=True). \
        parse_args()
    args = from_view_dict(args)
    args['name'] = name
    return new_application(**args)


@application.route("/<name>", methods=['DELETE'])
@json_response
def delete_application_api(name):
    return delete_application(name)


@application.route("/<name>", methods=['PATCH'])
@json_response
def patch_pipeline_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict, required=True). \
        add_argument("s3Buckets", type=str, required=True). \
        parse_args()
    args = from_view_dict(args)
    args['name'] = name
    return patch_application(**args)


@application.route("/<name>/search", methods=['POST'])
@json_response
def application_do_search_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict, required=True). \
        add_argument("topk", type=int, required=True). \
        add_argument("nprobe", type=int, required=True). \
        parse_args()
    args = from_view_dict(args)
    return search(name, fields=args['fields'], topk=args['topk'], nprobe=args['nprobe'])


@application.route("/<name>/upload", methods=["POST"])
@json_response
def application_do_upload_api(name):
    args = reqparse.RequestParser(). \
        add_argument("fields", type=dict). \
        add_argument("targetFields", type=dict). \
        parse_args()
    args = from_view_dict(args)
    return upload(name, **args)


@application.route("/<app_name>/entity")
@json_response
def entities_list_api(app_name):
    args = reqparse.RequestParser(). \
        add_argument("num", type=int, default=10). \
        add_argument("page", type=int, default=0). \
        parse_args()
    args = from_view_dict(args)
    num = args['num']
    page = args['page']
    return entities_list(app_name, num, page)


@application.route("/<app_name>/entity/<entity_name>", methods=["DELETE"])
@json_response
def delete_entity_api(app_name, entity_name):
    return delete_entity(app_name, entity_name)