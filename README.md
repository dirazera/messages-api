# Messages-API

*This is a service for sending and retrieving messages.*

---

## Install

First clone this repository and set up the python virtual environment. You need to have Python 3 installed locally

```
git clone https://github.com/dirazera/messages-api.git
cd messages-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the app

Before running the app you need to initialise the database. For simplicity an embedded SQLite3 database is used.

```
export FLASK_ENV=development
export FLASK_APP=messages
flask db_create
```

To run the application:

```
flask run
```

## Run the tests

```
pytest --cov=messages --cov-report=html
```

Test coverage report will be generated under `htmlcov/index.html`

## API Endpoints

### Fetch new messages

**URL**: `/recipients/<recipient>/messages`

**Method**: `GET`

Example:

```
curl -XGET 'http://127.0.0.1:5000/recipients/you1@test.com/messages'
```

**Response Code**: `200`

**Response Output**:

If there are new messages:

```json
[
  {
    "content": "Monday we will meet at 15",
    "creation_date": "2022-03-17T00:17:14.711349",
    "id": "75273891-8387-4cf8-a343-bf35b35f6d27",
    "new": true,
    "recipient": "you1@test.com",
    "sender": "test1@test.com",
    "subject": "First meeting"
  },
  {
    "content": "Tuesday we will meet at 15",
    "creation_date": "2022-03-17T00:17:19.341950",
    "id": "4a4cdbfd-63de-44cd-8c78-97623c5eb615",
    "new": true,
    "recipient": "you1@test.com",
    "sender": "test2@test.com",
    "subject": "Second meeting"
  },
  {
    "content": "Wednesday we will meet at 15",
    "creation_date": "2022-03-17T00:17:23.840222",
    "id": "28a54ed5-2bf4-481a-882c-fcedd131d6bf",
    "new": true,
    "recipient": "you1@test.com",
    "sender": "test3@test.com",
    "subject": "Third meeting"
  }
]
```

If there are **no** new messages:

```json
[]
```

### Fetch all messages

**URL**: `/recipients/<recipient>/messages?all=true`

**Method**: `GET`

```
curl -XGET 'http://127.0.0.1:5000/recipients/you1@test.com/messages?all=true'
```

**Response Code**: `200`

**Response Output**:

If there are messages:

```json
[
  {
    "content": "Monday we will meet at 15",
    "creation_date": "2022-03-17T00:17:14.711349",
    "id": "75273891-8387-4cf8-a343-bf35b35f6d27",
    "new": false,
    "recipient": "you1@test.com",
    "sender": "test1@test.com",
    "subject": "First meeting"
  },
  {
    "content": "Tuesday we will meet at 15",
    "creation_date": "2022-03-17T00:17:19.341950",
    "id": "4a4cdbfd-63de-44cd-8c78-97623c5eb615",
    "new": false,
    "recipient": "you1@test.com",
    "sender": "test2@test.com",
    "subject": "Second meeting"
  },
  {
    "content": "Wednesday we will meet at 15",
    "creation_date": "2022-03-17T00:17:23.840222",
    "id": "28a54ed5-2bf4-481a-882c-fcedd131d6bf",
    "new": false,
    "recipient": "you1@test.com",
    "sender": "test3@test.com",
    "subject": "Third meeting"
  }
]
```

If there are **no** messages:

```json
[]
```

### Fetch all messages with pagination

**Description**:

Fetches all messages with pagination starting from a defined page and returning page size number of messages. If no page size is provided a default of `5` is assumed.

**URL**: `/recipients/<recipient>/messages?all=true&page=<page>&page_size=<page_size>`

**Method**: `GET`

**Example**:

```
curl -XGET 'http://127.0.0.1:5000/recipients/you1@test.com/messages?all=true&page=0&page_size=2'
```

**Response Code**: `200`

**Response Output**:

If there are messages available on the defined page and page size:

```json
[
  {
    "content": "Monday we will meet at 15",
    "creation_date": "2022-03-17T00:17:14.711349",
    "id": "75273891-8387-4cf8-a343-bf35b35f6d27",
    "new": false,
    "recipient": "you1@test.com",
    "sender": "test1@test.com",
    "subject": "First meeting"
  },
  {
    "content": "Tuesday we will meet at 15",
    "creation_date": "2022-03-17T00:17:19.341950",
    "id": "4a4cdbfd-63de-44cd-8c78-97623c5eb615",
    "new": false,
    "recipient": "you1@test.com",
    "sender": "test2@test.com",
    "subject": "Second meeting"
  }
]
```

If there are **no** messages:

```json
[]
```

### Fetch single message (by id)

Returns a single message by message identifier.

**URL**: `/recipients/<recipient>/messages/<message_id>`

**Method**: `GET`

```
curl -XGET 'http://127.0.0.1:5000/recipients/you1@test.com/messages/75273891-8387-4cf8-a343-bf35b35f6d27'
```

**Response Code**: `200`

**Response Output**:

If there is a message for the given id:

```json
{
  "content": "Monday we will meet at 15",
  "creation_date": "2022-03-17T00:17:14.711349",
  "id": "75273891-8387-4cf8-a343-bf35b35f6d27",
  "new": false,
  "recipient": "you1@test.com",
  "sender": "test1@test.com",
  "subject": "First meeting"
}
```

If **no** message was found for the given id the response code `404` will be returned and with the following output:

```json
{
  "error": "404 Not Found: No message found for that id"
}
```

### Send new message

**URL**: `/recipients/<recipient>/messages`

**Method**: `POST`

**Content Type**: `application/json`

**Content Payload**:

```json
{
  "sender": "sender-email",
  "subject": "message subject",
  "content": "message content"
}
```

```
curl -XPOST -d '{"sender": "test1@test.com", "subject": "First meeting", "content": "Monday we will meet at 15"}' -H 'Content-Type: application/json' 'http://127.0.0.1:5000/recipients/you1@test.com/messages'
```

**Response Code**: `201`

**Response Output**:

If the message was created successfully:

```json
{
  "content": "Monday we will meet at 15",
  "creation_date": "2022-03-17T00:17:14.711349",
  "id": "75273891-8387-4cf8-a343-bf35b35f6d27",
  "new": true,
  "recipient": "you1@test.com",
  "sender": "test1@test.com",
  "subject": "First meeting"
}
```

If the payload is malformed the response code `400` will be returned together with a response explaining the issue:

```json
{
  "error": "400 Bad Request: Email invalid"
}
```

### Delete single message (by id)

**URL**: `/recipients/<recipient>/messages/<message_id>`

**Method**: `DELETE`

```
curl -XDELETE 'http://127.0.0.1:5000/recipients/you1@test.com/messages/75273891-8387-4cf8-a343-bf35b35f6d27'
```

**Response Code**: `200`

**Response Output**:

```json
{
  "count_deleted": 1
}
```

### Delete multiple messages (by id)

**URL**: `/recipients/<recipient>/messages`

**Method**: `DELETE`

**Content Type**: `application/json`

**Content Payload**:

```json
{
  "ids": ["list", "of", "ids"]
}
```

```
curl -XDELETE -H 'Content-Type: application/json' -d '{"ids": ["4a4cdbfd-63de-44cd-8c78-97623c5eb615", "28a54ed5-2bf4-481a-882c-fcedd131d6bf"]}' 'http://127.0.0.1:5000/recipients/you1@test.com/messages'
```

**Response Code**: `200`

**Response Output**:

The number of messages deleted will be returned

```json
{
  "count_deleted": 2
}
```
