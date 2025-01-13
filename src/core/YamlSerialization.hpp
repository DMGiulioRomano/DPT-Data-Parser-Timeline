// src/core/YamlSerialization.hpp
/**
 * @file YamlSerialization.hpp
 * @brief YAML serialization/deserialization for DPT metadata values
 * 
 * This file provides functions for converting between MetadataValue objects
 * and YAML format. It handles serialization of all supported value types
 * (numeric, list, string) and provides robust error handling.
 */

#pragma once

#include "MetadataValue.hpp"
#include <yaml-cpp/yaml.h>

namespace dpt::core {

/**
 * @brief Serialize a MetadataValue object to YAML format
 * 
 * Converts a metadata value to its YAML representation. The conversion
 * depends on the concrete type of the value:
 * - NumericValue: Converted to YAML scalar (int or float)
 * - ListValue: Converted to YAML sequence
 * - StringValue: Converted to YAML scalar string
 * 
 * @param value Smart pointer to the value to serialize
 * @return YAML node containing the serialized data
 * @throws std::runtime_error if value is null
 * @throws std::runtime_error if value is of unsupported type
 * 
 * @code
 * auto numValue = std::make_shared<NumericValue>(42);
 * YAML::Node node = serialize(numValue);
 * // node will contain scalar value 42
 * 
 * auto listValue = std::make_shared<ListValue>(std::vector{
 *     std::make_shared<NumericValue>(1),
 *     std::make_shared<StringValue>("test")
 * });
 * node = serialize(listValue);
 * // node will contain sequence [1, "test"]
 * @endcode
 */
YAML::Node serialize(const MetadataPtr& value);

/**
 * @brief Deserialize a YAML node to a MetadataValue object
 * 
 * Creates a new MetadataValue object from a YAML node. The type of the
 * created object depends on the YAML node type:
 * - Scalar node with number: NumericValue
 * - Scalar node with string: StringValue
 * - Sequence node: ListValue
 * 
 * @param node YAML node to deserialize
 * @return Smart pointer to the deserialized value
 * @throws std::runtime_error if node is undefined
 * @throws std::runtime_error if node is of unsupported type
 * 
 * @code
 * // From scalar
 * YAML::Node node = YAML::Load("42");
 * auto value = deserialize(node);
 * // value will be NumericValue(42)
 * 
 * // From sequence
 * node = YAML::Load("[1, hello]");
 * value = deserialize(node);
 * // value will be ListValue containing NumericValue(1) and StringValue("hello")
 * @endcode
 */
MetadataPtr deserialize(const YAML::Node& node);

} // namespace dpt::core