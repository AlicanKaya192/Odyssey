# Practice server for the API 1 exercises (copied into every exercise as
# api_routes.py). It runs inside the exercise runner on
# http://api.odyssey.test; nothing leaves the computer.
#
# Endpoints
#   GET  /                      links to the collections
#   GET  /status                plain text "ok"
#   GET  /books                 filters: author, tag, year_min, year_max, q
#                               sort: title | year | price (prefix - for descending)
#                               paging: page, per_page (default 5, max 20)
#   GET  /books/<id>            one book
#   POST /books                 needs "Authorization: Bearer letmein"; 201 + Location
#   PUT/PATCH/DELETE /books/<id>  same token; PUT replaces, PATCH changes fields
#   GET  /authors, /authors/<id>, /authors/<id>/books
#   GET  /offset/books          paging with offset + limit
#   GET  /cursor/books          paging with cursor; next_cursor is null at the end
#   GET  /stats                 needs "X-API-Key: demo-key-123" (401 without / wrong key)
#   GET  /admin/report          key "demo-key-123" is a reader key -> 403; "admin-key-999" -> 200
#   GET  /me                    "Authorization: Bearer letmein"
#   GET  /basic                 basic auth reader / pass123
#   GET  /flaky                 503 twice (Retry-After: 1), then 200
#   GET  /broken                always 500
#   GET  /slow                  answers after 3 seconds
#   GET  /limited               3 requests per window, then 429 + Retry-After: 1
#   GET  /changes?since=YYYY-MM-DD   books updated on or after the date
#   GET  /openapi.json          a small OpenAPI description of this API

import time

TOKEN = "letmein"
READER_KEY = "demo-key-123"
ADMIN_KEY = "admin-key-999"

AUTHORS = {
    1: {"id": 1, "name": "Austen", "country": "UK", "born": 1775},
    2: {"id": 2, "name": "Herbert", "country": "US", "born": 1920},
    3: {"id": 3, "name": "Joyce", "country": "IE", "born": 1882},
    4: {"id": 4, "name": "Lem", "country": "PL", "born": 1921},
    5: {"id": 5, "name": "Orwell", "country": "UK", "born": 1903},
    6: {"id": 6, "name": "Le Guin", "country": "US", "born": 1929},
    7: {"id": 7, "name": "Tolstoy", "country": "RU", "born": 1828},
    8: {"id": 8, "name": "Woolf", "country": "UK", "born": 1882},
}

_ROWS = [
    # id, title, author_id, year, price, tags, updated
    (1, "Emma", 1, 1815, 12.50, ["classic", "novel"], "2024-01-10"),
    (2, "Dune", 2, 1965, 9.99, ["scifi", "classic"], "2024-02-03"),
    (3, "Ulysses", 3, 1922, 15.00, [], "2024-01-22"),
    (4, "Solaris", 4, 1961, 11.20, ["scifi"], "2024-03-01"),
    (5, "Persuasion", 1, 1817, 8.75, ["classic", "romance", "novel"], "2024-02-14"),
    (6, "Pride and Prejudice", 1, 1813, 10.40, ["classic", "romance"], "2024-03-05"),
    (7, "Sense and Sensibility", 1, 1811, 9.10, ["classic", "romance"], "2024-01-05"),
    (8, "Dune Messiah", 2, 1969, 10.90, ["scifi"], "2024-02-20"),
    (9, "Dubliners", 3, 1914, 7.80, ["classic", "stories"], "2024-01-30"),
    (10, "The Cyberiad", 4, 1965, 12.00, ["scifi", "humor"], "2024-03-08"),
    (11, "Nineteen Eighty-Four", 5, 1949, 9.50, ["classic", "dystopia"], "2024-02-28"),
    (12, "Animal Farm", 5, 1945, 6.90, ["classic", "satire"], "2024-01-18"),
    (13, "The Dispossessed", 6, 1974, 11.75, ["scifi", "politics"], "2024-03-10"),
    (14, "The Left Hand of Darkness", 6, 1969, 10.25, ["scifi"], "2024-02-09"),
    (15, "A Wizard of Earthsea", 6, 1968, 8.40, ["fantasy"], "2024-01-12"),
    (16, "War and Peace", 7, 1869, 18.00, ["classic", "history"], "2024-02-17"),
    (17, "Anna Karenina", 7, 1878, 14.20, ["classic", "romance"], "2024-03-02"),
    (18, "Mrs Dalloway", 8, 1925, 9.30, ["classic", "novel"], "2024-01-25"),
    (19, "To the Lighthouse", 8, 1927, 9.80, ["classic", "novel"], "2024-02-22"),
    (20, "Orlando", 8, 1928, 8.60, ["novel"], "2024-03-12"),
    (21, "Fiasco", 4, 1986, 13.40, ["scifi"], "2024-02-25"),
    (22, "Homage to Catalonia", 5, 1938, 10.10, ["history"], "2024-01-08"),
    (23, "The Lathe of Heaven", 6, 1971, 9.95, ["scifi"], "2024-03-14"),
]

