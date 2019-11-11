from conans import ConanFile, CMake, tools
import os


class Open62541Conan(ConanFile):
    name = "open62541"
    version = "0.3.0"
    description = "open62541 (http://open62541.org) is an open source and free implementation of OPC UA " \
                  "(OPC Unified Architecture) written in the common subset of the C99 and C++98 languages"
    topics = ("conan", "open62541", "opcua", "iec62541")
    url = "https://github.com/bincrafters/conan-open62541"
    homepage = "https://github.com/open62541/open62541"
    license = "	MPL-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/open62541/open62541"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version),
                  sha256="114fead5ca83a3bf47241f68cad0a1a4f815538584a3ee9fe2c00ebf2bd85c19")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTS"] = False  # example
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "CMakeLists.txt"), "-Werror", "")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["open62541"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("ws2_32")
        self.cpp_info.defines.append("UA_NO_AMALGAMATION")
        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.bindirs.append(self.package_folder)
