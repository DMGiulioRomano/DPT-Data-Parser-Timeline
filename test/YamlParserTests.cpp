// test/YamlParserTests.cpp

#include <gtest/gtest.h>
#include "YamlParser.hpp"

using namespace dpt::core;

/**
 * @brief Fixture per i test di YamlParser.
 */
class YamlParserTests : public ::testing::Test {
protected:
    YamlParser parser;  ///< Parser con opzioni di default
    YamlParser strict_parser{YamlParser::ParseOptions{true, true}};  ///< Parser in modalità strict
};

/**
 * @brief Test per il metodo parse(string) con input valido.
 */
TEST_F(YamlParserTests, ParseStringValidInput) {
    auto result = parser.parse("42");
    ASSERT_TRUE(result->isNumeric());
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(result)->getValue<int>(), 42);
}

/**
 * @brief Test per il metodo parse(string) con YAML non valido.
 */
TEST_F(YamlParserTests, ParseStringInvalidYaml) {
    EXPECT_THROW(parser.parse("invalid: ]: yaml"), std::runtime_error);
}

/**
 * @brief Test per il metodo parse(Node) con un nodo scalare.
 */
TEST_F(YamlParserTests, ParseNodeScalar) {
    YAML::Node node = YAML::Load("3.14");
    auto result = parser.parse(node);
    ASSERT_TRUE(result->isNumeric());
    EXPECT_DOUBLE_EQ(std::dynamic_pointer_cast<NumericValue>(result)->getValue<double>(), 3.14);
}

/**
 * @brief Test per il metodo parse(Node) con un nodo indefinito.
 */
TEST_F(YamlParserTests, ParseNodeUndefined) {
    YAML::Node node;
    EXPECT_THROW(parser.parse(node), std::runtime_error);
}

/**
 * @brief Test per il metodo parseScalar con un intero.
 */
TEST_F(YamlParserTests, ParseScalarInteger) {
    YAML::Node node = YAML::Load("42");
    auto result = parser.parse(node);
    ASSERT_TRUE(result->isNumeric());
    EXPECT_EQ(std::dynamic_pointer_cast<NumericValue>(result)->getValue<int>(), 42);
}

/**
 * @brief Test per il metodo parseScalar con un double.
 */
TEST_F(YamlParserTests, ParseScalarDouble) {
    YAML::Node node = YAML::Load("3.14");
    auto result = parser.parse(node);
    ASSERT_TRUE(result->isNumeric());
    EXPECT_DOUBLE_EQ(std::dynamic_pointer_cast<NumericValue>(result)->getValue<double>(), 3.14);
}

/**
 * @brief Test per il parsing di stringhe in modalità strict con tag esplicito
 */
TEST_F(YamlParserTests, ParseScalarStringStrictModeWithTag) {
    YAML::Node node = YAML::Load("!str \"hello\"");
    auto result = strict_parser.parse(node);  // Using strict parser
    ASSERT_TRUE(result->isString());
    EXPECT_EQ(std::dynamic_pointer_cast<StringValue>(result)->getValue(), "hello");
}

/**
 * @brief Test per verificare che il parsing di stringhe senza tag fallisca in modalità strict
 */
TEST_F(YamlParserTests, ParseScalarStringStrictModeNoTag) {
    YAML::Node node = YAML::Load("\"hello\"");
    EXPECT_THROW({
        strict_parser.parse(node);
    }, std::runtime_error);
}

/**
 * @brief Test per il parsing di stringhe con tag in modalità non-strict
 */
TEST_F(YamlParserTests, ParseScalarStringWithTagNonStrictMode) {
    YAML::Node node = YAML::Load("!str \"hello\"");
    auto result = parser.parse(node);  // Using default parser (non-strict)
    ASSERT_TRUE(result->isString());
    EXPECT_EQ(std::dynamic_pointer_cast<StringValue>(result)->getValue(), "hello");
}

/**
 * @brief Test per il metodo parseSequence con una sequenza vuota.
 */
TEST_F(YamlParserTests, ParseSequenceEmpty) {
    YAML::Node node = YAML::Load("[]");
    auto result = parser.parse(node);
    ASSERT_TRUE(result->isList());
    EXPECT_EQ(std::dynamic_pointer_cast<ListValue>(result)->size(), 0);
}

/**
 * @brief Test per il metodo parseSequence con una sequenza mista.
 */
