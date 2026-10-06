from langchain_ollama import ChatOllama

from accounts.models import ChatMemory, ChatMessage


llm = ChatOllama(
    model="qwen3.5:4b",
    temperature=0,
)


def summarize_user_memory(user):
    """
    Summarize older chat messages while keeping the
    most recent 5 messages untouched.
    """

    memory, _ = ChatMemory.objects.get_or_create(
        user=user
    )

    messages = list(
        ChatMessage.objects
        .filter(user=user)
        .order_by("created_at")
    )

    if len(messages) < 30:
        return

    old_messages = messages[:-5]

    conversation = "\n".join(
        f"{message.role.upper()}: {message.content}"
        for message in old_messages
    )

    previous_summary = memory.summary or "No previous summary."

    prompt = f"""
You maintain long-term memory for a customer support chatbot.

Previous memory summary:
{previous_summary}

Here are the older messages that should be incorporated
into the memory:

{conversation}

Create a concise summary containing only useful information
that would help the assistant continue the conversation.

Focus on:
- User preferences
- Problems they discussed
- Questions they asked
- Important decisions
- Relevant account/content context
- Important unresolved issues

Do not include unnecessary conversational filler.

Return only the updated memory summary.
"""

    response = llm.invoke(prompt)

    memory.summary = response.content
    memory.save(update_fields=["summary", "updated_at"])

    ChatMessage.objects.filter(
        id__in=[message.id for message in old_messages]
    ).delete()