const API_URL = "http://127.0.0.1:8000";

// ---------------------------
// Token management
// ---------------------------
function setTokens(access, refresh) {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
}

function getAccessToken() {
    return localStorage.getItem("access");
}

function getRefreshToken() {
    return localStorage.getItem("refresh");
}

// ---------------------------
// Generic fetch with JWT
// ---------------------------
async function authFetch(url, options = {}) {
    const token = getAccessToken();
    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
    };

    let response = await fetch(url, options);

    if (response.status === 401) {
        // Try refreshing token
        const refresh = getRefreshToken();
        const r = await fetch(`${API_URL}/api/users/token/refresh/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });

        if (r.ok) {
            const data = await r.json();
            setTokens(data.access, refresh);
            return authFetch(url, options); // Retry original request
        } else {
            alert("Session expired. Please login again.");
            window.location.href = "/";
        }
    }

    return response;
}

// ---------------------------
// Redirect to login if not authenticated (tasks page)
// ---------------------------
if (window.location.pathname.endsWith("tasks-page/") ||
    window.location.pathname.endsWith("tasks.html")) {
    if (!getAccessToken()) {
        window.location.href = "/";
    }
}
