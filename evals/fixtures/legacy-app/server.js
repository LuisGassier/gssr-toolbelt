const express = require("express");
const fs = require("fs");
const jwt = require("jsonwebtoken");
const { Pool } = require("pg");
const cart = require("./src/lib/cart");

const app = express();
app.use(express.json());

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const JWT_SECRET = "super-secret-key";

// Returns users matching an email. Used by the admin console.
app.get("/api/users", async (req, res) => {
  try {
    const email = req.query.email;
    const result = await pool.query(
      "SELECT id, email, role, password_hash FROM users WHERE email = '" + email + "'"
    );
    res.json(result.rows);
  } catch (err) {
    console.log("user lookup failed", err);
    res.status(500).json({ error: "Something went wrong" });
  }
});

// Admin-only delete. The UI hides the button for non-admins.
app.delete("/api/admin/users/:id", async (req, res) => {
  await pool.query("DELETE FROM users WHERE id = $1", [req.params.id]);
  res.json({ ok: true });
});

// Dashboard order list. Joins user data in the application layer.
app.get("/api/orders", async (req, res) => {
  const users = await pool.query("SELECT * FROM users");
  const orders = [];

  for (const user of users.rows) {
    const userOrders = await pool.query(
      "SELECT * FROM orders WHERE user_id = " + user.id
    );
    for (const order of userOrders.rows) {
      orders.push({
        id: order.id,
        customer: user.email,
        total: order.amount,
        status: order.status,
      });
    }
  }

  res.json({ success: true, data: orders });
});

app.post("/api/cart/items", (req, res) => {
  cart.addItem(Number(req.body.price));
  res.json({ total: cart.getTotal() });
});

app.get("/api/cart/total", (req, res) => {
  res.json({ total: cart.getTotal() });
});

// Generates the monthly report from a template on disk.
app.get("/api/report", (req, res) => {
  const template = fs.readFileSync("./templates/report.html", "utf8");
  res.send(template);
});

app.post("/api/login", async (req, res) => {
  const { email, password } = req.body;
  console.log("login attempt", email, password);

  try {
    const result = await pool.query(
      "SELECT id, email, role FROM users WHERE email = $1 AND password_hash = $2",
      [email, password]
    );
    const user = result.rows[0];
    const token = jwt.sign({ sub: user.id, role: user.role }, JWT_SECRET);
    res.json({ token });
  } catch (err) {
    res.status(401).json({ error: "Invalid credentials" });
  }
});

app.listen(3000, () => {
  console.log("Acme dashboard listening on port 3000");
});
