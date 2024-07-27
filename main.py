import os
from github import Github
from github import GithubException
import base64
import markdown
from html2text import html2text
from dotenv import load_dotenv
from tqdm import tqdm
from colorama import init, Fore, Style

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
        contents = repo.get_contents(path)
        print(Fore.CYAN + f"Retrieved contents of '{path}': {len(contents)} items")
        return contents
    except GithubException as e:
        print(Fore.YELLOW + f"Warning: Unable to retrieve contents of '{path}': {str(e)}")
        return []

def is_markdown_file(file_name):
    return file_name.lower().endswith(('.md', '.mdx'))

def get_markdown_content(content):
    try:
        file_content = base64.b64decode(content.content).decode('utf-8')
        html = markdown.markdown(file_content)
        text = html2text(html)
        return text
    except Exception as e:
        print(Fore.RED + f"Error processing file {content.path}: {str(e)}")
        return ""

def process_readme(repo, output_dir):
    try:
        readme = repo.get_readme()
        print(Fore.CYAN + "Processing README.md")
        with tqdm(total=1, desc="Processing README.md", leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as file_progress:
            readme_content = get_markdown_content(readme)
            file_progress.update(1)
        
        output_path = os.path.join(output_dir, 'README.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# README.md\n\n")
            f.write(readme_content)
        
        print(Fore.GREEN + f"✔ Saved README.md to {output_path}")
    except GithubException as e:
        print(Fore.YELLOW + f"Warning: README.md not found in the root directory: {str(e)}")

def scrape_docs(g, repo_name, output_dir='output'):
    repo_output_dir = os.path.join(output_dir, repo_name)
    if not os.path.exists(repo_output_dir):
        os.makedirs(repo_output_dir)

    try:
        repo = g.get_repo(repo_name)
        print(Fore.GREEN + f"Successfully accessed repository: {repo_name}")
    except GithubException as e:
        print(Fore.RED + f"Error: Repository '{repo_name}' not found. Please check the repository name and your access rights.")
        return

    # Process README.md
    process_readme(repo, repo_output_dir)

    print(Fore.CYAN + "\nStarting scraping process for 'docs' folder...")

    docs_contents = get_repo_contents(repo, 'docs')
    if not docs_contents:
        print(Fore.YELLOW + f"Warning: 'docs' folder not found or empty in the repository '{repo_name}'.")
        return

    def process_contents(contents, current_path=''):
        for content in contents:
            try:
                if content.type == "dir":
                    print(Fore.CYAN + f"Entering directory: {content.path}")
                    subdir_contents = get_repo_contents(repo, content.path)
                    process_contents(subdir_contents, content.path)
                elif content.type == "file" and is_markdown_file(content.name):
                    print(Fore.CYAN + f"Processing file: {content.path}")
                    with tqdm(total=1, desc=f"Processing {content.name}", leave=False, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as file_progress:
                        markdown_content = get_markdown_content(content)
                        file_progress.update(1)
                    
                    relative_path = content.path.replace('docs/', '', 1)
                    output_path = os.path.join(repo_output_dir, 'docs', relative_path.replace('.md', '.txt').replace('.mdx', '.txt'))
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {content.name}\n\n")
                        f.write(markdown_content)
                    
                    print(Fore.GREEN + f"✔ Saved docs for {content.path} to {output_path}")
                else:
                    print(Fore.YELLOW + f"Skipping non-markdown file: {content.path}")
            except Exception as e:
                print(Fore.RED + f"Error processing {content.path}: {str(e)}")

    process_contents(docs_contents)

def main():
    print_banner()
    
    try:
        github_token = load_github_token()
        g = Github(github_token)

        try:
            user = g.get_user()
            print(Fore.GREEN + f"Authenticated as: {user.login}")
        except GithubException as e:
            print(Fore.RED + "Error: Invalid GitHub API key. Please check your GITHUB_TOKEN in the .env file.")
            return

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
        print(Fore.RED + f"GitHub API Error: {e.data.get('message', str(e))}")
    except Exception as e:
        print(Fore.RED + f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()