"""
Kart Rush - Main Entry Point
Autonomous agentic game development system.

Usage:
    python main.py              # Run normal game
    python main.py --qa         # Run QA suites headless
    python main.py --qa S_BOOT  # Run specific QA suite
"""

import sys
import argparse


def run_game():
    """Run the main game."""
    from src.game.game import Game
    
    print("=" * 50)
    print("KART RUSH - Starting...")
    print("=" * 50)
    
    try:
        game = Game()
        game.start_realtime_loop()
        game.run()
        return 0
    except Exception as e:
        print(f"Game error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_qa(suite_name=None):
    """Run QA suites."""
    from panda3d.core import loadPrcFileData
    
    # Configure for headless testing - must be done before importing Game
    loadPrcFileData('', 'window-type offscreen')
    loadPrcFileData('', 'show-frame-rate-meter 0')
    loadPrcFileData('', 'load-display p3tinydisplay')
    
    from src.game.game import Game
    from src.qa.harness import run_suite, run_all_suites, SUITES
    
    print("=" * 50)
    print("KART RUSH - QA Mode")
    print("=" * 50)
    
    try:
        game = Game()
        
        if suite_name:
            # Run specific suite
            if suite_name not in SUITES:
                print(f"Unknown suite: {suite_name}")
                print(f"Available: {list(SUITES.keys())}")
                return 1
            
            success = run_suite(suite_name, game)
        else:
            # Run all suites
            success = run_all_suites(game)
        
        return 0 if success else 1
    
    except Exception as e:
        print(f"QA error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    parser = argparse.ArgumentParser(description='Kart Rush Racing Game')
    parser.add_argument('--qa', nargs='?', const='ALL', metavar='SUITE',
                       help='Run QA suites (optionally specify suite name)')
    
    args = parser.parse_args()
    
    if args.qa:
        if args.qa == 'ALL':
            return run_qa()
        else:
            return run_qa(args.qa)
    else:
        return run_game()


if __name__ == '__main__':
    sys.exit(main())
