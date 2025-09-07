#!/usr/bin/env python3
import random
from pathlib import Path

def parse_itunes_txt(file_path):
    """Parse iTunes playlist export and extract tracks"""
    with open(file_path, 'r', encoding='utf-16') as f:
        lines = f.readlines()
    
    if len(lines) < 2:
        return []
    
    header = lines[0].strip().split('\t')
    tracks = []
    
    # Find field indices
    name_idx = header.index('Name')
    artist_idx = header.index('Artist') 
    location_idx = header.index('Location')
    time_idx = header.index('Time')
    
    for line in lines[1:]:
        fields = line.strip().split('\t')
        if len(fields) > location_idx and fields[location_idx].endswith('.aif'):
            tracks.append({
                'artist': fields[artist_idx],
                'name': fields[name_idx],
                'path': f"/Volumes/{fields[location_idx]}",
                'duration': fields[time_idx] if len(fields) > time_idx else "0"
            })
    
    return tracks

def dedupe_and_shuffle(tracks):
    """Remove duplicates and randomize order"""
    seen = set()
    unique = []
    
    for track in tracks:
        key = f"{track['artist']} - {track['name']}".lower()
        if key not in seen:
            seen.add(key)
            unique.append(track)
    
    random.shuffle(unique)
    return unique

def create_m3u(tracks, output_path):
    """Create M3U playlist file"""
    Path(output_path).parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        for track in tracks:
            duration = track.get('duration', '-1')
            f.write(f"#EXTINF:{duration},{track['artist']} - {track['name']}\n")
            f.write(f"{track['path']}\n")

def main():
    input_dir = Path('/Users/rekidderjr/code/apple_music_playlist_creator/data/exported_playlist')
    output_dir = Path('/Users/rekidderjr/code/apple_music_playlist_creator/playlists')
    
    for txt_file in input_dir.glob('*.txt'):
        print(f"Processing {txt_file.name}...")
        
        tracks = parse_itunes_txt(txt_file)
        print(f"Found {len(tracks)} tracks")
        
        unique_tracks = dedupe_and_shuffle(tracks)
        print(f"After dedup/shuffle: {len(unique_tracks)} tracks")
        
        output_file = output_dir / f"{txt_file.stem}_deduplicated.m3u"
        create_m3u(unique_tracks, output_file)
        print(f"Created: {output_file}\n")

if __name__ == "__main__":
    main()
