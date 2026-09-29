cmake_minimum_required(VERSION 3.16)
project(RoadVisionCppCamera LANGUAGES CXX)

find_package(OpenCV REQUIRED)

add_executable(roadvision_cpp_camera
    src/main.cpp
)

target_include_directories(roadvision_cpp_camera PRIVATE ${OpenCV_INCLUDE_DIRS} include)
target_link_libraries(roadvision_cpp_camera PRIVATE ${OpenCV_LIBS})
