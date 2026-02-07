import sys
import os
from datetime import datetime


def parse_arguments(args):
    """Parse command line arguments to extract directory path and file name."""
    directory_parts = []
    file_name = None
    
    i = 1  # Skip script name (args[0])
    while i < len(args):
        if args[i] == '-d':
            i += 1
            # Collect all directory parts until we hit '-f' or end of args
            while i < len(args) and args[i] != '-f':
                directory_parts.append(args[i])
                i += 1
        elif args[i] == '-f':
            i += 1
            # Next argument should be the file name
            if i < len(args):
                file_name = args[i]
                i += 1
        else:
            i += 1
    
    return directory_parts, file_name


def get_content_from_user():
    """Get content lines from user until 'stop' is entered."""
    lines = []
    while True:
        line = input("Enter content line: ")
        if line.lower() == "stop":
            break
        lines.append(line)
    return lines


def format_content(lines):
    """Format content with timestamp and line numbers."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_lines = [timestamp]
    
    for i, line in enumerate(lines, 1):
        formatted_lines.append(f"{i} {line}")
    
    return "\n".join(formatted_lines)


def create_file_with_content(file_path, content):
    """Create or append to a file with the given content."""
    mode = 'a' if os.path.exists(file_path) else 'w'
    
    with open(file_path, mode) as f:
        if mode == 'a' and os.path.getsize(file_path) > 0:
            # Add blank line before new content if file already has content
            f.write("\n\n")
        f.write(content)


def main():
    if len(sys.argv) < 2:
        print("Usage: python create_file.py [-d dir1 dir2 ...] [-f filename]")
        return
    
    directory_parts, file_name = parse_arguments(sys.argv)
    
    # Build directory path
    if directory_parts:
        directory_path = os.path.join(*directory_parts)
        os.makedirs(directory_path, exist_ok=True)
    else:
        directory_path = "."
    
    # Handle file creation if -f flag was provided
    if file_name:
        # Get content from user
        content_lines = get_content_from_user()
        
        # Format content with timestamp and line numbers
        formatted_content = format_content(content_lines)
        
        # Determine full file path
        file_path = os.path.join(directory_path, file_name)
        
        # Create or append to file
        create_file_with_content(file_path, formatted_content)
        
        print(f"File created/updated: {file_path}")
    elif directory_parts:
        print(f"Directory created: {directory_path}")
    else:
        print("No action taken. Please provide -d or -f flag.")


if __name__ == "__main__":
    main()
