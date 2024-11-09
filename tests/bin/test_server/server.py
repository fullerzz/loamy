from quart import Quart, jsonify, Response, Request

app = Quart(__name__)


@app.get("/")
async def index() -> Response:
    return jsonify({"message": "Hello, world!"})


@app.post("/foo")
async def post_foo() -> Response:
    resp = jsonify({"foo": "bar"})
    resp.headers["X-Test"] = "Test"
    return resp


@app.get("/exception")
async def mock_exception() -> Response:
    raise Exception("Mock exception")


if __name__ == "__main__":
    app.run()
