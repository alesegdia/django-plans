def get_user_quota(user):
    """
    Tiny helper for getting quota dict for user (left mostly for backward compatibility)
    """
    userplans = {}
    for userplan in user.userplan_set.iterator():
        userplans[userplan] = userplan.plan.get_quota_dict()
    return userplans

