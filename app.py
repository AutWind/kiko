from flask import request
from flask_api import FlaskAPI

app = FlaskAPI(__name__)


@app.route('/', methods=['GET', 'POST'])
def example():
    if request.method == 'POST':
        return {'post': request.data}
    return {'get': 'kiko'}


if __name__ == '__main__':
    app.run()
