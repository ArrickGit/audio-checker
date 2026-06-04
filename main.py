import csv
import re
import sys
from collections import defaultdict
from pathlib import Path
import librosa

FILENAME_PATTERN = re.compile(
    r"^[^_]+_(?P<scene>[^_]+_[^_]+_[^_]+_[^_]+_[^_]+)_[^@]+@(?P<id>[^#]+)#(?P<lang>[^.]+)$",
    re.IGNORECASE,
)

SUPPORTED_AUDIO_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac"}
BASE_LANGUAGE = "eng"
REPORT_LANGUAGES = ["eng", "sch", "jpn", "spa", "fre", "ita", "bra", "ger"]
CSV_COLUMNS = [
    "Line ID",
    "Scene",
    "ENG Duration",
    "SCH Duration",
    "JPN Duration",
    "SPA Duration",
    "FRE Duration",
    "ITA Duration",
    "BRA Duration",
    "GER Duration",
    "Biggest Diff",
]
folder_path = Path(__file__).parent / "example_audio"
default_output_path = Path(__file__).parent / "example_audio_duration_report.csv"


def main():
    print("Audio Checker")

    if len(sys.argv) > 1:
        audio_folder = Path(sys.argv[1])
    else:
        audio_folder = folder_path

    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
    else:
        output_path = default_output_path

    if not audio_folder.exists():
        print(f"Audio folder not found: {audio_folder}")
        sys.exit(1)

    audio_groups = collect_audio_groups(audio_folder)
    write_duration_report(audio_groups, output_path)
    print(f"CSV report written to: {output_path}")


def collect_audio_groups(audio_folder):
    audio_groups = defaultdict(dict)

    for file_path in audio_folder.rglob("*"):
        if not is_audio_file(file_path):
            continue

        audio_info = parse_audio_filename(file_path)
        if audio_info is None:
            print(f"Skipping invalid filename: {file_path.name}")
            continue

        audio_id = audio_info["id"]
        language = audio_info["lang"].lower()
        audio_groups[audio_id][language] = {
            "path": file_path,
            **audio_info,
        }

    return audio_groups


def write_duration_report(audio_groups, output_path):
    rows = build_duration_rows(audio_groups)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def build_duration_rows(audio_groups):
    rows = []

    for audio_id, files_by_language in sorted(audio_groups.items()):
        english_audio = files_by_language.get(BASE_LANGUAGE)

        if english_audio is None:
            print(f"Skipping ID {audio_id}: missing {BASE_LANGUAGE} audio")
            continue

        durations = get_group_durations(files_by_language)
        english_duration = durations[BASE_LANGUAGE]
        biggest_diff = 0

        row = {
            "Line ID": audio_id,
            "Scene": english_audio["scene"],
            "ENG Duration": format_duration(english_duration),
        }

        for language in REPORT_LANGUAGES:
            if language == BASE_LANGUAGE:
                continue

            duration = durations.get(language)
            column_name = f"{language.upper()} Duration"

            if duration is None:
                row[column_name] = "NIL"
                continue

            duration_difference = abs(duration - english_duration)
            biggest_diff = max(biggest_diff, duration_difference)
            row[column_name] = (
                "-"
                if round(duration, 2) == round(english_duration, 2)
                else format_duration(duration)
            )

        row["Biggest Diff"] = (
            "-"
            if round(biggest_diff, 2) == 0
            else format_duration(biggest_diff)
        )
        rows.append(row)

    return rows


def get_group_durations(files_by_language):
    durations = {}

    for language, audio in files_by_language.items():
        durations[language] = get_audio_duration(audio["path"])

    return durations


def is_audio_file(file_path):
    return (
        file_path.is_file()
        and file_path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
    )


def parse_audio_filename(file_path):
    match = FILENAME_PATTERN.match(file_path.stem)
    if match is None:
        return None

    return match.groupdict()


def get_audio_duration(file_path):
    duration = librosa.get_duration(path=file_path)
    return duration


def format_duration(duration):
    return f"{duration:.2f}"


if __name__ == "__main__":
    main()
