import React, { useState, useEffect } from "react";
import PropTypes from "prop-types";
import Like from "./likes";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the Post component.
export default function Post({ url }) {
  /* Display image and post owner of a single post */

  const [imgUrl, setImgUrl] = useState("");
  const [owner, setOwner] = useState("");
  const [lognameLikesThis, setLognameLikesThis] = useState(false);
  const [numsLikes, setNumLikes] = useState(0);
  const [likeUrl, setLikeUrl] = useState("");
  const [postid, setPostId] = useState(0);

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
          setLognameLikesThis(data.likes.lognameLikesThis)
          setNumLikes = data.likes.numLikes
          setLikeUrl = data.likes.url
          setPostId = data.postid
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

  // Render post image and post owner
  return (
    <div className="post">
        <img src={imgUrl} alt="post_image" />
        <p>{owner}</p>
        <Like  url={likeUrl} lognameLikesThis={lognameLikesThis}
            numLikes={numLikes} postid={postid}
            onRun={() => setLognameLikesThis(!lognameLikeThis)}
        />
    </div>
  );
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};
