cmake_minimum_required(VERSION 2.8.3)

project(hello)

find_package(catkin REQUIRED COMPONENTS roscpp)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

## Declare a cpp executable
add_executable(hello node/hello.cpp)

## Specify libraries to link a library or executable target against
target_link_libraries(hello ${catkin_LIBRARIES})