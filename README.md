# Apple Music Playlist Creator

[![Security Scan](https://github.com/rekidderjr/apple-music-playlist-creator/workflows/Security%20Scan/badge.svg)](https://github.com/rekidderjr/apple-music-playlist-creator/actions)
[![Code Quality](https://github.com/rekidderjr/apple-music-playlist-creator/workflows/Code%20Quality/badge.svg)](https://github.com/rekidderjr/apple-music-playlist-creator/actions)
[![Tests](https://github.com/rekidderjr/apple-music-playlist-creator/workflows/Tests/badge.svg)](https://github.com/rekidderjr/apple-music-playlist-creator/actions)

A tool to create and manage Apple Music playlists programmatically, with advanced music library analysis and sorting capabilities.

## Features

### Music Library Analysis & Sorting
- **BPM Sorting**: Automatically categorizes tracks by tempo ranges (Slow, Moderate, Upbeat, Fast, Very Fast, Extreme)
- **Genre Sorting**: Creates playlists based on music genres from your library
- **Duplicate Removal**: Automatically removes duplicate tracks from playlists (same artist-song combinations)
- **Random Shuffling**: Randomly sorts tracks within playlists to avoid artist/album grouping
- **Library Statistics**: Provides detailed analysis of your music collection
- **Playlist Generation**: Creates .m3u playlist files compatible with Apple Music, iTunes, and other players

### Current Sorting Capabilities
**BPM (Beats Per Minute)**: Sorts tracks into tempo-based playlists  
**Genre**: Creates genre-specific playlists  
**Musical Key**: Not currently supported - iTunes/Apple Music Library XML does not contain musical key data (C Major, D Minor, etc.)

### Data Requirements
This tool requires your iTunes/Apple Music library XML file to be placed in the `data/` directory as `Library.xml`.

#### How to Export iTunes/Apple Music Library

**On macOS:**
1. Open **Music** app (or iTunes if using older macOS)
2. Go to **File** → **Library** → **Export Library...**
3. Choose XML format and save as `Library.xml`
4. Copy the file to `data/Library.xml` in this project directory

**On Windows:**
1. Open **iTunes**
2. Go to **File** → **Library** → **Export Library...**
3. Choose XML format and save as `Library.xml`  
4. Copy the file to `data/Library.xml` in this project directory

**Note:** The exported XML contains metadata like BPM, Genre, Artist, Album, but does **not** include musical key information. Musical key detection would require audio analysis, which is beyond the scope of this tool.

### Additional Features
- **Security First**: Comprehensive security scanning and compliance
- **Quality Assured**: Automated code quality checks and testing
- **Enterprise Ready**: Meets customer compliance requirements

## Requirements

- Python 3.8 or higher
- iTunes/Apple Music library XML file
- Additional requirements listed in `requirements.txt`

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/rekidderjr/apple-music-playlist-creator.git
cd apple-music-playlist-creator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

### Development Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run compliance check
./customer-compliance-check.sh
```

## Usage

### Quick Start

```bash
# Run the complete setup and music sorter
./run_music_sorter.sh
```

### Manual Usage

```bash
# Run the music sorter (requires iTunes/Apple Music library XML)
python3 music_sorter.py
```

This will:
1. Parse your iTunes/Apple Music library XML file
2. Analyze your music collection by BPM and genre
3. Generate playlist files in the `playlists/` directory
4. Remove duplicate tracks from playlists
5. Randomly shuffle tracks to avoid artist/album grouping
6. Display detailed statistics about your library

### Basic API Usage

```python
from apple_music_playlist_creator import PlaylistCreator

# Create a playlist creator instance
creator = PlaylistCreator()

# Create a new playlist
playlist = creator.create_playlist("My Awesome Playlist")
```

### Example Output

```
=== MUSIC LIBRARY ANALYSIS ===
Total tracks: 49,396

--- BPM Distribution ---
Fast (141-160 BPM): 6 tracks
Upbeat (121-140 BPM): 19 tracks
Medium (101-120 BPM): 9 tracks
...

--- Top Genres ---
Rock: 9,932 tracks
Pop: 7,382 tracks
Country & Folk: 6,757 tracks
...
```

## Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_main.py
```

## Code Quality

This project maintains high code quality standards:

```bash
# Format code
black .
isort .

# Run linting
flake8 .
pylint src/

# Type checking
mypy src/

# Security scanning
bandit -r src/
safety check

# Run all quality checks
./customer-compliance-check.sh
```

## Project Structure

```
apple-music-playlist-creator/
├── .github/workflows/          # CI/CD workflows
├── src/                       # Source code
│   └── apple_music_playlist_creator/
├── tests/                     # Test files
├── data/                      # iTunes/Apple Music library XML files
│   └── Library.xml           # Your exported iTunes library (required)
├── music_sorter.py            # Music library sorting script
├── run_music_sorter.sh        # Quick start script
├── playlists/                 # Generated playlist files
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
└── README.md                 # This file
```

## Supported Formats

- **Input**: iTunes/Apple Music Library XML files
- **Output**: M3U playlist files (compatible with most music players)
- **Metadata**: BPM, Genre, Artist, Album, Track Name, Duration

## Planned Features

- **Musical Key Detection**: Sort tracks by musical key (C, D, E, F, G, A, B and their variations)
- **Advanced BPM Analysis**: More granular tempo categorization
- **Mood-based Sorting**: Classify tracks by energy and mood
- **Smart Playlist Generation**: AI-powered playlist creation
- **Multiple Export Formats**: Support for additional playlist formats

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with love for Apple Music enthusiasts.**
