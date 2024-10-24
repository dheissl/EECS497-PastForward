PRAGMA foreign_keys = ON;

-- users table
INSERT INTO users(username, fullname, email, filename, password)
VALUES
  ('jerrylol', 'Jerry Cool', 'jerry@umich.edu', 'jerry.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
  ('sonj', 'Son Jerry', 'jerryson@umich.edu', 'jerryson.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
  ('sherry', 'Sherry Cool', 'sherryc@umich.edu', 'sherry.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
  ('SherrySon', 'Son Sherry', 'sherryson@umich.edu', 'SherrySon.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8'),
  ('Boblol', 'Bob Dude', 'bob@umich.edu', 'Bob.jpg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

-- posts table
INSERT INTO posts(filename, owner)
VALUES
  ('jerrybird.jpg', 'jerrylol'),
  ('sonschool.jpg', 'sonj'),
  ('jerryforest.jpg', 'sherry'),
  ('BobDaughter.jpg', 'Boblol');

-- following table
INSERT INTO following(username1, username2)
VALUES
  -- sherry follows all
  ('sherry', 'sonj'),
  ('sherry', 'SherrySon'),
  ('sherry', 'jerrylol'),

  -- sonj follows all
  ('sonj', 'sherry'),
  ('sonj', 'SherrySon'),
  ('sonj', 'jerrylol'),

  -- SherrySon follows all
  ('SherrySon', 'sherry'),
  ('SherrySon', 'sonj'),
  ('SherrySon', 'jerrylol'),

  -- jerrylol follows all
  ('jerrylol', 'sherry'),
  ('jerrylol', 'sonj'),
  ('jerrylol', 'SherrySon');

-- comments table
INSERT INTO comments(owner, postid, text)
VALUES
  -- Comments on 'jerrybird.jpg' (postid 1)
  ('sherry', 1, 'Nice bird, Jerry!'),
  ('sonj', 1, 'Is that the same bird from last time?'),
  ('SherrySon', 1, 'Love the feathers!'),

  -- Comments on 'sonschool.jpg' (postid 2)
  ('jerrylol', 2, 'Back to school vibes.'),
  ('sherry', 2, 'Study hard, Son!'),
  ('SherrySon', 2, 'Nice shot! Where was this taken?'),

  -- Comments on 'jerryforest.jpg' (postid 3)
  ('Boblol', 3, 'Deep in the woods, I see!'),
  ('sonj', 3, 'Love the greenery!'),
  ('jerrylol', 3, 'One of my favorite spots.'),

  -- Comments on 'BobDaughter.jpg' (postid 4)
  ('sherry', 4, 'Beautiful portrait!'),
  ('sonj', 4, 'Captured perfectly.'),
  ('SherrySon', 4, 'Looks like a proud moment!');

-- likes table
INSERT INTO likes(owner, postid)
VALUES
  -- Likes on 'jerrybird.jpg' (postid 1)
  ('sonj', 1),
  ('Boblol', 1),

  -- Likes on 'sonschool.jpg' (postid 2)
  ('jerrylol', 2),
  ('SherrySon', 2),
  ('sherry', 2),

  -- Likes on 'jerryforest.jpg' (postid 3)
  ('sonj', 3),
  ('jerrylol', 3),
  ('SherrySon', 3),
  ('Boblol', 3),

  -- Likes on 'BobDaughter.jpg' (postid 4)
  ('sonj', 4),
  ('jerrylol', 4),
  ('SherrySon', 4);
