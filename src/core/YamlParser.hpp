// src/core/YamlParser.hpp
/**
 * @file YamlParser.hpp
 * @brief YAML Parsing and Serialization Utility for DPT System
 * 
 * @details
 * Provides a robust, flexible YAML parsing and serialization mechanism for the 
 * Delta Personal Timeline (DPT) system. Key features include:
 * 
 * - Flexible YAML parsing with configurable options
 * - Support for multiple value types (numeric, string, list)
 * - Strict and lenient parsing modes
 * - Schema validation support
 * - Advanced error handling
 * 
 * Design Principles:
 * - Type-safe parsing
 * - Configurable validation
 * - Detailed error reporting
 * - Extensible parsing strategy
 * 
 * @version 1.0
 * @date 2025
 * @author DPT Team
 * 
 * @note Requires yaml-cpp library for YAML processing
 */
#pragma once

#include "MetadataValue.hpp"
#include <yaml-cpp/yaml.h>
#include <string>
#include <optional>

namespace dpt::core {

/**
 * @brief Classe per il parsing e la serializzazione di YAML.
 */
class YamlParser {
public:
    /**
     * @struct ParseOptions
     * @brief Configuration options for YAML parsing
     * 
     * @details
     * Provides fine-grained control over the parsing process with:
     * - Strict mode toggle
     * - Schema validation control
     * 
     * Parsing modes:
     * - Strict mode: Enforces rigorous parsing rules
     * - Schema validation: Ensures document structure conformity
     */
    struct ParseOptions {
        /**
         * @brief Strict parsing mode flag
         * 
         * When true:
         * - Enforces more rigorous parsing rules
         * - Requires explicit type tags
         * - Performs stricter numeric format validation
         */
        bool strict_mode;   ///< Abilita/disabilita la modalità strict.
        /**
         * @brief Schema validation flag
         * 
         * When true:
         * - Validates document against predefined schema
         * - Checks structural integrity
         * - Prevents potential data inconsistencies
         */
        bool validate_schema;   ///< Abilita/disabilita la validazione dello schema.
        
        /**
         * @brief Construct ParseOptions with configurable parameters
         * 
         * @param strict Enable strict mode (default: true)
         * @param validate Enable schema validation (default: true)
         * 
         * @note Default configuration provides maximum safety
         */
        ParseOptions(bool strict = true, bool validate = true) 
            : strict_mode(strict), validate_schema(validate) {}
    };


    /**
     * @brief Construct a YamlParser with specified parsing options
     * 
     * @param options Parsing configuration (default: strict mode)
     * 
     * @example
     * ```cpp
     * // Create a lenient parser
     * YamlParser lenient_parser({false, false});
     * 
     * // Create a strict parser (default)
     * YamlParser strict_parser;
     * ```
     */
    explicit YamlParser(ParseOptions options = ParseOptions{});

    /**
     * @brief Parse a YAML string into a MetadataValue
     * 
     * @param yaml_content YAML-formatted string to parse
     * @return MetadataPtr Parsed metadata value
     * 
     * @throws std::runtime_error If parsing fails
     * 
     * @note Supports parsing of scalars, sequences, and nested structures
     * 
     * @example
     * ```cpp
     * auto value = parser.parse("42");  // Numeric value
     * auto list = parser.parse("[1, 2, 3]");  // List value
     * ```
     */    
    MetadataPtr parse(const std::string& yaml_content);

    /**
     * @brief Parse a YAML node into a MetadataValue
     * 
     * @param node YAML::Node to parse
     * @return MetadataPtr Parsed metadata value
     * 
     * @throws std::runtime_error If parsing fails
     * 
     * @note Primary parsing method used internally
     * @note Supports more complex parsing scenarios
     */
    MetadataPtr parse(const YAML::Node& node);
    
    /**
     * @brief Validate a YAML node against parsing rules
     * 
     * @param node YAML node to validate
     * @return bool True if valid, false otherwise
     * 
     * @details
     * Performs comprehensive validation based on current parsing options
     * 
     * Validation checks include:
     * - Node type compatibility
     * - Structural integrity
     * - Numeric and string format constraints
     */
    bool validateNode(const YAML::Node& node) const;
    
    /**
     * @brief Serialize a MetadataValue to a YAML string
     * 
     * @param value MetadataPtr to serialize
     * @return std::string YAML representation
     * 
     * @throws std::runtime_error If serialization fails
     * 
     * @note Supports serialization of:
     * - Numeric values (int/double)
     * - String values
     * - List values with mixed types
     * 
     * @example
     * ```cpp
     * auto numeric = std::make_shared<NumericValue>(42);
     * std::string yaml = parser.serialize(numeric);  // Returns "42"
     * 
     * auto list = std::make_shared<ListValue>({numeric, 
     *                  std::make_shared<StringValue>("hello")});
     * std::string list_yaml = parser.serialize(list);  // Returns "[42, hello]"
     * ```
     */
    std::string serialize(const MetadataPtr& value) const;

private:
    ParseOptions m_options;   ///< Opzioni di parsing.

    /**
     * @brief Parse a scalar YAML node
     * 
     * @param node Scalar YAML node to parse
     * @return MetadataPtr Parsed scalar value
     * 
     * @details
     * Attempts parsing in the following order:
     * 1. Integer
     * 2. Double
     * 3. String
     * 
     * Provides type-safe conversion and fallback mechanisms
     */
    MetadataPtr parseScalar(const YAML::Node& node);

    /**
     * @brief Parse a sequence (list) YAML node
     * 
     * @param node Sequence YAML node to parse
     * @return MetadataPtr Parsed list value
     * 
     * @details
     * Recursively parses list items, supporting:
     * - Homogeneous lists
     * - Heterogeneous lists
     * - Nested list structures
     */
    MetadataPtr parseSequence(const YAML::Node& node);
    
    /**
     * @brief Throw a parse error with contextual information
     * 
     * @param msg Error message
     * @param node YAML node causing the error
     * 
     * @throws std::runtime_error Always throws with detailed error information
     * 
     * @note Provides rich error context including:
     * - Error message
     * - Line number
     * - Column number
     */
    [[noreturn]] void throwParseError(const std::string& msg, const YAML::Node& node) const;
};

} // namespace dpt::core