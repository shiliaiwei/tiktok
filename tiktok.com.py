import subprocess
import os
import pyfiglet
from colorama import Fore, init
import time
import re
import sys
import argparse

# Initialize Colorama
init(autoreset=True)

# Version and author information
__version__ = "1.0.0"
__author__ = "eirsvi"
__github__ = "https://github.com/eirsvi"

def print_colored_logo():
    # Generate ASCII art for the logo with a modern font
    logo = pyfiglet.figlet_format("SRIEVi", font="slant")

    # Center the logo in the terminal
    terminal_width = os.get_terminal_size().columns
    centered_logo = "\n".join(line.center(terminal_width) for line in logo.splitlines())

    # Colors for the gradient effect (cyber-like appearance)
    colors = [Fore.LIGHTCYAN_EX, Fore.CYAN, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX]

    # Apply a glowing effect to each character in the logo
    print("\n")  # Add spacing before the logo
    for i, char in enumerate(centered_logo):
        if char.strip():  # Apply color only to non-space characters
            print(colors[i % len(colors)] + char, end='', flush=True)
            time.sleep(0.01)  # Slight delay to create a glowing effect
        else:
            print(char, end='', flush=True)
    print("\n")  # New line after the logo

def print_welcome():
    # Call the function to print the colored logo
    print_colored_logo()
    
    # Welcome message
    welcome_message = f"{Fore.LIGHTBLUE_EX}Welcome to the TikTok Video Downloader! \n"
    terminal_width = os.get_terminal_size().columns
    centered_message = welcome_message.center(terminal_width)
    print(centered_message)

    # Version info
    version_info = f"{Fore.LIGHTCYAN_EX}Version {__version__}"
    centered_version = version_info.center(terminal_width)
    print(centered_version)

    # Author credit
    author_info = f"{Fore.LIGHTGREEN_EX}Created by {__author__}"
    centered_author = author_info.center(terminal_width)
    print(centered_author)

    # GitHub link
    github_info = f"{Fore.LIGHTYELLOW_EX}GitHub: {__github__}"
    centered_github = github_info.center(terminal_width)
    print(centered_github)

    # Separator line
    separator = f"{Fore.LIGHTRED_EX}" + "=" * 40
    centered_separator = separator.center(terminal_width)
    print(centered_separator)

    print()  # Add an extra newline for spacing

def print_menu():
    """Display the main menu options"""
    print(f"{Fore.LIGHTYELLOW_EX}=" * 50)
    print(f"{Fore.LIGHTGREEN_EX}TikTok Downloader Options:")
    print(f"{Fore.LIGHTYELLOW_EX}=" * 50)
    print(f"{Fore.LIGHTCYAN_EX}1. Download a single video")
    print(f"{Fore.LIGHTCYAN_EX}2. Bulk download from a user profile")
    print(f"{Fore.LIGHTCYAN_EX}3. About")
    print(f"{Fore.LIGHTCYAN_EX}4. Exit")
    print(f"{Fore.LIGHTYELLOW_EX}=" * 50)

def get_output_directory():
    """Get the output directory from the user or use default"""
    default_dir = os.path.expanduser('~/Downloads')
    
    print(f"{Fore.LIGHTCYAN_EX}Default download directory: {default_dir}")
    custom_dir = input(f"{Fore.LIGHTCYAN_EX}Enter custom download directory (or press Enter for default): ").strip()
    
    if custom_dir:
        # Expand user directory if it starts with ~
        if custom_dir.startswith('~'):
            custom_dir = os.path.expanduser(custom_dir)
        
        # Create directory if it doesn't exist
        if not os.path.exists(custom_dir):
            try:
                os.makedirs(custom_dir)
                print(f"{Fore.LIGHTGREEN_EX}Created directory: {custom_dir}")
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}Error creating directory: {e}")
                print(f"{Fore.LIGHTCYAN_EX}Using default directory instead: {default_dir}")
                return default_dir
        return custom_dir
    return default_dir

def get_media_format():
    """Prompt user to choose between video or audio download"""
    while True:
        choice = input(f"{Fore.LIGHTCYAN_EX}Download as (v)ideo or (a)udio only? (v/a): ").strip().lower()
        if choice in ['v', 'a']:
            return choice
        print(f"{Fore.LIGHTRED_EX}Invalid choice. Please select 'v' for video or 'a' for audio.")

def download_media(url, output_file, media_format):
    """Download media based on the specified format"""
    try:
        if media_format == 'v':
            # Command to download the full video
            subprocess.run(['yt-dlp', '-o', output_file, url], check=True)
            return True
        elif media_format == 'a':
            # Command to download audio only
            subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', '-o', output_file, url], check=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f"{Fore.LIGHTRED_EX}Error downloading: {e}")
        return False
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Unexpected error: {e}")
        return False

