from flask import Response

def make_flask_response(r):
    return Response(
        response=r.content,
        status=r.status_code,
        content_type=r.headers.get("Content-Type", "application/octet-stream")
    )
