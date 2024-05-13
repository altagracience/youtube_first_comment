
# YouTube Comment Bot

This Python script automates the process of posting comments on YouTube videos. It utilizes the YouTube Data API to fetch the latest video uploaded by a specified channel and adds a predefined comment to it.

## Prerequisites

- Python 
- `httplib2`
- `oauth2client`
- `apiclient` (from google-api-python-client)

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/altagracience/youtube_first_comment.git
    ```

2. Navigate to the project directory:

    ```bash
    cd youtube_first_comment
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Obtain OAuth 2.0 credentials by following the instructions in the [YouTube Data API documentation](https://developers.google.com/youtube/registering_an_application).

5. Save the obtained `client_secrets.json` file in the project directory.

6. Modify the script:
   - Set the `intervel` variable to specify the time interval (in seconds) between each check for new videos.
   - Replace `"YOUR_MESSAGE"` in the `comment` variable with the desired comment you want to post.

## Usage

Run the script with the following command:

```bash
python youtube_comment_bot.py --cid <channel_id> --lastvid <last_video_id>
```

Replace `<channel_id>` with the ID of the YouTube channel you want to monitor and `<last_video_id>` with the ID of the last video you commented on (or any video ID to start monitoring from).

## Notes

- Make sure to comply with YouTube's [Community Guidelines](https://www.youtube.com/about/policies/).
- This script is for educational purposes only and should be used responsibly.

---

Feel free to expand on this README with additional details or instructions as needed.