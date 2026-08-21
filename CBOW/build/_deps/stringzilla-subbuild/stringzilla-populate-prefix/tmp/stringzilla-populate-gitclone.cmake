
if(NOT "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-subbuild/stringzilla-populate-prefix/src/stringzilla-populate-stamp/stringzilla-populate-gitinfo.txt" IS_NEWER_THAN "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-subbuild/stringzilla-populate-prefix/src/stringzilla-populate-stamp/stringzilla-populate-gitclone-lastrun.txt")
  message(STATUS "Avoiding repeated git clone, stamp file is up to date: '/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-subbuild/stringzilla-populate-prefix/src/stringzilla-populate-stamp/stringzilla-populate-gitclone-lastrun.txt'")
  return()
endif()

execute_process(
  COMMAND ${CMAKE_COMMAND} -E rm -rf "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-src"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to remove directory: '/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-src'")
endif()

# try the clone 3 times in case there is an odd git clone issue
set(error_code 1)
set(number_of_tries 0)
while(error_code AND number_of_tries LESS 3)
  execute_process(
    COMMAND "/usr/bin/git"  clone --no-checkout --config "advice.detachedHead=false" "https://github.com/ashvardanian/StringZilla.git" "stringzilla-src"
    WORKING_DIRECTORY "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps"
    RESULT_VARIABLE error_code
    )
  math(EXPR number_of_tries "${number_of_tries} + 1")
endwhile()
if(number_of_tries GREATER 1)
  message(STATUS "Had to git clone more than once:
          ${number_of_tries} times.")
endif()
if(error_code)
  message(FATAL_ERROR "Failed to clone repository: 'https://github.com/ashvardanian/StringZilla.git'")
endif()

execute_process(
  COMMAND "/usr/bin/git"  checkout 7fed3fb4201a34962cd456a4033bebc5ea09e74e --
  WORKING_DIRECTORY "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-src"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to checkout tag: '7fed3fb4201a34962cd456a4033bebc5ea09e74e'")
endif()

set(init_submodules TRUE)
if(init_submodules)
  execute_process(
    COMMAND "/usr/bin/git"  submodule update --recursive --init 
    WORKING_DIRECTORY "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-src"
    RESULT_VARIABLE error_code
    )
endif()
if(error_code)
  message(FATAL_ERROR "Failed to update submodules in: '/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-src'")
endif()

# Complete success, update the script-last-run stamp file:
#
execute_process(
  COMMAND ${CMAKE_COMMAND} -E copy
    "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-subbuild/stringzilla-populate-prefix/src/stringzilla-populate-stamp/stringzilla-populate-gitinfo.txt"
    "/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-subbuild/stringzilla-populate-prefix/src/stringzilla-populate-stamp/stringzilla-populate-gitclone-lastrun.txt"
  RESULT_VARIABLE error_code
  )
if(error_code)
  message(FATAL_ERROR "Failed to copy script-last-run stamp file: '/home/michael/Desktop/projects/pos_analysis/CBOW/build/_deps/stringzilla-subbuild/stringzilla-populate-prefix/src/stringzilla-populate-stamp/stringzilla-populate-gitclone-lastrun.txt'")
endif()

