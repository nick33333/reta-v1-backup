# NOTE ABOUT THIS REPO AND THE RETA WEBAPP BY LUKE KERBS

This repo was created for the need of public access to SupertechFT's RETA webapp through github. Original RETA webapp was developed by Luke Kerbs.

# RETA (Robotics Educational Teaching Agent)

RETA is a Python / [Flask](https://flask.palletsprojects.com/en/1.1.x/) based web application for teaching and learning robotics from anywhere. It is a web-based interface for remotely teaching and learning robotics. RETA is teaching tool for instructors and it offers students instant, live remote access to robots from their laptop.

If you are new to Flask, please do some research. Try to create a simple Flask app (there are many Flask tutorials you can follow along with on YouTube). Once you feel comfortable with the basics of Flask, Python, HTML, and Javascript, you will be ready to start developing RETA.

## Dependencies

If you are setting up a new Raspberry Pi, use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the necessary libraries used in RETA. **Note:** This will not apply to most users. If you are not setting up a new Raspberry Pi with a new robot then please skip this step.

```bash
pip3 install -r requirements.txt
```

## Usage

To run the app, execute the following terminal command:

```bash
python3 app.py
```
The app will start running, and you will be given a link to the RETA log in page. If you are connected to the same WiFi as the Dobot, then select the local link. For the majority of users, select the remote link.

We are not offering RETA to the public at this time, so please ask Luke for account credentials via Slack or email.

## Contributing
We will track all changes to RETA with issues on GitHub. When you are ready to contribute to the code base, talk to Luke about which issues to work on.

When you feel your code edits are ready for review, make a pull request. Someone will review and test your code. If your code passes review, it will be merged to the main branch.

If you are contributing please do all of your work on your own branch.
