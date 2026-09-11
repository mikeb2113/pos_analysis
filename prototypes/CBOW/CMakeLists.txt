# Set the minimum required CMake version
cmake_minimum_required(VERSION 3.22.1)

# Define your project name and programming language
project(SynonymPrediction LANGUAGES CXX)

# Enforce the modern C++ standard (e.g., C++17)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  stringzilla
  GIT_REPOSITORY https://github.com/ashvardanian/StringZilla.git
  GIT_TAG        7fed3fb4201a34962cd456a4033bebc5ea09e74e # release-v5.1.2^{}
)

FetchContent_MakeAvailable(stringzilla)

# Compile the executable by explicitly listing all .cpp source files
add_executable(synonym_resolution 
    test.cpp 
    synonym_resolution.cpp
)

target_include_directories(
    synonym_resolution
    PRIVATE
    ${stringzilla_SOURCE_DIR}/include
)