#!/usr/bin/env python3
"""
Apple Music Playlist Creator - Music Library Sorter

This module provides functionality to parse iTunes/Apple Music library XML files
and create sorted playlists based on BPM (tempo) and genre information.

Features:
- Parse iTunes Library.xml files
- Sort tracks by BPM ranges (Slow, Moderate, Upbeat, Fast, etc.)
- Sort tracks by genre
- Generate M3U playlist files
- Provide library statistics and analysis

Author: rekidderjr
"""

import random
import xml.etree.ElementTree as ET  # nosec B405 - parsing trusted iTunes library files
from collections import defaultdict
from pathlib import Path


class MusicSorter:
    """
    A class for parsing iTunes/Apple Music library XML files and creating sorted playlists.

    This class provides methods to:
    - Parse iTunes Library.xml files and extract track metadata
    - Sort tracks by BPM (beats per minute) ranges
    - Sort tracks by genre
    - Generate M3U playlist files
    - Create library analysis reports

    Attributes:
        library_xml_path (str): Path to the iTunes Library.xml file
        tracks (list): List of parsed track dictionaries
    """

    def __init__(self, library_xml_path):
        """
        Initialize the MusicSorter with a path to the iTunes Library.xml file.

        Args:
            library_xml_path (str): Path to the iTunes/Apple Music Library.xml file
        """
        self.library_xml_path = library_xml_path
        self.tracks = []

    def parse_library(self):
        """Parse iTunes Library.xml and extract track data"""
        tree = ET.parse(self.library_xml_path)  # nosec B314 - parsing trusted iTunes library files
        root = tree.getroot()

        # Find the tracks dictionary
        tracks_dict = None
        dict_children = list(root.find("dict"))
        for i, child in enumerate(dict_children):
            if child.tag == "key" and child.text == "Tracks":
                if i + 1 < len(dict_children):
                    tracks_dict = dict_children[i + 1]
                break

        if tracks_dict is None:
            print("No tracks found in library")
            return

        # Parse each track
        for i in range(0, len(tracks_dict), 2):
            track_data = tracks_dict[i + 1]

            track_info = self._parse_track_data(track_data)
            if track_info:
                self.tracks.append(track_info)

        print(f"Parsed {len(self.tracks)} tracks")

    def _parse_track_data(self, track_element):
        """Extract relevant data from a track element"""
        track = {}

        for i in range(0, len(track_element), 2):
            if i + 1 >= len(track_element):
                break

            key = track_element[i].text
            value_element = track_element[i + 1]

            if key in ["Name", "Artist", "Album", "Genre"]:
                track[key.lower()] = value_element.text or ""
            elif key == "BPM":
                track["bpm"] = int(value_element.text) if value_element.text else 0
            elif key == "Total Time":
                track["duration"] = int(value_element.text) if value_element.text else 0
            elif key == "Location":
                track["location"] = value_element.text or ""

        # Only include tracks with basic info
        if track.get("name") and track.get("artist"):
            return track
        return None

    def sort_by_bpm(self, bpm_ranges=None):
        """Sort tracks by BPM ranges"""
        if bpm_ranges is None:
            bpm_ranges = [
                (0, 80, "Slow (0-80 BPM)"),
                (81, 100, "Moderate (81-100 BPM)"),
                (101, 120, "Medium (101-120 BPM)"),
                (121, 140, "Upbeat (121-140 BPM)"),
                (141, 160, "Fast (141-160 BPM)"),
                (161, 180, "Very Fast (161-180 BPM)"),
                (181, 999, "Extreme (181+ BPM)"),
            ]

        bpm_sorted = defaultdict(list)
        no_bpm = []

        for track in self.tracks:
            bpm = track.get("bpm", 0)
            if bpm == 0:
                no_bpm.append(track)
                continue

            for min_bpm, max_bpm, label in bpm_ranges:
                if min_bpm <= bpm <= max_bpm:
                    bpm_sorted[label].append(track)
                    break

        if no_bpm:
            bpm_sorted["No BPM Data"].extend(no_bpm)

        return dict(bpm_sorted)

    def sort_by_genre(self):
        """Sort tracks by genre"""
        genre_sorted = defaultdict(list)

        for track in self.tracks:
            genre = track.get("genre", "Unknown").strip()
            if not genre:
                genre = "Unknown"
            genre_sorted[genre].append(track)

        return dict(genre_sorted)

    def create_playlists(self, output_dir="playlists"):
        """Create playlist files sorted by BPM and genre"""
        Path(output_dir).mkdir(exist_ok=True)

        # BPM playlists
        bpm_sorted = self.sort_by_bpm()
        for bpm_range, tracks in bpm_sorted.items():
            if tracks:
                self._write_playlist(
                    tracks, f"{output_dir}/BPM_{bpm_range.replace(' ', '_').replace('(', '').replace(')', '')}.m3u", bpm_range
                )

        # Genre playlists
        genre_sorted = self.sort_by_genre()
        for genre, tracks in genre_sorted.items():
            if len(tracks) >= 5:  # Only create playlist if 5+ tracks
                safe_genre = "".join(c for c in genre if c.isalnum() or c in (" ", "-", "_")).strip()
                self._write_playlist(tracks, f"{output_dir}/Genre_{safe_genre}.m3u", f"Genre: {genre}")

        # Remove duplicates from all playlists
        self._cleanup_duplicates(output_dir)

        # Random sort playlists to avoid grouping
        self._random_sort_playlists(output_dir)

    def _write_playlist(self, tracks, filename, title):
        """Write tracks to M3U playlist file"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write(f"#PLAYLIST:{title}\n")

            tracks_written = 0
            tracks_skipped = 0

            for track in sorted(tracks, key=lambda x: (x.get("artist", ""), x.get("name", ""))):
                duration = track.get("duration", 0) // 1000  # Convert to seconds
                f.write(f"#EXTINF:{duration},{track.get('artist', '')} - {track.get('name', '')}\n")

                location = track.get("location", "")
                if location.startswith("file://"):
                    # Convert file URL to local path
                    from urllib.parse import unquote

                    local_path = unquote(location[7:])  # Remove 'file://'

                    # Check if file exists
                    if Path(local_path).exists():
                        f.write(f"{local_path}\n")
                        tracks_written += 1
                    else:
                        f.write(f"# MISSING: {local_path}\n")
                        tracks_skipped += 1
                elif location:
                    # Handle other location formats
                    f.write(f"{location}\n")
                    tracks_written += 1
                else:
                    # No location available
                    f.write(f"# NO LOCATION: {track.get('artist', '')} - {track.get('name', '')}\n")
                    tracks_skipped += 1

        print(f"Created playlist: {filename}")
        print(f"  - {tracks_written} tracks with valid paths")
        print(f"  - {tracks_skipped} tracks skipped (missing/invalid paths)")

        if tracks_written == 0:
            print(f"  ⚠️  WARNING: No valid file paths found in playlist!")
            print(f"     This may be because:")
            print(f"     1. iTunes Library.xml doesn't contain file locations")
            print(f"     2. Music files have been moved or deleted")
            print(f"     3. Library.xml is from a different computer")

    def _cleanup_duplicates(self, output_dir):
        """Remove duplicate tracks from all .m3u files in the output directory"""
        playlist_files = Path(output_dir).glob("*.m3u")

        for playlist_file in playlist_files:
            seen_tracks = set()
            cleaned_lines = []

            with open(playlist_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            i = 0
            while i < len(lines):
                line = lines[i].strip()

                if line.startswith("#EXTINF:"):
                    # Extract track title from EXTINF line
                    if "," in line:
                        track_title = line.split(",", 1)[1]

                        if track_title not in seen_tracks:
                            seen_tracks.add(track_title)
                            cleaned_lines.append(lines[i])
                            # Add the next line (file path) if it exists
                            if i + 1 < len(lines):
                                cleaned_lines.append(lines[i + 1])
                            i += 2
                        else:
                            # Skip duplicate track and its path
                            i += 2
                    else:
                        cleaned_lines.append(lines[i])
                        i += 1
                else:
                    cleaned_lines.append(lines[i])
                    i += 1

            # Write cleaned playlist back to file
            with open(playlist_file, "w", encoding="utf-8") as f:
                f.writelines(cleaned_lines)

    def _random_sort_playlists(self, output_dir):
        """Randomly sort tracks in all .m3u files to avoid artist/album grouping"""
        playlist_files = Path(output_dir).glob("*.m3u")

        for playlist_file in playlist_files:
            with open(playlist_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Separate header lines from track entries
            header_lines = []
            track_entries = []

            i = 0
            while i < len(lines) and not lines[i].strip().startswith("#EXTINF:"):
                header_lines.append(lines[i])
                i += 1

            # Collect track entries (EXTINF + path pairs)
            while i < len(lines):
                if lines[i].strip().startswith("#EXTINF:") and i + 1 < len(lines):
                    track_entries.append((lines[i], lines[i + 1]))
                    i += 2
                else:
                    i += 1

            # Randomly shuffle track entries
            random.shuffle(track_entries)

            # Write back to file
            with open(playlist_file, "w", encoding="utf-8") as f:
                f.writelines(header_lines)
                for extinf_line, path_line in track_entries:
                    f.write(extinf_line)
                    f.write(path_line)

    def analyze_library_data(self):
        """Analyze the iTunes library data to help debug playlist issues"""
        if not self.tracks:
            print("No tracks loaded. Run parse_library() first.")
            return

        total_tracks = len(self.tracks)
        tracks_with_location = sum(1 for track in self.tracks if track.get("location"))
        tracks_with_file_urls = sum(1 for track in self.tracks if track.get("location", "").startswith("file://"))
        tracks_with_valid_paths = 0

        print(f"\n=== LIBRARY DATA ANALYSIS ===")
        print(f"Total tracks: {total_tracks}")
        print(f"Tracks with location data: {tracks_with_location}")
        print(f"Tracks with file:// URLs: {tracks_with_file_urls}")

        # Check first few tracks with locations
        sample_tracks = [t for t in self.tracks[:10] if t.get("location")]
        if sample_tracks:
            print(f"\nSample locations (first {len(sample_tracks)} tracks):")
            for i, track in enumerate(sample_tracks, 1):
                location = track.get("location", "")
                if location.startswith("file://"):
                    from urllib.parse import unquote

                    local_path = unquote(location[7:])
                    exists = Path(local_path).exists()
                    tracks_with_valid_paths += 1 if exists else 0
                    print(f"  {i}. {track.get('artist', 'Unknown')} - {track.get('name', 'Unknown')}")
                    print(f"     Path: {local_path}")
                    print(f"     Exists: {'✅' if exists else '❌'}")
                else:
                    print(f"  {i}. {track.get('artist', 'Unknown')} - {track.get('name', 'Unknown')}")
                    print(f"     Location: {location}")

        if tracks_with_file_urls == 0:
            print(f"\n⚠️  No file:// URLs found in library!")
            print(f"   This means iTunes Library.xml doesn't contain local file paths.")
            print(f"   Possible solutions:")
            print(f"   1. Re-export your iTunes library with 'Export Library' option")
            print(f"   2. Check if music files are stored locally (not streaming/cloud)")
            print(f"   3. Ensure iTunes has indexed your local music files")

        return {
            "total_tracks": total_tracks,
            "tracks_with_location": tracks_with_location,
            "tracks_with_file_urls": tracks_with_file_urls,
            "tracks_with_valid_paths": tracks_with_valid_paths,
        }

    def generate_report(self):
        """Generate a summary report"""
        bpm_sorted = self.sort_by_bpm()
        genre_sorted = self.sort_by_genre()

        print("\n=== MUSIC LIBRARY ANALYSIS ===")
        print(f"Total tracks: {len(self.tracks)}")

        print("\n--- BPM Distribution ---")
        for bpm_range, tracks in bpm_sorted.items():
            print(f"{bpm_range}: {len(tracks)} tracks")

        print("\n--- Top Genres ---")
        sorted_genres = sorted(genre_sorted.items(), key=lambda x: len(x[1]), reverse=True)
        for genre, tracks in sorted_genres[:10]:
            print(f"{genre}: {len(tracks)} tracks")

        # BPM statistics
        bpm_tracks = [t for t in self.tracks if t.get("bpm", 0) > 0]
        if bpm_tracks:
            bpms = [t["bpm"] for t in bpm_tracks]
            print("\n--- BPM Statistics ---")
            print(f"Tracks with BPM data: {len(bpm_tracks)}")
            print(f"Average BPM: {sum(bpms) / len(bpms):.1f}")
            print(f"BPM range: {min(bpms)} - {max(bpms)}")


def main():
    """
    Main function to run the music sorter application.

    This function:
    1. Checks for the iTunes Library.xml file
    2. Creates a MusicSorter instance
    3. Parses the library and generates reports
    4. Creates playlist files in the 'playlists' directory
    """
    library_path = "data/Library.xml"

    if not Path(library_path).exists():
        print(f"❌ iTunes Library file not found: {library_path}")
        print("Please export your iTunes/Apple Music library:")
        print("1. Open Music app (or iTunes)")
        print("2. Go to File → Library → Export Library...")
        print("3. Save as 'Library.xml' in the 'data/' directory")
        return

    print("🎵 Starting Apple Music Playlist Creator...")
    sorter = MusicSorter(library_path)

    print("📖 Parsing iTunes library...")
    sorter.parse_library()

    print("🔍 Analyzing library data...")
    sorter.analyze_library_data()

    print("📊 Generating library report...")
    sorter.generate_report()

    print("🎼 Creating playlists...")
    sorter.create_playlists()

    print("✅ Complete! Check the 'playlists/' directory for your new playlists.")


if __name__ == "__main__":
    main()
