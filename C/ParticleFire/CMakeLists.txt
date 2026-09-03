cmake_minimum_required(VERSION 3.20)
project(pixelfire C)


# Create an option to switch between a system sdl library and a vendored SDL library
option(MYGAME_VENDORED "Use vendored libraries" OFF)


if(MYGAME_VENDORED)
    FetchContent_Declare(
        SDL3
        GIT_REPOSITORY https://github.com/libsdl-org/SDL.git
        GIT_TAG release-3.2.0
    )

    FetchContent_MakeAvailable(SDL3)
else()
    find_package(SDL3 REQUIRED CONFIG REQUIRED COMPONENTS SDL3-shared)
endif()

include(FetchContent)


add_executable(pixelfire
    main.c
    graphics.c
    hslrgb.c
    swarm.c
)

# Default to Release mode unless user specifies otherwise
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
endif()

target_link_libraries(pixelfire PRIVATE SDL3::SDL3)

if(UNIX AND NOT APPLE)
    target_link_libraries(pixelfire PRIVATE m)
endif()