import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Like({url, numLikes, lognameLikesThis, postid}, onRun) {
    const [isLiked, setIsLiked] = useState(lognameLikesThis);

    const run = () => {
        if (lognameLikesThis){
            fetch(url, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .catch((error) => console.log(error));
            
            setIsLiked(!isLiked);
        } else {
            fetch("/api/v1/likes/?postid={postid}", { credentials: "same-origin" })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
            .catch((error) => console.log(error));
            
            setIsLiked(!isLiked);
        }
    };
  
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
