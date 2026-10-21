LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def parse_event(line: str) -> dict:
    data = line.split(maxsplit=2)
    if len(data) < 3 or data[1] not in LEVELS:
        raise ValueError
    return {"time": data[0], "level": data[1], "message": data[2].rstrip("\r\n")}


def count_levels(lines: list[str]) -> dict:
    res = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            res["BROKEN"] = res.get("BROKEN", 0) + 1
        else:
            level = event['level']
            res[level] = res.get(level, 0) + 1
    return res


def top_errors(lines, n) -> list[list]:
    counts = {}
    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            continue
        if event["level"] != "ERROR":
            continue
        message = event["message"]
        counts[message] = counts.get(message, 0) + 1

    res = [[message, cnt] for message, cnt in counts.items()]
    res.sort(key=lambda x: (-x[1], x[0]))
    return res[:n]


def format_report(counts: dict, errors: list[list]) -> str:
    lines = ["Отчёт по журналу", ""]
    for level in sorted(counts):
        lines.append(f"{level}: {counts[level]}")
    lines.append("")
    lines.append("Частые ошибки:")
    for message, count in errors:
        lines.append(f"- {message} — {count}")
    return "\n".join(lines) + "\n"