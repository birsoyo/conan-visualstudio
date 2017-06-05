from conans import ConanFile
import os

channel = os.getenv('CONAN_CHANNEL', 'testing')
username = os.getenv('CONAN_USERNAME', 'orhun')

class AdvancedVisualStudioGeneratorTestConan(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    requires = f'AdvancedVisualStudioGenerator/0.0.1@{username}/{channel}'
    generators = 'AdvancedVisualStudio'

    def build(self):
        pass

    def test(self):
        pass
