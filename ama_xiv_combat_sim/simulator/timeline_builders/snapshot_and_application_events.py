import copy
import heapq

from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from collections import namedtuple


class SnapshotAndApplicationEvents:
    class EventTimes(namedtuple("EventTimes", ["primary", "secondary"])):
        def __eq__(self, other):
            return self.primary == other.primary and self.secondary == other.secondary

        # Some annoying things so we don't compare to None.
        def __lt__(self, other):
            if self.primary != other.primary:
                return self.primary < other.primary
            if self.secondary is None:
                return True
            if other.secondary is None:
                return False
            return self.secondary < other.secondary

    class Event(
        namedtuple(
            "Event",
            [
                "priority",
                "event_times",
                "skill",
                "skill_modifier",
                "snapshot_status",
                "targets",
                "event_id",
                "job_resources_added",
                "job_conditional_processed",
                "combo_conditional_processed",
            ],
        )
    ):
        def __lt__(self, other):
            return (self.priority, self.skill.name) < (other.priority, other.skill.name)

    def __init__(self):
        self.__q = []
        self.__event_id = 0
        heapq.heapify(self.__q)

    @staticmethod
    def __create_event(
        priority,
        primary_time,
        secondary_time,
        skill,
        skill_modifier,
        snapshot_status,
        event_id,
        job_resources_added,
        job_conditional_processed,
        combo_conditional_processed,
        targets,
    ):
        event_times = SnapshotAndApplicationEvents.EventTimes(
            primary=primary_time, secondary=secondary_time
        )
        res = SnapshotAndApplicationEvents.Event(
            priority=priority,
            event_times=event_times,
            skill=skill,
            skill_modifier=skill_modifier,
            snapshot_status=snapshot_status,
            targets=targets,
            event_id=event_id,
            job_resources_added=job_resources_added,
            job_conditional_processed=job_conditional_processed,
            combo_conditional_processed=combo_conditional_processed,
        )
        return res

    def add(
        self,
        priority,
        primary_time,
        secondary_time,
        skill,
        skill_modifier,
        snapshot_status,
        event_id=None,
        job_resources_added=False,
        job_conditional_processed=False,
        combo_conditional_processed=False,
        targets=(SimConsts.DEFAULT_TARGET,),
    ):
        if event_id is None:
            event_id = self.__event_id
            self.__event_id += 1

        # If the application and snapshot times are the same, then we can collapse them into 1 timing.
        if primary_time == secondary_time:
            secondary_time = None
            snapshot_status = [True, True]
        heapq.heappush(
            self.__q,
            self.__create_event(
                priority,
                primary_time,
                secondary_time,
                skill,
                skill_modifier,
                snapshot_status,
                event_id,
                job_resources_added,
                job_conditional_processed,
                combo_conditional_processed,
                targets,
            ),
        )

    def get_first_damage_time(self):
        first_damage_time = None
        for _, event_times, skill, skill_modifier, _, _, _, _, _, _ in self.__q:
            if skill.get_damage_spec(skill_modifier) is None:
                continue
            curr_time = (
                event_times.primary
                if event_times.secondary is None
                else event_times.secondary
            )
            first_damage_time = (
                curr_time
                if first_damage_time is None
                else min(curr_time, first_damage_time)
            )
        return first_damage_time

    def get_last_event_time(self):
        last_event_time = None
        for _, event_times, _, _, _, _, _, _, _, _ in self.__q:
            curr_time = (
                event_times.primary
                if event_times.secondary is None
                else event_times.secondary
            )
            last_event_time = (
                curr_time
                if last_event_time is None
                else max(curr_time, last_event_time)
            )
        return last_event_time

    def clear(self):
        self.__event_id = 0
        self.__q.clear()

    def is_empty(self):
        return len(self.__q) == 0

    def get_next(self):
        return heapq.heappop(self.__q)

    def get_q(self):
        res = copy.deepcopy(self.__q)
        res.sort()
        return res

    def __str__(self):
        q = copy.deepcopy(self.__q)
        res = ""
        for r in q:
            res += str(r) + "\n"
        return res
