import React, { useState, useEffect } from "react";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [nextPageUrl, setNextPageUrl] = useState("/api/v1/posts/");
  const [initialFetchComplete, setInitialFetchComplete] = useState(false);

  const fetchMoreData = () => {
    if (!nextPageUrl) return; // No more posts to fetch

    fetch(nextPageUrl, { credentials: "same-origin" })
      .then(response => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then(data => {
        if (!initialFetchComplete) {
          // If initial fetch, replace posts with data.results
          setPosts(data.results);
          setInitialFetchComplete(true);
        } else {
          // If not initial fetch, append to existing posts
          setPosts(prevPosts => [...prevPosts, ...data.results]);
        }
        setNextPageUrl(data.next);
      })
      .catch(error => console.log(error));
  };

  useEffect(() => {
    fetchMoreData();
  }, []);

  return (
    <InfiniteScroll
      dataLength={posts.length}
      next={fetchMoreData}
      hasMore={nextPageUrl !== null} // Fetch more only if there's a next page
      loader={<h4>Loading...</h4>}
      endMessage={
        <p style={{ textAlign: "center" }}>
          <b>End of feed</b>
        </p>
      }
    >
      {posts.map(post => (
        <Post key={post.postid} url={post.url} />
      ))}
    </InfiniteScroll>
  );
}
