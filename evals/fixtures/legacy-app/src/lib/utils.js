// Shared helpers. Imported from many places, so keep them generic.
function safeGet(obj, path, fallback) {
  const parts = path.split(".");
  let current = obj;
  for (const part of parts) {
    if (current == null) return fallback;
    current = current[part];
  }
  return current == null ? fallback : current;
}

function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

function formatDate(date) {
  const d = new Date(date);
  return d.getMonth() + 1 + "/" + d.getDate() + "/" + d.getFullYear();
}

function formatCurrency(amount) {
  return "$" + amount.toFixed(2);
}

function isEmpty(value) {
  if (value == null) return true;
  if (typeof value === "string") return value.trim().length === 0;
  if (Array.isArray(value)) return value.length === 0;
  if (typeof value === "object") return Object.keys(value).length === 0;
  return false;
}

function noop() {}

function padNumber(value) {
  return value < 10 ? "0" + value : String(value);
}

module.exports = {
  safeGet,
  deepClone,
  formatDate,
  formatCurrency,
  isEmpty,
  noop,
  padNumber,
};
