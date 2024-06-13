# Social Media Backend

This is a microservice-based application for managing discussions. It includes services for user, discussions and comments.

## Project Structure

The project is structured into separate services:

- `user_service`: Handles registration/login of users, user follow operations and searching of users.

- `discussion_service`: Handles creating, updating, retrieving and deleting posts. Posts can also be searching using either tags or text.

- `comment_service`: Handles adding/modifying comments, replies, likes to posts.

TODO:
The `api_gateway.py` file at the root of the project is the API gateway that routes requests to the appropriate service.

## Setup

1. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

You can interact with the application using any HTTP client like curl or Postman. Here are the available endpoints:

### user service

- `POST /register`: register a user.
- `POST /login`: login
- `POST /follow`: follow a user
- `POST /unfollow`: unfollow a user
- `GET search/users`: search user

### Discussion service

- `POST /discussions`: Create a new discussion/post. The request body should include `text`, `image`, `user_id`, and `tags`.
- `GET /discussions/<id>`: Retrieve a discussion by ID.
- `PUT /discussions/<id>`: Update a discussion by ID. The request body should include `text`, `image`, `user_id`, and `tags`.
- `DELETE /discussions/<id>`: Delete a discussion by ID.
- `GET /discussions/search`: Search for discussions based on text or tags. Include `text` and/or `tags` as query parameters.

### Comment service

- `POST /comments`: Create a new comment. The request body should include `text`, `post_id`, and `user_id`.
- `POST /comments/<id>/like`: Like a comment.
- `POST /comments/<id>/replies`: Reply to a comment. The request body should include `text` and `user_id`.
- `GET /comments/<id>`: Retrieve a comment by ID.
- `PUT /comments/<id>`: Update a comment by ID. The request body should include `text`.
- `DELETE /comments/<id>`: Delete a comment by ID.

## Testing

You can test the application using the Postman collections in the test_postman folder. Import the collections into Postman and send the requests to your server. There is a collection to test each service.
