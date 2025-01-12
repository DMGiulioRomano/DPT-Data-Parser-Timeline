// test/StringValueTests.cpp
#include "MetadataValue.hpp"
#include <gtest/gtest.h>

using namespace dpt::core;

TEST(StringValueTests, SimpleString) {
    StringValue value("hello");
    EXPECT_EQ(value.getValue(), "hello");
    EXPECT_EQ(value.toString(), "hello");
    EXPECT_TRUE(value.validate());
    EXPECT_TRUE(value.isString());
}

TEST(StringValueTests, EmptyString) {
    StringValue value("");
    EXPECT_EQ(value.getValue(), "");
    EXPECT_EQ(value.toString(), "");
    EXPECT_TRUE(value.validate());
    EXPECT_TRUE(value.isString());
}

TEST(StringValueTests, Clone) {
    StringValue original("hello");
    auto clone = original.clone();
    EXPECT_TRUE(clone->isString());
    EXPECT_EQ(static_cast<StringValue*>(clone.get())->getValue(), "hello");
}

TEST(StringValueTests, TypeChecking) {
    StringValue value("hello");
    EXPECT_FALSE(value.isNumeric());
    EXPECT_FALSE(value.isList());
    EXPECT_TRUE(value.isString());
}