// test/NumericValueTests.cpp
#include "MetadataValue.hpp"
#include <gtest/gtest.h>

using namespace dpt::core;

TEST(NumericValueTests, IntegerValue) {
    NumericValue value(42);
    EXPECT_EQ(value.getValue<int>(), 42);
    EXPECT_EQ(value.toString(), "42");
    EXPECT_TRUE(value.validate());
    EXPECT_TRUE(value.isNumeric());
}

TEST(NumericValueTests, DoubleValue) {
    NumericValue value(3.14);
    EXPECT_DOUBLE_EQ(value.getValue<double>(), 3.14);
    EXPECT_EQ(value.toString(), "3.14");
    EXPECT_TRUE(value.validate());
    EXPECT_TRUE(value.isNumeric());
}

TEST(NumericValueTests, Clone) {
    NumericValue original(42);
    auto clone = original.clone();
    EXPECT_TRUE(clone->isNumeric());
    EXPECT_EQ(static_cast<NumericValue*>(clone.get())->getValue<int>(), 42);
}

TEST(NumericValueTests, InvalidValue) {
    NumericValue value(std::nan(""));
    EXPECT_FALSE(value.validate());
}

TEST(NumericValueTests, TypeChecking) {
    NumericValue intValue(42);
    EXPECT_TRUE(intValue.isNumeric());
    EXPECT_FALSE(intValue.isList());
    EXPECT_FALSE(intValue.isString());

    NumericValue doubleValue(3.14);
    EXPECT_TRUE(doubleValue.isNumeric());
    EXPECT_FALSE(doubleValue.isList());
    EXPECT_FALSE(doubleValue.isString());
}