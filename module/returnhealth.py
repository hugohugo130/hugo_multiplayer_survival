def returnishealth(diff):
    if diff == 3:
        return False
    else:
        return True


def returnmonsterinfo(diff):
    if diff == 1:
        health = 50
        attackage = 5
    elif diff == 2:
        health = 100
        attackage = 15
    elif diff == 3:
        health = 1000
        attackage = 99
    if diff in (1, 2, 3):
        return [health, attackage]
