const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static("."));

// ─── In-memory storage ────────────────────────────────────────────────────────
let users = [];
let posts = [];
let comments = [];
let likes = [];
let follows = [];
let userIdCounter = 1;
let postIdCounter = 1;
let commentIdCounter = 1;

// ─── Helper ───────────────────────────────────────────────────────────────────
const notFound = (res, msg) => res.status(404).json({ error: msg });
const badRequest = (res, msg) => res.status(400).json({ error: msg });

// ══════════════════════════════════════════════════════════════════════════════
// USERS
// ══════════════════════════════════════════════════════════════════════════════

// POST /users  – register a user
app.post("/users", (req, res) => {
  const { username, email } = req.body;
  if (!username || !email) return badRequest(res, "username and email are required");
  if (users.find(u => u.username === username))
    return res.status(409).json({ error: "Username already taken" });

  const user = { id: userIdCounter++, username, email, createdAt: new Date().toISOString() };
  users.push(user);
  res.status(201).json(user);
});

// GET /users  – list all users
app.get("/users", (req, res) => {
  const result = users.map(u => ({
    ...u,
    followersCount: follows.filter(f => f.followedId === u.id).length,
    followingCount: follows.filter(f => f.followerId === u.id).length,
  }));
  res.json(result);
});

// GET /users/:id  – get user by id
app.get("/users/:id", (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  if (!user) return notFound(res, "User not found");
  res.json({
    ...user,
    followersCount: follows.filter(f => f.followedId === user.id).length,
    followingCount: follows.filter(f => f.followerId === user.id).length,
    posts: posts.filter(p => p.userId === user.id),
  });
});

// ══════════════════════════════════════════════════════════════════════════════
// FOLLOW / UNFOLLOW
// ══════════════════════════════════════════════════════════════════════════════

// POST /users/:id/follow  – follow a user
app.post("/users/:id/follow", (req, res) => {
  const followedId = parseInt(req.params.id);
  const { followerId } = req.body;
  if (!followerId) return badRequest(res, "followerId is required");

  const followed = users.find(u => u.id === followedId);
  const follower = users.find(u => u.id === followerId);
  if (!followed || !follower) return notFound(res, "User not found");
  if (followedId === followerId) return badRequest(res, "Cannot follow yourself");

  const already = follows.find(f => f.followerId === followerId && f.followedId === followedId);
  if (already) return res.status(409).json({ error: "Already following" });

  follows.push({ followerId, followedId });
  res.status(201).json({ message: `User ${followerId} now follows user ${followedId}` });
});

// DELETE /users/:id/follow  – unfollow a user
app.delete("/users/:id/follow", (req, res) => {
  const followedId = parseInt(req.params.id);
  const { followerId } = req.body;
  if (!followerId) return badRequest(res, "followerId is required");

  const idx = follows.findIndex(f => f.followerId === followerId && f.followedId === followedId);
  if (idx === -1) return notFound(res, "Follow relationship not found");

  follows.splice(idx, 1);
  res.json({ message: `User ${followerId} unfollowed user ${followedId}` });
});

// ══════════════════════════════════════════════════════════════════════════════
// POSTS
// ══════════════════════════════════════════════════════════════════════════════

// POST /posts  – create a post
app.post("/posts", (req, res) => {
  const { userId, content } = req.body;
  if (!userId || !content) return badRequest(res, "userId and content are required");
  if (!users.find(u => u.id === userId)) return notFound(res, "User not found");

  const post = { id: postIdCounter++, userId, content, createdAt: new Date().toISOString() };
  posts.push(post);
  console.log(`Adding new post ${JSON.stringify(post)}`);
  res.status(201).json(post);
});

// GET /posts  – get all posts (with like/comment counts)
app.get("/posts", (req, res) => {
  const result = posts.map(p => enrichPost(p));
  res.json(result);
});

// GET /posts/:id  – get single post
app.get("/posts/:id", (req, res) => {
  const post = posts.find(p => p.id === parseInt(req.params.id));
  if (!post) return notFound(res, "Post not found");
  res.json(enrichPost(post));
});

// DELETE /posts/:id  – delete a post
app.delete("/posts/:id", (req, res) => {
  const idx = posts.findIndex(p => p.id === parseInt(req.params.id));
  if (idx === -1) return notFound(res, "Post not found");
  posts.splice(idx, 1);
  // cascade delete likes and comments
  likes = likes.filter(l => l.postId !== parseInt(req.params.id));
  comments = comments.filter(c => c.postId !== parseInt(req.params.id));
  res.json({ message: "Post deleted" });
});

function enrichPost(post) {
  const author = users.find(u => u.id === post.userId);
  return {
    ...post,
    author: author ? author.username : "unknown",
    likesCount: likes.filter(l => l.postId === post.id).length,
    commentsCount: comments.filter(c => c.postId === post.id).length,
  };
}

// ══════════════════════════════════════════════════════════════════════════════
// LIKES
// ══════════════════════════════════════════════════════════════════════════════

// POST /posts/:id/like  – like a post
app.post("/posts/:id/like", (req, res) => {
  const postId = parseInt(req.params.id);
  const { userId } = req.body;
  if (!userId) return badRequest(res, "userId is required");
  if (!posts.find(p => p.id === postId)) return notFound(res, "Post not found");
  if (!users.find(u => u.id === userId)) return notFound(res, "User not found");

  const already = likes.find(l => l.postId === postId && l.userId === userId);
  if (already) return res.status(409).json({ error: "Already liked" });

  likes.push({ postId, userId });
  res.status(201).json({ message: "Post liked", likesCount: likes.filter(l => l.postId === postId).length });
});

// DELETE /posts/:id/like  – unlike a post
app.delete("/posts/:id/like", (req, res) => {
  const postId = parseInt(req.params.id);
  const { userId } = req.body;
  if (!userId) return badRequest(res, "userId is required");

  const idx = likes.findIndex(l => l.postId === postId && l.userId === userId);
  if (idx === -1) return notFound(res, "Like not found");

  likes.splice(idx, 1);
  res.json({ message: "Post unliked", likesCount: likes.filter(l => l.postId === postId).length });
});

// ══════════════════════════════════════════════════════════════════════════════
// COMMENTS
// ══════════════════════════════════════════════════════════════════════════════

// POST /posts/:id/comments  – add a comment
app.post("/posts/:id/comments", (req, res) => {
  const postId = parseInt(req.params.id);
  const { userId, content } = req.body;
  if (!userId || !content) return badRequest(res, "userId and content are required");
  if (!posts.find(p => p.id === postId)) return notFound(res, "Post not found");
  if (!users.find(u => u.id === userId)) return notFound(res, "User not found");

  const comment = { id: commentIdCounter++, postId, userId, content, createdAt: new Date().toISOString() };
  comments.push(comment);
  res.status(201).json(comment);
});

// GET /posts/:id/comments  – get comments for a post
app.get("/posts/:id/comments", (req, res) => {
  const postId = parseInt(req.params.id);
  if (!posts.find(p => p.id === postId)) return notFound(res, "Post not found");

  const result = comments
    .filter(c => c.postId === postId)
    .map(c => {
      const author = users.find(u => u.id === c.userId);
      return { ...c, author: author ? author.username : "unknown" };
    });
  res.json(result);
});

// ──────────────────────────────────────────────────────────────────────────────
// Root – serve the frontend
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
