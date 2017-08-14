from conans.model import Generator
from conans import ConanFile

class AdvancedVisualStudio(Generator):
    @property
    def filename(self):
        pass

    @property
    def content(self):
        result = { # filename: content map
            'conanbuildinfo.props': self._gen_props().replace("\\", "\\\\"),
            'conanbuildinfo.xml': self._gen_xml(),
            'conanbuildinfo.bat': self._gen_bat()
        }
        return result

    def _gen_bat(self):
        template = '''{rootdir_items}'''
        fields = {
            'rootdir_items': self._format_rootdir_items_bat(),
        }
        return template.format(**fields)

    def _gen_xml(self):
        template = '''<?xml version="1.0" encoding="utf-8"?>
<ProjectSchemaDefinitions xmlns="http://schemas.microsoft.com/build/2009/properties" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" xmlns:sys="clr-namespace:System;assembly=mscorlib">

  <Rule Name="ConanDependencies"
        DisplayName="Conan Dependencies"
        PageTemplate="tool"
        Description="Settings for Conan Dependencies"
        Order="300"
        xmlns="http://schemas.microsoft.com/build/2009/properties">

    <Rule.Categories>
{categories}    </Rule.Categories>

    <Rule.DataSource>
      <DataSource Persistence="ProjectFile" />
    </Rule.DataSource>
{properties}
  </Rule>
</ProjectSchemaDefinitions>
'''
        fields = {
            'categories': self._format_category_items(),
            'properties': self._format_property_items(),
        }
        return template.format(**fields)

    def _format_category_items(self):
        category_item_template = '''      <Category Name="{name}" DisplayName="{display_name}"/>
'''
        sections = []
        for name, cpp_info in self.deps_build_info.dependencies:
            if name == 'AdvancedVisualStudioGenerator':
                continue
            fields = { 
                'name': name.upper().replace('.', '-'),
                'display_name': name
            }
            section = category_item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _format_property_items(self):
        property_item_template = '''
    <BoolProperty Name="USES_{name}_BINARIES" DisplayName="Use binaries" Category="{name}"/>
    <BoolProperty Name="USES_{name}_COMPILE" DisplayName="Use compile" Category="{name}"/>
    <BoolProperty Name="USES_{name}_LINK" DisplayName="Use link" Category="{name}"/>
'''
        sections = []
        for name, cpp_info in self.deps_build_info.dependencies:
            if name == 'AdvancedVisualStudioGenerator':
                continue
            fields = {
                'name': name.upper().replace('.', '-'),
                'display_name': name
            }
            section = property_item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _gen_props(self):
        template = '''<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <PropertyPageSchema Include="$(MSBuildThisFileDirectory)conanbuildinfo.xml" >
      <Context>Project</Context>
    </PropertyPageSchema>
  </ItemGroup>

  <PropertyGroup>{uses_items}</PropertyGroup>

  <ImportGroup Label="PropertySheets" />
  <PropertyGroup Label="UserMacros" />
  <PropertyGroup Label="Conan-RootDirs">{rootdir_items}
  </PropertyGroup>
  
  {conditional_property_items}
</Project>'''

        fields = {
            'uses_items': self._format_uses_items(),
            'rootdir_items': self._format_rootdir_items_props(),
            'conditional_property_items': self._format_conditional_properties_items()
        }
        return template.format(**fields)


    def _format_uses_items(self):
        uses_item_template = '''
    <USES_{name}_BINARIES>false</USES_{name}_BINARIES>
    <USES_{name}_COMPILE>false</USES_{name}_COMPILE>
    <USES_{name}_LINK>false</USES_{name}_LINK>
'''
        sections = []
        for name, cpp_info in self.deps_build_info.dependencies:
            if name == 'AdvancedVisualStudioGenerator':
                continue
            fields = { 
                'name': name.upper().replace('.', '-')
            }
            section = uses_item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _format_rootdir_items_props(self):
        rootdir_item_template = '''
    <Conan-{name}-Root>{rootdir}</Conan-{name}-Root>'''
        sections = []
        for name, cpp_info in self.deps_build_info.dependencies:
            if name == 'AdvancedVisualStudioGenerator':
                continue
            fields = { 
                'rootdir': cpp_info.rootpath,
                'name': name.replace('.', '-')
            }
            section = rootdir_item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _format_rootdir_items_bat(self):
        rootdir_item_template = '''
    set Conan-{name}-Root={rootdir}'''
        sections = []
        for name, cpp_info in self.deps_build_info.dependencies:
            if name == 'AdvancedVisualStudioGenerator':
                continue
            fields = { 
                'rootdir': cpp_info.rootpath.replace('/', '\\'),
                'name': name.replace('.', '-')
            }
            section = rootdir_item_template.format(**fields)
            sections.append(section)
        return "".join(sections)

    def _format_conditional_properties_items(self):
        sections = []
        for name, cpp_info in self.deps_build_info.dependencies:
            if name == 'AdvancedVisualStudioGenerator':
                continue
            sections.append(self._format_conditional_binaries(name, cpp_info))
            sections.append(self._format_conditional_compile(name, cpp_info))
            sections.append(self._format_conditional_link(name, cpp_info))
        return "".join(sections)

    def _format_conditional_binaries(self, name, cpp_info):
        template = '''<PropertyGroup Condition="'$(USES_{name}_BINARIES)'">
    <ExecutablePath>{exec_paths}$(ExecutablePath)</ExecutablePath>
  </PropertyGroup>
'''
        fields = {
            'name': name.upper().replace('.', '-'),
            'exec_paths': "".join("%s;" % p for p in cpp_info.bin_paths)
        }
        return template.format(**fields)

    def _format_conditional_compile(self, name, cpp_info):
        template = '''  <ItemDefinitionGroup Condition="'$(USES_{name}_COMPILE)'">
    <ClCompile>
      <AdditionalIncludeDirectories>{include_paths}%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <PreprocessorDefinitions>{defines}%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <AdditionalOptions>{cflags}{cppflags}%(AdditionalOptions)</AdditionalOptions>
    </ClCompile>
  </ItemDefinitionGroup>
'''
        fields = {
            'name': name.upper().replace('.', '-'),
            'include_paths': "".join("%s;" % p for p in cpp_info.include_paths),
            'defines': "".join("%s;" % p for p in cpp_info.defines),
            'cflags': "".join("%s;" % p for p in cpp_info.cflags),
            'cppflags': "".join("%s;" % p for p in cpp_info.cppflags),
        }
        return template.format(**fields)

    def _format_conditional_link(self, name, cpp_info):
        template = '''  <ItemDefinitionGroup Condition="'$(USES_{name}_LINK)'">
    <Link>
      <AdditionalLibraryDirectories>{lib_paths}%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
      <AdditionalDependencies>{libs}%(AdditionalDependencies)</AdditionalDependencies>
      <AdditionalOptions>{flags}%(AdditionalOptions)</AdditionalOptions>
    </Link>
  </ItemDefinitionGroup>
'''
        fields = {
            'name': name.upper().replace('.', '-'),
            'lib_paths': "".join("%s;" % p for p in cpp_info.lib_paths),
            'libs': "".join(["%s.lib;" % p if not p.endswith(".lib")
                                           else "%s;" % p for p in cpp_info.libs]),
            'flags': "".join("%s;" % p for p in cpp_info.sharedlinkflags),
        }
        return template.format(**fields)

class AdvancedVisualStudioGeneratorPackage(ConanFile):
    name = 'AdvancedVisualStudioGenerator'
    version = '0.0.1'
    url = 'http://example.com'
    license = 'MIT'
    description = 'Advanced Visual Studio Generator'
    settings = []
    generator = []

    def configure(self):
        self.settings.clear()
        self.options.remove('static')

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.include_dirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
