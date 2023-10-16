import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);


// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [time, setTime] = useState("");
  const [lognameLikesThis, setLognameLikesThis] = useState(false);
  const [numLikes, setNumLikes] = useState(0);
  const [likesUrl, setLikesUrl] = useState("");
  const [postId, setPostId] = useState(0);
  const [comments, setComments] = useState([]);
  const[text, setText] = useState("");

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          setImgUrl(data.imgUrl);
          setOwner(data.owner);
          setTime(dayjs(data.created).fromNow());
          setLognameLikesThis(data.likes.lognameLikesThis);
          setNumLikes(data.likes.numLikes);
          setLikesUrl(data.likes.url);
          setPostId(data.postid);
          setComments(data.comments);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the Post component
      // unmounts or re-renders. If a Post is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
    };
  }, [url]);
  
    const likeButton = () => {
        // Make an API call to like/unlike the post
        // You will need to implement this API endpoint on your server.
        if (lognameLikesThis) {
            fetch(likesUrl, {method: "DELETE", credentials: "same-origin",})
                .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
                })
                .catch((error) => console.log(error));
            
            setLikesUrl(null);
            setLognameLikesThis(!lognameLikesThis);
            setNumLikes(numLikes - 1);
        } else {
            fetch(`/api/v1/likes/?postid=${postId}`, {method: "POST", credentials: "same-origin",})
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
            fetch(`/api/v1/likes/?postid=${postId}`, {method: "POST", credentials: "same-origin",})
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
        fetch(`/api/v1/comments/${commentId}`, {method: "DELETE",
            credentials: "same-origin",})
            .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
            })
            .catch((error) => console.log(error));
            
        setComments((comments.filter((comment) => comment.commentid !== commentId)));
    };
    
    const enter = (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            addComment();
        }
    };
        
    const addComment = () => {
        if (text.trim() === "") {
            return; // Don't add empty comments
        }
    
        fetch(`/api/v1/comments/?postid=${postId}`, {method: "POST",
            credentials: "same-origin",
             headers: {"Content-Type": "application/json",},
              body: JSON.stringify({text}),})
            .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
            })
            .then((data) => {
                setComments([...comments, data])
            })
            .catch((error) => console.log(error));
        
        setText("");
    };


  // Render post image and post owner
  return (
    <div className="post">
        <a href=`/Users/${owner}/`>{owner}</a>
        <p>{time}</p>
        <img src={imgUrl} alt="post_image" onDoubleClick={() => doubleClick()} />
        <button data-testid="like-unlike-button" onClick={likeButton}>
           {lognameLikesThis ? 'Unlike' : 'Like'}
        </button>
        <p>{numLikes === 1 ? '1 like' : `${numLikes} likes`}</p>
        <div className="comments">
        {comments.map((comment) => (
          <div key={comment.commentid}>
            <p>{comment.owner}</p>
            <span data-testid="comment-text">{comment.text}</span>
            {comment.lognameOwnsThis && (
                <button data-testid="delete-comment-button" onClick={() =>
                    commentButton(comment.commentid)}>
                    Delete Comment
                </button>
            )}
          </div>
        ))}
        <form data-testid="comment-form" onSubmit={e => {e.preventDefault();
                alert('Submitting!'); addComment()}}>
            <input type="text" value={text} onChange={(e) => setText(e.target.value)}
                onKeyPress={enter} placeholder="Add a comment..." />
        </form>
        
      </div>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
