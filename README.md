# GitHub Docs Scraper

<pre style="font-family: 'Courier New', Courier, monospace;">
 :::::::: ::::::::::: ::::::::::: :::::::::   ::::::::   ::::::::              ::::::::::: :::::::::: :::    ::: ::::::::::: 
:+:    :+:    :+:         :+:     :+:    :+: :+:    :+: :+:    :+:                 :+:     :+:        :+:    :+:     :+:     
+:+           +:+         +:+     +:+    +:+ +:+    +:+ +:+                        +:+     +:+         +:+  +:+      +:+     
:#:           +#+         +#+     +#+    +:+ +#+    +:+ +#+       +#++:++#++:++    +#+     +#++:++#     +#++:+       +#+     
+#+   +#+#    +#+         +#+     +#+    +#+ +#+    +#+ +#+                        +#+     +#+         +#+  +#+      +#+     
#+#    #+#    #+#         #+#     #+#    #+# #+#    #+# #+#    #+#                 #+#     #+#        #+#    #+#     #+#     
 ######## ###########     ###     #########   ########   ########                  ###     ########## ###    ###     ###     
</pre>

## Description

GitHub Docs Scraper is a Python script that allows you to easily scrape and compile Markdown documentation from GitHub repositories.

## Prerequisites

- Python 3.6 or higher
- GitHub Personal Access Token

## Installation

### Option 1: Using Conda (Recommended for a fresh Python installation)

1. Install Miniconda:
   - Visit the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) and download the appropriate installer for your operating system.
   - Follow the installation instructions for your OS.

2. Create a new Conda environment:
   ```
   conda create -n github-scraper python=3.8
   ```

3. Activate the environment:
   ```
   conda activate github-scraper
   ```

4. Install the required packages:
   ```
   pip install PyGithub markdown html2text python-dotenv tqdm colorama
   ```

### Option 2: Using venv (For existing Python installations)

1. Create a new virtual environment:
   ```
   python -m venv github-scraper-env
   ```

2. Activate the environment:
   - On Windows:
     ```
     github-scraper-env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source github-scraper-env/bin/activate
     ```

3. Install the required packages:
   ```
   pip install PyGithub markdown html2text python-dotenv tqdm colorama
   ```

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/softee-p/gitdoc-text.git
   cd github-docs-scraper
   ```

2. Create a `.env` file in the project root directory:
   ```
   touch .env
   ```

3. Open the `.env` file and add your GitHub Personal Access Token:
   ```
   GITHUB_TOKEN=your_personal_access_token_here
   ```

   To get your GitHub Personal Access Token:
   - Click on your profile picture in the top right corner of GitHub
   - Go to Settings
   - Click on "Developer settings" in the left sidebar
   - Click on "Personal access tokens"
   - Generate a new token with the "repo" scope

## Usage

Run the script:

```
python github_docs_scraper.py
```

Follow the prompts to enter the repository name and start the scraping process.

## Features

- Scrapes Markdown files from GitHub repositories
- Combines Markdown content from each directory into a single file

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.