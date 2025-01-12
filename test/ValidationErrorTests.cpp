// test/ValidationErrorTests.cpp
#include "MetadataValue.hpp"
#include <gtest/gtest.h>

using namespace dpt::core;

TEST(ValidationErrorTests, DefaultMessage) {
    ValidationError error("Invalid value");
    EXPECT_EQ(std::string(error.what()), "Invalid value");
}

TEST(ValidationErrorTests, CustomMessage) {
    ValidationError error("Value out of range");
    EXPECT_EQ(std::string(error.what()), "Value out of range");
}