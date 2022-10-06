from dataclasses import dataclass
import os
import shutil
from typing import Dict, List
from baku import consts, environment, utils

# Get the key/values that show up in the package config but not in the blog
# config
def diff_configs() -> Dict[str, str]:
    current_config = environment.load_config()
    package_path = os.path.abspath(os.path.dirname(__file__))
    new_config = environment.load_config(
        os.path.join(package_path, 'templates', consts.CONFIG))

    diff = new_config.keys() - current_config.keys()
    result = {}
    for key in diff:
        result[key] = new_config[key]
    return result


def upgrade_config() -> None:
    diff = diff_configs()
    if not diff:
        print('✅ No blog.cfg changes')
        return

    with utils.open_utf8(consts.CONFIG, 'a') as f:
        f.writelines([f'{k} = {v}\n' for k, v in diff.items()])
    print('✅ blog.cfg updated, new settings available')


def diff_files(current: str, new: str) -> bool:
    with open(current, 'rb') as f:
        current_content = f.read()

    with open(new, 'rb') as f:
        new_content = f.read()

    return current_content != new_content


@dataclass
class FileUpgrade:
    def __init__(self, current: str, new: str):
        self.current, self.new = current, new
        # If current doesn't exist, this is a new file to be copied
        if not os.path.exists(current):
            self.action = 'copy_new'
            return

        # If current differs from new file, we'll prompt user
        if diff_files(current, new):
            self.action = 'upgrade'
            return

        # If files are identical, we don't need to do anything
        self.action = 'ignore'


def prep_files_upgrade() -> List[FileUpgrade]:
    result = []
    package_path = os.path.abspath(os.path.dirname(__file__))
    package_dir = os.path.join(package_path, 'templates')

    for f in consts.TEMPLATES:
        result.append(FileUpgrade(
            os.path.join('templates', f), os.path.join(package_dir, f)))

    for f in consts.STATICS:
        result.append(FileUpgrade(
            os.path.join('static', f), os.path.join(package_dir, f)))

    return result


def upgrade_prompt(file: str, prompted: bool) -> str:
    # First prompt should provide more details.
    if not prompted:
        print(f'{file} in your blog is different than the latest template. ' \
            'Upgrading will overwrite the file. If you haven\'t modified it, ' \
            'you can ignore this and proceed with the upgrade. If you want ' \
            'preserve your version, choose the backup option then merge ' \
            'your changes in the new template.')
    # Subsequent prompts are simplified.
    else:
        print(f'{file} in your blog is different than the latest template.')

    options = '[O]verwrite, overwrite [a]ll, [b]ackup, bac[k]up all (oabk)? '

    while (handle := input(options).strip().upper()) not in 'OABK':
        print('Options are o, a, b, or k.')

    return handle


def upgrade_files() -> None:
    upgrades, handle, prompted = prep_files_upgrade(), None, False
    for u in upgrades:
        # Nothing to do for this file
        if u.action == 'ignore':
            continue

        # Modified file, figure out proper handling
        if u.action == 'upgrade':
            # Skip prompt if user already opted to overwrite or backup all
            if handle in ['A', 'K']:
                act = handle
            # Otherwise prompt
            else:
                act = upgrade_prompt(u.current, prompted)
                # Show simplified prompt after first prompt
                prompted = True
                # Remember if user wants to overwrite or backup all
                if act in ['A', 'K']:
                    handle = act

            # Backup if needed
            if act in ['B', 'K']:
                backup = u.current + '.bak'
                shutil.move(u.current, backup)
                print(f'Backed up {u.current} as {backup}')

        # Upgrade
        shutil.copy(u.new, u.current)
        print(f'✅ Upgraded {u.current}')


def upgrade() -> None:
    upgrade_config()
    upgrade_files()
