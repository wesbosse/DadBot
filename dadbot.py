import os
import time
import re
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

time_delay = .2 # 1 second delay between reading from RTM 
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
IM_REGEX = "^([Ii]'[Mm])(.*)" #hi regex, I'm dad

def parse_commands(slack_events):
    '''
        searches for bot mentions and keywords in messages

        for mentions:
            returns the user mentioned and text that follows

        for "I'm" statements:
            returns junk and the joke punchline
    '''
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            print(event["text"])
            user_id, message = parse_direct_mention(event["text"], MENTION_REGEX)
            print(message)
            if user_id == None:
                print(event["text"])
                _, message = parse_direct_mention(event["text"], IM_REGEX)
                print(message)
            if user_id == starterbot_id or ((message != None) and (user_id == None)):
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text, operator):
    '''
        checks message text against the specific cases we have designated
        returns the corresponding groups if a pattern matches, otherwise returns (None, None)
    '''
    matches = re.search(operator, message_text)
    try:
        print(matches.group)
    except:
        pass
    #first group will be the matched phrase (username, "I'm", etc). Second Group is the message text
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    default_response = "Try again, idiot"

    # Finds and executes the given command, filling in response
    response = None

    if command.startswith('tell me about'):
        response = "Wesley is a nerd, and his code is lame"
    else:
        response = "Hi '{}', I'm Dad.".format(command)
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Why would you even want to build something like this......")
        print("Anyways, its working. ")
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(time_delay)
    else:
        print("Connection failed. Read through all of this bullshit to figure it out ^^^")