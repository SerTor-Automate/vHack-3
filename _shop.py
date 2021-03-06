def buy(userTK: str = None, abilityNM: str = None):
    """
    :param userTK:
    :param abilityNM:
    :return:
    """
    if not userTK or not abilityNM: return False, ["Invalid Arguments"]

    from _users import getUsersByQuery
    from _settings import SETTINGS
    from _database import CURSOR, CONNECTION

    if not abilityNM in SETTINGS["ABILITIES"]: return False, ["Invalid Ability"]

    for data in getUsersByQuery("SELECT coins,{1} FROM users WHERE token='{0}'".format(userTK, abilityNM))[1]:
        if data[0] >= (SETTINGS["ABILITIES"][abilityNM] * data[1]):
            CURSOR.execute("UPDATE users SET coins=coins-{1}, {2}={2}+1 WHERE token='{0}'".format(userTK, SETTINGS["ABILITIES"][abilityNM] * data[1], abilityNM))
            CONNECTION.commit()

            return True, ["Bought"]

        return False, ["Not Enougth Money"]


def getUserAbilityPriceByTK(userTK: str = None, abilityNM: str = None):
    """
    :param userTK:
    :param abilityNM:
    :return:
    """
    if not userTK or not abilityNM: return False, ["Invalid Arguments"]

    from _users import getUsersByQuery
    from _settings import SETTINGS

    if not abilityNM in SETTINGS["ABILITIES"]: return False, ["Invalid Ability"]

    data = getUsersByQuery("SELECT {1} FROM users WHERE token='{0}'".format(userTK, abilityNM))[1][0]

    return True, data[0] * SETTINGS["ABILITIES"][abilityNM]


def getUserAbilityMenuByTK(userTK: str = None):
    from _settings import SETTINGS
    from _users import getUsersByQuery

    returnMenu = list()
    replaceData = {
        ".defenseLVL": getUsersByQuery("SELECT defense FROM users WHERE token='{0}'".format(userTK))[1][0][0],
        ".defensePRICE": getUserAbilityPriceByTK(userTK, "defense")[1],
        ".attackLVL": "NONE",
        ".attackPRICE": "NONE"
    }
    for menu in SETTINGS["ABILITIES.MENU"]:
        for key, val in replaceData.items():
            menu = menu.replace(key, str(val))

        returnMenu.append(menu)

    return True, returnMenu
