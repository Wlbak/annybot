from telethon import events

from .. import client


@client.on(events.NewMessage(pattern=r'^-da$', outgoing=True))
async def dat(context):
    input_chat = await context.get_input_chat()
    messages = []
    count = 0
    async for message in context.client.iter_messages(input_chat, min_id=1):
        messages.append(message)
        count += 1
        messages.append(1)
        if len(messages) == 100:
            await context.client.delete_messages(input_chat, messages)
            messages = []
        if messages:
            await context.client.delete_messages(input_chat, messages)