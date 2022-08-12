# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import os
import json
import base64
from github import GithubIntegration


def handler(event, context):

    app_id = os.environ["BOT_ID"]
    app_key_encoded = os.environ["BOT_CERT"]
    app_key = base64.b64decode(app_key_encoded)

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
