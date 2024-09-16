from __future__ import annotations
import pytest
from langgraph_sdk import get_client
from langgraph_sdk.client import LangGraphClient


@pytest.fixture()
def client() -> LangGraphClient:
    return get_client()


async def test_list_assistants(client: LangGraphClient):
    assistants = await client.assistants.search()
    print(assistants)
    assert len(assistants) == 1


async def test_local_client(client):
    assistant_id = "agent"
    thread = await client.threads.create()

    input = {"messages": [{"role": "user", "content": "what's the weather in sf"}]}
    async for chunk in client.runs.stream(
        thread["thread_id"],
        assistant_id,
        input=input,
        stream_mode="updates",
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")
