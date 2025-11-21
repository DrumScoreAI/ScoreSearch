# ScoreSearch Installation Guide

This guide will walk you through setting up the `ScoreSearch` project, including the critical API key configuration.

## 1. Prerequisites

-   **Python**: Version 3.8 or higher.
-   **Git**: For cloning the repository.

## 2. API Configuration (Required)

`ScoreSearch` requires two Google API credentials to function.

### Step 1: Get a Google API Key (for Gemini AI)
1.  Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
2.  Click **"Create API Key"**.
3.  Copy the generated key. You will need it in a moment.

### Step 2: Get a Programmable Search Engine ID
1.  Go to the [Google Programmable Search Engine](https://programmablesearchengine.google.com/) control panel.
2.  Click **"Add"** to create a new search engine.
3.  Give it a name (e.g., "ScoreSearcher").
4.  Enable the **"Search the entire web"** option.
5.  Click **"Create"**.
6.  On the next page, copy the **"Search engine ID"**.

## 3. Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/DrumScoreAI/ScoreSearch.git
cd ScoreSearch
```

### Step 2: Set SCORESEARCHHOME environment variable (optionally add this to your .bashrc)
```bash
export SCORESEARCHSHOME=$PWD
```

### Step 2: Create a Virtual Environment
```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install ScoreSearch
```bash
pip install -e .
```

## 4. Environment Setup

### Step 1: Create the `.scoresearch` file
Copy the example environment file to create your local configuration:
```bash
cp .scoresearch.example ~/.scoresearch
```

### Step 2: Add Your API Credentials
Open the newly created `.scoresearch` file in a text editor and paste the keys you obtained earlier:
```bash
# .scoresearch

# For Google Gemini AI analysis
GOOGLE_API_KEY=your_google_api_key_here

# For Google Custom Search
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
```
Save and close the file.

## 5. Verifying the Installation

Run the built-in configuration check to ensure your keys are being read correctly:
```bash
scoresearch check
```
If everything is set up properly, you will see green checkmarks for all configuration items. If you see an error, double-check your `.scoresearch` file.

## 6. Next Steps

You are now ready to use `ScoreSearch`.
-   For usage examples, see the [USAGE.md](USAGE.md) file.
-   For a project overview, read the main [README.md](README.md).