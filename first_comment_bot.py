import httplib2
import os
import sys
import time

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# ======== Configure the following variables ===========
# waiting time intervel in seconds
intervel = 3.5
# comment you need to post
comment = "YOUR_MESSAGE"

CLIENT_SECRETS_FILE = "./client_secrets.json"
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the APIs Console
https://console.developers.google.com
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(
    os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE)
)


def get_authenticated_service(args):
    flow = flow_from_clientsecrets(
        CLIENT_SECRETS_FILE,
        scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
    )

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)
    with open("youtube-v3-discoverydocument.json", "r") as f:
        doc = f.read()
        return build_from_document(doc, http=credentials.authorize(httplib2.Http()))


def insert_comment(youtube, parent_id, text):
    insert_result = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": parent_id,
                "topLevelComment": {"snippet": {"textOriginal": text}},
            }
        },
    )
    response = insert_result.execute()
    print("comment added")


def lastvideo(youtube, cid):
    request = youtube.activities().list(
        channelId=cid,
        part="contentDetails",
        maxResults=1,
    )
    response = request.execute()
    return response["items"][0]["contentDetails"]["upload"]["videoId"]


argparser.add_argument("--cid", help="Required; YouTube client ID")
argparser.add_argument("--lastvid", help="Required; Last video ID")
args = argparser.parse_args()


youtube = get_authenticated_service(args)


while True:
    last = lastvideo(youtube, args.cid)

    if last != args.lastvid:
        print(last)
        try:
            insert_comment(youtube, last, comment)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        else:
            print("Comment Inserted")
            break
    time.sleep(intervel)
    print("waiting......")
