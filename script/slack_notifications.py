import requests
import argparse

webhook_url = "https://hooks.slack.com/services/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"
payload = {'channels': ['#ci-cd']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host_address', type=str, required=False, default=None, help="Host machine address")
    arguments = parser.parse_args()

    attachments = [
      {
          "color": "#2eb886",
          "pretext": "AWS CodePipeline has completed successfully.",
          "title": "Library Management System",
          "title_link": "http://{}:8000/".format(arguments.host_address),
          "text": " The web application has been deployed over AWS EC2 Instance",
          "fields": [
              {
                  "title": "Application Server URL",
                  "value": "http://{}:8000/".format(arguments.host_address)
              }
          ],
          "footer": "Copper App notification"

      }
  ]
    payload['attachments'] = attachments
    r = requests.post(webhook_url, json=payload)
    print(r)

if __name__ == "__main__":
    main()

