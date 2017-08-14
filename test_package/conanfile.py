from conans import ConanFile
import os

class AdvancedVisualStudioGeneratorTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    generators = 'AdvancedVisualStudio'

    def build(self):
        pass

    def test(self):
        pass
