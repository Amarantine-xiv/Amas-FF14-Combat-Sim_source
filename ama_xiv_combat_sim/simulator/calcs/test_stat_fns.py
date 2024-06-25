import pytest

from ama_xiv_combat_sim.simulator.calcs.stat_fns import StatFns

TEST_DATA = {
    'fAP': {
        'Test 1 - No tank': {
            'args': [390],
            'kwargs': {'is_tank': False},
            'expected': 100,
        },
        'Test 2 - No tank': {
            'args': [699],
            'kwargs': {'is_tank': False},
            'expected': 254,
        },
        'Test 3 - No tank': {
            'args': [1219],
            'kwargs': {'is_tank': False},
            'expected': 514
        },
        'Test 1 - Tank': {
            'args': [390],
            'kwargs': {'is_tank': True},
            'expected': 100,
        },
        'Test 2 - Tank': {
            'args': [699],
            'kwargs': {'is_tank': True},
            'expected': 223,
        },
        'Test 3 - Tank': {
            'args': [1219],
            'kwargs': {'is_tank': True},
            'expected': 431
        }
    },
    'fAuto': {
        'Test 1': {
            'args': [120, 3.44, 105],
            'expected': 183,
        },
        'Test 2': {
            'args': [126, 2.6, 115],
            'expected': 147,
        },
    },
    'fDet': {
        'Test 1': {
            'args': [390],
            'expected': 1000,
        },
        'Test 2': {
            'args': [566],
            'expected': 1012,
        },
        'Test 3': {
            'args': [567],
            'expected': 1013,
        },
        'Test 4': {
            'args': [1706],
            'expected': 1096,
        },
        'Test 5': {
            'args': [1707],
            'expected': 1097,
        },
        'Test 6': {
            'args': [1708],
            'expected': 1097,
        },
    },
    'fDetDH': {
        'Test 1': {
            'args': [390, 400],
            'expected': 1000,
        },
        'Test 2': {
            'args': [1706, 1360],
            'expected': 1096+70,
        },
        'Test 3': {
            'args': [1707, 1369],
            'expected': 1097 + 71,
        },
    },
    'fSpd': {
        'Test 1': {
            'args': [859],
            'expected': 1031,
        },
        'Test 2': {
            'args': [1700],
            'expected': 1088,
        },
    },
    'fTnc': {
        'Test 1': {
            'args': [751],
            'expected': 1018,
        },
        'Test 2': {
            'args': [1100],
            'expected': 1036,
        },
        'Test 3': {
            'args': [500],
            'expected': 1005,
        }
    },
    'fWD': {
        'Test 1': {
            'args': [120, 100],
            'expected': 159,
        },
        'Test 2': {
            'args': [126, 115],
            'expected': 170,
        },
    },
    'get_crit_stats': {
        'Test 1': {
            'args': [400],
            'expected': (0.05, 0.40),
        },
        'Test 2': {
            'args': [475],
            'expected': (0.057, 0.407),
        },
        'Test 3': {
            'args': [476],
            'expected': (0.058, 0.408),
        },
        'Test 4': {
            'args': [1150],
            'expected': (0.128, 0.478),
        },
        'Test 5': {
            'args': [1151],
            'expected': (0.129, 0.479),
        },
        'Test 6': {
            'args': [1152],
            'expected': (0.129, 0.479),
        },
    },
    'get_dh_rate': {
        'Test 1': {
            'args': [400],
            'expected': 0,
        },
        'Test 2': {
            'args': [472],
            'expected': 0.020,
        },
        'Test 3': {
            'args': [473],
            'expected': 0.021,
        },
        'Test 4': {
            'args': [1360],
            'expected': 0.277,
        },
        'Test 5': {
            'args': [1361],
            'expected': 0.278,
        },
        'Test 6': {
            'args': [1362],
            'expected': 0.278,
        },
    },
    'get_time_using_speed_stat': {
        'Test 1': {
            'args': [2500, 1408],
            'expected': 2330,
        },
        'Test 2': {
            'args': [2500, 1409],
            'expected': 2320,
        },
        'Test 3': {
            'args': [2500, 1410],
            'expected': 2320,
        },
        'Test 4': {
            'args': [3500, 999],
            'expected': 3360,
        },
        'Test 5': {
            'args': [3500, 1000],
            'expected': 3350,
        },
        'Test 6': {
            'args': [3500, 1001],
            'expected': 3350,
        },
    },
}


def _run_function_test(test: dict, function: callable) -> None:
    """Runs a test case against the specified function."""
    expected = test.get('expected')
    args = test.get('args') or []
    kwargs = test.get('kwargs') or {}
    result = function(*args, **kwargs)
    assert result == expected, f'Expected: {expected}. Actual: {result}'


@pytest.mark.parametrize('test', TEST_DATA['fAP'].values(), ids=TEST_DATA['fAP'])
def test_statfns_fap(test: dict):
    _run_function_test(test, StatFns.fAP)


@pytest.mark.parametrize('test', TEST_DATA['fAuto'].values(), ids=TEST_DATA['fAuto'])
def test_statfns_fauto(test: dict):
    _run_function_test(test, StatFns.fAuto)


@pytest.mark.parametrize('test', TEST_DATA['fDet'].values(), ids=TEST_DATA['fDet'])
def test_statfns_fdet(test: dict):
    _run_function_test(test, StatFns.fDet)


@pytest.mark.parametrize('test', TEST_DATA['fDetDH'].values(), ids=TEST_DATA['fDetDH'])
def test_statfns_fdetdh(test: dict):
    _run_function_test(test, StatFns.fDetDH)


@pytest.mark.parametrize('test', TEST_DATA['fSpd'].values(), ids=TEST_DATA['fSpd'])
def test_statfns_fspd(test: dict):
    _run_function_test(test, StatFns.fSpd)


@pytest.mark.parametrize('test', TEST_DATA['fTnc'].values(), ids=TEST_DATA['fTnc'])
def test_statfns_ftnc(test: dict):
    _run_function_test(test, StatFns.fTnc)


@pytest.mark.parametrize('test', TEST_DATA['fWD'].values(), ids=TEST_DATA['fWD'])
def test_statfns_fwd(test: dict):
    _run_function_test(test, StatFns.fWD)


@pytest.mark.parametrize('test', TEST_DATA['get_dh_rate'].values(), ids=TEST_DATA['get_dh_rate'])
def test_statfns_get_dh_rate(test: dict):
    _run_function_test(test, StatFns.get_dh_rate)


@pytest.mark.parametrize('test', TEST_DATA['get_crit_stats'].values(), ids=TEST_DATA['get_crit_stats'])
def test_statfns_get_crit_stats(test: dict):
    _run_function_test(test, StatFns.get_crit_stats)


@pytest.mark.parametrize('test', TEST_DATA['get_time_using_speed_stat'].values(), ids=TEST_DATA['get_time_using_speed_stat'])
def test_statfns_get_time_using_speed_stat(test: dict):
    _run_function_test(test, StatFns.get_time_using_speed_stat)
