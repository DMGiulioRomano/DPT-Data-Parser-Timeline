// test/YamlSerializationTests.cpp
#include "YamlSerialization.hpp"
#include <gtest/gtest.h>

using namespace dpt::core;

TEST(YamlSerializationTests, SerializeNumericInt) {
    auto value = std::make_shared<NumericValue>(42);
    YAML::Node node = serialize(value);
    EXPECT_EQ(node.as<int>(), 42);
}

TEST(YamlSerializationTests, SerializeNumericDouble) {
    auto value = std::make_shared<NumericValue>(3.14);
    YAML::Node node = serialize(value);
    EXPECT_DOUBLE_EQ(node.as<double>(), 3.14);
}

TEST(YamlSerializationTests, SerializeList) {
    auto value = std::make_shared<ListValue>(ListValue::ValueType{
        std::make_shared<NumericValue>(1),
        std::make_shared<NumericValue>(2),
        std::make_shared<NumericValue>(3)
    });
    YAML::Node node = serialize(value);
    EXPECT_EQ(node.size(), 3);
    EXPECT_EQ(node[0].as<int>(), 1);
    EXPECT_EQ(node[1].as<int>(), 2);
    EXPECT_EQ(node[2].as<int>(), 3);
}

TEST(YamlSerializationTests, SerializeString) {
    auto value = std::make_shared<StringValue>("hello");
    YAML::Node node = serialize(value);
    EXPECT_EQ(node.as<std::string>(), "hello");
}

TEST(YamlSerializationTests, DeserializeInt) {
    YAML::Node node = YAML::Load("42");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isNumeric());
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(value)->getValue<int>(), 42);
}

TEST(YamlSerializationTests, DeserializeDouble) {
    YAML::Node node = YAML::Load("3.14");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isNumeric());
    EXPECT_DOUBLE_EQ(std::dynamic_pointer_cast<NumericValue>(value)->getValue<double>(), 3.14);
}

TEST(YamlSerializationTests, DeserializeList) {
    YAML::Node node = YAML::Load("[1, 2, 3]");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isList());
    auto list = std::dynamic_pointer_cast<ListValue>(value);
    EXPECT_EQ(list->size(), 3);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(list->getValues()[0])->getValue<int>(), 1);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(list->getValues()[1])->getValue<int>(), 2);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(list->getValues()[2])->getValue<int>(), 3);
}

TEST(YamlSerializationTests, DeserializeString) {
    YAML::Node node = YAML::Load("\"hello\"");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isString());
    EXPECT_EQ(std::dynamic_pointer_cast<StringValue>(value)->getValue(), "hello");
}


TEST(YamlSerializationTests, SerializeUnsupportedType) {
    class UnsupportedValue : public MetadataValue {
    public:
        std::string toString() const override { return ""; }
        MetadataPtr clone() const override { return nullptr; }
        bool validate() const override { return true; }
    };

    auto value = std::make_shared<UnsupportedValue>();
    EXPECT_THROW(serialize(value), std::runtime_error);
}

TEST(YamlSerializationTests, DeserializeUnsupportedType) {
    YAML::Node node = YAML::Load("{ key: value }");
    EXPECT_THROW(deserialize(node), std::runtime_error);
}

TEST(YamlSerializationTests, SerializeDeserializeNullptr) {
    MetadataPtr null_value = nullptr;
    EXPECT_THROW(serialize(null_value), std::runtime_error);

    YAML::Node node;
    EXPECT_THROW(deserialize(node), std::runtime_error);
}

TEST(YamlSerializationTests, SerializeDeserializeNestedList) {
    auto inner_list = std::make_shared<ListValue>(ListValue::ValueType{
        std::make_shared<NumericValue>(1),
        std::make_shared<NumericValue>(2)
    });
    auto outer_list = std::make_shared<ListValue>(ListValue::ValueType{
        std::make_shared<NumericValue>(0),
        inner_list
    });

    YAML::Node node = serialize(outer_list);
    auto deserialized = deserialize(node);

    ASSERT_TRUE(deserialized->isList());
    auto outer = std::dynamic_pointer_cast<ListValue>(deserialized);
    EXPECT_EQ(outer->size(), 2);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(outer->getValues()[0])->getValue<int>(), 0);
    
    auto inner = std::dynamic_pointer_cast<ListValue>(outer->getValues()[1]);
    EXPECT_EQ(inner->size(), 2);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(inner->getValues()[0])->getValue<int>(), 1);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(inner->getValues()[1])->getValue<int>(), 2);
}


TEST(YamlSerializationTests, SerializeNumericIntFromDouble) {
    auto value = std::make_shared<NumericValue>(42.0);
    YAML::Node node = serialize(value);
    EXPECT_EQ(node.as<int>(), 42);
}

TEST(YamlSerializationTests, SerializeEmptyList) {
    auto value = std::make_shared<ListValue>(ListValue::ValueType{});
    YAML::Node node = serialize(value);
    EXPECT_EQ(node.size(), 0);
}

TEST(YamlSerializationTests, SerializeMixedList) {
    auto value = std::make_shared<ListValue>(ListValue::ValueType{
        std::make_shared<NumericValue>(1),
        std::make_shared<StringValue>("hello"),
        std::make_shared<NumericValue>(2.5)
    });
    YAML::Node node = serialize(value);
    EXPECT_EQ(node.size(), 3);
    EXPECT_EQ(node[0].as<int>(), 1);
    EXPECT_EQ(node[1].as<std::string>(), "hello");
    EXPECT_DOUBLE_EQ(node[2].as<double>(), 2.5);
}

TEST(YamlSerializationTests, DeserializeScalarInt) {
    YAML::Node node = YAML::Load("42");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isNumeric());
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(value)->getValue<int>(), 42);
}

TEST(YamlSerializationTests, DeserializeScalarDouble) {
    YAML::Node node = YAML::Load("3.14");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isNumeric());
    EXPECT_DOUBLE_EQ(std::dynamic_pointer_cast<NumericValue>(value)->getValue<double>(), 3.14);
}

TEST(YamlSerializationTests, DeserializeScalarString) {
    YAML::Node node = YAML::Load("\"hello\"");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isString());
    EXPECT_EQ(std::dynamic_pointer_cast<StringValue>(value)->getValue(), "hello");
}

TEST(YamlSerializationTests, DeserializeEmptyList) {
    YAML::Node node = YAML::Load("[]");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isList());
    auto list = std::dynamic_pointer_cast<ListValue>(value);
    EXPECT_EQ(list->size(), 0);
}

TEST(YamlSerializationTests, DeserializeMixedList) {
    YAML::Node node = YAML::Load("[1, \"hello\", 2.5]");
    auto value = deserialize(node);
    ASSERT_TRUE(value->isList());
    auto list = std::dynamic_pointer_cast<ListValue>(value);
    EXPECT_EQ(list->size(), 3);
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(list->getValues()[0])->getValue<int>(), 1);
    EXPECT_EQ(std::dynamic_pointer_cast<StringValue>(list->getValues()[1])->getValue(), "hello");
    EXPECT_DOUBLE_EQ(std::dynamic_pointer_cast<NumericValue>(list->getValues()[2])->getValue<double>(), 2.5);
}