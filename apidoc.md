# Daedam API Reference

Calls
- [`GET` */calls*](#get-calls)
- [`POST` */calls*](#post-calls)
- [`DELETE` */calls/:id*](#delete-calls-id)
- [`GET` */calls/:id*](#get-calls-id)
- [`PATCH` */calls/:id*](#patch-calls-id)

Offers
- [`GET` */offers*](#get-offers)
- [`POST` */offers*](#post-offers)
- [`DELETE` */offers/:id*](#delete-offers-id)
- [`GET` */offers/:id*](#get-offers-id)
- [`PATCH` */offers/:id*](#patch-offers-id)

## `GET` */calls* <a name="get-calls"></a>

Fetch existing calls with pagination (latest ones first). Each page contains 10 calls.
If no page is specified, `page=1` is assigned by default.

### REQUEST

- *Path Parameters:* None

- *Query Parameters:*
    - `page` [integer] [optional]: Page to fetch and render. Defaults to 1.

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

## `POST` */calls* <a name="post-calls"></a>

Create a new call record.

### REQUEST

- *Path Parameters:* None

- *Query Parameters:* None

- *Request Body:*
    - `question` [string] [required]: Question to be discussed.
    - `description` [string] [optional]: Additional information about the question such as its context and scope.
    - `topics` [array of string] [optional]: Topic categories related to the question.

- *Example:*
```
$ curl "https://daedam.herokuapp.com/calls" \
    -X POST \
    -H "Authorization: Bearer $JWT_AUDIENCE" \
    -H "Content-Type: application/json" \
    -d '{
        "question": "What is the nature of self?",
        "description": "I want a discussion around the origin of our self-awareness and its position in the evolutionary process.",
        "topics": ["psychology", "biology", "self"]
    }'
```

### RESPONSE

- `201`: Returns success message and ID of the created call record.

- *Example:*
```
{
  "id": 4,
  "message": "Call record has been created successfully.",
  "success": true
}
```

## `DELETE` */calls/:id* <a name="delete-calls-id"></a>

Delete a specific call record.

### REQUEST

- *Path Parameters:* None
    - `id` [integer] [required]: ID of the call record to be deleted.

- *Query Parameters:* None

- *Request Body:* None

- *Example:*
```
$ curl "https://daedam.herokuapp.com/calls/4" \
    -X DELETE \
    -H "Authorization: Bearer $JWT_AUDIENCE"
```

### RESPONSE

- `200`: Returns success message and ID of the deleted call record.

- *Example:*
```
{
  "id": 4,
  "message": "Call record has been deleted successfully.",
  "success": true
}
```

## `GET` */calls/:id* <a name="get-calls-id"></a>

Fetch a specific call record.

### REQUEST

- *Path Parameters:*
    - `id` [integer] [required]: ID of the call record to be fetched.

- *Query Parameters:* None

- *Request Body:* None

- *Example:*
```
$ curl "https://daedam.herokuapp.com/calls/1" \
    -H "Authorization: Bearer $JWT_AUDIENCE"
```

### RESPONSE

- `200`: Returns the requested call record.

- *Example:*
```
{
  "calls": [
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
  "total_calls": 1
}
```

## `PATCH` */calls/:id* <a name="patch-calls-id"></a>

Update an existing call record.

### REQUEST

- *Path Parameters:* None
    - `id` [integer] [required]: ID of the call record to be updated.

- *Query Parameters:* None

- *Request Body:*
    - `question` [string] [optional]: Question to be discussed.
    - `description` [string] [optional]: Additional information about the question such as its context and scope.
    - `topics` [array of string] [optional]: Topic categories related to the question.

- *Example:*
```
$ curl "https://daedam.herokuapp.com/calls/1" \
    -X PATCH \
    -H "Authorization: Bearer $JWT_AUDIENCE" \
    -H "Content-Type: application/json" \
    -d '{
        "description": "I want various scientific perspectives.",
        "topics": ["psychology", "neuroscience", "biology"]
    }'
```

### RESPONSE

- `200`: Returns success message and ID of the updated call record.

- *Example:*
```
{
  "id": 1,
  "message": "Call record has been updated successfully.",
  "success": true
}
```

## `GET` */offers* <a name="get-offers"></a>

Fetch existing offers with pagination (latest ones first). Each page contains 10 offers.
If no page is specified, `page=1` is assigned by default.

### REQUEST

- *Path Parameters:* None

- *Query Parameters:*
    - `page` [integer] [optional]: Page to fetch and render. Defaults to 1.

- *Request Body:* None

- *Example:*
```
$ curl "https://daedam.herokuapp.com/offers?page=1" \
    -H "Authorization: Bearer $JWT_AUDIENCE"
```

### RESPONSE

- `200`: Returns a collection of offers in the requested page.

- *Example:*
```
{
  "offers": [
    {
      "contents": "Today, we observe increasing rates of divorce. Is lasting love just another social construct fabricated to sustain organized life? We shall discuss this timely question with three distinguished experts on love and relationship.",
      "event_time": "Tue, 25 May 2021 19:00:00 GMT",
      "finalized": false,
      "id": 1,
      "panelists": [
        "Adam Sheck",
        "Todd Creager",
        "April Masini"
      ],
      "title": "Can love last forever?",
      "topics": [
        "philosophy",
        "science",
        "love"
      ]
    }
  ],
  "success": true,
  "total_offers": 1
}
```

## `POST` */offers* <a name="post-offers"></a>

Create a new offer record.

### REQUEST

- *Path Parameters:* None

- *Query Parameters:* None

- *Request Body:*
    - `title` [string] [required]: Title of the discussion event.
    - `contents` [string] [optional]: Detailed information about the event such as themes and questions to be addressed.
    - `event_time` [string] [optional]: Date and time of the event. To be passed in ISO format.
    - `finalized` [boolean] [optional]: Whether the event has been finalized/confirmed to take place. Defaults to false.
    - `topics` [array of string] [optional]: Topic categories related to the event.
    - `panelists` [array of string] [optional]: Discussion panelists.

- *Example:*
```
$ curl "https://daedam.herokuapp.com/offers" \
    -X POST \
    -H "Authorization: Bearer $JWT_MODERATOR" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Does extraterrestrial life exist?",
        "contents": "Professor Avi Loeb is a theoretical physicist whose areas of professional interest include cosmology and astrophysics. His new book, \"Extraterrestrial: The First Sign of Intelligent Life Beyond Earth\", proposes that Oumuamua, the interstellar object that passed through our solar system in 2017, may have been the creation of an alien intelligence.",
        "event_time": "2021-07-25T19:00:00",
        "finalized": false,
        "topics": ["astrophysics", "cosmology", "extraterrestrial life"],
        "panelists": ["Avi Loeb", "Neil deGrasse Tyson", "Lex Fridman"]
    }'
```

### RESPONSE

- `201`: Returns success message and ID of the created offer record.

- *Example:*
```
{
  "id": 2,
  "message": "Offer record has been created successfully.",
  "success": true
}
```

## `DELETE` */offers/:id* <a name="delete-offers-id"></a>

Delete a specific offer record.

### REQUEST

- *Path Parameters:* None
    - `id` [integer] [required]: ID of the offer record to be deleted.

- *Query Parameters:* None

- *Request Body:* None

- *Example:*
```
$ curl "https://daedam.herokuapp.com/offers/2" \
    -X DELETE \
    -H "Authorization: Bearer $JWT_MODERATOR"
```

### RESPONSE

- `200`: Returns success message and ID of the deleted offer record.

- *Example:*
```
{
  "id": 2,
  "message": "Offer record has been deleted successfully.",
  "success": true
}
```

## `GET` */offers/:id* <a name="get-offers-id"></a>

Fetch a specific offer record.

### REQUEST

- *Path Parameters:*
    - `id` [integer] [required]: ID of the offer record to be fetched.

- *Query Parameters:* None

- *Request Body:* None

- *Example:*
```
$ curl "https://daedam.herokuapp.com/offers/1" \
    -H "Authorization: Bearer $JWT_MODERATOR"
```

### RESPONSE

- `200`: Returns the requested offer record.

- *Example:*
```
{
  "offers": [
    {
      "contents": "Today, we observe increasing rates of divorce. Is lasting love just another social construct fabricated to sustain organized life? We shall discuss this timely question with three distinguished experts on love and relationship.",
      "event_time": "Tue, 25 May 2021 19:00:00 GMT",
      "finalized": false,
      "id": 1,
      "panelists": [
        "Adam Sheck",
        "Todd Creager",
        "April Masini"
      ],
      "title": "Can love last forever?",
      "topics": [
        "philosophy",
        "science",
        "love"
      ]
    }
  ],
  "success": true,
  "total_offers": 1
}
```

## `PATCH` */offers/:id* <a name="patch-offers-id"></a>

Update an existing offer record.

### REQUEST

- *Path Parameters:* None
    - `id` [integer] [required]: ID of the offer record to be updated.

- *Query Parameters:* None

- *Request Body:*
    - `title` [string] [optional]: Title of the discussion event.
    - `contents` [string] [optional]: Detailed information about the event such as themes and questions to be addressed.
    - `event_time` [string] [optional]: Date and time of the event. To be passed in ISO format.
    - `finalized` [boolean] [optional]: Whether the event has been finalized/confirmed to take place. Defaults to false.
    - `topics` [array of string] [optional]: Topic categories related to the event.
    - `panelists` [array of string] [optional]: Discussion panelists.

- *Example:*
```
$ curl "https://daedam.herokuapp.com/offers/1" \
    -X PATCH \
    -H "Authorization: Bearer $JWT_MODERATOR" \
    -H "Content-Type: application/json" \
    -d '{
        "finalized": true
    }'
```

### RESPONSE

- `200`: Returns success message and ID of the updated offer record.

- *Example:*
```
{
  "id": 1,
  "message": "Offer record has been updated successfully.",
  "success": true
}
```
