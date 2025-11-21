"""
Command-line interface for ScoreSearch.

Provides an interactive CLI for searching and processing drum notation.
"""

import logging
import sys
import click
from colorama import init, Fore, Style

from . import __version__
from .app import ScoreSearch
from .config import config

# Initialize colorama for Windows support
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    ScoreSearch - Find drum notation.
    
    Search for drum scores using Google Search and Google Gemini AI.
    """
    pass


@cli.command()
@click.argument('song_name')
@click.option('--artist', '-a', help='Artist name to refine search')
def find(song_name: str, artist: str):
    """
    Find drum notation search results.
    
    SONG_NAME: Name of the song to search for
    
    Example:
        scoresearch find "Enter Sandman" --artist "Metallica"
    """
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║         ScoreSearch v{__version__}                ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    try:
        app = ScoreSearch()
        results = app.list_results(song_name=song_name, artist=artist)
        
        if results:
            print(f"\n{Fore.GREEN}✓ Found {len(results)} results{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"\n{Fore.YELLOW}No results found{Style.RESET_ALL}")
            sys.exit(1)
    
    except ValueError as e:
        print(f"\n{Fore.RED}✗ Configuration Error:{Style.RESET_ALL} {e}")
        print(f"\n{Fore.YELLOW}Please create a .scoresearch file with your API keys.{Style.RESET_ALL}")
        print(f"See .scoresearch.example for reference.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {e}")
        logging.exception("Unexpected error")
        sys.exit(1)


@cli.command()
def check():
    """Check configuration and dependencies."""
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║         ScoreSearch Configuration            ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # Check API keys
    print(f"{Fore.YELLOW}API Configuration:{Style.RESET_ALL}")
    
    if config.google_search_api_key:
        print(f"  ✓ Google Search API Key: {Fore.GREEN}Set{Style.RESET_ALL}")
    else:
        print(f"  ✗ Google Search API Key: {Fore.RED}Not set{Style.RESET_ALL}")
    
    if config.google_search_engine_id:
        print(f"  ✓ Google Search Engine ID: {Fore.GREEN}Set{Style.RESET_ALL}")
    else:
        print(f"  ✗ Google Search Engine ID: {Fore.RED}Not set{Style.RESET_ALL}")
    
    if config.gemini_api_key:
        print(f"  ✓ Google Gemini API Key: {Fore.GREEN}Set{Style.RESET_ALL}")
    else:
        print(f"  ✗ Google Gemini API Key: {Fore.RED}Not set{Style.RESET_ALL}")
    
    # Check directories
    print(f"\n{Fore.YELLOW}Directories:{Style.RESET_ALL}")
    print(f"  Output: {config.output_dir}")
    print(f"  Temp: {config.temp_dir}")
    
    if config.validate():
        print(f"{Fore.GREEN}✓ Configuration is complete{Style.RESET_ALL}\n")
        sys.exit(0)
    else:
        print(f"{Fore.YELLOW}⚠ Configuration incomplete - please review above{Style.RESET_ALL}\n")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
