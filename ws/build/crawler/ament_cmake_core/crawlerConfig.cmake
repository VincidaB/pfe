# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_crawler_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED crawler_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(crawler_FOUND FALSE)
  elseif(NOT crawler_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(crawler_FOUND FALSE)
  endif()
  return()
endif()
set(_crawler_CONFIG_INCLUDED TRUE)

# output package information
if(NOT crawler_FIND_QUIETLY)
  message(STATUS "Found crawler: 0.0.0 (${crawler_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'crawler' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${crawler_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(crawler_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${crawler_DIR}/${_extra}")
endforeach()
