// src/core/YamlSerialization.cpp
#include "YamlSerialization.hpp"

namespace dpt::core {

/**
 * @note Type detection is done through dynamic_pointer_cast to maintain
 * type safety. Each type has its own serialization logic to ensure
 * proper YAML representation.
 */
YAML::Node serialize(const MetadataPtr& value) {
    if (!value) {
        throw std::runtime_error("Cannot serialize null pointer");
    }
    if (auto numeric = std::dynamic_pointer_cast<NumericValue>(value)) {
        // Handle numeric values by checking variant type first
        if (std::holds_alternative<int>(numeric->getVariant())) {
            return YAML::Node(std::get<int>(numeric->getVariant()));
        } else {
            return YAML::Node(std::get<double>(numeric->getVariant()));
        }
    } else if (auto list = std::dynamic_pointer_cast<ListValue>(value)) {
        YAML::Node node;
        for (const auto& item : list->getValues()) {
            node.push_back(serialize(item));
        }
        return node;
    } else if (auto str = std::dynamic_pointer_cast<StringValue>(value)) {
        return YAML::Node(str->getValue());
    }
    throw std::runtime_error("Unsupported MetadataValue type");
}

/**
 * @note Deserialization attempts conversions in order of specificity:
 * int -> double -> string for scalar values. Sequences are recursively
 * processed.
 */
MetadataPtr deserialize(const YAML::Node& node) {
    if (!node.IsDefined()) {
        throw std::runtime_error("Cannot deserialize undefined node");
    }
    switch (node.Type()) {
        case YAML::NodeType::Scalar: {
            try {
                return std::make_shared<NumericValue>(node.as<int>());
            } catch (...) {
                try {
                    return std::make_shared<NumericValue>(node.as<double>());
                } catch (...) {
                    return std::make_shared<StringValue>(node.as<std::string>());
                }
            }
        }
        case YAML::NodeType::Sequence: {
            ListValue::ValueType values;
            for (const auto& item : node) {
                values.push_back(deserialize(item));
            }
            return std::make_shared<ListValue>(values);
        }
        default:
            throw std::runtime_error("Unsupported YAML node type");
    }
}

} // namespace dpt::core