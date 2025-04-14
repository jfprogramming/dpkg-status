cmake_minimum_required(VERSION 3.16)

project(dpkg-status VERSION 0.1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# Set the build type to Debug by default
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()


# Find required Qt packages
find_package(Qt6 6.7 REQUIRED COMPONENTS Core Gui Widgets Quick Qml Network DBus)

qt_standard_project_setup(REQUIRES 6.7)

# Add the executable
qt_add_executable(appdpkg-status
    main.cpp
)

qt_add_qml_module(appdpkg-status
    URI dpkgstatus
    VERSION 1.0
    SOURCES
        dpkgmodeldata.h
        dpkgmodeldata.cpp
    QML_FILES
        qml/Main.qml
    RESOURCES
        resource.qrc
)

# Set target properties for bundle/executable
set_target_properties(appdpkg-status PROPERTIES
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

# Link required libraries
target_link_libraries(appdpkg-status
    PRIVATE Qt6::Core
    PRIVATE Qt6::Gui
    PRIVATE Qt6::Widgets
    PRIVATE Qt6::Quick
    PRIVATE Qt6::Qml
    PRIVATE Qt6::Network
    PRIVATE Qt6::DBus
)

# Install the application
include(GNUInstallDirs)
install(TARGETS appdpkg-status
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
