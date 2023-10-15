import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [lognameLikesThis, setLognameLikesThis] = useState(false);
  const [numLikes, setNumLikes] = useState(0);
  const [likesUrl, setLikesUrl] = useState("");
  const [postId, setPostId] = useState(0);

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
          setLognameLikesThis(data.likes.lognameLikesThis);
          setNumLikes(data.likes.numLikes);
          setLikesUrl(data.likes.url);
          setPostId(data.postid);
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
            
            setLognameLikesThis(!lognameLikesThis);
            setNumLikes(numLikes - 1);
        } else {
            fetch("/api/v1/likes/?postid=${postid}", {method: "POST", credentials: "same-origin",})
                .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
                })
                .then((data) => {
                    if (!ignoreStaleRequest) {
                        setLikesUrl(data.url);
                    }
                })
                .catch((error) => console.log(error));
                
            setLognameLikesThis(!lognameLikesThis);
            setNumLikes(numLikes + 1);
                
        }
      };
      
      const doubleClick = () => {
        if (!lognameLikesThis) {
            fetch("/api/v1/likes/?postid={postid}", {credentials: "same-origin",})
                .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
                })
                .then((data) => {
                    if (!ignoreStaleRequest) {
                        setLikesUrl(data.url);
                    }
                })
                .catch((error) => console.log(error));
                
            setLognameLikesThis(!lognameLikesThis);
            setNumLikes(numLikes + 1);
        }
}

  // Render post image and post owner
  return (
    <div className="post">
        <img src={imgUrl} alt="post_image" onDoubleClick={() => doubleClick()} />
        <p>{owner}</p>
        <button data-testid="like-unlike-button" onClick={likeButton}>
           {lognameLikesThis ? 'Unlike' : 'Like'}
        </button>
        <p>{numLikes === 1 ? '1 like' : `${numLikes} likes`}</p>
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};