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
INSERT INTO posts(filename, owner, description)
VALUES
  ('jerrybird.jpg', 'jerrylol', 'I remember the first time I saw a bird; I was just a boy, maybe five or six, and I’d never ventured far from our little stone house nestled in the valley. One morning, as the sun peeked over the hills, a flash of red and gold darted across my vision, landing on the fence post. I froze, mesmerized by the tiny creature with feathers gleaming like embers in the light, its head tilting inquisitively as if it were just as curious about me. It let out a high, melodic whistle, and for a moment, the whole world seemed to pause in harmony with that sound. To this day, I can’t hear a bird sing without being pulled back to that instant of wonder, standing barefoot in the dew-soaked grass, watching something so ordinary and yet so miraculous.'),
  ('sonschool.jpg', 'sonj', 'The moment I stepped onto the University of Michigan campus, it felt like stepping into a world I’d only dreamed about. The iconic maize and blue banners fluttered in the breeze, and the hum of student life buzzed around me, equal parts thrilling and intimidating. My sneakers squeaked against the brick paths as I passed towering buildings that seemed to hold centuries of knowledge, and I felt a mix of awe and determination. Standing beneath the shadow of the Big House, I took a deep breath, realizing this was the first step of a journey that would shape the rest of my life.'),
  ('jerryforest.jpg', 'sherry', 'I had never seen anything so grand in my life. The towering mountains stretched endlessly, their peaks kissed by the clouds, and the sunlight painted them in hues of gold and blue. Standing there, the crisp air filling my lungs, I felt both insignificant and profoundly connected to something greater. Tears welled in my eyes—not out of sadness, but from the overwhelming beauty that reminded me how vast and wondrous the world truly is.'),
  ('BobDaughter.jpg', 'Boblol', 'Love life.');

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
