#coding=utf-8
__author__ = 'ron975'
import os
import steamapi
import steamshortcut.steam_shortcut_manager as shortcutmanager
import steamshortcut.steam_user_manager as usermanager


def insert_shortcut(manager, name, exe, icon=""):
    manager.add_shortcut(name, "\""+exe+"\"", "\""+os.path.dirname(exe)+"\"", icon=icon)
    manager.save()


def shortcut_exists(manager, name):
    for shortcut in manager.shortcuts:
        if shortcut.appname == name:
            return True
    return False


def associate_ids_with_users():
    steamusers = []
    for id in usermanager.user_ids_on_this_machine():
        steamusers.append({'steamid32': id, 'customurl': usermanager.name_from_communityid32(id)})
    return steamusers


def get_customurls_on_machine():
    steamusers = []
    for id in usermanager.user_ids_on_this_machine():
        steamusers.append(usermanager.name_from_communityid32(id))
    return steamusers


def choose_userdata_folder():
    for index, user in enumerate(associate_ids_with_users()):
        print index+1, user['steamid32'], user['customurl']

    index = int(raw_input())
    return shortcutmanager.SteamShortcutManager(
        usermanager.shortcuts_file_for_user_id(associate_ids_with_users()[index-1]['steamid32'])
    )


def check_steam_version(steamid, name):
    steamapi.core.APIConnection('26CD88279076DCE178B6D47E167850AB')
    user = steamapi.user.SteamUser(steamid)
    for game in user.owned_games:
        if game.name == name:
            return True
    return False