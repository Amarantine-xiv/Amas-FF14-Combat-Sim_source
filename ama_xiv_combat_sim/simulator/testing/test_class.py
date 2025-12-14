import time


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
                f"Sets are not equal. Expected vs actual: {expected} \n\n {result}"
            )
        return test_passed, err_msg

    @staticmethod
    def _compare_sequential(results, expected, relative_tol=None):
        test_passed = True
        err_msg = ""
        if len(expected) != len(results):
            test_passed = False
            err_msg += f"Expected {len(expected)} skills returned. Instead got {len(results)}. "
        for i in range(max(len(expected), len(results))):
            expect = expected[i] if i < len(expected) else None
            result = results[i] if i < len(results) else None
            invalid_result = expect is None or result is None
            if relative_tol is None:
                if invalid_result or expect != result:
                    test_passed = False
                    err_msg += f"Position {i} was not the same.\n Expected: {expect}\n Actual: {result}\n"
            else:
                if invalid_result or (abs(result - expect) / expect >= relative_tol):
                    test_passed = False
                    err_msg += f"Position {i} was not the same.\n Expected: {expect}\n Actual: {result}\n"
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

    def run_single(self, test_name, show_timing=False):
        for test_fn in self._get_test_methods():
            if test_name == test_fn.__name__:
                t0 = time.time()
                test_passed, err_msg = test_fn()
                if test_passed:
                    print(f"{test_name} passed!")
                else:
                    print(f"{test_name} failed: {err_msg}")
                t1 = time.time()
                if show_timing:
                    print(f"Test '{test_name}' took {t1-t0:.2f}s")
                return
        print(f"No test found with name {test_name}")

    def run_all(self, verbose=False, show_timing=False):
        passing = []
        failing = []
        tot_time = 0
        for test_fn in self._get_test_methods():
            t0 = time.time()
            test_name = test_fn.__name__
            test_passed, err_msg = test_fn()
            if test_passed:
                passing.append(test_name)
            else:
                failing.append((test_name, err_msg))
            t1 = time.time()
            if show_timing:
                print(f"Test '{test_name}' took {t1-t0:.2f}s")
            tot_time += t1 - t0
        if verbose or len(failing) > 0:
            self.print_result(passing, failing)
            print("================")
        if show_timing:
            print(f"total time taken: {tot_time:.2f}s")
        return (len(passing), len(failing))
