const test = require("node:test");
const assert = require("node:assert");
const cart = require("../src/lib/cart");

test1 = test("test1", async () => {
  cart.reset();
  cart.addItem(10);
  await new Promise((resolve) => setTimeout(resolve, 1000));
  assert.equal(cart.getTotal(), 10);
  console.log("cart test passed");
});

test("test2", async () => {
  const fakeDb = {
    query: async () => ({ rows: [{ id: 1, email: "john@example.com" }] }),
  };
  await fakeDb.query("SELECT * FROM users");
  assert.ok(fakeDb.query);
});
