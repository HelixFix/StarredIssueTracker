# Starred Issue Tracker

This script retrieves and filters help-wanted issues from GitHub repositories that a specified user has starred. 

## Usage

To use this script, you will need to set your GitHub username and personal access token as environment variables in a `.env` file in the same directory as the script. The `.env` file should contain the following lines:
```
MYUSERNAME=yourgithubusername
TOKEN=yourpersonalaccesstoken
```
You can then run the script by executing the following command in your terminal:
```
python starred_issue_tracker.py
```

The script will retrieve and filter help-wanted issues from all of the repositories that you have starred on GitHub and print the titles of the relevant issues to the console.

## Dependencies

This script requires the following dependencies:

- requests
- python-dotenv

You can install these dependencies by running the following command in your terminal:
```
pip install -r requirements.txt
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
