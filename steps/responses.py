from fastapi.responses import Response


def ok(content=None):
    """
    Creates 200 Ok Http Response
    :param content: content of the response
    :return: Ok Http Response
    """
    return Response(content=content)


def created(content=None):
    """
    Creates 201 Created Http Response
    :param content: content of the response
    :return: Created Http Response
    """
    return Response(content=content, status_code=201)


def bad_request(content=None):
    """
    Creates 400 Bad Request Http Response
    :param content: content of the response
    :return: Bad Request Http Response
    """
    return Response(content=content, status_code=400)


def not_found():
    """
    Creates 404 Not Found Http Response
    :return: Not Found Http Response
    """
    return Response(status_code=404)


def internal_server_error(content=None):
    """
    Creates 500 Internal Server Error Http Response
    :param content: content of the response
    :return: Internal Server Error Http Response
    """
    return Response(content=content, status_code=500)

