from twilio.rest import Client

# Replace these with your actual Twilio credentials and phone numbers
accsid='AC157275876e1b54339b681aa208316e18'
acctoken='a5bfa826229ac5ac18ccbae4d24f9d05'

twilionm='+19045670832'
targetnm='+919987342709'    

client = Client(accsid, acctoken)

message = client.messages.create(
    body="Hello there!",
    from_=twilionm,
    to=targetnm
)

print(f"Message SID: {message.sid}")  # Added print to see if it works.