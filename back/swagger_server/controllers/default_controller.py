import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.query import Query  # noqa: E501
from swagger_server.models.result import Result  # noqa: E501
from swagger_server.models.status import Status  # noqa: E501
from swagger_server import util


def new_query(body):  # noqa: E501
    """Requset a new query

    새로운 작업을 요청 # noqa: E501

    :param body: Pet object that needs to be added to the store
    :type body: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        body = Query.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def show_progress(id):  # noqa: E501
    """show_progress

     # noqa: E501

    :param id: query to lookup
    :type id: str

    :rtype: Status
    """
    return 'do some magic!'


def show_result(id):  # noqa: E501
    """show_result

     # noqa: E501

    :param id: query to lookup
    :type id: str

    :rtype: Result
    """
    return 'do some magic!'
