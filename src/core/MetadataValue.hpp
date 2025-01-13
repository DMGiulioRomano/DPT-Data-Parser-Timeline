/**
 * @file MetadataValue.hpp
 * @brief Core value types for the DPT (Delta Personal Timeline) system
 * 
 * @details 
 * This header defines a flexible, type-safe metadata value system with support for:
 * - Numeric values (integers and floating-point numbers)
 * - Lists of heterogeneous metadata values
 * - String values
 * 
 * Key design principles:
 * - Type safety through polymorphic value types
 * - Immutable value semantics
 * - Runtime type checking
 * - Validation support
 * - Deep copy and cloning capabilities
 * 
 * Namespace: dpt::core
 * 
 * @version 1.0
 * @date 2025
 * @author DPT Team
 */

#pragma once

#include <memory>
#include <string>
#include <vector>
#include <variant>
#include <stdexcept>

namespace dpt::core {

/**
 * @class ValidationError
 * @brief Custom exception for validation failures in metadata values
 * 
 * @details 
 * Provides a rich error reporting mechanism with:
 * - Detailed error messages
 * - Location tracking (line, column, context)
 * - Severity levels
 * 
 * Severity levels allow for different handling of validation issues:
 * - WARNING: Minor issue, can potentially continue processing
 * - ERROR: Significant problem, requires attention
 * - CRITICAL: Severe issue that prevents further processing
 */
class ValidationError : public std::runtime_error {
public:
    /**
     * @enum Severity
     * @brief Represents the severity of a validation error
     */
    enum class Severity {
        WARNING,    ///< Minor validation issue
        ERROR,      ///< Significant validation problem
        CRITICAL    ///< Severe validation failure
    };

    /**
     * @struct Location
     * @brief Represents the precise location of a validation error
     * 
     * @details 
     * Tracks line, column, and contextual information for pinpointing
     * the exact source of a validation issue
     */
    struct Location {
        std::size_t line;       ///< Line number of the error
        std::size_t column;     ///< Column number of the error
        std::string context;    ///< Additional contextual information

        /**
         * @brief Construct a Location with optional parameters
         * @param l Line number (default: 0)
         * @param c Column number (default: 0)
         * @param ctx Context string (default: empty)
         */
        Location(std::size_t l = 0, std::size_t c = 0, std::string ctx = "")
            : line(l), column(c), context(std::move(ctx)) {}
    };

    ValidationError(
        const std::string& message,
        const Location& location = Location{},
        Severity severity = Severity::ERROR
    ) : std::runtime_error(formatMessage(message, location)),
        message_(message),
        location_(location),
        severity_(severity) {}

    const std::string& rawMessage() const { return message_; }
    const Location& location() const { return location_; }
    Severity severity() const { return severity_; }

private:
    static std::string formatMessage(const std::string& msg, const Location& loc) {
        std::string result = msg;
        if (loc.line > 0 || loc.column > 0) {
            result += " at line " + std::to_string(loc.line) + 
                     ", column " + std::to_string(loc.column);
        }
        if (!loc.context.empty()) {
            result += " (context: " + loc.context + ")";
        }
        return result;
    }

    std::string message_;
    Location location_;
    Severity severity_;
};

// Forward declarations
class MetadataValue;
using MetadataPtr = std::shared_ptr<MetadataValue>;

/**
 * @class MetadataValue
 * @brief Abstract base class for all metadata value types
 * 
 * @details
 * Defines the core interface for metadata values in the DPT system.
 * Provides a polymorphic mechanism for handling different value types
 * with a consistent set of operations.
 * 
 * Key abstract methods:
 * - toString(): Converts value to string representation
 * - clone(): Creates a deep copy of the value
 * - validate(): Checks value validity
 * 
 * Type checking methods:
 * - isNumeric(): Checks if value is numeric
 * - isList(): Checks if value is a list
 * - isString(): Checks if value is a string
 */
class MetadataValue {
public:
    /**
     * @brief Virtual destructor for proper polymorphic behavior
     */
    virtual ~MetadataValue() = default;
    
    /**
     * @brief Convert the value to its string representation
     * @return String representation of the value
     */
    virtual std::string toString() const = 0;
    