def download_single_video():
    """Function to download a single TikTok video"""
    print(f"\n{Fore.LIGHTYELLOW_EX}=== Single Video Download ===")
    
    # Example URL
    print(f"EXAMPLE URL: {Fore.LIGHTYELLOW_EX}https://www.tiktok.com/@user/video/123456789")
    
    # Prompt user for the TikTok video URL
    url = input(f"{Fore.LIGHTCYAN_EX}Enter the TikTok video URL: ").strip()
    
    if not url:
        print(f"{Fore.LIGHTRED_EX}No URL provided. Returning to main menu.")
        return
    
    # Get output directory
    output_dir = get_output_directory()
    
    # Generate the output file name
    output_file = os.path.join(output_dir, '%(title)s.%(ext)s')
    
    # Get media format choice
    media_format = get_media_format()
    
    print(f"{Fore.LIGHTCYAN_EX}Downloading... Please wait.")
    
    if download_media(url, output_file, media_format):
        media_type = "Video" if media_format == 'v' else "Audio"
        print(f"{Fore.LIGHTGREEN_EX}{media_type} downloaded successfully to: {output_dir}")
    
    input(f"{Fore.LIGHTYELLOW_EX}Press Enter to continue...")

def extract_username_from_url(url):
    """Extract username from a TikTok profile URL"""
    # Pattern to match TikTok username from URL
    patterns = [
        r'tiktok\.com/@([^/?]+)',  # Standard TikTok URL
        r'tiktok\.com/([^/?]+)'    # Alternative format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def download_profile_videos(username, output_dir, media_format, limit=None):
    """Download videos from a user profile with the given parameters"""
    # Create a subdirectory for this user
    user_dir = os.path.join(output_dir, f"tiktok_{username}")
    try:
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        print(f"{Fore.LIGHTGREEN_EX}Saving to: {user_dir}")
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error creating user directory: {e}")
        print(f"{Fore.LIGHTCYAN_EX}Using main directory instead: {output_dir}")
        user_dir = output_dir
    
    # Generate the output file name
    output_file = os.path.join(user_dir, '%(title)s.%(ext)s')
    
    # Set limit argument if provided
    limit_arg = f"--max-downloads {limit}" if limit else ""
    
    print(f"{Fore.LIGHTCYAN_EX}Starting bulk download from @{username}... This may take a while.")
    
    try:
        # Construct the URL for the user's profile
        profile_url = f"https://www.tiktok.com/@{username}"
        
        # Command to download all videos from the user
        if media_format == 'v':
            cmd = f"yt-dlp -o '{output_file}' {limit_arg} {profile_url}"
            subprocess.run(cmd, shell=True, check=True)
        else:  # audio
            cmd = f"yt-dlp -x --audio-format mp3 -o '{output_file}' {limit_arg} {profile_url}"
            subprocess.run(cmd, shell=True, check=True)
            
        print(f"{Fore.LIGHTGREEN_EX}Bulk download completed successfully!")
        print(f"{Fore.LIGHTGREEN_EX}Files saved to: {user_dir}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.LIGHTRED_EX}Error during bulk download: {e}")
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Unexpected error: {e}")

def download_user_profile():
    """Function to bulk download videos from a user's profile (interactive mode)"""
    print(f"\n{Fore.LIGHTYELLOW_EX}=== Bulk Profile Download ===")
    
    # Example URL
    print(f"EXAMPLE URL: {Fore.LIGHTYELLOW_EX}https://www.tiktok.com/@username")
    
    # Prompt user for the TikTok profile URL or username
    profile_input = input(f"{Fore.LIGHTCYAN_EX}Enter the TikTok profile URL or username: ").strip()
    
    if not profile_input:
        print(f"{Fore.LIGHTRED_EX}No profile provided. Returning to main menu.")
        return
    
    # Process the input to get the username
    username = None
    if profile_input.startswith(('http://', 'https://', 'www.')):
        username = extract_username_from_url(profile_input)
        if not username:
            print(f"{Fore.LIGHTRED_EX}Could not extract username from URL. Please check the format.")
            input(f"{Fore.LIGHTYELLOW_EX}Press Enter to continue...")
            return
    else:
        # If just the username was provided (without @)
        username = profile_input.lstrip('@')
    
    # Get output directory
    output_dir = get_output_directory()
    
    # Get media format choice
    media_format = get_media_format()
    
    # Ask for download limit
    try:
        limit_input = input(f"{Fore.LIGHTCYAN_EX}Maximum number of videos to download (press Enter for all): ").strip()
        limit = int(limit_input) if limit_input else None
    except ValueError:
        print(f"{Fore.LIGHTRED_EX}Invalid number. Downloading all videos.")
        limit = None
    
    # Download the videos
    download_profile_videos(username, output_dir, media_format, limit)
    
    input(f"{Fore.LIGHTYELLOW_EX}Press Enter to continue...")

def check_dependencies():
    """Check if yt-dlp is installed"""
    try:
        subprocess.run(['yt-dlp', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Fore.LIGHTRED_EX}Error: yt-dlp is not installed or not in PATH.")
        print(f"{Fore.LIGHTYELLOW_EX}Please install it using: pip install yt-dlp")
        return False

def show_about():
    """Display information about the application and its creator"""
    print(f"\n{Fore.LIGHTYELLOW_EX}=== About TikTok Downloader ===")
    print(f"{Fore.LIGHTCYAN_EX}Version: {__version__}")
    print(f"{Fore.LIGHTGREEN_EX}Created by: {__author__}")
    print(f"{Fore.LIGHTYELLOW_EX}GitHub: {__github__}")
    print(f"\n{Fore.LIGHTMAGENTA_EX}Description:")
    print(f"{Fore.WHITE}A powerful TikTok video and audio downloader that allows you to")
    print(f"{Fore.WHITE}download single videos or bulk download from user profiles.")
    print(f"\n{Fore.LIGHTMAGENTA_EX}Features:")
    print(f"{Fore.WHITE}• Download single TikTok videos")
    print(f"{Fore.WHITE}• Bulk download from user profiles")
    print(f"{Fore.WHITE}• Download as video or extract audio")
    print(f"{Fore.WHITE}• Custom download directories")
    print(f"{Fore.WHITE}• User-friendly interface")
    
    print(f"\n{Fore.LIGHTMAGENTA_EX}License:")
    print(f"{Fore.WHITE}This software is provided as-is with no warranty.")
    print(f"{Fore.WHITE}© 2023 {__author__}. All rights reserved.")
    
    input(f"\n{Fore.LIGHTYELLOW_EX}Press Enter to return to the main menu...")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="TikTok Video Downloader by eirsvi",
        epilog="Example: python ttdl.py -u https://www.tiktok.com/@username/video/123456789 -f video"
    )
    
    # Add arguments
    parser.add_argument("-u", "--url", help="TikTok video or profile URL")
    parser.add_argument("-p", "--profile", help="TikTok profile username (without @)")
    parser.add_argument("-f", "--format", choices=["video", "audio"], help="Download format (video or audio)")
    parser.add_argument("-o", "--output", help="Output directory path")
    parser.add_argument("-l", "--limit", type=int, help="Maximum number of videos to download from profile")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    
    return parser.parse_args()

def process_command_line_args(args):
    """Process command line arguments and perform downloads accordingly"""
    # Set output directory
    output_dir = args.output if args.output else os.path.expanduser('~/Downloads')
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"{Fore.LIGHTGREEN_EX}Created directory: {output_dir}")
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}Error creating directory: {e}")
            output_dir = os.path.expanduser('~/Downloads')
    
    # Set media format
    media_format = 'v' if args.format == 'video' or not args.format else 'a'
    
    # Process URL or profile
    if args.url:
        # Check if it's a video URL or profile URL
        if '/video/' in args.url:
            # It's a video URL
            output_file = os.path.join(output_dir, '%(title)s.%(ext)s')
            print(f"{Fore.LIGHTCYAN_EX}Downloading video... Please wait.")
            
            if download_media(args.url, output_file, media_format):
                media_type = "Video" if media_format == 'v' else "Audio"
                print(f"{Fore.LIGHTGREEN_EX}{media_type} downloaded successfully to: {output_dir}")
        else:
            # It might be a profile URL
            username = extract_username_from_url(args.url)
            if username:
                download_profile_videos(username, output_dir, media_format, args.limit)
            else:
                print(f"{Fore.LIGHTRED_EX}Invalid URL format. Could not determine if it's a video or profile URL.")
    
    elif args.profile:
        # It's a profile username
        username = args.profile.lstrip('@')
        download_profile_videos(username, output_dir, media_format, args.limit)
    
    # If no URL or profile provided, return False to launch interactive mode
    else:
        return False
    
    return True

def main():
    """Main function to run the TikTok downloader"""
    # Check dependencies
    if not check_dependencies():
        input(f"{Fore.LIGHTYELLOW_EX}Press Enter to exit...")
        sys.exit(1)
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Process command line arguments if provided
    # If successful, exit after processing
    if process_command_line_args(args):
        return
    
    # If no command line arguments or processing failed, launch interactive mode
    # Display welcome message
    print_welcome()
    
    while True:
        # Display menu
        print_menu()
        
        # Get user choice
        try:
            choice = input(f"{Fore.LIGHTCYAN_EX}Enter your choice (1-4): ").strip()
            
            if choice == '1':
                download_single_video()
            elif choice == '2':
                download_user_profile()
            elif choice == '3':
                show_about()
            elif choice == '4':
                print(f"{Fore.LIGHTGREEN_EX}Thank you for using TikTok Downloader! Goodbye!")
                break
            else:
                print(f"{Fore.LIGHTRED_EX}Invalid choice. Please select a number between 1 and 4.")
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTGREEN_EX}Program interrupted. Exiting...")
            break
        except Exception as e:
            print(f"{Fore.LIGHTRED_EX}An error occurred: {e}")

if __name__ == "__main__":
    main()
