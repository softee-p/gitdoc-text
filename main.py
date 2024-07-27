import os
from github import Github
from github import GithubException
import base64
import markdown
from html2text import html2text
from dotenv import load_dotenv
from tqdm.auto import tqdm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = r"""
 :::::::: ::::::::::: ::::::::::: :::::::::   ::::::::   ::::::::              ::::::::::: :::::::::: :::    ::: ::::::::::: 
:+:    :+:    :+:         :+:     :+:    :+: :+:    :+: :+:    :+:                 :+:     :+:        :+:    :+:     :+:     
+:+           +:+         +:+     +:+    +:+ +:+    +:+ +:+                        +:+     +:+         +:+  +:+      +:+     
:#:           +#+         +#+     +#+    +:+ +#+    +:+ +#+       +#++:++#++:++    +#+     +#++:++#     +#++:+       +#+     
+#+   +#+#    +#+         +#+     +#+    +#+ +#+    +#+ +#+                        +#+     +#+         +#+  +#+      +#+     
#+#    #+#    #+#         #+#     #+#    #+# #+#    #+# #+#    #+#                 #+#     #+#        #+#    #+#     #+#     
 ######## ###########     ###     #########   ########   ########                  ###     ########## ###    ###     ###     
    """
    print(Fore.CYAN + Style.BRIGHT + banner)

def load_github_token():
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GitHub token not found. Make sure it's set in your .env file.")
    return token

def get_repo_contents(repo, path=''):
    try:
        return repo.get_contents(path)
    except GithubException as e:
        if e.status == 404:
            print(Fore.YELLOW + f"Warning: Path '{path}' not found in the repository. Skipping.")
            return []
        else:
            raise

def is_markdown_file(file_name):
    return file_name.lower().endswith('.md')

def get_markdown_content(content):
    try:
        file_content = base64.b64decode(content.content).decode('utf-8')
        html = markdown.markdown(file_content)
        text = html2text(html)
        return text
    except Exception as e:
        print(Fore.RED + f"Error processing file {content.path}: {str(e)}")
        return ""

def scrape_docs(g, repo_name, output_dir='output'):
    repo_output_dir = os.path.join(output_dir, repo_name)
    if not os.path.exists(repo_output_dir):
        os.makedirs(repo_output_dir)

    try:
        repo = g.get_repo(repo_name)
    except GithubException as e:
        if e.status == 404:
            print(Fore.RED + f"Error: Repository '{repo_name}' not found. Please check the repository name and your access rights.")
            return
        else:
            raise

    print(Fore.CYAN + "\nStarting scraping process...")

    def process_contents(contents, current_path=''):
        markdown_contents = {}
        
        for content in contents:
            try:
                if content.type == "dir":
                    subdir_path = os.path.join(current_path, content.name)
                    process_contents(get_repo_contents(repo, content.path), subdir_path)
                elif content.type == "file" and is_markdown_file(content.name):
                    dir_name = os.path.dirname(content.path)
                    if dir_name not in markdown_contents:
                        markdown_contents[dir_name] = []
                    
                    with tqdm(total=1, desc=f"Processing {content.name}", leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as file_progress:
                        markdown_contents[dir_name].append((content.name, get_markdown_content(content)))
                        file_progress.update(1)
            except Exception as e:
                print(Fore.RED + f"Error processing {content.path}: {str(e)}")

        for dir_path, contents in markdown_contents.items():
            file_name = dir_path.replace('/', '_') if dir_path else 'root'
            output_file = os.path.join(repo_output_dir, f"{file_name}.txt")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                for file_name, content in contents:
                    f.write(f"# {file_name}\n\n")
                    f.write(content)
                    f.write("\n\n" + "="*80 + "\n\n")
            print(Fore.GREEN + f"✔ Saved combined docs for {dir_path} to {output_file}")

    process_contents(get_repo_contents(repo))

def main():
    print_banner()
    
    try:
        github_token = load_github_token()
        g = Github(github_token)

        try:
            g.get_user().login
        except GithubException as e:
            if e.status == 401:
                print(Fore.RED + "Error: Invalid GitHub API key. Please check your GITHUB_TOKEN in the .env file.")
                return
            else:
                raise

        while True:
            repo_name = input(Fore.CYAN + "Enter the repository name in the format 'owner/repo': ").strip()
            if '/' in repo_name:
                break
            print(Fore.YELLOW + "Invalid format. Please use 'owner/repo' format.")

        scrape_docs(g, repo_name)
        print(Fore.GREEN + Style.BRIGHT + f"\n✨ Scraping completed for {repo_name}")

    except ValueError as e:
        print(Fore.RED + f"Error: {str(e)}")
    except GithubException as e:
        if e.status == 404:
            print(Fore.RED + f"Error: Repository '{repo_name}' not found. Please check the repository name and your access rights.")
        else:
            print(Fore.RED + f"GitHub API Error: {e.data.get('message', str(e))}")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()