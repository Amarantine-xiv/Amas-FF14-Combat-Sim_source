from example_rotations.caster.rdm import *
from example_rotations.caster.blm import *
from example_rotations.caster.smn import *

from example_rotations.healer.ast import *
from example_rotations.healer.sge import *
from example_rotations.healer.whm import *
from example_rotations.healer.sch import *

from example_rotations.melee.sam import *
from example_rotations.melee.drg import *
from example_rotations.melee.mnk import *
from example_rotations.melee.rpr import *
from example_rotations.melee.nin import *
from example_rotations.melee.vpr import *

from example_rotations.ranged.dnc import *
from example_rotations.ranged.brd import *
from example_rotations.ranged.mch import *

from example_rotations.tank.war import *
from example_rotations.tank.gnb import *
from example_rotations.tank.pld import *
from example_rotations.tank.drk import *

from example_rotations.get_my_rotations import *


def add_to_rotation_library(rotation_name_and_rb, rotation_library):
    rotation_name, rb = (rotation_name_and_rb)
    if rotation_name in rotation_library:
        print('Updating rotation \"{}\" in the rotation library.'.format(rotation_name))
    rotation_library[rotation_name] = rb


def get_example_rotations(skill_library):
    res = {}
    add_to_rotation_library(get_rotation_WAR(skill_library), res)
    add_to_rotation_library(get_rotation_WAR_extended(skill_library), res)
    add_to_rotation_library(get_rotation_WAR_party_buffs(skill_library), res)
    add_to_rotation_library(get_rotation_GNB(skill_library), res)
    add_to_rotation_library(get_rotation_PLD(skill_library), res)
    add_to_rotation_library(get_rotation_DRK(skill_library), res)
    add_to_rotation_library(get_drk_log_rotation(skill_library), res)

    add_to_rotation_library(get_rotation_AST(skill_library), res)
    add_to_rotation_library(get_rotation_SGE(skill_library), res)
    add_to_rotation_library(get_rotation_WHM(skill_library), res)
    add_to_rotation_library(get_rotation_SCH(skill_library), res)

    add_to_rotation_library(get_rotation_SAM(skill_library), res)
    add_to_rotation_library(get_rotation_SAM_manual(skill_library), res)
    add_to_rotation_library(get_rotation_DRG(skill_library), res)
    add_to_rotation_library(get_rotation_MNK(skill_library), res)
    add_to_rotation_library(get_rotation_RPR(skill_library), res)
    add_to_rotation_library(get_rotation_NIN(skill_library), res)
    
    # hack
    vpr_rot = get_rotation_VPR(skill_library)
    if vpr_rot:
        print('added')
        add_to_rotation_library(vpr_rot, res)

    add_to_rotation_library(get_rotation_DNC(skill_library), res)
    add_to_rotation_library(get_rotation_DNC_extended(skill_library), res)
    add_to_rotation_library(get_rotation_BRD(skill_library), res)
    add_to_rotation_library(get_rotation_MCH(skill_library), res)

    add_to_rotation_library(get_rotation_RDM(skill_library), res)
    add_to_rotation_library(get_rotation_BLM(skill_library), res)
    add_to_rotation_library(get_rotation_SMN(skill_library), res)

    add_to_rotation_library(get_my_rotation(skill_library), res)
    # add_to_rotation_library(get_my_rotation_from_CSV(skill_library), res)    
    return res
