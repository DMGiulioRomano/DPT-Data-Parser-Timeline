// test/MetadataValueTests.cpp
#include "MetadataValue.hpp"
#include <gtest/gtest.h>

using namespace dpt::core;

TEST(MetadataValueTests, DefaultImplementations) {
    class TestValue : public MetadataValue {
    public:
        std::string toString() const override { return ""; }
        MetadataPtr clone() const override { return nullptr; }
        bool validate() const override { return true; }
    };

    TestValue value;
    EXPECT_FALSE(value.isNumeric());
    EXPECT_FALSE(value.isList());
    EXPECT_FALSE(value.isString());
}