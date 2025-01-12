// src/core/MetadataValue.hpp
#pragma once

#include <memory>
#include <string>
#include <vector>
#include <variant>
#include <stdexcept>

namespace dpt::core {

class ValidationError : public std::runtime_error {
public:
    explicit ValidationError(const std::string& msg) : std::runtime_error(msg) {}
};

// Forward declarations
class MetadataValue;
using MetadataPtr = std::shared_ptr<MetadataValue>;

// Base class for all metadata values
class MetadataValue {
public:
    virtual ~MetadataValue() = default;
    
    // Core interface
    virtual std::string toString() const = 0;
    virtual MetadataPtr clone() const = 0;
    virtual bool validate() const = 0;
    
    // Type checking
    virtual bool isNumeric() const { return false; }
    virtual bool isList() const { return false; }
    virtual bool isString() const { return false; }
};

// Numeric value (supports both int and float)
class NumericValue : public MetadataValue {
public:
    using ValueType = std::variant<int, double>;
    
    explicit NumericValue(int value) : m_value(value) {}
    explicit NumericValue(double value) : m_value(value) {}
    
    bool isNumeric() const override { return true; }
    
    template<typename T>
    T getValue() const {
        return std::get<T>(m_value);
    }

    const ValueType& getVariant() const { return m_value; }

    std::string toString() const override;
    MetadataPtr clone() const override;
    bool validate() const override;

private:
    ValueType m_value;
};

// List value for arrays
class ListValue : public MetadataValue {
public:
    using ValueType = std::vector<MetadataPtr>;
    
    explicit ListValue(const ValueType& values) : m_values(values) {}
    
    bool isList() const override { return true; }
    const ValueType& getValues() const { return m_values; }
    
    std::string toString() const override;
    MetadataPtr clone() const override;
    bool validate() const override;
    
    // List specific operations
    void append(MetadataPtr value);
    size_t size() const { return m_values.size(); }
    
private:
    ValueType m_values;
};

// String value
class StringValue : public MetadataValue {
public:
    explicit StringValue(std::string value) : m_value(std::move(value)) {}
    
    bool isString() const override { return true; }
    const std::string& getValue() const { return m_value; }
    
    std::string toString() const override;
    MetadataPtr clone() const override;
    bool validate() const override;
    
private:
    std::string m_value;
};

} // namespace dpt::core