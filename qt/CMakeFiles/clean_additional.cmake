# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles/appdpkg-status_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/appdpkg-status_autogen.dir/ParseCache.txt"
  "appdpkg-status_autogen"
  )
endif()
