UNITS = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
paths = ["docs/report.PDF", "notes.txt", "docs/img/logo.png", "Makefile"]


def count_by_extension(paths: list[str]) -> dict[str, int]:
    res = {}
    for path in paths:
        data = path.split('.')
        if len(data) == 1:
            data.append('')
        ext = data[-1].lower()
        res[ext] = res.get(ext, 0)+1
    return res


def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return min(paths, key=lambda x: (-x.count("/"), x))


def human_size(n_bytes: int) -> str:
    res = 0
    while n_bytes//1024 != 0:
        n_bytes = n_bytes/1024
        res += 1
    if n_bytes == int(n_bytes):
        return f'{n_bytes} {UNITS[res]}'
    return f'{n_bytes:.1f} {UNITS[res]}'


print(human_size(900))
