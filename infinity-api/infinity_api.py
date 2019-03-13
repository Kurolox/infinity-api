from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)


@app.route("/test/", methods=['GET'])
def notes_detail():
    return {'request data': request.data}


if __name__ == "__main__":
    app.run()
