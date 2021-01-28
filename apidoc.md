# Daedam API Reference

Endpoints:
- [`GET` */calls*](#get-calls)

## `GET` */calls* <a name="get-calls"></a>

Fetch existing calls with pagination (latest ones first). Each page contains 10 calls.
If no page is specified, `page=1` is assigned by default.

### REQUEST

- *Path Parameters:* None

- *Query Parameters:*
    - `page` (optional): Page to fetch and render. Defaults to 1.

- *Request Body:* None

- *Example:*
```
$ curl "https://daedam.herokuapp.com/calls?page=1" \
    -H "Authorization: Bearer $JWT_AUDIENCE"
```

### RESPONSE

- `200`: Returns a collection of calls in the requested page.

- *Example:*
```
{
  "calls": [
    {
      "description": "I would like in-depth discussion of strengths and weaknesses of modern democracy, plus its alternatives in future.",
      "id": 3,
      "question": "Will democracy survive the 21st century?",
      "topics": [
        "philosophy",
        "sociology",
        "political science",
        "government",
        "democracy"
      ]
    },
    {
      "description": "Would prefer empirical and scientific perspectives.",
      "id": 2,
      "question": "Is a happy marriage possible? If so, how?",
      "topics": [
        "psychology",
        "biology",
        "relationship",
        "marriage"
      ]
    },
    {
      "description": "I want a blend of diverse perspectives including those from philosophy, science, and religion.",
      "id": 1,
      "question": "Is violence unavoidable?",
      "topics": [
        "philosophy",
        "psychology",
        "sociology",
        "biology",
        "religion"
      ]
    }
  ],
  "success": true,
  "total_calls": 3
}
```
