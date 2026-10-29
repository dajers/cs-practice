import json


def csv_to_records(text: str) -> list[dict]:
    lines = text.split('\n')
    headers = lines[0].split(',')
    lines = lines[1:]
    res = []
    for line in lines:
        line = line.split(',')
        if len(line) == 2:
            res.append({headers[0].strip(): line[0].strip(), headers[1].strip(): line[1].strip()})    
    return res


def parsing(value: str):
    lowered = value.lower()
    if lowered in ("true", "yes"):
        return True
    if lowered in ("false", "no"):
        return False
    try:
        if ',' in value:
            value = value.replace(',', '.')
        return int(value) 
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def parse_settings(lines: list[str]) -> dict:
    result = {}
    current_list_key = None
    for rawLine in lines:
        line = rawLine.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if current_list_key is not None:
                item = stripped[2:].strip()
                result[current_list_key].append(parsing(item))
            continue
        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value == "":
                result[key] = []
                current_list_key = key
            else:
                result[key] = parsing(value)
                current_list_key = None
    return result


def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    merged = []
    for row in rows:
        new_row = {}
        lookup_key = row.get(key)
        extra_data = extra.get(lookup_key, {}) if lookup_key is not None else {}
        new_row.update(extra_data)
        new_row.update(row)
        merged.append(new_row)
    return merged



def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)


print(parse_settings(["rate: 3,5 # с запятой",]))