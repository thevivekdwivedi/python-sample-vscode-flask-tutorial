from flask import Flask  # Import the Flask class
app = Flask(__name__)    # Create an instance of the class for our use

app.config.update(
    AZURE_CLIENT_ID='92ea35ba-dae9-4731-941c-51bbd2f7dac6',
    AZURE_TENANT='ea7bec13-76eb-4f00-ad1a-4da88023607f',
    AZURE_SECRET='qw?ppzdARMd5t6qfly[MQNs?8oKMyi4='
)
