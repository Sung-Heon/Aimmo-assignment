from flask import Blueprint, make_response, jsonify
from flask import request, jsonify
from service import post_service
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def hello_world():
    return 'Hello! blueprint'


@bp.route('/create', methods=['POST'])
@jwt_required()
def create():
    current_user_id = get_jwt_identity()
    body = request.get_json()
    id = post_service.create_post(body["title"], body["content"], current_user_id)
    return make_response(jsonify(msg='success', status_code=201, id=str(id)), 201)


@bp.route('/posts', methods=['GET'])
def read_post_list():
    page = request.args.get('page', type=int, default=1)
    post_list = post_service.read_post_list(page)
    return make_response(jsonify(post_list))


@bp.route('/posts/<id>', methods=['GET'])
def read_detail(id):
    post = post_service.read_post_detail(id)
    return make_response(jsonify(post))


@bp.route('/posts/<id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update(id):
    current_user_id = get_jwt_identity()
    body = request.get_json()
    if post_service.update_post(id, body["title"], body["content"], current_user_id):
        return make_response(jsonify(msg='update_success', status_code=201, id=str(id)), 201)
    return make_response(jsonify(msg="권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요", status_code=401), 401)


@bp.route('/posts/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    current_user_id = get_jwt_identity()
    if post_service.delete_post_if_user_authorized(id, current_user_id):
        return make_response('', 204)
    return make_response(jsonify(msg="권한이 없습니다. 해당 글을 쓰신 유저가 맞는지 확인해주세요.", status_code=401), 401)
