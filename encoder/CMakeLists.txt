# Set the minimum required CMake version
cmake_minimum_required(VERSION 3.22.1)

# Define your project name and programming language
project(Encoder LANGUAGES CXX)

# Enforce the modern C++ standard (e.g., C++17)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Compile the executable by explicitly listing all .cpp source files
add_executable(encode
    encoder.cpp
)

target_include_directories(
    encode
    PRIVATE
)