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
# set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
set(CMAKE_INSTALL_RPATH "$ORIGIN/lib;/opt/Qt/6.7.2/gcc_64/lib")
# set(CMAKE_INSTALL_RPATH "$ORIGIN/lib")
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)

# Prevent CPack from modifying the RPATH
# set(CPACK_SET_DESTDIR ON)
# set(CPACK_STRIP_FILES OFF)
# set(CPACK_INSTALL_RPATH "$ORIGIN/lib;/opt/Qt/6.7.2/gcc_64/lib")
# set(CPACK_INSTALL_RPATH "$ORIGIN/lib")
# set(CPACK_INSTALL_RPATH_USE_LINK_PATH FALSE)

# Install the Qt libraries bundled by linuxdeployqt
install(DIRECTORY ${CMAKE_BINARY_DIR}/lib/ DESTINATION lib)
install(DIRECTORY ${CMAKE_BINARY_DIR}/lib/ DESTINATION /usr/lib)
# Install the .desktop file
install(FILES ${CMAKE_SOURCE_DIR}/default.desktop DESTINATION share/applications)
# Install the icon
install(FILES ${CMAKE_SOURCE_DIR}/icon.png DESTINATION share/icons/hicolor/64x64/apps)

# Install the Qt QML modules
# install(DIRECTORY /opt/Qt/6.7.2/gcc_64/qml/QtQuick DESTINATION lib/qt/qml)
# install(DIRECTORY /opt/Qt/6.7.2/gcc_64/qml/QtQuick/Controls DESTINATION lib/qt/qml)
# install(DIRECTORY /opt/Qt/6.7.2/gcc_64/qml/QtQuick/Layouts DESTINATION lib/qt/qml)

install(DIRECTORY /opt/Qt/6.7.2/gcc_64/qml/QtQuick
        DESTINATION lib/qt/qml/QtQuick)

install(DIRECTORY /opt/Qt/6.7.2/gcc_64/qml/QtQuick/Controls
        DESTINATION lib/qt/qml/QtQuick/Controls)

install(DIRECTORY /opt/Qt/6.7.2/gcc_64/qml/QtQuick/Layouts
        DESTINATION lib/qt/qml/QtQuick/Layouts)

install(FILES
    /opt/Qt/6.7.2/gcc_64/lib/libQt6QuickControls2Impl.so.6
    DESTINATION lib
)

# Install the application binary and resources
install(TARGETS appdpkg-status DESTINATION bin)
install(DIRECTORY ${CMAKE_SOURCE_DIR}/qml/ DESTINATION share/appdpkg-status)

# Install the Python script to /usr/share/dpkg-status/
install(FILES ${CMAKE_SOURCE_DIR}/dpkg_status.py DESTINATION share/appdpkg-status
    PERMISSIONS OWNER_EXECUTE OWNER_WRITE OWNER_READ GROUP_EXECUTE GROUP_READ WORLD_EXECUTE WORLD_READ)

# Install the Qt platform plugins
install(FILES
    /opt/Qt/6.7.2/gcc_64/plugins/platforms/libqxcb.so
    /opt/Qt/6.7.2/gcc_64/plugins/platforms/libqwayland-generic.so
    DESTINATION lib/qt/plugins/platforms
)

# Install XCB-related libraries
install(FILES
    /lib/x86_64-linux-gnu/libxcb.so.1
    /lib/x86_64-linux-gnu/libxkbcommon.so.0
    /lib/x86_64-linux-gnu/libxkbcommon-x11.so.0
    /lib/x86_64-linux-gnu/libxcb-cursor.so.0
    /lib/x86_64-linux-gnu/libxcb-icccm.so.4
    /lib/x86_64-linux-gnu/libxcb-image.so.0
    /lib/x86_64-linux-gnu/libxcb-keysyms.so.1
    /lib/x86_64-linux-gnu/libxcb-randr.so.0
    /lib/x86_64-linux-gnu/libxcb-render.so.0
    /lib/x86_64-linux-gnu/libxcb-shape.so.0
    /lib/x86_64-linux-gnu/libxcb-shm.so.0
    /lib/x86_64-linux-gnu/libxcb-sync.so.1
    /lib/x86_64-linux-gnu/libxcb-util.so.1
    /lib/x86_64-linux-gnu/libxcb-xfixes.so.0
    /lib/x86_64-linux-gnu/libxcb-xkb.so.1
    /lib/x86_64-linux-gnu/libwayland-client.so.0
    /lib/x86_64-linux-gnu/libwayland-cursor.so.0
    /lib/x86_64-linux-gnu/libwayland-egl.so.1
    DESTINATION lib
)


# install(DIRECTORY /opt/Qt/6.7.2/gcc_64/plugins/platforms DESTINATION lib/qt/plugins)
