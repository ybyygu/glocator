#! /usr/bin/env python3
# [[file:~/Workspace/Programming/glocator/glocator.note::60effdbd-c99a-4f7e-b2b5-ccb95a6577f2][60effdbd-c99a-4f7e-b2b5-ccb95a6577f2]]
#===============================================================================#
#   DESCRIPTION:  ---
#
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#         NOTES:  ---
#        AUTHOR:  Wenping Guo <ybyygu@gmail.com>
#       LICENCE:  GPL version 2 or upper
#       CREATED:  <2017-10-16 Mon 14:45>
#       UPDATED:  <2017-11-19 Sun 20:35>
#===============================================================================#
# 60effdbd-c99a-4f7e-b2b5-ccb95a6577f2 ends here

# [[file:~/Workspace/Programming/glocator/glocator.note::9844612f-9f1d-4f9d-a4ce-c04bfca62610][9844612f-9f1d-4f9d-a4ce-c04bfca62610]]
import os
import sqlite3

from contextlib import contextmanager

ZOTERO_DB_FILENAME = os.path.expanduser("~/Data/zotero/zotero.sqlite.bak")
# 9844612f-9f1d-4f9d-a4ce-c04bfca62610 ends here

# [[file:~/Workspace/Programming/glocator/glocator.note::9adff0ef-a1e8-4a96-9200-d756bc56ef30][9adff0ef-a1e8-4a96-9200-d756bc56ef30]]
# attachment item
# i.e: zotero://select/items/1_2HQN5BHJ
SQL_ATTACHMENT_ITEM = """
SELECT    itemAttachments.path
FROM      items, itemAttachments
WHERE     itemAttachments.ItemID  = items.itemID
          and itemAttachments.contentType = "application/pdf"
          and items.key = ?;
"""
# 9adff0ef-a1e8-4a96-9200-d756bc56ef30 ends here

# [[file:~/Workspace/Programming/glocator/glocator.note::71f64d9a-adb3-4d7b-9308-c413eb2334f6][71f64d9a-adb3-4d7b-9308-c413eb2334f6]]
# article item
# i.e: zotero://select/items/1_NIUYMGLJ
SQL_PARENT_ITEM = """
SELECT    itemAttachments.path
FROM      items, itemAttachments
WHERE     itemAttachments.parentItemID  = items.itemID
          and itemAttachments.contentType = "application/pdf"
          and items.key = ?;
"""
# 71f64d9a-adb3-4d7b-9308-c413eb2334f6 ends here

# [[file:~/Workspace/Programming/glocator/glocator.note::72722bc5-b5c6-485f-9b99-07df482ba3d2][72722bc5-b5c6-485f-9b99-07df482ba3d2]]
@contextmanager
def _zotdb():
    with sqlite3.connect(ZOTERO_DB_FILENAME) as conn:
        cursor = conn.cursor()
        yield cursor
# 72722bc5-b5c6-485f-9b99-07df482ba3d2 ends here

# [[file:~/Workspace/Programming/glocator/glocator.note::0113ad5b-cead-4128-9fe9-ad679138be76][0113ad5b-cead-4128-9fe9-ad679138be76]]
def _get_attachment_from_itemkey(itemkey):
    """get pdf attachement from zotero database

    Parameters
    ----------
    itemkey: item key pointing to an article or attachment
    """
    with _zotdb() as cur:
        # first support itemkey pointing to an attachment
        query = cur.execute(SQL_ATTACHMENT_ITEM, (itemkey,))
        rows = query.fetchall()
        # if found nothing, search its parent item instead
        if len(rows) < 1:
            query = cur.execute(SQL_PARENT_ITEM, (itemkey, ))
            rows = query.fetchall()
        # if found many, return the first attachment
        print(rows)
        if len(rows) >= 1:
            return rows[0][0]
        else:
            print("found nothing")
            return None

def get_attachement_from_zotero_link(link):
    """open attachment from zotero protocol link

    Parameters
    ----------
    link: zotero item selection link, i.e: zotero://select/items/1_NIUYMGLJ
    """

    assert link.startswith("zotero://"), link
    itemkey = link.split("_", maxsplit=1)[-1]
    assert len(itemkey) == 8, "{} ==> {}".format(link, itemkey)

    path_str = _get_attachment_from_itemkey(itemkey)
    if not path_str:
        return

    dir_base = os.path.dirname(ZOTERO_DB_FILENAME)
    if path_str.startswith("storage:"):
        attachname = path_str[8:]
    else:
        attachname = path_str

    full_path = os.path.join(dir_base, "storage", itemkey, attachname)
    return full_path
# 0113ad5b-cead-4128-9fe9-ad679138be76 ends here

# [[file:~/Workspace/Programming/glocator/glocator.note::56b26039-4f86-4e57-82dc-9cb4e40c70e4][56b26039-4f86-4e57-82dc-9cb4e40c70e4]]
def main():
    version = "%(prog)s "
    desc = "default description"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-v', '--version',
                        version=version,
                        action='version')

    parser.add_argument('itemlink',
                        help='zotero selection item link')

    if len(sys.argv) == 1:
        parser.print_help()
        return

    cmdl = parser.parse_args()

    if cmdl.itemlink:
        path = get_attachement_from_zotero_link(cmdl.itemlink)
        print(path)
    else:
        parser.print_help()


if __name__ == '__main__':
    import sys
    import argparse

    main()
# 56b26039-4f86-4e57-82dc-9cb4e40c70e4 ends here
