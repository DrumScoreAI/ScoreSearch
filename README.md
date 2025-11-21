# ScoreSearch

An AI-powered command-line tool to find links to drum score notation online. ScoreSearch uses the Google Search API and Google Gemini to locate and analyze potential sources for drum sheet music across the web.

---

### **Ethical Use and Licensing Disclaimer**

**ScoreSearch is a tool designed to help users find publicly available drum score notation on the internet. It is the user's sole responsibility to ensure they have the legal right, license, or permission to access, download, and use any content found through this tool.**

The developers of ScoreSearch do not condone copyright infringement. Please respect the intellectual property of musicians and publishers. Many websites found may require a purchase or subscription to access the content. Always check the licensing terms of the source website.

---

## Features

- 🔍 **Smart Search**: Uses the Google Custom Search API to find drum notation files across the entire web.
- 🤖 **AI-Powered Analysis**: Leverages Google Gemini to analyze search results and linked pages to identify the most relevant sources for drum scores.
- 🔗 **Link Aggregation**: Provides a clean, ranked list of direct links to potential scores, helping you find what you need faster.

## Installation

### Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini AI)
- Google Custom Search Engine ID

### Install from source

```bash
git clone https://github.com/DrumScoreAI/ScoreSearch.git
cd ScoreSearch
pip install -r requirements.txt
pip install -e .
```

## Configuration

1.  Copy the example environment file:
    ```bash
    cp .scoresearch.example .scoresearch
    ```

2.  Set up environment variable (optionally add this to your .bashrc):
    ```bash
    export SCORESEARCHSOME=$PWD
    ```


3.  Edit `.scoresearch` and add your API credentials:
    ```bash
    GOOGLE_API_KEY=your_google_api_key_here
    GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
    ```


### Getting API Credentials

#### Google API Key
1.  Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2.  Create a new API key
3.  Copy the key to your `.scoresearch` file

#### Google Custom Search Engine ID
1.  Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/)
2.  Create a new search engine
3.  Enable "Search the entire web"
4.  Copy the Search Engine ID to your `.scoresearch` file

## Usage

### Find Drum Notation Links

```bash
scoresearch search "Seven Nation Army" --artist "The White Stripes"
```

This command will:
1.  Search Google for drum notation related to the query.
2.  Analyze the results to find the most promising links.
3.  Display a list of URLs, along with a brief description and a reminder to check the license.

### Check Configuration

```bash
scoresearch check
```
This will verify your API keys and dependencies.

## How It Works

### 1. Search Phase
- Uses the Google Custom Search API to find web pages that may contain drum notation in formats like PDF, MusicXML, or Guitar Pro.

### 2. Analysis Phase
- For promising search results, ScoreSearch can use Google Gemini to analyze the content of the linked page.
- This helps filter out irrelevant results and prioritize pages that explicitly offer drum scores for download or purchase.

### 3. Reporting Phase
- The tool presents a ranked list of URLs to the user, allowing them to visit the sites and acquire the sheet music according to the site's specific terms.

## Dependencies

- `google-generativeai`: Google Gemini AI API
- `google-api-python-client`: Google Search API
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests
- `beautifulsoup4`: HTML parsing
- `click`: CLI framework
- `colorama`: Terminal colors

## License

Apache 2.0 - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.