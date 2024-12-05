import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);

export default function Post({ url }) {
  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [time, setTime] = useState("");
  const [lognameLikesThis, setLognameLikesThis] = useState(false);
  const [numLikes, setNumLikes] = useState(0);
  const [likesUrl, setLikesUrl] = useState("");
  const [postId, setPostId] = useState(0);
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");
  const [profilePic, setProfilePic] = useState("");
  const [ownerUrl, setOwnerUrl] = useState("");
  const [postUrl, setPostUrl] = useState("");

  useEffect(() => {
    let ignoreStaleRequest = false;
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          setTime(dayjs(data.created).fromNow());
          setLognameLikesThis(data.likes.lognameLikesThis);
          setNumLikes(data.likes.numLikes);
          setLikesUrl(data.likes.url);
          setPostId(data.postid);
          setComments(data.comments);
          setProfilePic(data.ownerImgUrl);
          setOwnerUrl(data.ownerShowUrl);
          setPostUrl(data.postShowUrl);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }, [url]);

  const likeButton = () => {
    if (lognameLikesThis) {
      fetch(likesUrl, { method: "DELETE", credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .catch((error) => console.log(error));

      setLikesUrl(null);
      setLognameLikesThis(!lognameLikesThis);
      setNumLikes(numLikes - 1);
    } else {
      fetch(`/api/v1/likes/?postid=${postId}`, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setLikesUrl(data.url);
        })
        .catch((error) => console.log(error));

      setLognameLikesThis(!lognameLikesThis);
      setNumLikes(numLikes + 1);
    }
  };

  const doubleClick = () => {
    if (!lognameLikesThis) {
      fetch(`/api/v1/likes/?postid=${postId}`, {
        method: "POST",
        credentials: "same-origin",
      })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          setLikesUrl(data.url);
        })
        .catch((error) => console.log(error));

      setLognameLikesThis(!lognameLikesThis);
      setNumLikes(numLikes + 1);
    }
  };

  const commentButton = (commentId) => {
    fetch(`/api/v1/comments/${commentId}`, {
      method: "DELETE",
      credentials: "same-origin",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));

    setComments(comments.filter((comment) => comment.commentid !== commentId));
  };

  const addComment = () => {
    if (text.trim() === "") {
      return;
    }

    fetch(`/api/v1/comments/?postid=${postId}`, {
      method: "POST",
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setComments([...comments, data]);
      })
      .catch((error) => console.log(error));

    setText("");
  };

  return (
    <div className="col-12 col-md-6 mb-3">
      <div className="card h-100 shadow-sm" style={{ maxWidth: "500px", margin: "0 auto" }}>
        <div className="card-header d-flex align-items-center p-2">
          <a href={ownerUrl}>
            <img
              src={profilePic}
              alt="Profile"
              className="me-2"
              style={{ width: "40px", height: "40px", objectFit: "cover"}}
            />
          </a>
          <div>
            <a href={ownerUrl} className="text-decoration-none fw-bold" style={{ fontSize: "1.3rem" }}>
              {owner}
            </a>
            <small className="text-muted ms-2" style={{ fontSize: "1.0rem" }}>
              {time}
            </small>
          </div>
        </div>
        <img
          src={imgUrl}
          className="card-img-top"
          alt="Post"
          style={{ maxHeight: "auto", maxWidth: "auto", objectFit: "contain" }}
          onDoubleClick={() => likeButton()}
        />
        <div className="card-body p-2">
          <button
            className={`btn btn-sm ${
              lognameLikesThis ? "btn-danger" : "btn-success"
            }`}
            onClick={likeButton}
          >
            {lognameLikesThis ? "Unlike" : "Like"}
          </button>
          <p className="mt-1" style={{ fontSize: "1.1rem" }}>
            <strong>{numLikes}</strong> {numLikes === 1 ? "like" : "likes"}
          </p>
          <div className="comments">
          {comments.map((comment) => (
            <div key={comment.commentid} className="d-flex align-items-center mb-1">
              <a
                href={`/users/${comment.owner}/`}
                className="me-1 fw-bold text-decoration-none"
                style={{ fontSize: "1.rem" }}
              >
                {comment.owner}
              </a>
              <span style={{ fontSize: "1.1rem" }}>{comment.text}</span>
              {comment.lognameOwnsThis && (
                <button
                  className={`btn btn-sm btn-danger ms-2`}
                  type="button"
                  data-testid="delete-comment-button"
                  onClick={() => commentButton(comment.commentid)}
                >
                  Delete
                </button>
              )}
            </div>
          ))}

            <form
              onSubmit={(e) => {
                e.preventDefault();
                addComment();
              }}
              className="d-flex mt-2"
            >
              <input
                type="text"
                className="form-control form-control-sm me-2"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Add a comment..."
              />
              <button type="submit" className="btn btn-primary btn-sm btn-success">
                Post
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
