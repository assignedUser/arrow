import os
import json
from github import GithubIntegration


def handler(event, context):

    app_id = os.environ["BOT_ID"]
    app_key = os.environ["BOT_CERT"]

    git_integration = GithubIntegration(
        app_id,
        app_key,
    )

    # Check if the event is a GitHub PR creation event
    if not all(k in event.keys() for k in ['action', 'issue', 'comment']) \
       or not 'pull_request' in event['issue'] \
       or not event['action'] in ['created', 'edited'] \
       or not event['comment']['body'].startswith('@github-actions'):
        print("Not a triggering PR comment.")
        return {
            'statusCode': 200
        }

    # if payload['comment']['user'] == "crossbow-bot[bot]":
    #   return "Don't react to own comments."

    installation_id = event['installation']['id']
    payload_json = json.dumps(event)

    with open('/tmp/payload.json', 'w') as f:
        f.write(payload_json)

    # setup archery env
    comment_token = git_integration.get_access_token(installation_id).token

    os.environ["GITHUB_SERVER_URL"] = "https://github.com"
    os.environ["GITHUB_RUN_ID"] = "42"
    os.environ["GITHUB_REPOSITORY"] = event['repository']['full_name']
    os.environ["ARROW_GITHUB_TOKEN"] = comment_token

    cmd = ("archery trigger-bot --event-name issue_comment --event-payload /tmp/payload.json")
    archery_out = os.popen(cmd).read()

    print(archery_out)
    return {
        'statusCode': 200
    }
