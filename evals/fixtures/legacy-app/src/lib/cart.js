// Shared cart state for the dashboard. One process, so one total.
let total = 0;

function addItem(price) {
  total += price;
}

function getTotal() {
  return total;
}

function reset() {
  total = 0;
}

module.exports = { addItem, getTotal, reset };
