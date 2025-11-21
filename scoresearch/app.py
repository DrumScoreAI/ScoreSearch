"""
Main application module for ScoreSearch.

Coordinates the search, conversion and verification of
drum notation files.
"""

import logging
from pathlib import Path
from typing import List, Optional

from .config import config
from .search import NotationSearcher, SearchResult

logger = logging.getLogger(__name__)


class ScoreSearch:
    """Main application class for finding and processing drum notation."""

    def __init__(self):
        """Initialize ScoreSearch with all required components."""
        # Validate configuration
        if not config.validate():
            raise ValueError(
                "Invalid configuration. Please ensure all required settings are "
                "set in ~/.scoresearch file"
            )
        
        self.searcher = NotationSearcher()
        self.skipped_urls_file = config.project_root / "skipped_urls.txt"
        self.skipped_urls = self._load_skipped_urls()

    def _load_skipped_urls(self) -> set[str]:
        """Load skipped URLs from the data file."""
        if not self.skipped_urls_file.exists():
            return set()
        with open(self.skipped_urls_file, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()}

    def _add_skipped_url(self, url: str):
        """Add a URL to the skipped list and save it to the file."""
        if url not in self.skipped_urls:
            self.skipped_urls.add(url)
            with open(self.skipped_urls_file, 'a', encoding='utf-8') as f:
                f.write(f"{url}\n")
            logger.info(f"Added skipped URL to list: {url}")

    def find_notation(
        self,
        song_name: str,
        artist: Optional[str] = None,
        found_counter: int = 0,
        skipped_counter : int = 0
    ) -> tuple[int, int]:
        """
        Find drum notation for a song, with interactive prompts for processing.
        """
        logger.info(f"Finding drum notation for: {song_name}" + 
                   (f" by {artist}" if artist else ""))
        
        # Step 1: Search for notation
        print(f"\n🔍 Searching for drum notation...")
        results = self.searcher.search_drum_notation(song_name, artist, skipped_urls=self.skipped_urls)

        found_counter += len(results)
        
        if not results:
            print("❌ No new results found")
            return None
        
        print(f"✓ Found {len(results)} new results to process.")

        # Step 2: Interactively process results
        for i, result in enumerate(results, 1):
            print(f"\n{"-"*20}\n📄 Result {i}/{len(results)}: {result.title}")
            print(f"   Format: {result.file_format}, URL: {result.url}")
            
            # Interactive prompt
            while True:
                if i < len(results):
                    choice = input("   ➡️  Choose an action: (S)kip, (Q)uit: ").lower()
                    if choice in ['s', 'q']:
                        break
                else:
                    choice = input(f"   ➡️  Choose an action: (F)ind {len(results) - i} more, (S)kip, (Q)uit: ").lower()
                    if choice in ['f', 's', 'q']:
                        break
                
                print("      Invalid choice, please try again.")

            if choice == 'q':
                print("\n🛑 Quitting.")
                return None
            elif choice == 's':
                print("   ⏭️  Skipping.")
                self._add_skipped_url(result.url) # Add to skipped list so we don't see it again
                skipped_counter += 1
                continue
            elif choice == 'f':
                print(f"   🔄 Finding {len(results) - i} more results...")
                return self.find_notation(song_name, artist, found_counter=found_counter, skipped_counter=skipped_counter)
        
        print("\n❌ Could not process any results successfully")
        return found_counter, skipped_counter
