import requests
from os import environ
from functools import wraps

class SlackReporter:
    """
    Sends status updates to Slack.

    The webhook_url can be obtained by creating a new app on Slack with 
    the 'incoming-webhook' scope and linking it to your Slack workspace and channel.

    SlackReporter will look for a webhook_url environment variable. 

    To add a value to environment variables in a virtual environment, add
    'export SLACK_WEBHOOK_URL=value' to the end of your bin/activate script.  
    """
    def __init__(self, webhook_url=None):
        self.webhook_url = webhook_url   
        if not webhook_url:
            self.webhook_url = environ.get('SLACK_WEBHOOK_URL')

    def send_message(self, title, message, status):
        """
        Send a message to Slack

        args:
            massage: message text. Use '\n' for newline, supports markdown formatting **, ~~ etc.
            title: title of the report
            status: 'good', 'warning' or 'danger'

        Prints an error message if Slack does not return 200 status codes
        """
        headers = {'Content-type': 'application/json; charset=utf-8'}
        payload = {
            "text": ":robot_face: \n",
            "mrkdwn": True,
            "attachments": [
                {
                    "title": title,
                    "text": message,
                    "color": status,
                }
            ]
        }

        r = requests.post(self.webhook_url, headers=headers, json=payload)
        
        if not r.status_code == 200:
            print("Error sending message to Slack", message)

    def report(self, title='New Report', status='good'):
        """
        Send the return value of the decorated function to Slack
    
        args:
            title: title of the report
            status: 'good', 'warning' or 'danger'
        """
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                message = function(*args, **kwargs)
                self.send_message(title, message, status)     
            return wrapper
        return decorator


reporter = SlackReporter()
reporter.send_message('this is a new title', 'Hi max!', 'good')

@reporter.report(title='Rendering', status='good')
def do_stuff(name):
    return name

# do_stuff('things have happened')

