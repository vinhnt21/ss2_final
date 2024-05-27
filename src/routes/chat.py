from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.utils import rag

chat_bp = Blueprint('chat_bp', __name__)


@chat_bp.route('/get-answer', methods=['POST'])
@jwt_required()
def get_answer():
    """
    get the answer to a question
    """
    user_question = request.json['question']
    print(user_question)
    answer = rag.get_answer(user_question)
    return {
        'answer': answer
    }
