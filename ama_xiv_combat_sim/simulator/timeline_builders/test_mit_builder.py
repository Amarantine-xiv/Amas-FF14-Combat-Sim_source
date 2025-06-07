from ama_xiv_combat_sim.simulator.calcs.forced_crit_or_dh import ForcedCritOrDH
from ama_xiv_combat_sim.simulator.calcs.damage_class import DamageClass
from ama_xiv_combat_sim.simulator.skills.skill_modifier import SkillModifier
from ama_xiv_combat_sim.simulator.sim_consts import SimConsts
from ama_xiv_combat_sim.simulator.stats import Stats
from ama_xiv_combat_sim.simulator.testing.test_class import TestClass
from ama_xiv_combat_sim.simulator.testing.create_test_skill_library import (
    create_test_skill_library,
)
from ama_xiv_combat_sim.simulator.timeline_builders.snapshot_and_application_events import (
    SnapshotAndApplicationEvents,
)

from ama_xiv_combat_sim.simulator.timeline_builders.mit_builder import (
    MitBuilder,
)

from ama_xiv_combat_sim.simulator.utils import Utils


class TestMitBuilder(TestClass):
    def __init__(self):
        super().__init__()
        self.__stats = Stats(
            wd=126,
            weapon_delay=3.44,
            main_stat=2945,
            det_stat=1620,
            crit_stat=2377,
            dh_stat=1048,
            speed_stat=708,
            job_class="test_job",
            version="test",
        )
        self.__skill_library = create_test_skill_library()

    @TestClass.is_a_test
    def test_basic_mit(self):
        mb = MitBuilder(
            self.__stats
        )
        
        rb_result = SnapshotAndApplicationEvents()
        rb_result.add(
            0,
            0,
            0,
            self.__skill_library.get_skill("test_damage_mit_generic_buff", "test_job"),
            SkillModifier(),
            [True, True],
        )
        #this should get filtered
        rb_result.add(
            Utils.transform_time_to_prio(500),
            500,
            500,
            self.__skill_library.get_skill("test_ogcd", "test_job"),
            SkillModifier(),
            [True, True],
        )
        rb_result.add(
            Utils.transform_time_to_prio(1000),
            1000,
            1000,
            self.__skill_library.get_skill("test_damage_mit_split_buff", "test_job"),
            SkillModifier(),
            [True, True],
        )
        
        result = mb.get_mit_windows(rb_result)        
        expected = [
            (
                0,
                30000,
                self.__skill_library.get_skill("test_damage_mit_generic_buff", "test_job"),                
                (SimConsts.DEFAULT_TARGET,),
            ),
            (
                1000,
                31000,
                self.__skill_library.get_skill("test_damage_mit_split_buff", "test_job"),                
                (SimConsts.DEFAULT_TARGET,),
            ),
        ]

        return self._compare_sequential(result, expected)