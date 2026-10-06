from accounts.models import ChatMemory, ChatMessage


SUMMARY_THRESHOLD = 30
KEEP_LAST_MESSAGES = 5
SUMMARIZE_MESSAGES = 25


def save_message(user, role, content):
    """Save a chat message for the authenticated user."""

    return ChatMessage.objects.create(
        user=user,
        role=role,
        content=content,
    )


def get_chat_history(user):
    """
    Return the user's summary and recent messages.

    When there are 30 or more messages, the caller
    should trigger summarization first.
    """

    memory, _ = ChatMemory.objects.get_or_create(
        user=user
    )

    messages = list(
        ChatMessage.objects
        .filter(user=user)
        .order_by("created_at")
    )

    return memory.summary, messages


def get_messages_for_agent(user):
    """
    Get the memory that should be passed to the agent.
    """

    memory, _ = ChatMemory.objects.get_or_create(
        user=user
    )

    messages = list(
        ChatMessage.objects
        .filter(user=user)
        .order_by("-created_at")[:KEEP_LAST_MESSAGES]
    )

    messages.reverse()

    return {
        "summary": memory.summary,
        "messages": messages,
    }


def needs_summarization(user):
    """Check whether the user's chat history needs summarization."""

    count = ChatMessage.objects.filter(user=user).count()

    return count >= SUMMARY_THRESHOLD


def get_agent_memory(user):
    memory, _ = ChatMemory.objects.get_or_create(
        user=user
    )

    messages = list(
        ChatMessage.objects
        .filter(user=user)
        .order_by("-created_at")[:KEEP_LAST_MESSAGES]
    )

    messages.reverse()

    return {
        "summary": memory.summary,
        "messages": messages,
    }