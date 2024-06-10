from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.timeline_builders.rotation_builder import RotationBuilder


def get_rotation_MCH(skill_library):
    stats = Stats(wd=132, weapon_delay=2.64, main_stat=3376, det_stat=2114,
                  crit_stat=2557, dh_stat=1254, speed_stat=400, job_class='MCH', version="6.55",)
    rotation_name = 'MCH 6.55 Delayed Tools (Extended)'

    rb = RotationBuilder(stats, skill_library, enable_autos=True,
                         ignore_trailing_dots=True, snap_dots_to_server_tick_starting_at=0)
    rb.add_next('Grade 8 Tincture')
    rb.add_next('Heated Split Shot')
    rb.add_next('Gauss Round')
    rb.add_next('Ricochet')
    rb.add_next('Drill')
    rb.add_next('Barrel Stabilizer')
    rb.add_next('Heated Slug Shot')
    rb.add_next('Ricochet')
    rb.add_next('Heated Clean Shot')
    rb.add_next('Reassemble')
    rb.add_next('Gauss Round')
    rb.add_next('Air Anchor')
    rb.add_next('Reassemble')
    rb.add_next('Wildfire')
    rb.add_next('Chain Saw')
    rb.add_next('Automaton Queen')
    rb.add_next('Hypercharge')
    rb.add_next('Heat Blast')
    rb.add_next('Ricochet')
    rb.add_next('Heat Blast')
    rb.add_next('Gauss Round')
    rb.add_next('Heat Blast')
    rb.add_next('Ricochet')
    rb.add_next('Heat Blast')
    rb.add_next('Gauss Round')
    rb.add_next('Heat Blast')
    rb.add_next('Ricochet')
    rb.add_next('Drill')
    rb.add_next('Ricochet')
    rb.add_next('Heated Split Shot')
    rb.add_next('Heated Slug Shot')
    rb.add_next('Heated Clean Shot')
    return (rotation_name, rb)
