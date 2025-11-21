"""
Main application module for ScoreFinder.

Coordinates the search, conversion and verification of
drum notation files.
"""

import logging
from pathlib import Path
from typing import List, Optional
import sys
import subprocess
import os

from .config import config
from .search import NotationSearcher, SearchResult

logger = logging.getLogger(__name__)


class ScoreFinder:
    """Main application class for finding and processing drum notation."""

    def __init__(self):
        """Initialize ScoreFinder with all required components."""
        # Validate configuration
        if not config.validate():
            raise ValueError(
                "Invalid configuration. Please ensure all required settings are "
                "set in .scorefinder file"
            )
        
        self.searcher = NotationSearcher()
        self.failed_urls_file = config.project_root / "failed_urls.txt"
        self.failed_urls = self._load_failed_urls()

    def _load_failed_urls(self) -> set[str]:
        """Load failed URLs from the data file."""
        if not self.failed_urls_file.exists():
            return set()
        with open(self.failed_urls_file, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()}

    def _add_failed_url(self, url: str):
        """Add a URL to the failed list and save it to the file."""
        if url not in self.failed_urls:
            self.failed_urls.add(url)
            with open(self.failed_urls_file, 'a', encoding='utf-8') as f:
                f.write(f"{url}\n")
            logger.info(f"Added failed URL to list: {url}")

    def find_notation(
        self,
        song_name: str,
        artist: Optional[str] = None,
    ) -> Optional[Path]:
        """
        Find drum notation for a song, with interactive prompts for processing.
        """
        logger.info(f"Finding drum notation for: {song_name}" + 
                   (f" by {artist}" if artist else ""))
        
        # Step 1: Search for notation
        print(f"\n🔍 Searching for drum notation...")
        results = self.searcher.search_drum_notation(song_name, artist, failed_urls=self.failed_urls)
        
        if not results:
            print("❌ No new results found")
            return None
        
        print(f"✓ Found {len(results)} new results to process.")

        # Step 2: Interactively process results
        for i, result in enumerate(results, 1):
            print(f"\n{"-"*20}\n📄 Result {i}/{len(results)}: {result.title}")
            print(f"   Format: {result.file_format}, URL: {result.url}")

            temp_file_path, preview_path, start_page = self._get_preview(result, song_name)

            if not preview_path:
                print("   ⚠️  Could not generate a preview for this format. Automatically skipping.")
                self._add_failed_url(result.url)
                if temp_file_path and temp_file_path.exists():
                    temp_file_path.unlink()
                continue

            print(f"   🖼️  Displaying preview...")
            # Open preview with system default viewer, suppressing output
            if sys.platform == "win32":
                os.startfile(preview_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", preview_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(["xdg-open", preview_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Interactive prompt
            while True:
                choice = input("   ➡️  Choose an action: (P)roceed, (S)kip, (D)ownload Source, (Q)uit: ").lower()
                if choice in ['p', 's', 'd', 'q']:
                    break
                print("      Invalid choice, please try again.")

            if choice == 'q':
                print("\n🛑 Quitting.")
                return None
            elif choice == 's':
                print("   ⏭️  Skipping.")
                self._add_failed_url(result.url) # Add to failed list so we don't see it again
                continue
            elif choice == 'd':
                self._save_source_document(result, temp_file_path, song_name)
                # We still add to failed_urls so we don't re-process it next time
                self._add_failed_url(result.url)
                continue
            elif choice == 'p':
                print("   ⚙️  Proceeding with conversion and verification...")
                try:
                    # If config is set, save a copy of the source before processing
                    if config.save_intermediate:
                        print("   💾  Saving intermediate source file (as configured)...")
                        self._save_source_document(result, temp_file_path, song_name)

                    # Pass the downloaded file and start page to the processing method
                    file_path = self._process_result(result, song_name, temp_file_path, start_page)
                    if file_path:
                        print(f"\n🎉 Successfully saved to: {file_path}")
                        return file_path
                    else:
                        # If processing failed after proceeding, add to failed list
                        self._add_failed_url(result.url)
                except Exception as e:
                    logger.error(f"Error processing result {i}: {e}")
                    print(f"   ❌ Error: {e}")
                    self._add_failed_url(result.url)
                    continue
        
        print("\n❌ Could not process any results successfully")
        return None

    def _get_preview(self, result: SearchResult, song_name: str) -> tuple[Optional[Path], Optional[Path], int]:
        """Downloads a file and generates a preview if possible."""
        print("   Downloading for preview...")
        temp_file_path = self.downloader.download_file(result.url, config.temp_dir)
        if not temp_file_path:
            print("   ❌ Download failed.")
            return None, None, 0

        preview_path = None
        start_page = 0
        if result.file_format == 'pdf':
            preview_path, start_page = self.converter.get_pdf_preview_image(temp_file_path, song_name)
        
        return temp_file_path, preview_path, start_page

    def list_results(
        self,
        song_name: str,
        artist: Optional[str] = None
    ) -> List[SearchResult]:
        """
        List search results without processing them.

        Args:
            song_name: Name of the song
            artist: Optional artist name

        Returns:
            A list of SearchResult objects.
        """
        print(f"\n🔍 Searching for drum notation...")
        results = self.searcher.search_drum_notation(song_name, artist, failed_urls=self.failed_urls)
        
        if not results:
            print("❌ No new results found")
            return []
        
        print(f"\n✓ Found {len(results)} new results:\n")

        if not results:
            return []
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result.title}")
            print(f"   Format: {result.file_format}")
            print(f"   URL: {result.url}")
            print(f"   {result.snippet[:100]}...")
            print()
        
        return results
