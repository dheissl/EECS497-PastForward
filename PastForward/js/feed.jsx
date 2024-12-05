import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Post from "./post";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [nextPageUrl, setNextPageUrl] = useState("/api/v1/posts/");
  const [hasMore, setHasMore] = useState(true);

  const fetchMoreData = () => {
    if (!nextPageUrl) {
      setHasMore(false); // No more posts to fetch
      return;
    }

    fetch(nextPageUrl, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setPosts((prevPosts) => [...prevPosts, ...data.results]);
        setNextPageUrl(data.next);
        if (!data.next) setHasMore(false);
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    fetch("/api/v1/posts/", { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        setPosts(data.results);
        setNextPageUrl(data.next);
        if (!data.next) setHasMore(false);
      })
      .catch((error) => console.log(error));
  }, []);

  return (
    <div
      className="container-fluid my-4 overflow-hidden"
      style={{ padding: 0, margin: 0 }}
    >
      <InfiniteScroll
        dataLength={posts.length}
        next={fetchMoreData}
        hasMore={hasMore}
        loader={<h4 className="text-center">Loading...</h4>}
        endMessage={
          <p className="text-center text-muted mt-4">
            <b>No more posts to load</b>
          </p>
        }
      >
        <div className="row g-4 mx-0">
          {posts.map((post) => (
            <Post key={post.postid} url={post.url} />
          ))}
        </div>
      </InfiniteScroll>
    </div>
  );
}
