
class ActivityEntry:
    def __init__(self, description, created_at, type):
        self.description = description
        self.created_at = created_at
        self.type = type

    def get_icon(self):
        return {
            'project': 'kanban',
            'task': 'check2-square',
            'sale': 'cash-coin',
            'inventory': 'box',
        }.get(self.type, 'activity')

    def get_color(self):
        return {
            'project': 'primary',
            'task': 'success',
            'sale': 'warning',
            'inventory': 'info',
        }.get(self.type, 'secondary')