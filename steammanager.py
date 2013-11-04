#coding=utf-8
__author__ = 'ron975'
import os
import steam.steam_shortcut_manager as shortcutmanager
import steam.steam_user_manager as usermanager


def insert_shortcut(manager, name, exe, icon=""):
    for shortcut in manager.shortcuts:
        if shortcut.appname == name:
            print shortcut.appname, "already exists, skipping"
            return
    manager.add_shortcut(name, "\""+exe+"\"", "\""+os.path.dirname(exe)+"\"", icon=icon)
    print "Added game", name, "to the Steam Library"

def associate_ids_with_users():
    steamusers = []
    for id in usermanager.user_ids_on_this_machine():
        steamusers.append({'steamid32': id, 'customurl': usermanager.name_from_communityid32(id)})
    return steamusers

def choose_userdata_folder():
    for index, user in enumerate(associate_ids_with_users()):
        print index+1, user['steamid32'], user['customurl']

    index = int(raw_input())
    return shortcutmanager.SteamShortcutManager(
        usermanager.shortcuts_file_for_user_id(associate_ids_with_users()[index-1]['steamid32'])
    )
