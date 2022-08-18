# github-repository-automation
A simple python automation script, which initializes a repository on GitHub and clones it to your local machine. 
### Installation: 
```bash
git clone "https://github.com/sergenciftci/github-repository-automation.git"
cd github-repository-automation
pip install -r requirements.txt
chmod +x create.py
```
### Usage:
```bash
cd ~/github-repository-automation
./create.py -n <name of your repository>
```
You can store your username, GitHub access token and desired path in the `.env` file. These act as default arguments and can be overruled by passing them on script execution.
```bash
./create.py -n <name of your repository> -u <username> -t <GitHub token> -p <project base path> --public
```
Add the command with an alias to your `~/.bashrc`, if you don't want to navigate to the `<project base path>/github-repository-automation` directory to execute the command. 

```bash
alias <mycoolscript>=".<project base path>/github-repository-automation/create.py" >> ~/.bashrc
```
Now you can execute your command from anywhere.
```bash
mycoolscript -n my_new_repository
```