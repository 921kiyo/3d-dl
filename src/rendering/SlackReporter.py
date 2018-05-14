import requests
from os import environ
from functools import wraps

class SlackReporter:
    """
    Sends status updates to Slack.

    SlackReporter supports to methods for sending messages:
        a send_message() method where a message is passed as an argument
        a @report() decorator which sends a message containing the return value of the 
            function passed to it

    Connecting to Slack:
        SlackReporter will look for a SLACK_WEBHOOK_URL environment variable to 
        authenticate with Slack.

        To add a value to environment variables in a virtual environment, add
        'export SLACK_WEBHOOK_URL=value' to the end of your bin/activate script.  

        The webhook_url can be obtained by creating a new app on Slack with 
        the 'incoming-webhook' scope and linking it to your Slack workspace and channel.

    Example usage:
        reporter = SlackReporter()

        reporter.send_message('message')

        @reporter.report(title='Rendering', status='good')
        def do_stuff(words):
            return words
        do_stuff('things have happened')

    """
    def __init__(self, webhook_url=None, disable=False):
        self.webhook_url = webhook_url   
        if not webhook_url:
            self.webhook_url = environ.get('SLACK_WEBHOOK_URL')
            self.disable = True #disable

    def send_message(self, message, title='New report', status='', print_message=False):
        """
        Send a message to Slack

        args:
            message: message text. Use '\n' for newline, supports markdown formatting **, ~~ etc.
            title: title of the report
            status: 'good', 'warning', 'danger' or ''. These alter to the attachement colour in Slack.
            print_message: also print the message to the screen

        Prints an error message if Slack does not return 200 status codes
        """
        if self.disable:
            return

        if print_message:
            print(message)

        headers = {'Content-type': 'application/json; charset=utf-8'}
        payload = {
            # "text": ":robot_face: \n",
            "mrkdwn": True,
            "attachments": [
                {
                    "title": title,
                    "text": str(message),
                    "color": status,
                }
            ]
        }

        r = requests.post(self.webhook_url, headers=headers, json=payload)
        
        if not r.status_code == 200:
            print("Error sending message to Slack", message)

    def report(self, title='New Report', status='', print_message=False):
        """
        Send the return value of the decorated function to Slack
    
        args:
            title: title of the report
            status: 'good', 'warning' or 'danger'
            print_message: also print the message to the screen
            
        """
        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                message = str(function(*args, **kwargs))
                
                if self.disable:
                    return

                if print_message:
                    print(message)

                self.send_message(message, title, status)     
            return wrapper
        return decorator

# reporter = SlackReporter(disable=False)

# # blender_attributes = {
# #     "attribute_distribution_params": [["num_lamps","mid", 6], ["num_lamps","scale", 0.4], ["lamp_energy","mu", 500.0], ["lamp_size","mu",5], ["camera_radius","sigmu",0.1]],
# #     "attribute_distribution" : []
# # }

# # reporter.send_message(blender_attributes)

# @reporter.report(title='Rendering', status='good', print_message=True)
# def do_stuff(words):
#     return words

# do_stuff('things have happened')


