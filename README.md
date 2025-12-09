# Slack Formatter

A FastAPI-based web service and CLI tool for fetching and formatting Slack thread conversations. This tool retrieves Slack threads via permalink URLs and returns them as formatted plain text, making them easy to read and process.

## Features

- **FastAPI Web Service**: HTTP API endpoint for fetching Slack threads
- **CLI Tool**: Command-line script for direct thread retrieval
- **Docker Support**: Containerized deployment with Red Hat UBI base image
- **Clean Formatting**: Converts Slack threads into readable conversation format
- **User Name Resolution**: Automatically resolves Slack user IDs to real names

## Prerequisites

- Python 3.11+
- Slack Bot Token (`xoxb-...`)
- Slack User Token (`xoxp-...`)

## Installation

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd slack-formatter

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SLACK_TOKEN=xoxb-your-bot-token
export USER_TOKEN=xoxp-your-user-token
```

### Docker

```bash
# Build the image
docker build -t slack-formatter .

# Run the container
docker run -p 8000:8000 \
  -e SLACK_TOKEN=xoxb-your-bot-token \
  -e USER_TOKEN=xoxp-your-user-token \
  slack-formatter
```

## Configuration

The application requires two environment variables:

| Variable | Description | Example    |
|----------|-------------|------------|
| `SLACK_TOKEN` | Slack Bot Token | `xoxb-...` |
| `USER_TOKEN` | Slack User Token | `xoxp-...` |

**Note**: The application will crash at startup if these environment variables are not set.

## Usage

### FastAPI Web Service

Start the server:

```bash
# Development mode with auto-reload
uvicorn app:app --reload

# Production mode
uvicorn app:app --host 0.0.0.0 --port 8000
```

Access the API:

```bash
curl "http://localhost:8000/thread?url=https://workspace.slack.com/archives/CHANNEL_ID/pTIMESTAMP"
```

### CLI Tool

```bash
python fetch_conversation.py "https://workspace.slack.com/archives/CHANNEL_ID/pTIMESTAMP"
```

Example:

```bash
python fetch_conversation.py "https://redhat-internal.slack.com/archives/CB95J6R4N/p1764683404081219"
```

### Docker

```bash
docker run -p 8000:8000 \
  -e SLACK_TOKEN=$SLACK_TOKEN \
  -e USER_TOKEN=$USER_TOKEN \
  slack-formatter
```

Then access via curl:

```bash
curl "http://localhost:8000/thread?url=https://workspace.slack.com/archives/CHANNEL_ID/pTIMESTAMP"
```

## API Endpoints

### `GET /thread`

Fetch and format a Slack thread.

**Query Parameters:**
- `url` (required): Slack permalink URL

**Example Request:**

```bash
curl "http://localhost:8000/thread?url=https://workspace.slack.com/archives/CB95J6R4N/p1764683404081219"
```

**Example Response:**

```
- John Doe: Hey team, we need to discuss the deployment
- Jane Smith: I agree, let's schedule a meeting
- John Doe: How about tomorrow at 2pm?
- Jane Smith: Works for me!
```

**Error Responses:**
- `404 Not Found`: Thread not found or invalid URL format
- `500 Internal Server Error`: Missing environment variables

### `GET /`

API information and usage instructions.

**Example Request:**

```bash
curl http://localhost:8000/
```

## How It Works

1. **Permalink Parsing**: Extracts channel ID and timestamp from Slack permalink URLs
   - Format: `https://{workspace}.slack.com/archives/{CHANNEL_ID}/p{TIMESTAMP}`
   - Timestamp conversion: `1234567890123456` → `1234567890.123456`

2. **Thread Retrieval**: Uses Slack API's `conversations.replies` endpoint to fetch all messages in the thread

3. **User Resolution**: Resolves Slack user IDs to real names using the `users.info` endpoint (with caching)

4. **Formatting**: Converts messages to readable format: `- Username: Message text`
