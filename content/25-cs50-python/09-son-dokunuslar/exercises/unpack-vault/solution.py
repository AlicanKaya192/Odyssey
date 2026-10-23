def total(galleons, sickles, knuts):
    return (galleons * 17 + sickles) * 29 + knuts


def total_from_list(coins):
    return total(*coins)


def total_from_dict(coins):
    return total(**coins)


def total_all(*vaults):
    return sum(total(*vault) for vault in vaults)
