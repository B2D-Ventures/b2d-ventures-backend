from b2d_ventures.app.models import Admin, Investor


def get_user_role(user):
    """Determine the role of a user."""
    if isinstance(user, Admin):
        return "admin"
    elif isinstance(user, Investor):
        return "investor"
    else:
        return "startup"
