"""
Basic tool to find dates when the sun aligns with a given street azimuth at a specific location.
Negative Azimuth's for Sunsets (West) and Positive Azimuth's for Sunrise (East)
"""
import datetime
from astral import sun, LocationInfo
from astral.location import Observer
from astral.geocoder import lookup, database
from astral.sun import sunrise, sunset
import osmnx as ox
import numpy as np

# User parameters

# LATITUDE = 40.74908576453197  # Example: New York City
# LONGITUDE = -73.97044936096869
# STREET_AZIMUTH = -298.87  # Example: Manhattan's main streets (degrees from North)


LATITUDE = 40.56519252366112
LONGITUDE = -74.59539637542379
STREET_AZIMUTH = -278.5  # Example: Manhattan's main streets (degrees from North)

TOLERANCE = 2  # degrees
YEAR = 2025


def is_aligned(sun_azimuth, street_azimuth, tolerance):
    diff = abs((sun_azimuth - street_azimuth + 180) % 360 - 180)
    return diff <= tolerance


def find_alignment_dates(lat, lon, street_azimuth, year, tolerance):
    observer = Observer(latitude=lat, longitude=lon)
    aligned_dates = []
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                date = datetime.date(year, month, day)
                sr = sunrise(observer, date=date)
                ss = sunset(observer, date=date)
                # Calculate azimuth at sunrise and sunset using sun.azimuth
                sr_az = sun.azimuth(observer, sr)
                ss_az = sun.azimuth(observer, ss)
                # Only add if aligned, and mark sign
                if is_aligned(sr_az, street_azimuth, tolerance):
                    aligned_dates.append((str(date), abs(sr_az)))  # Positive for sunrise
                if is_aligned(ss_az, street_azimuth, tolerance):
                    aligned_dates.append((str(date), -abs(ss_az)))  # Negative for sunset
            except Exception:
                continue  # Skip invalid dates
    return aligned_dates


def find_alignment_dates_both_directions(lat, lon, street_azimuth, year, tolerance):
    """
    Returns alignment dates for both the given azimuth and its reverse (azimuth+180).
    Sunrise azimuths are positive, sunset azimuths are negative.
    """
    city = LocationInfo(latitude=lat, longitude=lon)
    observer = Observer(latitude=lat, longitude=lon)
    aligned_dates = []
    azimuths = [street_azimuth, (street_azimuth + 180) % 360]
    for az in azimuths:
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    date = datetime.date(year, month, day)
                    sr = sunrise(observer, date=date)
                    ss = sunset(observer, date=date)
                    sr_az = sun.azimuth(observer, sr)
                    ss_az = sun.azimuth(observer, ss)
                    if is_aligned(sr_az, az, tolerance):
                        aligned_dates.append((str(date), abs(sr_az)))
                    if is_aligned(ss_az, az, tolerance):
                        aligned_dates.append((str(date), -abs(ss_az)))
                except Exception:
                    continue
    # Remove duplicates
    aligned_dates = list(set(aligned_dates))
    aligned_dates.sort()
    return aligned_dates


def calculate_street_azimuths(min_lat, min_lon, max_lat, max_lon):
    """
    Fetch street network in bounding box and calculate azimuth for each street segment.
    Returns a list of (segment_id, (lat1, lon1), (lat2, lon2), azimuth_degrees)
    """
    # Download street network from OSM
    G = ox.graph_from_bbox((min_lon, min_lat, max_lon, max_lat), network_type='drive')
    street_segments = []
    for u, v, k, data in G.edges(keys=True, data=True):
        try:
            point1 = G.nodes[u]
            point2 = G.nodes[v]
            lat1, lon1 = point1['y'], point1['x']
            lat2, lon2 = point2['y'], point2['x']
            # Calculate azimuth
            dlon = np.radians(lon2 - lon1)
            y = np.sin(dlon) * np.cos(np.radians(lat2))
            x = np.cos(np.radians(lat1)) * np.sin(np.radians(lat2)) - \
                np.sin(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.cos(dlon)
            azimuth = (np.degrees(np.arctan2(y, x)) + 360) % 360
            street_segments.append({
                'segment': (u, v, k),
                'start': (lat1, lon1),
                'end': (lat2, lon2),
                'azimuth': azimuth
            })
        except Exception:
            continue
    return street_segments


def filter_streets_by_azimuth(street_segments, target_azimuth, tolerance):
    """
    Filter street segments whose azimuth is within tolerance degrees of the target azimuth.
    Returns a list of matching street segments.
    """
    filtered = []
    for seg in street_segments:
        diff = abs((seg['azimuth'] - target_azimuth + 180) % 360 - 180)
        if diff <= tolerance:
            filtered.append(seg)
    return filtered


def find_street_alignments_in_bbox(min_lat, min_lon, max_lat, max_lon, year, tolerance):
    """
    For each street segment in the bounding box, find sun alignment dates for both azimuth directions.
    Returns a list of dicts with segment info and alignment dates.
    """
    segments = calculate_street_azimuths(min_lat, min_lon, max_lat, max_lon)
    results = []
    for seg in segments:
        lat1, lon1 = seg['start']
        lat2, lon2 = seg['end']
        mid_lat = (lat1 + lat2) / 2
        mid_lon = (lon1 + lon2) / 2
        alignment_dates = find_alignment_dates_both_directions(mid_lat, mid_lon, seg['azimuth'], year, tolerance)
        if alignment_dates:
            results.append({
                'segment': seg['segment'],
                'start': seg['start'],
                'end': seg['end'],
                'azimuth': seg['azimuth'],
                'alignment_dates': alignment_dates
            })
    return results


def main():
    results = find_alignment_dates(LATITUDE, LONGITUDE, STREET_AZIMUTH, YEAR, TOLERANCE)
    print(f"Dates in {YEAR} when the sun aligns with azimuth {STREET_AZIMUTH}° (±{TOLERANCE}°):")
    for date, sunrise_az, sunset_az in results:
        print(f"{date}: Sunrise azimuth={sunrise_az:.1f}°, Sunset azimuth={sunset_az:.1f}°")
    
    # Example usage of find_street_alignments_in_bbox
    bbox = (LATITUDE-0.01, LONGITUDE-0.01, LATITUDE+0.01, LONGITUDE+0.01)  # Small bbox around the point
    alignments = find_street_alignments_in_bbox(*bbox, YEAR, STREET_AZIMUTH, TOLERANCE)
    for a in alignments:
        print(a)


if __name__ == "__main__":
    main()