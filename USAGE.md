# ScoreSearch Usage Examples

## **Important: Ethical Use and Licensing**

ScoreSearch is a tool to help you find links to drum scores online. It does not download, convert, or process any files.

**It is your sole responsibility to ensure you have the legal right, license, or permission to access, download, and use any content found through this tool.** Always check the licensing terms of the source website. Many sites may require a purchase or subscription.

---

## Basic Usage

### 1. Configuration Check
Before your first search, check that your API configuration is correct:
```bash
scoresearch check
```

Expected output when properly configured:
```
╔══════════════════════════════════════════════╗
║         ScoreSearch Configuration           ║
╚══════════════════════════════════════════════╝

API Configuration:
  ✓ Google API Key: Set
  ✓ Google Search Engine ID: Set

──────────────────────────────────────────────
✓ Configuration is complete
```

### 2. Search for Drum Notation
The primary command is `search`. It will use Google Search and Gemini AI to find and list relevant URLs.

```bash
scoresearch search "Enter Sandman" --artist "Metallica"
```

This will list potential results with their URLs for you to investigate manually.

## Search Examples

### Example 1: Popular Rock Song
```bash
scoresearch search "Smells Like Teen Spirit" --artist "Nirvana"
```

### Example 2: Jazz Standard
```bash
scoresearch search "Take Five" --artist "Dave Brubeck"
```

### Example 3: Song with a Famous Drum Solo
```bash
scoresearch search "Moby Dick" --artist "Led Zeppelin"
```

## Understanding the Output

### Successful Search
The tool will provide a list of URLs it has identified as potential sources for the score.
```
🔍 Searching for drum notation for "Seven Nation Army" by The White Stripes...
✓ Found 10 potential results. Analyzing...

🔗 Result 1/3:
   Title: Seven Nation Army - The White Stripes - Drum Score
   URL: https://www.drumscore.com/scores/seven-nation-army
   Note: This appears to be a dedicated score website. Please check for licensing and purchase options.

🔗 Result 2/3:
   Title: Seven Nation Army Drum Tab by The White Stripes
   URL: https://www.ultimate-guitar.com/tabs/seven-nation-army-drums
   Note: This may be a tab or a user-submitted score.

🔗 Result 3/3:
   Title: How to Play "Seven Nation Army" on Drums - PDF
   URL: https://www.drumeo.com/beat/seven-nation-army-beat/
   Note: This may be a lesson or a partial score.

✓ Search complete. Please visit the URLs to check for scores.
```

### No Results Found
If no relevant links can be found, you will see:
```
🔍 Searching for drum notation...
❌ No results found for your query.
```

## Troubleshooting

### Error: "Google API key is required"
This means your `.env` file is missing or incomplete.
1.  Create the file if it doesn't exist: `cp .env.example .env`
2.  Edit the `.env` file and add your API keys.

## API Usage Considerations

### Google Search API
- The free tier has a limit of 100 queries per day. Each `scoresearch search` command uses one query.

### Google Gemini API
- Has usage limits based on your plan. The AI analysis of search results can consume tokens.
- Be mindful of how many searches you run to stay within the free tier limits.