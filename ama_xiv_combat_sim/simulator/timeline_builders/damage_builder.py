import copy
import heapq
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import SnapshotAndApplicationEvents
from ama_xiv_combat_sim.simulator.utils import Utils
from ama_xiv_combat_sim.simulator.trackers.combo_tracker import ComboTracker
from ama_xiv_combat_sim.simulator.trackers.job_resource_tracker import JobResourceTracker
from ama_xiv_combat_sim.simulator.trackers.status_effect_tracker import StatusEffectTracker
from ama_xiv_combat_sim.simulator.trackers.status_effects import StatusEffects

class DamageBuilder():
  
  def __init__(self, stats, skill_library):
    self.__skill_library = skill_library
    self.__stats = stats
    self.__status_effect_priority = skill_library.get_status_effect_priority(stats.job_class)
    self.se = StatusEffectTracker(self.__status_effect_priority)
    self.job_resource_tracker = JobResourceTracker(self.__skill_library.get_all_resource_settings(stats.job_class))
    self.combo_tracker = ComboTracker(self.__skill_library.get_all_combo_breakers(self.__stats.job_class))

  @staticmethod
  def __is_application_time(event_times):
    return event_times.secondary is None

  # output is a list, sorted by timestamp of damage instance (not necessarily in stable-sort order, according to the rotation).
  # Format of the elements of the output: (time, skill, (buffs, debuffs))
  def get_damage_instances(self, q_snapshot_and_applications: SnapshotAndApplicationEvents):
    last_primary_time = None

    q = [] # (current_time, skill, skill_modifier, (buffs, debuffs), job_resources)
    while not q_snapshot_and_applications.is_empty():
      [priority, event_times, skill, skill_modifier, snapshot_status, event_id, job_resources_added, job_conditional_processed, combo_contional_processed] = q_snapshot_and_applications.get_next()
      if last_primary_time is None:
        last_primary_time = event_times.primary
      else:
        assert last_primary_time <= event_times.primary, "We have gone backwards in time. This should never happen. Please contact the devs. last primary time/new primary time: {}/{}".format(last_primary_time, event_times.primary)
      last_primary_time = event_times.primary
      curr_time = event_times.primary
      self.se.expire_status_effects(curr_time)

      is_application_time = self.__is_application_time(event_times)
      skill_modifier = copy.deepcopy(skill_modifier)
      if is_application_time:
        if not job_conditional_processed:
          job_resource_conditional = self.job_resource_tracker.compile_job_resources(curr_time, skill)
          skill_modifier.add_to_condition(job_resource_conditional)

        if not job_resources_added:
          self.job_resource_tracker.add_resource(curr_time, skill, skill_modifier)

        if not combo_contional_processed:
          combo_conditional = self.combo_tracker.compile_and_update_combo(curr_time, skill, skill_modifier)
          skill_modifier.add_to_condition(combo_conditional)
          try:
            skill_modifier.add_to_condition(Utils.get_positional_condition(skill, skill_modifier))
          except ValueError as v:
            print(str(v))

        if not isinstance(snapshot_status[0], StatusEffects):
          snapshot_status[0], skill_modifier_from_buffs = self.se.compile_buffs(curr_time, skill)
          skill_modifier.add_to_condition(skill_modifier_from_buffs)

        if not isinstance(snapshot_status[1], StatusEffects):
          snapshot_status[1], skill_modifier_from_debuffs= self.se.compile_debuffs(curr_time, skill)
          skill_modifier.add_to_condition(skill_modifier_from_debuffs)

        if skill.get_damage_spec(skill_modifier) is not None:
          heapq.heappush(q, (curr_time, skill, skill_modifier, tuple(snapshot_status), event_id))
      else:
        if snapshot_status[0] is True:
          snapshot_status[0], skill_modifier_from_buffs = self.se.compile_buffs(curr_time, skill)
          skill_modifier.add_to_condition(skill_modifier_from_buffs)

        if snapshot_status[1] is True:
          snapshot_status[1], skill_modifier_from_debuffs= self.se.compile_debuffs(curr_time, skill)
          skill_modifier.add_to_condition(skill_modifier_from_debuffs)

        priority_modifier = Utils.transform_time_to_prio(event_times.primary) - priority
        new_priority = Utils.transform_time_to_prio(event_times.secondary) + priority_modifier

        job_conditional_was_processed = False
        if not job_conditional_processed and skill.job_resources_snapshot:
          job_resource_conditional = self.job_resource_tracker.compile_job_resources(curr_time, skill)
          skill_modifier.add_to_condition(job_resource_conditional)
          job_conditional_was_processed = True

        combo_conditional_was_processed = False
        if not combo_contional_processed:
          combo_conditional = self.combo_tracker.compile_and_update_combo(curr_time, skill, skill_modifier)
          skill_modifier.add_to_condition(combo_conditional)
          try:
            skill_modifier.add_to_condition(Utils.get_positional_condition(skill, skill_modifier))
          except ValueError as v:
            print(str(v))
          combo_conditional_was_processed = True

        if not job_resources_added:
          self.job_resource_tracker.add_resource(curr_time, skill, skill_modifier)

        q_snapshot_and_applications.add(new_priority, event_times.secondary, None, skill, skill_modifier, copy.deepcopy(snapshot_status), event_id, True, job_conditional_was_processed, combo_conditional_was_processed)

      # by default, we apply buffs as the last step of any skill application
      if is_application_time:
        self.se.add_to_status_effects(curr_time, skill, skill_modifier)

    q.sort(key=lambda x: x[0])
    return q