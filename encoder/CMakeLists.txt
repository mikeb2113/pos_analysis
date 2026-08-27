cmake_minimum_required(VERSION 3.22.1)

project(Encoder LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(FetchContent)

FetchContent_Declare(
    stringzilla
    GIT_REPOSITORY https://github.com/ashvardanian/StringZilla.git
    GIT_TAG 0d4d5c17e483755a178f1322a5311e569eee6451
)

FetchContent_MakeAvailable(stringzilla)

add_executable(encode
    test.cpp
    encoder.cpp
)

target_include_directories(
    encode
    PRIVATE
    ${stringzilla_SOURCE_DIR}/include
)