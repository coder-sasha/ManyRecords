cmake_minimum_required(VERSION 3.10)

project(MR_QE_PAR LANGUAGES CXX)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Collect all source files
set(SOURCES
    src/main.cpp
)

# Create executable
add_executable(mr-qe-par ${SOURCES})

# Add header file search path
target_include_directories(mr-qe-par
    PRIVATE ${CMAKE_SOURCE_DIR}/include
)

# Optional: output executable to ./bin
set_target_properties(mr-qe-par PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin
)

# Set compiler flags depending on build type
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    message(STATUS "Building in Release mode with -O3")
    target_compile_options(mr-qe-par PRIVATE -O3)
elseif(CMAKE_BUILD_TYPE STREQUAL "Debug")
    message(STATUS "Building in Debug mode with -g -O0")
    target_compile_options(mr-qe-par PRIVATE -g -O0)
else()
    message(WARNING "Unknown or unset CMAKE_BUILD_TYPE: defaulting to Debug")
    target_compile_options(mr-qe PRIVATE -g -O0)
endif()
