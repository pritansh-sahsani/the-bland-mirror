# helper functions
from main.models import Notification

def get_notification_for_navbar():
    notifications_in_navbar = Notification.query.filter_by(is_read = False)\
    .order_by(Notification.date.desc())\
    .limit(5)\
    .all()
    no_notifications = True if len(notifications_in_navbar) == 0 else False

    return notifications_in_navbar, no_notifications
