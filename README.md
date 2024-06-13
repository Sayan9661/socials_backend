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

- `POST /discussion_service`: Create a new post.
- `GET /discussion_service/<id>`: Retrieve a post by ID.
- `PUT /discussion_service/<id>`: Update a post by ID.
- `DELETE /discussion_service/<id>`: Delete a post by ID.
- `GET /discussion_service/search`: Search for posts.

- `POST /comment`: Add a comment to a post.
- `PUT /comment/<id>`: Update a comment by ID.
- `DELETE /comment/<id>`: Delete a comment by ID.
- `GET /comment/<post_id>`: Get all comments for a post.

Replace `discussion_service` and `comment` with the appropriate service name to interact with those services.

## Testing

You can test the application using the provided Postman collection. Import the collection into Postman and send the requests to your server.
