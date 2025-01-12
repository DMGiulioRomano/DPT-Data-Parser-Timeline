// test/ListValueTests.cpp
#include "MetadataValue.hpp"
#include <gtest/gtest.h>

using namespace dpt::core;

TEST(ListValueTests, EmptyList) {
    ListValue value({});
    EXPECT_EQ(value.toString(), "[]");
    EXPECT_TRUE(value.validate());
    EXPECT_TRUE(value.isList());
    EXPECT_EQ(value.size(), 0);
}

TEST(ListValueTests, IntegerList) {
    ListValue value({std::make_shared<NumericValue>(1), std::make_shared<NumericValue>(2)});
    EXPECT_EQ(value.toString(), "[1, 2]");
    EXPECT_TRUE(value.validate());
    EXPECT_TRUE(value.isList());
    EXPECT_EQ(value.size(), 2);
}

TEST(ListValueTests, Clone) {
    ListValue original({std::make_shared<NumericValue>(1), std::make_shared<NumericValue>(2)});
    auto clone = original.clone();
    EXPECT_TRUE(clone->isList());
    EXPECT_EQ(clone->toString(), "[1, 2]");
}

TEST(ListValueTests, Append) {
    ListValue value({std::make_shared<NumericValue>(1)});
    value.append(std::make_shared<NumericValue>(2));
    EXPECT_EQ(value.toString(), "[1, 2]");
    EXPECT_EQ(value.size(), 2);
}

TEST(ListValueTests, InvalidList) {
    ListValue value({std::make_shared<NumericValue>(1), nullptr});
    EXPECT_FALSE(value.validate());
}

TEST(ListValueTests, MixedTypeList) {
    ListValue value({
        std::make_shared<NumericValue>(1),
        std::make_shared<StringValue>("hello")
    });
    EXPECT_EQ(value.toString(), "[1, hello]");
    EXPECT_TRUE(value.validate());
    EXPECT_EQ(value.size(), 2);
}

TEST(ListValueTests, AppendInvalidValue) {
    ListValue value({std::make_shared<NumericValue>(1)});
    EXPECT_THROW(value.append(nullptr), ValidationError);
}

TEST(ListValueTests, TypeChecking) {
    ListValue value({});
    EXPECT_FALSE(value.isNumeric());
    EXPECT_TRUE(value.isList());
    EXPECT_FALSE(value.isString());
}