BOOKS = {}
for _id, _title, _author, _year, _price, _tags, _updated in _ROWS:
    BOOKS[_id] = {"id": _id, "title": _title, "author_id": _author, "year": _year,
                  "price": _price, "tags": list(_tags), "updated": _updated}

NEXT_ID = {"books": 24}
COUNTERS = {"flaky": 0, "limited": [], }


def _book_out(book):
    out = dict(book)
    author = AUTHORS.get(book["author_id"])
    out["author"] = {"id": author["id"], "name": author["name"], "country": author["country"]} if author else None
    return out


def _error(status, message, **extra):
    body = {"error": message}
    body.update(extra)
    return status, body


def _int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _filtered(query):
    books = [_book_out(b) for b in sorted(BOOKS.values(), key=lambda b: b["id"])]
    author = query.get("author")
    if author:
        books = [b for b in books if b["author"] and b["author"]["name"].lower() == author.lower()]
    tag = query.get("tag")
    if tag:
        books = [b for b in books if tag in b["tags"]]
    if query.get("year_min"):
        books = [b for b in books if b["year"] >= _int(query["year_min"], 0)]
    if query.get("year_max"):
        books = [b for b in books if b["year"] <= _int(query["year_max"], 9999)]
    text = query.get("q")
    if text:
        books = [b for b in books if text.lower() in b["title"].lower()]
    sort = query.get("sort")
    if sort:
        field = sort.lstrip("-")
        if field in ("title", "year", "price", "id"):
            books.sort(key=lambda b: b[field], reverse=sort.startswith("-"))
    return books


def _page(books, query, path):
    per_page = min(max(_int(query.get("per_page"), 5), 1), 20)
    page = max(_int(query.get("page"), 1), 1)
    total = len(books)
    pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    data = books[start:start + per_page]
    rest = {k: v for k, v in query.items() if k not in ("page",)}

    def link(number):
        if number < 1 or number > pages:
            return None
        parts = [f"{k}={v}" for k, v in rest.items()] + [f"page={number}"]
        return path + "?" + "&".join(parts)

    return 200, {
        "data": data,
        "meta": {"page": page, "per_page": per_page, "total": total, "pages": pages},
        "links": {"next": link(page + 1), "prev": link(page - 1)},
    }


def _authorised(request):
    return request.headers.get("authorization") == "Bearer " + TOKEN


def _validate(data, partial=False):
    if not isinstance(data, dict):
        return "the body must be a JSON object"
    if not partial or "title" in data:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            return "title must be a non-empty string"
    if not partial or "price" in data:
        price = data.get("price")
        if not isinstance(price, (int, float)) or isinstance(price, bool) or price <= 0:
            return "price must be a positive number"
    if "author_id" in data and data["author_id"] not in AUTHORS:
        return "author_id does not exist"
    return ""


def _books_item(request, book_id):
    book = BOOKS.get(book_id)
    if request.method == "GET":
        return (200, _book_out(book)) if book else _error(404, "book not found", id=book_id)
    if not _authorised(request):
        return _error(401, "missing or invalid token")
    if book is None:
        return _error(404, "book not found", id=book_id)
    if request.method == "DELETE":
        del BOOKS[book_id]
        return 204, None
    data = request.json
    problem = _validate(data, partial=request.method == "PATCH")
    if problem:
        return _error(422, "validation", detail=problem)
    if request.method == "PUT":
        new = {"id": book_id, "title": data["title"], "author_id": data.get("author_id", 0),
               "year": data.get("year", 0), "price": data["price"], "tags": data.get("tags", []),
               "updated": "2024-03-15"}
        BOOKS[book_id] = new
    else:
        for key in ("title", "price", "year", "tags", "author_id"):
            if key in data:
                book[key] = data[key]
        book["updated"] = "2024-03-15"
    return 200, _book_out(BOOKS[book_id])


OPENAPI = {
    "openapi": "3.1.0",
    "info": {"title": "Odyssey Library API", "version": "1.0"},
    "paths": {
        "/books": {
            "get": {"summary": "List books", "parameters": [
                {"name": "author", "in": "query"}, {"name": "tag", "in": "query"},
                {"name": "sort", "in": "query"}, {"name": "page", "in": "query"},
                {"name": "per_page", "in": "query"}]},
            "post": {"summary": "Add a book", "security": [{"bearer": []}]},
        },
        "/books/{id}": {
            "get": {"summary": "Get one book"},
            "put": {"summary": "Replace a book", "security": [{"bearer": []}]},
            "patch": {"summary": "Change a book", "security": [{"bearer": []}]},
            "delete": {"summary": "Delete a book", "security": [{"bearer": []}]},
        },
        "/authors": {"get": {"summary": "List authors"}},
        "/authors/{id}/books": {"get": {"summary": "Books of one author"}},
        "/stats": {"get": {"summary": "Library statistics", "security": [{"apiKey": []}]}},
    },
}


