#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "skid_drive_controller::skid_drive_controller" for configuration ""
set_property(TARGET skid_drive_controller::skid_drive_controller APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(skid_drive_controller::skid_drive_controller PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libskid_drive_controller.so"
  IMPORTED_SONAME_NOCONFIG "libskid_drive_controller.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS skid_drive_controller::skid_drive_controller )
list(APPEND _IMPORT_CHECK_FILES_FOR_skid_drive_controller::skid_drive_controller "${_IMPORT_PREFIX}/lib/libskid_drive_controller.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
