from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)


class MitBuilder:
    """A utility class used to get all the mit-related skills from a rotation, and prepares
    cached timeline usages to make it easier to detect superfluous usages.
    """

    def __init__(self, stats):
        self.__stats = stats

    def get_mit_windows(
        self, q_snapshot_and_applications: SnapshotAndApplicationEvents
    ):

        res = []  # start time, end time, skill, targets
        while not q_snapshot_and_applications.is_empty():
            [
                _,
                event_times,
                skill,
                skill_modifier,
                _,
                targets,
                _,
                _,
                _,
                _,
            ] = q_snapshot_and_applications.get_next()

            buff_spec = skill.get_buff_spec(skill_modifier)
            has_damage_reduction_buff = (
                buff_spec is not None and buff_spec.has_damage_reduction
            )
            debuff_spec = skill.get_debuff_spec(skill_modifier)
            has_damage_reduction_debuff = (
                debuff_spec is not None and debuff_spec.has_damage_reduction
            )

            if not has_damage_reduction_buff and not has_damage_reduction_debuff:
                continue

            assert (
                not has_damage_reduction_buff or not has_damage_reduction_debuff
            ), "Internal error: Mits should only be specified on buff or debuff. For multi-effects split into follow ups."

            spec_to_use = buff_spec if buff_spec is not None else debuff_spec

            # assume primary time is the only one we want
            start_time = event_times.primary
            end_time = start_time + spec_to_use.duration

            res.append((start_time, end_time, skill, targets))
        return res