TEST_F(YamlParserTests, ParseSequenceMixed) {
    YAML::Node node = YAML::Load("[1, \"hello\", 3.14]");
    auto result = parser.parse(node);
    ASSERT_TRUE(result->isList());
    auto list = std::dynamic_pointer_cast<ListValue>(result);
    EXPECT_EQ(list->size(), 3);
    
    EXPECT_TRUE(list->getValues()[0]->isNumeric());
    EXPECT_TRUE(list->getValues()[1]->isString());
    EXPECT_TRUE(list->getValues()[2]->isNumeric());
}

/**
 * @brief Test per il metodo validateNode con un nodo scalare.
 */
TEST_F(YamlParserTests, ValidateNodeScalar) {
    YAML::Node node = YAML::Load("42");
    EXPECT_TRUE(parser.validateNode(node));
}

/**
 * @brief Test per il metodo validateNode con un nodo di sequenza.
 */
TEST_F(YamlParserTests, ValidateNodeSequence) {
    YAML::Node node = YAML::Load("[1, 2, 3]");
    EXPECT_TRUE(parser.validateNode(node));
}

/**
 * @brief Test per il metodo validateNode con un nodo di mappa (non supportato).
 */
TEST_F(YamlParserTests, ValidateNodeMap) {
    YAML::Node node = YAML::Load("{key: value}");
    EXPECT_THROW(parser.validateNode(node), std::runtime_error); // Maps non supportate
}

/**
 * @brief Test per il metodo serialize con un valore numerico intero.
 */
TEST_F(YamlParserTests, SerializeNumericInt) {
    auto value = std::make_shared<NumericValue>(42);
    auto yaml = parser.serialize(value);
    EXPECT_EQ(yaml, "42");
}

/**
 * @brief Test per il metodo serialize con un valore numerico double.
 */
TEST_F(YamlParserTests, SerializeNumericDouble) {
    auto value = std::make_shared<NumericValue>(3.14);
    auto yaml = parser.serialize(value);
    EXPECT_EQ(yaml, "3.14");
}

/**
 * @brief Test per il metodo serialize con un valore stringa.
 */
TEST_F(YamlParserTests, SerializeString) {
    auto value = std::make_shared<StringValue>("hello");
    auto yaml = parser.serialize(value);
    EXPECT_EQ(yaml, "hello");
}

/**
 * @brief Test per il metodo serialize con un valore di lista.
 */
TEST_F(YamlParserTests, SerializeList) {
    ListValue::ValueType values{
        std::make_shared<NumericValue>(1),
        std::make_shared<StringValue>("test"),
        std::make_shared<NumericValue>(2.50)
    };
    auto value = std::make_shared<ListValue>(values);
    auto yaml = parser.serialize(value);
    EXPECT_EQ(yaml, "[1, test, 2.50]");
}

/**
 * @brief Test per il metodo serialize con un valore nullo.
 */
TEST_F(YamlParserTests, SerializeNull) {
    MetadataPtr value = nullptr;
    EXPECT_THROW(parser.serialize(value), std::runtime_error);
}

/**
 * @brief Test per la validazione in modalità strict.
 */
TEST_F(YamlParserTests, StrictModeValidation) {
    YamlParser strict_parser({true, true});
    YamlParser lenient_parser({false, false});
    
    // Un input che dovrebbe essere invalido in strict mode
    YAML::Node node = YAML::Load("{key: value}");
    
    EXPECT_THROW(strict_parser.parse(node), std::runtime_error);
    EXPECT_THROW(lenient_parser.parse(node), std::runtime_error); // Sempre invalido perché non supportiamo maps
}

/**
 * @brief Test per casi limite.
 */
TEST_F(YamlParserTests, EdgeCases) {
    // Numeri molto grandi
    EXPECT_NO_THROW(parser.parse("1e300"));
    
    // Stringhe vuote
    EXPECT_NO_THROW(parser.parse("\"\""));
    
    // Liste annidate
    EXPECT_NO_THROW(parser.parse("[[[]]]"));
}

/**
 * @brief Test per errori di formattazione.
 */
TEST_F(YamlParserTests, FormatErrors) {
    EXPECT_THROW(parser.parse("pino:\n 3\t6 i\n- item1\n  - subitem1\n    badindent"), std::runtime_error);
}