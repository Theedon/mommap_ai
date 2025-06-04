from typing import Dict, List

from langchain.schema import AIMessage, HumanMessage


def format_chat_history(message_list: List[Dict]):
    """
    Convert a list of message dictionaries to a chat history format.

    Args:
        message_list: List of dictionaries containing message data

    Returns:
        List of HumanMessage or AIMessage objects

    Raises:
        TypeError: If input is not a list or messages are not dictionaries
        ValueError: If required message fields are missing or role is invalid
    """
    if not isinstance(message_list, list):
        raise TypeError("Input must be a list of messages")

    chat_history = []

    for i, msg in enumerate(message_list):
        if msg is None:
            continue

        if not isinstance(msg, dict):
            raise TypeError(f"Message at index {i} must be a dictionary")

        try:
            role = msg.get("identifier", "").strip().lower()
            content = msg.get("message", "")

            if not role:
                raise ValueError(f"Message at index {i} is missing 'identifier' field")
            if not content:
                raise ValueError(f"Message at index {i} is missing 'message' field")

            if role == "human":
                chat_history.append(HumanMessage(content=content))
            elif role == "agent":
                chat_history.append(AIMessage(content=content))
            else:
                raise ValueError(f"Invalid message role at index {i}: {role}")

        except AttributeError as e:
            raise TypeError(f"Invalid message format at index {i}: {str(e)}")

    return chat_history
