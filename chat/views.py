from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from ai.agent import agent
from ai.memory import get_agent_memory, save_message
from ai.memory_summarizer import summarize_user_memory


@login_required
def chat_page(request):
    return render(request, "chat/chat.html")


@login_required
def chat_api(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required."},
            status=405,
        )

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse(
            {"error": "Message cannot be empty."},
            status=400,
        )

    user = request.user

    # Save current user message
    save_message(
        user=user,
        role="user",
        content=message,
    )

    memory = get_agent_memory(user)

    # Build conversation for the agent
    agent_messages = []

    if memory["summary"]:
        agent_messages.append(
            {
                "role": "system",
                "content": (
                    "Here is the customer's previous conversation "
                    f"memory:\n\n{memory['summary']}"
                ),
            }
        )

    for chat_message in memory["messages"]:
        agent_messages.append(
            {
                "role": chat_message.role,
                "content": chat_message.content,
            }
        )

    # Current message is already included in memory because
    # it was saved above.
    response = agent.invoke(
        {
            "messages": agent_messages,
        },
        context={
            "user_id": request.user.id,
        },
    )

    answer = response["messages"][-1].content

    # Save assistant response
    save_message(
        user=user,
        role="assistant",
        content=answer,
    )

    # Compress old history when necessary
    summarize_user_memory(user)

    return JsonResponse(
        {
            "response": answer,
        }
    )