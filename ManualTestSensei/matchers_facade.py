from matchers import conditional_test_logic, ambiguous_test, conditional_test_logic, eager_step
from ubuntu_data import UbuntuSmellsData

if __name__ == '__main__':
    tests = UbuntuSmellsData('ubuntu_files.csv') #files.csv contains ubuntu files
    test = tests.by_catalog_index(2)[0]
    eager_step.find(test)
    conditional_test_logic.find(test)
    ambiguous_test.find(test)
    conditional_test_logic.find(test)
    eager_step.find(test)
    print(test.smells)