    /**
     * @brief Create a deep copy of this value
     * @return Smart pointer to the cloned value
     */
    virtual MetadataPtr clone() const = 0;
    
    /**
     * @brief Validate the value according to type-specific rules
     * @return true if valid, false otherwise
     */
    virtual bool validate() const = 0;
    
    /**
     * @brief Check if the value is numeric (int or double)
     * @return true if numeric, false otherwise
     */
    virtual bool isNumeric() const { return false; }
    
    /**
     * @brief Check if the value is a list
     * @return true if list, false otherwise
     */
    virtual bool isList() const { return false; }
    
    /**
     * @brief Check if the value is a string
     * @return true if string, false otherwise
     */
    virtual bool isString() const { return false; }
};

/**
 * @class NumericValue
 * @brief Represents a numeric value supporting both integers and floating-point numbers
 * 
 * @details
 * Uses std::variant to store either an int or double value.
 * Provides type-safe access and conversion between numeric types.
 * 
 * Key features:
 * - Type-safe numeric storage
 * - Runtime type checking
 * - Validation of numeric values (checking for NaN/Inf)
 */
class NumericValue : public MetadataValue {
public:
    /**
     * @brief Supported value types using std::variant
     */
    using ValueType = std::variant<int, double>;
    
    /**
     * @brief Construct a numeric value from an integer
     * @param value Integer value to store
     */
    explicit NumericValue(int value) : m_value(value) {}
    
    /**
     * @brief Construct a numeric value from a double
     * @param value Double value to store
     */
    explicit NumericValue(double value) : m_value(value) {}
    
    bool isNumeric() const override { return true; }
    
    /**
     * @brief Get the stored value as the requested numeric type
     * @tparam T Target numeric type (int or double)
     * @return Value converted to type T
     * @throws std::bad_variant_access if requested type doesn't match stored type
     */
    template<typename T>
    T getValue() const {
        return std::get<T>(m_value);
    }

    /**
     * @brief Get the underlying variant storing the value
     * @return Const reference to the variant
     */
    const ValueType& getVariant() const { return m_value; }

    std::string toString() const override;
    MetadataPtr clone() const override;
    bool validate() const override;

private:
    ValueType m_value;  ///< Stored numeric value
};

/**
 * @class ListValue
 * @brief Represents a heterogeneous list of metadata values
 * 
 * @details
 * Stores a collection of MetadataPtr values with the following properties:
 * - Supports mixed-type lists
 * - Validates all contained values
 * - Supports deep copying
 * - Dynamic modification through append
 */
class ListValue : public MetadataValue {
public:
    using ValueType = std::vector<MetadataPtr>;
    
    /**
     * @brief Construct a list from a vector of metadata values
     * @param values Vector of values to store
     */
    explicit ListValue(const ValueType& values) : m_values(values) {}
    
    bool isList() const override { return true; }
    
    /**
     * @brief Get the stored values
     * @return Const reference to the vector of values
     */
    const ValueType& getValues() const { return m_values; }
    
    std::string toString() const override;
    MetadataPtr clone() const override;
    bool validate() const override;
    
    /**
     * @brief Append a new value to the list
     * @param value Value to append
     * @throws ValidationError if value is null
     */
    void append(MetadataPtr value);
    
    /**
     * @brief Get the number of values in the list
     * @return List size
     */
    size_t size() const { return m_values.size(); }
    
private:
    ValueType m_values;  ///< Stored list of values
};

/**
 * @class StringValue
 * @brief Represents a string metadata value
 * 
 * @details
 * Simple string storage with basic metadata value interface.
 * Currently, all strings are considered valid.
 */
class StringValue : public MetadataValue {
public:
    /**
     * @brief Construct a string value
     * @param value String to store
     */
    explicit StringValue(std::string value) : m_value(std::move(value)) {}
    
    bool isString() const override { return true; }
    
    /**
     * @brief Get the stored string value
     * @return Const reference to the string
     */
    const std::string& getValue() const { return m_value; }
    
    std::string toString() const override;
    MetadataPtr clone() const override;
    bool validate() const override;
    
private:
    std::string m_value;  ///< Stored string value
};

} // namespace dpt::core