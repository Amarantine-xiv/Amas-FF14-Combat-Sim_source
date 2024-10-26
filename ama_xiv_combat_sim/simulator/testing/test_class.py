class TestClass:
    def __init__(self):
        self.test_fns = []

    @staticmethod
    def is_a_test(f):
        f.__is_a_test__ = True
        return f

    def _get_test_methods(self):
        test_methods = []
        for fn_name in dir(self):
            fn = getattr(self, fn_name)
            if getattr(fn, "__is_a_test__", False):
                test_methods.append(fn)
        return test_methods

    @staticmethod
    def _compare_sets(result, expected):
        test_passed = True
        err_msg = ""
        if len(expected) != len(result):
            test_passed = False
            err_msg += (
                f"Expected {len(expected)} skills returned. Instead got {len(result)}."
            )
            return test_passed, err_msg
        if expected != result:
            test_passed = False
            err_msg += (
                f"Sets are not equal.Expected vs actual: {expected} \n\n {result}"
            )
        return test_passed, err_msg

    @staticmethod
    def _compare_sequential(result, expected, relative_tol=None):
        test_passed = True
        err_msg = ""
        if len(expected) != len(result):
            test_passed = False
            err_msg += f"Expected {len(expected)} skills returned. Instead got {len(result)}. "
            return test_passed, err_msg
        for i, expect in enumerate(expected):
            if relative_tol is None:
                if expect != result[i]:
                    test_passed = False
                    err_msg += f"Position {i} was not the same.\n Expected: {expect}\n Actual: {result[i]}\n"
            else:
                diff = abs(result[i] - expected[i])
                if diff / expected[i] >= relative_tol:
                    test_passed = False
                    err_msg += f"Position {i} was not the same.\n Expected: {expect}\n Actual: {result[i]}\n"
        return test_passed, err_msg

    def print_result(self, passing, failing):
        print(
            f"Testing for {self.__class__.__name__}. {len(passing)}/{len(passing) + len(failing)} tests passed."
        )
        if len(failing) > 0:
            print("Failing tests:")
            for test_info in failing:
                print(f"{test_info[0]}: {test_info[1]}\n")
        print("Passing tests:")
        for test_name in passing:
            print(f"{test_name}")

    def run_single(self, test_name):
        for test_fn in self._get_test_methods():
            if test_name == test_fn.__name__:
                test_passed, err_msg = test_fn()
                if test_passed:
                    print(f"{test_name} passed!")
                    return
                else:
                    print(f"{test_name} failed: {err_msg}")
                    return
        print(f"No test found with name {test_name}")

    def run_all(self, verbose=False):
        passing = []
        failing = []
        for test_fn in self._get_test_methods():
            test_name = test_fn.__name__
            test_passed, err_msg = test_fn()
            if test_passed:
                passing.append(test_name)
            else:
                failing.append((test_name, err_msg))
        if verbose or len(failing) > 0:
            self.print_result(passing, failing)
            print("================")
        return (len(passing), len(failing))
