import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Like({url, numLikes, lognameLikesThis, postid}, onRun) {

  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    
    const run = () => {
        if (lognameLikesThis){
            fetch(url, { credentials: "same-origin" })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                
                .then((data) => {
                    if (!ignoreStaleRequest) {
                        setIsliked(!isLiked);
                        }
                })
                .catch((error) => console.log(error));
        } else {
            fetch("/api/v1/likes/?postid=postid", { credentials: "same-origin" })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                
                .then((data) => {
                    if (!ignoreStaleRequest) {
                        setIsliked(!isLiked);
                    }
                })
                .catch((error) => console.log(error));
        }
    };
    
    return () => {
        ignoreStaleRequest = true;
    };
  }, [lognameLikesThis]);
  
  // Render like and unlike button
  return (
    <div>
        <p>{numLikes === 1 ? `${numLikes} like` : `${numLikes} likes`}</p>
        <button onClick={onRun} data-testid="like-unlike-button">
            {lognameLikesThis ? 'Unlike' : 'Like'}
        </button>
    </div>
  );
  
}

Post.propTypes = {
 url: PropTypes.string.isRequired,
  numLikes: PropTypes.number.isRequired,
  lognameLikesThis: PropTypes.bool.isRequired,
  postid: PropTypes.string.isRequired,
};
