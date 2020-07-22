import requests
import html2text
from bs4 import BeautifulSoup
import argparse

webhook_url = "https://hooks.slack.com/services/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"
payload = { 'channels': ['#cicd-test'] }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html_report_path', type=str, required=False, default=None, help="Path to the HTML report")
    parser.add_argument('--build_number', type=str, required=False, default=None, help="CodeBuild Build Number")
    arguments = parser.parse_args()

    with open(arguments.html_report_path, "r") as f:
        text = f.read()
        soup = BeautifulSoup(text, 'html.parser')
        status = soup.find_all('span', attrs={'class': 'method-stats'})

        h = html2text.HTML2Text()
        status = h.handle(str(status[0]))
    
    
    methods = "0 method"
    passed = "0 passed"
    failed = "0 failed"
    skipped= "0 skipped"
    get_status = status.split(",")
    for i in get_status:
        if "methods" in i:
            methods = i
        elif "passed" in i:
            passed = i
        elif "failed" in i:
            failed = i
        elif "skip" in i:
            skipped = i
    
    title = "Mobile CI/CD:  Tests execution details for build #" + str(arguments.build_number)
    
    if(failed != "0 failed"):
        status = "danger"
    elif(skipped != "0 skipped"):
        if(failed != "0 failed"):
            status = "danger"
        else:
            status = "warning"
    else:
        status = "good"

    attachments = [{
        "pretext": title,
        "color": status,
        "fields": [{
            "title": "Passed Test Cases",
            "value": passed,
            "short": True,
        }, {
            "title": "Failed Test Cases",
            "value": failed,
            "short": True
        }, {
            "title": "Skipped Test Cases",
            "value": skipped,
            "short": True
        }]
    }]
    payload['attachments'] = attachments
    r = requests.post(webhook_url, json=payload)
    print(r)

if __name__ == "__main__":
    main()

