class TimelineUtils:
    @staticmethod
    def filter_by_downtime_range_and_damage_class(downtime_windows, t, target, damage_class):
        for r in downtime_windows.get(target, tuple()):
            # None indicates filtering all damage types
            is_filtered_damage_type = (r[2] is None) or (r[2] == damage_class)
            if (r[0] <= t < r[1]) and is_filtered_damage_type:
                return True
        return False