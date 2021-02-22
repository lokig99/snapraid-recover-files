from typing import List, Set
import os
import shutil

UNRECOVERABLE_EXT = '.unrecoverable'


def find_unrecoverable_files(dirpath: str) -> Set[str]:
    """
    :param dirpath: path to scanned directory
    :return: list of unrecoverable files (paths relative to given dirpath and with original extension)
    """
    unrec_files: Set[str] = set()
    for root, _, files in os.walk(dirpath):
        root = os.path.relpath(root, dirpath)
        for file in files:
            file = os.path.join(root, file)
            filename, ext = os.path.splitext(file)
            if ext == UNRECOVERABLE_EXT:
                unrec_files.add(filename)
    return unrec_files


def find_backup_files(backup: str, unrecoverable_files: Set[str]) -> List[str]:
    """
    :param backup:
    :param unrecoverable_files:
    :return:
    """
    result: List[str] = []
    for root, _, files in os.walk(backup):
        root = os.path.relpath(root, backup)
        for file in files:
            file = os.path.join(root, file)
            if file in unrecoverable_files:
                result.append(file)
    return result


def copy_from_backup(backup: str, target: str, relpaths: List[str]) -> bool:
    """
    :param backup:
    :param target:
    :param relpaths:
    :return:
    """
    for path in relpaths:
        src = os.path.join(backup, path)
        dst = os.path.join(target, path)
        print(f'copying: "{src}" --> "{dst}"')
        res = shutil.copy2(src, dst)
        if not os.path.exists(res):
            print(f'failed to copy: {res}')
            return False
    return True


def delete_unrecoverable_files(dirpath: str, unrecoverable_files: Set[str]) -> None:
    """
    :param dirpath:
    :param unrecoverable_files:
    :return:
    """
    for path in unrecoverable_files:
        path = os.path.join(dirpath, f'{path}{UNRECOVERABLE_EXT}')
        print(f'deleting: {path}')
        os.remove(path)


if __name__ == '__main__':
    target = input('target path: ')
    backup = input('backup path: ')

    unrec_files: Set[str] = find_unrecoverable_files(target)
    backup_files = find_backup_files(backup, unrec_files)
    if copy_from_backup(backup, target, backup_files):
        delete_unrecoverable_files(target, unrec_files)
