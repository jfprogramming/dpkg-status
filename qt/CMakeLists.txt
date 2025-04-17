cmake_minimum_required(VERSION 3.10)
project(dpkg-status)

# Set compiler flags
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

# Set the CMake module path to find Qt modules
if(Qt6_VERSION VERSION_GREATER 6.3)
    qt_standard_project_setup()
else()
    # Fall back for older Qt versions
    set(CMAKE_AUTOUIC ON)
    set(CMAKE_AUTORCC ON)
    set(CMAKE_AUTOMOC ON)
endif()

# Find required Qt modules
find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)


# Add the executable
qt_add_executable(appdpkg-status
    main.cpp
)

# Add Qt resources
qt_add_resources(appdpkg-status "resources"
    PREFIX "/dpkgstatus"
    FILES
        resource.qrc
)

# Add QML module
qt_add_qml_module(appdpkg-status
    URI dpkgstatus
    VERSION 1.0
    SOURCES
        dpkgmodeldata.h
        dpkgmodeldata.cpp
    QML_FILES
        qml/Main.qml
)

# Link Qt libraries
target_link_libraries(appdpkg-status PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
)

# Packaging information
set(CPACK_PACKAGE_NAME "dpkg-status")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A tool for managing dpkg status files")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Jesse Finneamn <jfprogramming@yahoo.com>")
set(CPACK_PACKAGE_HOMEPAGE_URL "https://example.com")
set(CPACK_PACKAGE_LICENSE "MIT")
set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6core6, libqt6gui6, libqt6qml6, python3")
set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
include(CPack)

# Install the application binary and resources
install(TARGETS appdpkg-status DESTINATION bin)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/qml DESTINATION share/appdpkg-status)
# Install the Python script to /usr/share/dpkg-status/
install(FILES ${CMAKE_SOURCE_DIR}/dpkg_status.py DESTINATION share/appdpkg-status
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ)
