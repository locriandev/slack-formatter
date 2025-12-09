#!/usr/bin/env python3

"""
FastAPI application for fetching and formatting Slack conversations.

This web service provides an HTTP endpoint to fetch Slack thread conversations
by permalink and return them as formatted plain text.

Examples:
    Run the server:
        uvicorn app:app --reload

    Access the endpoint:
        curl "http://localhost:8000/thread?url=https://redhat-internal.slack.com/archives/CB95J6R4N/p1764683404081219"
"""

import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

from summarizerlib.slack import SlackThreadFinder


app = FastAPI(
    title="Slack Thread Summarizer",
    description="Fetch and format Slack conversations by permalink",
    version="1.0.0"
)

# Initialize Slack tokens from environment
# Will crash at startup if these are not set
SLACK_TOKEN = os.environ['SLACK_TOKEN']
USER_TOKEN = os.environ['USER_TOKEN']


def _get_slack_finder() -> SlackThreadFinder:
    """
    Initialize and return a SlackThreadFinder instance.

    Return Value(s):
        SlackThreadFinder: Configured instance for fetching Slack threads.
    """
    return SlackThreadFinder(SLACK_TOKEN, USER_TOKEN)


@app.get("/thread", response_class=PlainTextResponse)
async def get_thread(
    url: str = Query(..., description="Slack permalink URL to the thread")
) -> str:
    """
    Fetch a Slack thread by permalink and return it as formatted plain text.

    Arg(s):
        url (str): The Slack permalink URL (e.g., https://workspace.slack.com/archives/CHANNEL/pTIMESTAMP).

    Return Value(s):
        str: Formatted conversation as plain text.

    Raises:
        HTTPException: If the URL is invalid or the thread cannot be fetched.
    """
    finder = _get_slack_finder()

    # Fetch the thread
    conversation = finder.fetch_thread_by_permalink(url)

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="No conversation found. Please check the URL format and try again."
        )

    # Format the thread for display
    formatted = finder.format_thread_for_summary(conversation)

    return formatted


@app.get("/", response_class=PlainTextResponse)
async def root() -> str:
    """
    Root endpoint providing API usage information.

    Return Value(s):
        str: API usage instructions.
    """
    return """Slack Thread Summarizer API

Usage:
  GET /thread?url=<slack-permalink>

Example:
  curl "http://localhost:8000/thread?url=https://redhat-internal.slack.com/archives/CB95J6R4N/p1764683404081219"
"""
