# conan-visualstudio

This is an experimental conan generator for visual studio.

One could select different set of dependencies for each project listed in the conan file.

* Run `conan test_package user` so that the generator is installed.
* Copy Conan.props to your project. It should be added to source control.
* Add Conan.props to all the projects in your solution.
* Create a conanfile.txt next to where your solution file is.
* Rebuild your solution.
* Close solution and reopen it. (VS 2017 might require a restart).
* There should be a [Conan Dependencies](images/conan-property-pages.png) section in project properties.
