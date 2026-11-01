# FrightForge
A REST API for sharing and approving Halloween costume ideas. Users submit ideas; admins approve them via the API.  


## 🎃 Features  
- User-submitted costume ideas  
- Admin approval system (via API)  
- RESTful endpoints for managing ideas  


## 🧰 Tech Stack  
- Python + FastAPI
- Uvicorn (ASGI server)
- PostgreSQL (with Pydantic models)
- JWT for admin authentication

## 🚀 API Endpoints
<details>
  <summary>GET <code>/generate</code></summary>
  <pre><code>{
  "adjective": "evil",
  "creature": "bat",
  "accessory": "ring"
}</code></pre>
</details>

<details>
  <summary>GET <code>/costumes</code></summary>
  <pre><code>{
  "ok": true,
  "suits": [] # approved suits list
}</code></pre>
</details>

<details>
  <summary>POST <code>/costumes</code></summary>
  <p>Expected request JSON body:</p>
  <pre><code>{
  "adjective": string,
  "creature": string,
  "accessory": string,
  "author": string | email | unique
}</code></pre>

  <p>Response JSON body:</p>
  <pre><code>{
  "ok": bool,
  "message": string | error message
}</code></pre>
</details>

### Admin routes

<details>
  <summary>POST <code>/admin/login</code></summary>
  <p>Expected request JSON body:</p>
  <pre><code>{
  "login": string,
  "password": string,
}</code></pre>

  <p>Response JSON body:</p>
  <pre><code>{
  "access_token": string | JWT token,
  "expires_in": int
}</code></pre>
</details>


<details>
  <summary>GET <code>/admin/costumes</code></summary>
  <pre><code>{
  "ok": bool,
  "suits": [] # list of pending suits
}</code></pre>
</details>


<details>
  <summary>PATCH <code>/admin/costumes/{id}</code></summary>
  <p>Expected request JSON body:</p>
  <pre><code>{
  "status": "approved" | "rejected"
}</code></pre>

  <p>Response JSON body:</p>
  <pre><code>{
  "ok": bool,
  "message": string | error message
}</code></pre>
</details>

---

<p>Unauthorized Error Response:</p>
<pre><code># Status Code: 401
{
  "detail": "Invalid or expired token"
}</code></pre>
