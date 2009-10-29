import unittest
import rpy2test

def run():
    loader = unittest.TestLoader()
    suite  = loader.loadTestsFromModule(rpy2test)
    runner = unittest.TextTestRunner()
    runner.run(suite)
        
        
if __name__ == '__main__':
    run()