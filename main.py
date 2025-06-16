import openai
import os
import random
import time
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_warehouse_capacity(warehouse_id: str):
    cap = random.randint(20, 120)
    return {"capacity": cap}

warehouse_tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_warehouse_capacity",
            "description": "Get real-time available capacity for a given warehouse.",
            "parameters": {
                "type": "object",
                "properties": {
                    "warehouse_id": {
                        "type": "string",
                        "description": "ID or name of the warehouse."
                    }
                },
                "required": ["warehouse_id"]
            }
        }
    }
]

class OrderInput(BaseModel):
    customer_name: str
    order_id: str
    items: str
    region: str
    priority: str

@app.post("/assign-warehouse")
async def assign_warehouse(order: OrderInput):
    assistant = openai.beta.assistants.create(
        model="gpt-4o",
        instructions=(
            "You are a warehouse fulfillment agent. "
            "For EVERY incoming order, you MUST use the get_warehouse_capacity tool for EACH warehouse you want to consider. "
            "Never answer based on your own knowledge; always call the tool first and only then decide. "
            "If you do not call the tool, you are making a mistake."
        ),
        tools=warehouse_tool_schema
    )

    thread = openai.beta.threads.create()

    user_content = (
        f"Customer: {order.customer_name}\n"
        f"Order ID: {order.order_id}\n"
        f"Items: {order.items}\n"
        f"Region: {order.region}\n"
        f"Priority: {order.priority}\n"
        "Please check the real-time capacity of the warehouses and assign the best one."
    )
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_content
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print("run status is " + str(run_status.status))
        if run_status.status == "requires_action":
            tool_outputs = []
            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                args = eval(tool_call.function.arguments)
                output = get_warehouse_capacity(args["warehouse_id"])
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(output)
                })
            run = openai.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        elif run_status.status in ["completed", "failed", "cancelled", "expired"]:
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data[::-1]:
        if msg.role == "assistant":
            answer = msg.content[0].text.value
            break
    else:
        answer = "No answer received."
    return {"result": answer}
