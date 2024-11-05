class AllTest:
    def __init__(self):
        self.__all_test_classes = []

    def register_test_class(self, test_class):
        self.__all_test_classes.append(test_class)

    def run_all(self):
        total_passing = 0
        total_failing = 0
        for test_class in self.__all_test_classes:
            print("Running: {}".format(test_class.__class__.__name__))
            (num_pass, num_fail) = test_class.run_all()
            total_passing += num_pass
            total_failing += num_fail
        print(
            "All tests done. Num passing: {}. Num failing: {}".format(
                total_passing, total_failing
            )
        )
