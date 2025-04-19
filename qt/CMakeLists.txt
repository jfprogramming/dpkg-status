cmake_minimum_required(VERSION 3.10)
project(dpkg-status)

# Set compiler flags
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

# Qt setup based on version
if(Qt6_VERSION VERSION_GREATER 6.3)
    qt_standard_project_setup()
else()
    set(CMAKE_AUTOUIC ON)
    set(CMAKE_AUTORCC ON)
    set(CMAKE_AUTOMOC ON)
endif()

# Find required Qt modules
find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)

# Add the executable
qt_add_executable(appdpkg-status main.cpp)

# Add Qt resources
qt_add_resources(appdpkg-status "resources"
    PREFIX "/dpkgstatus"
    FILES resource.qrc
)

# Add QML module
qt_add_qml_module(appdpkg-status
    URI dpkgstatus
    VERSION 1.0
    SOURCES dpkgmodeldata.h dpkgmodeldata.cpp
    QML_FILES qml/Main.qml
)

# Link Qt libraries
target_link_libraries(appdpkg-status PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)

# Packaging information
set(CPACK_PACKAGE_NAME "dpkg-status")
set(CPACK_PACKAGE_VERSION "1.0.0")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "A tool for managing dpkg status files")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Jesse Finneamn <jfprogramming@yahoo.com>")
set(CPACK_PACKAGE_HOMEPAGE_URL "https://example.com")
set(CPACK_PACKAGE_LICENSE "MIT")
set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6core6, libqt6gui6, libqt6qml6, python3,
                                  libwayland-client0, libwayland-cursor0, libwayland-egl1,
                                  libxcb-cursor0, libxcb1, libx11-xcb1, libxcb-util1,
                                  libxcb-xkb1, libxkbcommon0, libxkbcommon-x11-0,
                                  libxcb-cursor-dev, binutils,
                                  qml-module-qtquick2, qml-module-qtquick-controls2, qml-module-qtquick-layouts")
set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
include(CPack)

# Enable RPATH handling
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "$ORIGIN/lib")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)

# Prevent CMake from automatically removing RPATH during installation
set(CMAKE_SKIP_RPATH FALSE)
set(CMAKE_SKIP_INSTALL_RPATH FALSE)

message("Binary path: ${CMAKE_BINARY_DIR}/appdpkg-status")
message("QML path: ${CMAKE_SOURCE_DIR}/qml/")
message("RPATH: ${CMAKE_INSTALL_RPATH}")


install(TARGETS appdpkg-status DESTINATION bin)
message(STATUS "Final RPATH for appdpkg-status: ${CMAKE_INSTALL_RPATH}")
install(DIRECTORY ${CMAKE_SOURCE_DIR}/qml/ DESTINATION share/appdpkg-status)
install(FILES ${CMAKE_SOURCE_DIR}/dpkg_status.py DESTINATION share/appdpkg-status
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
)

add_custom_command(
    OUTPUT linuxdeployqt_bundle
    COMMAND linuxdeployqt ${CMAKE_BINARY_DIR}/appdpkg-status
            -qmldir=${CMAKE_SOURCE_DIR}/qml
            -qmake=/opt/Qt/6.7.2/gcc_64/bin/qmake
    DEPENDS appdpkg-status
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running linuxdeployqt to bundle Qt dependencies for .deb"
)

# Add a custom target to trigger the linuxdeployqt step
add_custom_target(bundle ALL
    DEPENDS linuxdeployqt_bundle
)


# Add a custom target to set RPATH after appdpkg-status is built
add_custom_target(set_rpath
    COMMAND patchelf --set-rpath "/opt/Qt/6.7.2/gcc_64/lib:" ${CMAKE_BINARY_DIR}/appdpkg-status
    COMMENT "Setting RPATH for appdpkg-status"
)

# Ensure set_rpath runs after appdpkg-status is built
add_dependencies(set_rpath appdpkg-status)

# Add a custom target for packaging with cpack
add_custom_target(package_with_cpack
    DEPENDS set_rpath
    COMMAND ${CMAKE_COMMAND} -E echo "Starting CPack..."
    COMMAND cpack
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running CPack to generate the package"
    VERBATIM
)

# Add the 'package' target as an alias for 'package_with_cpack'
add_custom_target(custom_package DEPENDS package_with_cpack)
