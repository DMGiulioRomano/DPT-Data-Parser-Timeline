// src/core/MetadataValue.cpp
#include "MetadataValue.hpp"
#include <sstream>

namespace dpt::core {

// NumericValue implementation
std::string NumericValue::toString() const {
    std::ostringstream oss;
    std::visit([&oss](auto&& value) { oss << value; }, m_value);
    return oss.str();
}

/**
 * @note Uses std::visit to handle both int and double values while
 * maintaining type safety and avoiding unnecessary conversions
 */

MetadataPtr NumericValue::clone() const {
    return std::visit([](auto&& value) -> MetadataPtr {
        return std::make_shared<NumericValue>(value);
    }, m_value);
}

/**
 * @note For floating point values, checks for NaN/Inf.
 * Integer values are always considered valid.
 */

bool NumericValue::validate() const {
    return std::visit([](auto&& value) -> bool {
        using T = std::decay_t<decltype(value)>;
        if constexpr (std::is_same_v<T, double>) {
            return std::isfinite(value); // Check for NaN/Inf
        }
        return true; // Integers are always valid
    }, m_value);
}

// ListValue implementation
std::string ListValue::toString() const {
    std::ostringstream oss;
    oss << "[";
    bool first = true;
    for (const auto& value : m_values) {
        if (!first) oss << ", ";
        first = false;
        oss << value->toString();
    }
    oss << "]";
    return oss.str();
}

/**
 * @note Performs deep copy of all contained values to maintain
 * value semantics and avoid shared state
 */
MetadataPtr ListValue::clone() const {
    ValueType newValues;
    newValues.reserve(m_values.size());
    for (const auto& value : m_values) {
        newValues.push_back(value->clone());
    }
    return std::make_shared<ListValue>(newValues);
}

/**
 * @note A list is valid only if all its elements are valid
 * and no null pointers are present
 */
bool ListValue::validate() const {
    return std::all_of(m_values.begin(), m_values.end(),
        [](const auto& value) { return value && value->validate(); });
}

void ListValue::append(MetadataPtr value) {
    if (!value) throw ValidationError("Cannot append null value");
    m_values.push_back(std::move(value));
}

// StringValue implementation
std::string StringValue::toString() const {
    return m_value;
}

MetadataPtr StringValue::clone() const {
    return std::make_shared<StringValue>(m_value);
}

bool StringValue::validate() const {
    return true; // Strings are always valid in our context
}

} // namespace dpt::core