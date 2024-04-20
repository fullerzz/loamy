from blacksheep import Application, Request, Response, get, json, post

app = Application()


@get("/")
async def index() -> Response:
    return json({"message": "Hello, world!"})


@post("/foo")
async def post_foo(request: Request) -> Response:
    data = await request.json()
    return json(data)


@get("/exception")
async def mock_exception() -> Response:
    raise Exception("Mock exception")
