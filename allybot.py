import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
INTRO_COMMAND = "intro"
introCommands = ['intro', 'Who can I tweet?', 'Get to know community', 'ally portal']
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def intro_command(command, channel):


    response = "Not sure what you mean. Use the *" + INTRO_COMMAND + \
               "* command with numbers, delimited by spaces."

    if command.startswith("ally portal"):
        response=("Welcome. Now to learn allyship. This will: \n"
        "1) Teach you some concepts and terms\n"
        "2) Teach you how the 'contept and terms' can be translated into 'roles and responsibilities'\n"



    if command.startswith("intro"):
        response = ("Hello. Thank you for accessing Allybot! Please enter: "
        " \n `Who can I tweet?`         To reach out to know allies on twitter "
        " \n `Get to know community`    To learn about well known community members"
        " \n `Ally Portal`        To talk to me about some concepts and terms related to allyship")


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
