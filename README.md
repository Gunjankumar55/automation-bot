-----

# 🎬 YouTube Video Processor API

This Flask API simplifies YouTube video downloading and resizing using **`yt-dlp`** and **`ffmpeg`**. It's perfect for automating workflows (e.g., YouTube Shorts creation with **n8n**) and deploys easily on **Railway**.

-----

## 📦 Key Features

  * **Download & Resize:** Downloads YouTube videos and resizes them to 720px width (maintains aspect ratio).
  * **Cookie Support:** Handles age-restricted or trending videos by using browser cookies.
  * **Easy Deployment:** Designed for quick deployment on **Railway** with a **Dockerfile**.
  * **Automation-Friendly:** Integrates smoothly with tools like **n8n** via a simple POST request.

-----

## 🛠️ Get Started

### 1\. Project Setup

Clone the repository and ensure you have `main.py`, `Dockerfile`, and `cookies.txt` (see next step) in your project root.

```bash
git clone https://github.com/your-username/youtube-video-api.git
cd youtube-video-api
```

### 2\. Get Your `cookies.txt`

For restricted videos, install the "Get cookies.txt" browser extension (Chrome/Firefox). Log in to YouTube, export your cookies as a Netscape-formatted `cookies.txt` file, and place it in your project's root.

### 3\. Deploy to Railway

Go to [Railway.app](https://railway.app), create a new project, and deploy from your GitHub repo. Railway will automatically detect the **Dockerfile** and give you a public URL upon successful deployment.

-----

## 🔌 API Usage

Send a **POST** request to `/process` with a JSON body.

**Endpoint:** `/process`
**Method:** `POST`
**Content-Type:** `application/json`

**Request Body Example:**

```json
{
  "videoId": "dQw4w9WgXcQ",
  "title": "Optional Video Title"
}
```

**Successful Response:**

```json
{
  "status": "success",
  "output": "output.mp4"
}
```

**n8n Example:** Use an HTTP Request node with your Railway URL, Method: `POST`, and `videoId` (and optional `title`) in the JSON body.

-----

## 🧠 Why `cookies.txt`?

It allows **`yt-dlp`** to bypass login requirements for age-restricted, trending, or CAPTCHA-protected YouTube videos by mimicking your browser's authenticated session.

-----

## 📁 Project Structure

```
.
├── main.py         # Flask application
├── Dockerfile      # For containerized deployment
└── cookies.txt     # Exported YouTube cookies
```

-----

## 🛠 Tech Stack

**Python 3.10**, **Flask**, **`yt-dlp`**, **`ffmpeg`**, **Docker**, **Railway**.

-----

## 📬 Support & 📄 License

For issues, open a [GitHub Issue](https://www.google.com/search?q=https://github.com/your-username/youtube-video-api/issues) or reach out. This project is under the **MIT License**.

```
```
