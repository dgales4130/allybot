import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
INTRO_COMMAND = "intro"
introCommands = ['intro', 'Who can I tweet?', 'Get to know community', 'I\'m just starting']
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def intro_command(command, channel):

    response = "Not sure what you mean. Use the *" + INTRO_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(INTRO_COMMAND):
        response = ("Hello. Thank you for accessing Allybot! Please enter: "
        " \n `Who can I tweet?`         To reach out to know allies on twitter "
        " \n `Get to know community`    To learn about well known community members"
        " \n `I'm just starting`        To interact with bot about concepts and in allyship")
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                return output['text'].strip().lower(), output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("allybot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                if command in introCommands:
                    intro_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
