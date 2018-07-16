#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class LibnameConan(ConanFile):
    name = "m4"
    version = "1.4.18"
    description = "GNU M4 is an implementation of the traditional Unix macro processor."
    url = "https://github.com/helmesjo/conan-m4"
    homepage = "https://www.gnu.org/software/m4/m4.html"
    author = "helmesjo <helmesjo@gmail.com>"
    # Indicates License type of the packaged library
    license = "GPL"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"fPIC": [True, False]}
    default_options = "fPIC=True"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    # Update 2/9/18 - Per conan team, ranges are slow to resolve.
    # So, with libs like zlib, updates are very rare, so we now use static version


    requires = ()

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        
        source_url = "http://ftp.gnu.org/gnu/m4/"
        tools.get("{0}/m4-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        
        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            if self.settings.os != 'Windows':
                env_build.fpic = self.options.fPIC
            env_build.configure()
            env_build.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        
        with tools.chdir(self.source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.install()

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))