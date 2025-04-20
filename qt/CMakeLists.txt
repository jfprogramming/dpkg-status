cmake_minimum_required(VERSION 3.10)
project(dpkg-status)

# Set compiler flags
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Qt setup based on version
if(Qt6_VERSION VERSION_GREATER 6.3)
    qt_standard_project_setup()
else()
    set(CMAKE_AUTOUIC ON)
    set(CMAKE_AUTORCC ON)
    set(CMAKE_AUTOMOC ON)
endif()

# Update to configure the Qt installation path for a specific version
set(CMAKE_PREFIX_PATH "/opt/Qt/6.7.2/gcc_64/lib/cmake")
set(Qt6_DIR "/opt/Qt/6.7.2/gcc_64/lib/cmake/Qt6")

# Find Qt dynamically based on user environment or default paths
find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick PATHS ENV{QTDIR} NO_DEFAULT_PATH)

if(NOT DEFINED ENV{QTDIR})
    message(WARNING "QTDIR environment variable is not set. Trying default paths.")
    find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick HINTS
        "/opt/Qt/6.7.2/gcc_64"
        "/usr/lib/qt6"
        "/usr/local/qt6"
    )
endif()

# Check if Qt6 was found
message(STATUS "Detected Qt Installation Path: ${Qt6_DIR}")
message(STATUS "Using qmake Path: ${QT_QMAKE_PATH}")

if(NOT Qt6_FOUND)
    message(FATAL_ERROR "Qt6 not found! Please set the QTDIR environment variable or install Qt6.")
endif()

# Dynamically determine the qmake path
set(QT_QMAKE_PATH "${Qt6_DIR}/../../../bin/qmake")
message(STATUS "Using qmake Path: ${QT_QMAKE_PATH}")

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
set(CPACK_DEBIAN_PACKAGE_DEPENDS "libqt6core6, libqt6gui6, libqt6qml6, python3, binutils,
                                  qml-module-qtquick2, qml-module-qtquick-controls2,
                                  qml-module-qtquick-layouts")
set(CPACK_PACKAGING_INSTALL_PREFIX "/usr")
include(CPack)

# Enable RPATH handling
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH "/usr/lib/appdpkg-status:/usr/lib/appdpkg-status/platforms")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Output the paths for debugging
message("Binary path: ${CMAKE_BINARY_DIR}/appdpkg-status")
message("QML path: ${CMAKE_SOURCE_DIR}/qml/")
message("RPATH: ${CMAKE_INSTALL_RPATH}")


install(TARGETS appdpkg-status DESTINATION bin)
message(STATUS "Final RPATH for appdpkg-status: ${CMAKE_INSTALL_RPATH}")
install(DIRECTORY ${CMAKE_SOURCE_DIR}/qml/ DESTINATION share/appdpkg-status)
install(FILES ${CMAKE_SOURCE_DIR}/dpkg_status.py DESTINATION share/appdpkg-status
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ
)

# Ensure lib directory is created and installed
install(DIRECTORY ${CMAKE_BINARY_DIR}/lib/
        DESTINATION lib/appdpkg-status
        FILES_MATCHING PATTERN "*.so*")

# Ensure platforms directory is installed with all platform plugins
install(DIRECTORY ${CMAKE_BINARY_DIR}/plugins/platforms/
        DESTINATION lib/appdpkg-status/platforms
        FILES_MATCHING PATTERN "*.so*")

# Install the script as postinst for automatic execution during installation
install(FILES ${CMAKE_SOURCE_DIR}/set-target-env-vars.sh
        DESTINATION DEBIAN
        RENAME postinst
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ)

# Install the script for manual use by the user
install(FILES ${CMAKE_SOURCE_DIR}/set-target-env-vars.sh
        DESTINATION share/appdpkg-status
        PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ)

# Set the postinst script to be executable
set(CPACK_DEBIAN_PACKAGE_CONTROL_EXTRA "${CMAKE_SOURCE_DIR}/postinst")

install(DIRECTORY ${CMAKE_BINARY_DIR}/qml/
        DESTINATION share/appdpkg-status/qml)

# Update linuxdeployqt to bundle plugins explicitly
add_custom_command(
    COMMAND_EXPAND_LISTS
    COMMAND ${CMAKE_COMMAND} -E remove -f ${CMAKE_BINARY_DIR}/qt.conf
    COMMAND ${CMAKE_COMMAND} -E echo "Running Linuxdeployqt to bundle Qt dependencies for .deb"
    OUTPUT linuxdeployqt_bundle
    COMMAND linuxdeployqt ${CMAKE_BINARY_DIR}/appdpkg-status
            -qmldir=${CMAKE_SOURCE_DIR}/qml
            -qmake=${QT_QMAKE_PATH}
            -bundle-non-qt-libs
            -extra-plugins=platforms
    DEPENDS appdpkg-status
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Finished running linuxdeployqt to bundle Qt dependencies for .deb"
)

# Ensure the shell script is copied to the build directory
add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/set-target-env-vars.sh
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/set-target-env-vars.sh ${CMAKE_BINARY_DIR}/set-target-env-vars.sh
    COMMENT "Copying shell script to the build directory for packaging"
)

# Add a target to ensure the shell script is copied during the build process
add_custom_target(copy_shell_script
    DEPENDS ${CMAKE_BINARY_DIR}/set-target-env-vars.sh
)

# Update RPATH and include CPack for packaging
add_custom_target(package_with_cpack
    DEPENDS linuxdeployqt_bundle
    #COMMAND patchelf --set-rpath "/usr/lib/appdpkg-status:/usr/lib/appdpkg-status/platforms/opt/Qt/6.7.2/gcc_64/lib:" ${CMAKE_BINARY_DIR}/appdpkg-status
    COMMAND patchelf --set-rpath "/opt/Qt/6.7.2/gcc_64/lib:" ${CMAKE_BINARY_DIR}/appdpkg-status
    COMMAND ${CMAKE_COMMAND} -E echo "RPATH set to:"
    COMMAND patchelf --print-rpath ${CMAKE_BINARY_DIR}/appdpkg-status
    COMMAND ${CMAKE_COMMAND} -E echo "Starting CPack... ${CMAKE_INSTALL_RPATH}"
    COMMAND cpack
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running CPack to generate the package"
    VERBATIM
)

# Add the 'package' target as an alias for 'package_with_cpack'
add_custom_target(custom_package DEPENDS package_with_cpack)


