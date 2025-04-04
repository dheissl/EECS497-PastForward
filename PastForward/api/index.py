"""REST API for posts."""
import flask
import PastForward


@PastForward.app.route('/api/v1/')
def get_index():
    """Index stuff."""
    return {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": "/api/v1/"
    }
