# Apple Music Playlist Creator

[![Security Scan](https://github.com/rekidderjr/apple-music-playlist-creator/workflows/Security%20Scan/badge.svg)](https://github.com/rekidderjr/apple-music-playlist-creator/actions)
[![Code Quality](https://github.com/rekidderjr/apple-music-playlist-creator/workflows/Code%20Quality/badge.svg)](https://github.com/rekidderjr/apple-music-playlist-creator/actions)
[![Tests](https://github.com/rekidderjr/apple-music-playlist-creator/workflows/Tests/badge.svg)](https://github.com/rekidderjr/apple-music-playlist-creator/actions)

A tool to create and manage Apple Music playlists programmatically, with advanced music library analysis and sorting capabilities.

## Features

### Enhanced Music Library Analysis & Sorting
- **BPM Sorting**: Automatically categorizes tracks by tempo ranges (Slow, Moderate, Upbeat, Fast, Very Fast, Extreme)
- **Genre Sorting**: Creates playlists based on music genres from your library
- **Duplicate Removal**: Automatically removes duplicate tracks from playlists (same artist-song combinations)
- **Random Shuffling**: Randomly sorts tracks within playlists to avoid artist/album grouping
- **Library Statistics**: Provides detailed analysis of your music collection
- **Playlist Generation**: Creates .m3u playlist files compatible with Apple Music, iTunes, and other players

### New Enhanced Features
- **Library Data Analysis**: Diagnoses iTunes XML issues and missing file paths
- **Enhanced Debugging**: Detailed feedback on playlist creation with file path validation
- **Missing File Detection**: Identifies tracks with invalid or missing file locations
- **Improved Error Handling**: Better error messages and troubleshooting guidance
- **File Path Validation**: Checks if music files actually exist on disk

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

### Troubleshooting "Empty Playlist" Issues
If you're getting empty playlists, the enhanced version now provides detailed diagnostics:

- **Library Analysis**: Run the tool to see how many tracks have valid file paths
- **File Path Validation**: Checks if music files actually exist on your system
- **Missing Location Data**: Identifies if iTunes XML lacks file location information
- **Detailed Reporting**: Shows exactly how many tracks were written vs. skipped

### Additional Features
- **Security First**: Comprehensive security scanning and compliance
- **Quality Assured**: Automated code quality checks and testing
- **Enterprise Ready**: Meets customer compliance requirements

## Requirements

- Python 3.8 or higher (tested with Python 3.11.13)
- iTunes/Apple Music library XML file
- Additional requirements listed in `requirements.txt` (uses Python standard library only)

## Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/rekidderjr/apple-music-playlist-creator.git
cd apple-music-playlist-creator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (development tools only - no runtime dependencies)
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pre-commit install

# Run compliance check (optional)
./customer-compliance-check.sh
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
2. **Analyze your music collection** for file path issues
3. Generate playlist files in the `playlists/` directory
4. Remove duplicate tracks from playlists
5. Randomly shuffle tracks to avoid artist/album grouping
6. **Display detailed statistics** about your library and any issues found
7. **Provide troubleshooting guidance** if problems are detected

### Enhanced Output Example

```
🎵 Starting Apple Music Playlist Creator...
📖 Parsing iTunes library...
🔍 Analyzing library data...

=== LIBRARY DATA ANALYSIS ===
Total tracks: 49,396
Tracks with location data: 45,230
Tracks with file:// URLs: 45,230

Sample locations (first 5 tracks):
  1. Artist Name - Song Title
     Path: /Users/username/Music/Artist/Album/Song.mp3
     Exists: ✅
  2. Another Artist - Another Song
     Path: /Users/username/Music/Another/Album/Song.mp3
     Exists: ✅

📊 Generating library report...
🎼 Creating playlists...

Created playlist: playlists/BPM_Upbeat_121-140_BPM.m3u
  - 1,234 tracks with valid paths
  - 12 tracks skipped (missing/invalid paths)

✅ Complete! Check the 'playlists/' directory for your new playlists.
```

### Basic API Usage

```python
from apple_music_playlist_creator import PlaylistCreator

# Create a playlist creator instance
creator = PlaylistCreator()

# Create a new playlist
playlist = creator.create_playlist("My Awesome Playlist")
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
bandit -r src/ music_sorter.py
safety scan

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
├── music_sorter.py            # Enhanced music library sorting script
├── run_music_sorter.sh        # Quick start script
├── playlists/                 # Generated playlist files
│   └── sample_playlist.m3u   # Example output format
├── requirements.txt           # Production dependencies (none - uses stdlib)
├── requirements-dev.txt       # Development dependencies
└── README.md                 # This file
```

## Supported Formats

- **Input**: iTunes/Apple Music Library XML files
- **Output**: M3U playlist files (compatible with most music players)
- **Metadata**: BPM, Genre, Artist, Album, Track Name, Duration, File Paths

## Security & Compliance

This project includes comprehensive security measures:
- ✅ **Bandit security scanning** - No HIGH/CRITICAL vulnerabilities
- ✅ **Code quality standards** - Black, isort, flake8, pylint
- ✅ **Automated testing** - pytest with coverage
- ✅ **Pre-commit hooks** - Automated quality checks
- ✅ **GitHub Actions** - CI/CD with security scanning

## Troubleshooting

### Empty Playlists
If you're getting empty playlists, the tool now provides detailed diagnostics:
1. Run `python3 music_sorter.py` to see the library analysis
2. Check if tracks have valid file locations in the iTunes XML
3. Verify that music files haven't been moved or deleted
4. Ensure the Library.xml is from the same computer where music files are stored

### Missing File Paths
The enhanced version will show you exactly what's wrong:
- How many tracks have location data
- Sample file paths and whether they exist
- Specific guidance on re-exporting your iTunes library

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
