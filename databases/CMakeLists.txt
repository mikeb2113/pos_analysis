cmake_minimum_required(VERSION 3.25.0)

project(database_functions LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Arrow REQUIRED)
find_package(Parquet REQUIRED)

add_executable(databases
    database.cpp
)

target_link_libraries(
    databases
    PRIVATE
    Arrow::arrow_static
    Parquet::parquet_static
)