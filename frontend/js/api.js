const API_BASE_URL = "http://127.0.0.1:8000/api";

const api = {
  getToken() { return localStorage.getItem("access_token"); },
  setTokens(access, refresh) {
    localStorage.setItem("access_token", access);
    if (refresh) localStorage.setItem("refresh_token", refresh);
  },
  clearTokens() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },
  isLoggedIn() { return !!this.getToken(); },

  async request(path, { method = "GET", body = null, auth = true } = {}) {
    const headers = { "Content-Type": "application/json" };
    if (auth && this.getToken()) headers["Authorization"] = `Bearer ${this.getToken()}`;

    const response = await fetch(`${API_BASE_URL}${path}`, {
      method, headers, body: body ? JSON.stringify(body) : null,
    });

    let data = null;
    const text = await response.text();
    if (text) { try { data = JSON.parse(text); } catch (e) { data = text; } }

    if (!response.ok) {
      const error = new Error("API request failed");
      error.status = response.status;
      error.data = data;
      throw error;
    }
    return data;
  },

  get(path, opts = {}) { return this.request(path, { ...opts, method: "GET" }); },
  post(path, body, opts = {}) { return this.request(path, { ...opts, method: "POST", body }); },
};

function extractErrorMessage(err) {
  const data = err && err.data;
  if (!data) return "Something went wrong. Please try again.";
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  if (data.non_field_errors) return data.non_field_errors.join(" ");
  const firstKey = Object.keys(data)[0];
  if (firstKey && Array.isArray(data[firstKey])) return `${firstKey}: ${data[firstKey][0]}`;
  return "Something went wrong. Please try again.";
}

function requireAuth() {
  if (!api.isLoggedIn()) window.location.href = "login.html";
}

function logout() {
  api.clearTokens();
  window.location.href = "login.html";
}

function renderNavbar(active) {
  const el = document.getElementById("navbar");
  if (!el) return;
  const loggedIn = api.isLoggedIn();
  const links = loggedIn
    ? `<a href="stations.html" class="${active === "stations" ? "active" : ""}">Find Stations</a>
       <a href="bookings.html" class="${active === "bookings" ? "active" : ""}">My Bookings</a>
       <a href="history.html" class="${active === "history" ? "active" : ""}">History</a>
       <a href="#" onclick="logout(); return false;">Logout</a>`
    : `<a href="login.html">Login</a> <a href="signup.html">Sign Up</a>`;
  el.innerHTML = `<div class="brand">⚡ EV<span>Charge</span></div>
    <nav><a href="index.html" class="${active === "home" ? "active" : ""}">Home</a>${links}</nav>`;
}
