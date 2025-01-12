cmake_minimum_required(VERSION 3.15)
project(MetadataValueTests)

set(CMAKE_CXX_STANDARD 17)
# Aggiungi tutti i file sorgente nella directory src/core
file(GLOB_RECURSE SOURCES src/core/*.cpp)
# Aggiungi il codice sorgente
add_library(MetadataValue ${SOURCES})
target_include_directories(MetadataValue PUBLIC src/core)

# Aggiungi i test
enable_testing()
find_package(yaml-cpp REQUIRED)
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

add_executable(NumericValueTests test/NumericValueTests.cpp)
target_link_libraries(NumericValueTests MetadataValue GTest::gtest_main)
add_test(NumericValueTests NumericValueTests)

add_executable(ListValueTests test/ListValueTests.cpp)
target_link_libraries(ListValueTests MetadataValue GTest::gtest_main)
add_test(ListValueTests ListValueTests)

add_executable(StringValueTests test/StringValueTests.cpp)
target_link_libraries(StringValueTests MetadataValue GTest::gtest_main)
add_test(StringValueTests StringValueTests)

add_executable(ValidationErrorTests test/ValidationErrorTests.cpp)
target_link_libraries(ValidationErrorTests MetadataValue GTest::gtest_main)
add_test(ValidationErrorTests ValidationErrorTests)

add_executable(MetadataValueTests test/MetadataValueTests.cpp)
target_link_libraries(MetadataValueTests MetadataValue GTest::gtest_main)
add_test(MetadataValueTests MetadataValueTests)

add_executable(YamlSerializationTests test/YamlSerializationTests.cpp)
target_link_libraries(YamlSerializationTests MetadataValue yaml-cpp GTest::gtest_main)
add_test(YamlSerializationTests YamlSerializationTests)