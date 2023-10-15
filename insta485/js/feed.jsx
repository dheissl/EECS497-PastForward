import React, { useState, useEffect } from "react";
import Post from "./post";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Feed() {
  const [posts, setPosts] = useState([]);
  const [nextPageUrl, setNextPageUrl] = useState("/api/v1/posts/");

  const fetchMoreData = () => {
    if (!nextPageUrl) return; // No more posts to fetch

    fetch(nextPageUrl, { credentials: "same-origin" })
      .then(response => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then(data => {
        setPosts(prevPosts => [...prevPosts, ...data.results]);
        setNextPageUrl(data.next);
      })
      .catch(error => console.log(error));
  };

    // Initial data fetch on mount
    useEffect(() => {
        fetch("/api/v1/posts/", { credentials: "same-origin" })
        .then(response => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
        })
        .then(data => {
            setPosts(data.results);
            setNextPageUrl(data.next);
        })
        .catch(error => console.log(error));
    }, []);  // Empty dependency array means this will only run once on mount
    

  return (
    <InfiniteScroll
      dataLength={posts.length}
      next={fetchMoreData}
      hasMore={nextPageUrl !== null} // Fetch more only if there's a next page
    >
      {posts.map(post => (
        <Post key={post.postid} url={post.url} />
      ))}
    </InfiniteScroll>
  );
}
