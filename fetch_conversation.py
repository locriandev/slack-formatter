#!/usr/bin/env python3

"""
This program fetches a Slack conversation by permalink and formats it for reading.
Example usage:
    python fetch_conversation.py "https://redhat-internal.slack.com/archives/CB95J6R4N/p1764683404081219"
"""

import os
import sys

from summarizerlib.slack import SlackThreadFinder


def main(permalink: str) -> None:
    """
    Fetch and format a Slack conversation.

    Arg(s):
        permalink (str): Slack permalink URL.
    """
    # Get tokens from environment - will crash if not set
    try:
        slack_token = os.environ['SLACK_TOKEN']
        user_token = os.environ['USER_TOKEN']
    except KeyError as e:
        print(f"Error: Required environment variable {e} is not set")
        print("Please set SLACK_TOKEN and USER_TOKEN environment variables")
        sys.exit(1)

    # Initialize the Slack thread finder
    finder = SlackThreadFinder(slack_token, user_token)

    print(f"Fetching conversation from: {permalink}\n")

    # Fetch the thread
    conversation = finder.fetch_thread_by_permalink(permalink)

    if not conversation:
        print("No conversation found or error occurred.")
        return

    # Format the thread for display
    formatted = finder.format_thread_for_summary(conversation)

    print("=" * 80)
    print("FORMATTED CONVERSATION")
    print("=" * 80)
    print(formatted)
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_conversation.py <slack_permalink>")
        print('Example: python fetch_conversation.py "https://redhat-internal.slack.com/archives/CB95J6R4N/p1764683404081219"')
        sys.exit(1)

    permalink = sys.argv[1]
    main(permalink)
