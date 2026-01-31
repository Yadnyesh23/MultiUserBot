from pyrogram import Client

api_id = int(input("Enter API ID: "))
api_hash = input("Enter API HASH: ")

with Client(
    name="session",
    api_id=9468065,
    api_hash='658aa517e60ea5fed17eb99c9466279e',
    in_memory=True
) as app:
    print("\n✅ SESSION STRING:\n")
    print(app.export_session_string())