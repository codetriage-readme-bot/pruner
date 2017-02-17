"""
This CLI tool should be used with the following command:
    plum <requirements_file> <output_file> <test_command>
"""
import os
import subprocess
import sys

class Raisins(object):
    def __init__(self):
        self._loadArgs()
        self._getRequirements()
        self._loadVirtualEnv()
        self._installRequirements()

    def _call(self, *args, **kwargs):

        initial = kwargs.pop('initial', False)
        if not initial:
            with open(os.devnull, "w") as f:
                if isinstance(args[0], list):
                    s = subprocess.call(args[0], stdout=f, stderr=f)
                else:
                    s = subprocess.call(*args, stdout=f, stderr=f, **kwargs)
        else:
            if isinstance(args[0], list):
                s = subprocess.call(args[0])
            else:
                s = subprocess.call(*args, **kwargs)

        return s

    def _cleanUp(self):
        print('PLUM: rm -rf plumtests')
        self._call('rm -rf plumtests', shell=True)

    def run(self):
        # Run initial test to make sure things work as is
        print('PLUM: Running initial test...')
        success = self._runTest(initial=True)
        if success:
            print('PLUM: Initial test was a success, beginning requirement tests...')
        else:
            print('PLUM: Initial test was a failure, we cannot tell why, cleaning and exiting...')
            self._cleanUp()

        for r in self.requirements.keys():
            print('PLUM: Testing {}'.format(r))
            # Uninstall the requirement
            self._call(['pip', 'uninstall', '-y', r])
            # Run the test
            success = self._runTest()
            # Was the test successful?
            if success:
                print('PLUM: {} was not needed'.format(r))
                self.requirements[r] = False
            else:
                print('PLUM: {} was needed'.format(r))
            # Reinstall the req so that it doesn't change the other reqs results
            self._call(['pip', 'install', r])

        # Kill the virtualenv
        self._cleanUp()

        # Output the results
        print('PLUM: Writing results to {}'.format(self.outputFile))
        with open(self.outputFile, 'w') as f:
            for r in self.requirements.keys():
                if not self.requirements[r]:
                    f.write(r + '\n')
        print('PLUM: DONE')

    def _loadArgs(self):
        self.args = sys.argv
        self.reqFile = self.args[1]
        self.outputFile = self.args[2]
        self.testCommand = self.args[3:]

    def _getRequirements(self):
        self.requirements = {r.strip(): True for r in open(self.reqFile, mode='r')}

    def _loadVirtualEnv(self):
        print('PLUM: virtualenv plumtests')
        self._call('virtualenv plumtests', shell=True)
        print('PLUM: source plumtests/bin/activate')
        self._call('source plumtests/bin/activate', shell=True)

    def _installRequirements(self):
        # For the initial install we can just use the initial requirements file
        print('PLUM: pip install -r {}'.format(self.reqFile))
        self._call(['pip', 'install', '-r', self.reqFile])

    def _runTest(self, initial=False):
        return not bool(self._call(self.testCommand, initial=initial))


def main():
    r = Raisins()
    r.run()


if __name__ == '__main__': main()