def handle(request):
    path = request.path.rstrip("/") or "/"
    parts = [p for p in path.split("/") if p]
    method = request.method

    if path == "/":
        return 200, {"links": {"books": "/books", "authors": "/authors", "stats": "/stats"}}
    if path == "/status":
        return 200, "ok"
    if path == "/openapi.json":
        return 200, OPENAPI

    if parts[:1] == ["books"]:
        if len(parts) == 1:
            if method == "GET":
                return _page(_filtered(request.query), request.query, "/books")
            if method == "POST":
                if not _authorised(request):
                    return _error(401, "missing or invalid token")
                data = request.json
                problem = _validate(data)
                if problem:
                    return _error(422, "validation", detail=problem)
                book_id = NEXT_ID["books"]
                NEXT_ID["books"] += 1
                BOOKS[book_id] = {"id": book_id, "title": data["title"], "author_id": data.get("author_id", 0),
                                  "year": data.get("year", 0), "price": data["price"],
                                  "tags": data.get("tags", []), "updated": "2024-03-15"}
                return 201, _book_out(BOOKS[book_id]), {"Location": f"/books/{book_id}"}
            return 405, {"error": "method not allowed"}, {"Allow": "GET, POST"}
        if len(parts) == 2:
            book_id = _int(parts[1], -1)
            if method not in ("GET", "PUT", "PATCH", "DELETE"):
                return 405, {"error": "method not allowed"}, {"Allow": "GET, PUT, PATCH, DELETE"}
            return _books_item(request, book_id)

    if parts[:1] == ["authors"]:
        if len(parts) == 1:
            return 200, {"data": [AUTHORS[k] for k in sorted(AUTHORS)]}
        author_id = _int(parts[1], -1)
        if author_id not in AUTHORS:
            return _error(404, "author not found", id=author_id)
        if len(parts) == 2:
            return 200, AUTHORS[author_id]
        if len(parts) == 3 and parts[2] == "books":
            books = [_book_out(b) for b in sorted(BOOKS.values(), key=lambda b: b["id"]) if b["author_id"] == author_id]
            return 200, {"data": books}

    if path == "/offset/books":
        books = _filtered(request.query)
        offset = max(_int(request.query.get("offset"), 0), 0)
        limit = min(max(_int(request.query.get("limit"), 5), 1), 20)
        return 200, {"items": books[offset:offset + limit], "offset": offset, "limit": limit, "total": len(books)}

    if path == "/cursor/books":
        books = _filtered(request.query)
        start = 0
        cursor = request.query.get("cursor")
        if cursor:
            if not cursor.startswith("c") or _int(cursor[1:], -1) < 0:
                return _error(400, "invalid cursor")
            start = _int(cursor[1:], 0)
        items = books[start:start + 4]
        nxt = start + 4
        return 200, {"results": items, "next_cursor": f"c{nxt}" if nxt < len(books) else None}

    if path == "/stats":
        key = request.headers.get("x-api-key")
        if key not in (READER_KEY, ADMIN_KEY):
            return _error(401, "missing or invalid api key")
        years = [b["year"] for b in BOOKS.values() if b["year"]]
        return 200, {"books": len(BOOKS), "authors": len(AUTHORS), "oldest": min(years), "newest": max(years)}

    if path == "/admin/report":
        key = request.headers.get("x-api-key")
        if key not in (READER_KEY, ADMIN_KEY):
            return _error(401, "missing or invalid api key")
        if key != ADMIN_KEY:
            return _error(403, "this key cannot read admin reports")
        return 200, {"report": "all good", "books": len(BOOKS)}

    if path == "/me":
        if not _authorised(request):
            return _error(401, "missing or invalid token")
        return 200, {"user": "ada", "role": "editor"}

    if path == "/basic":
        import base64

        expected = "Basic " + base64.b64encode(b"reader:pass123").decode("ascii")
        if request.headers.get("authorization") != expected:
            return 401, {"error": "login required"}, {"WWW-Authenticate": 'Basic realm="library"'}
        return 200, {"user": "reader"}

    if path == "/flaky":
        COUNTERS["flaky"] += 1
        if COUNTERS["flaky"] <= 2:
            return 503, {"error": "busy, try again"}, {"Retry-After": "1"}
        return 200, {"report": "ready", "attempt": COUNTERS["flaky"]}

    if path == "/broken":
        return _error(500, "internal error")

    if path == "/slow":
        return 200, {"ok": True}, {"X-Delay": "3"}

    if path == "/limited":
        now = time.monotonic()
        window = [t for t in COUNTERS["limited"] if now - t < 1.0]
        if len(window) >= 3:
            COUNTERS["limited"] = window
            return 429, {"error": "rate limit"}, {"Retry-After": "1", "X-RateLimit-Limit": "3",
                                                  "X-RateLimit-Remaining": "0"}
        window.append(now)
        COUNTERS["limited"] = window
        return 200, {"ok": True}, {"X-RateLimit-Limit": "3", "X-RateLimit-Remaining": str(3 - len(window))}

    if path == "/changes":
        since = request.query.get("since", "")
        if len(since) != 10:
            return _error(400, "since must look like 2024-03-01")
        changed = [_book_out(b) for b in sorted(BOOKS.values(), key=lambda b: b["id"]) if b["updated"] >= since]
        return 200, {"since": since, "data": changed}

    return _error(404, "not found", path=request.path)
