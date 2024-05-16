# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)
set(PICO_SDK_PATH "D:/Tools/pico/pico-sdk")

set(PICO_BOARD pico_w CACHE STRING "Board type")
set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type")
# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.4.0")
  message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.4.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

project(linefollow C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

add_executable(linefollow linefollow.c)

pico_set_program_name(linefollow "linefollow")
pico_set_program_version(linefollow "0.1")

pico_enable_stdio_uart(linefollow 0)
pico_enable_stdio_usb(linefollow 1)

add_library(motor_driver motor_driver.c)
target_link_libraries(motor_driver hardware_gpio hardware_clocks hardware_pwm)
# Add the standard library to the build
target_link_libraries(linefollow
        pico_stdlib  motor_driver pico_bootsel_via_double_reset pico_double)
target_compile_options(linefollow PRIVATE -Wall)
# Add the standard include files to the build
target_include_directories(linefollow PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/..
  ${PROJECT_SOURCE_DIR} # for our common lwipopts or any other standard includes, if required
)

pico_add_extra_outputs(linefollow)

