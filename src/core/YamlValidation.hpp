// src/core/YamlValidation.hpp
/**
 * @file YamlValidation.hpp
 * @brief Advanced YAML Validation System
 * 
 * @details
 * Provides a robust and configurable validation framework for YAML documents
 * with the following key features:
 * 
 * - Detailed error reporting
 * - Configurable validation options
 * - Context-aware validation
 * - Support for complex validation scenarios
 * 
 * The validation system is designed to:
 * - Ensure data integrity
 * - Prevent potential security risks
 * - Support flexible validation rules
 * - Provide detailed error diagnostics
 * 
 * Core Components:
 * - ValidationError: Custom exception for validation failures
 * - ValidationContext: Tracks validation location and context
 * - YamlValidator: Primary validation class with configurable rules
 * 
 * @version 1.0
 * @date 2024
 * @author DPT Team
 */

#pragma once
#include "MetadataValue.hpp"
#include <yaml-cpp/yaml.h>
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>

namespace dpt::core {
/**
 * @class ValidationContext
 * @brief Manages the context and location during YAML validation
 * 
 * @details
 * Tracks the current validation location through a stack of locations.
 * Provides methods to push, pop, and retrieve the current validation context.
 * 
 * Use cases:
 * - Track nested validation locations
 * - Provide detailed error reporting
 * - Maintain validation state across recursive validations
 */
class ValidationContext {
public:
    /**
     * @brief Push a new location onto the validation stack
     * 
     * @param loc Location to add to the context
     * 
     * @note Allows tracking of nested validation contexts
     */
    void pushLocation(const ValidationError::Location& loc) { locations.push_back(loc); }

    /**
     * @brief Remove the most recently added location
     * 
     * @note Used when moving out of a nested validation context
     */
    void popLocation() { if (!locations.empty()) locations.pop_back(); }

    /**
     * @brief Retrieve the current validation location
     * 
     * @return Current ValidationError::Location
     * @retval Returns an empty location if the stack is empty
     */    
    ValidationError::Location currentLocation() const {
        return locations.empty() ? ValidationError::Location{} : locations.back();
    }

private:
    /// Stack of validation locations
    std::vector<ValidationError::Location> locations;
};

/**
 * @class YamlValidator
 * @brief Primary YAML validation class with extensive configuration options
 * 
 * @details
 * Provides a comprehensive YAML validation mechanism with:
 * - Configurable validation rules
 * - Depth and length restrictions
 * - Numeric and string format validation
 * - Flexible error handling
 * 
 * Validation Capabilities:
 * - Limit sequence depth and length
 * - Restrict string length
 * - Enforce numeric format
 * - Control empty sequence handling
 * - Require explicit string tags
 */
class YamlValidator {
public:
    /**
     * @struct ValidationOptions
     * @brief Configuration parameters for YAML validation
     * 
     * @details
     * Allows fine-grained control over validation rules
     */
    struct ValidationOptions {
        /**
         * @brief Default constructor with sensible default validation rules
         */
        ValidationOptions() 
            : max_sequence_depth(10)
            , max_sequence_length(1000)
            , max_string_length(10000)
            , strict_numeric_format(true)
            , allow_empty_sequences(true)
            , require_explicit_string_tags(false) {}

        std::size_t max_sequence_depth;        ///< Maximum allowed nesting depth for sequences
        std::size_t max_sequence_length;       ///< Maximum number of items in a sequence
        std::size_t max_string_length;         ///< Maximum allowed string length
        bool strict_numeric_format;            ///< Enforce strict numeric formatting
        bool allow_empty_sequences;            ///< Permit empty sequences
        bool require_explicit_string_tags;     ///< Require explicit string tags
    };

    /**
     * @brief Construct a YamlValidator with optional validation options
     * 
     * @param options Validation configuration (defaults to standard options)
     */
    explicit YamlValidator(ValidationOptions options = ValidationOptions())
        : options_(std::move(options)) {}

    /**
     * @brief Validate a YAML node
     * 
     * @param node YAML node to validate
     * @param context Validation context for tracking and error reporting
     * 
     * @throws ValidationError if validation fails
     */
    void validate(const YAML::Node& node, ValidationContext& context) {
        validateNode(node, context, 0);
    }

private:
    ValidationOptions options_;
    /**
     * @brief Recursive node validation method
     * 
     * @param node YAML node to validate
     * @param context Current validation context
     * @param depth Current validation depth
     * 
     * @details
     * Performs recursive validation with the following checks:
     * - Node definition
     * - Maximum depth
     * - Node-specific validations
     */
    void validateNode(const YAML::Node& node, ValidationContext& context, std::size_t depth) {
        if (!node.IsDefined()) {
            throw ValidationError("Undefined node", context.currentLocation());
        }

        if (depth > options_.max_sequence_depth) {
            throw ValidationError(
                "Maximum sequence depth exceeded",
                context.currentLocation(),
                ValidationError::Severity::CRITICAL
            );
        }

        context.pushLocation(ValidationError::Location(
            static_cast<std::size_t>(node.Mark().line + 1),
            static_cast<std::size_t>(node.Mark().column + 1),
            getNodeContext(node)
        ));

        try {
            switch (node.Type()) {
                case YAML::NodeType::Scalar:
                    validateScalar(node, context);
                    break;
                case YAML::NodeType::Sequence:
                    validateSequence(node, context, depth);
                    break;
                default:
                    throw ValidationError(
                        "Unsupported node type",
                        context.currentLocation()
                    );
            }
        }
        catch (...) {
            context.popLocation();
            throw;
        }

        context.popLocation();
    }

    /**
     * @brief Convalida un nodo scalare YAML secondo regole configurabili
     * 
     * @details
     * Esegue una serie di controlli di validazione su un nodo scalare YAML:
     * - Verifica della lunghezza massima
     * - Validazione rigorosa del formato numerico
     * - Gestione dei tag espliciti per stringhe
     * 
     * @param node Nodo YAML scalare da validare
     * @param context Contesto di validazione per la tracciatura degli errori
     * 
     * @throws ValidationError Se il nodo non soddisfa i criteri di validazione
     * 
     * Regole di validazione:
     * - Lunghezza massima della stringa definita da options_.max_string_length
     * - Formato numerico rigoroso per valori numerici
     * - Richiesta di tag espliciti per stringhe non vuote e non numeriche in modalità strict
     * 
     * @note La funzione utilizza le opzioni di validazione correnti per determinare 
     *       il livello di rigore dei controlli
     * 
     * @warning Langia un'eccezione di ValidationError in caso di violazione delle regole
     * 
     * @see ValidationOptions
     * @see ValidationContext
     * 
     * @example
     * ```cpp
     * // Esempio di utilizzo
     * YAML::Node node = YAML::Load("example");
     * ValidationContext context;
     * validator.validateScalar(node, context);  // Potrebbe lanciare ValidationError
     * ```
     * 
     * @todo Possibile estensione per supportare validazioni personalizzate
     */
    void validateScalar(const YAML::Node& node, ValidationContext& context) {
        std::string value = node.Scalar();
        
        // Controllo lunghezza massima
        if (value.length() > options_.max_string_length) {
            throw ValidationError(
                "String exceeds maximum length",
                context.currentLocation()
            );
        }

        // Validazione formato numerico rigoroso
        if (options_.strict_numeric_format && isNumericValue(value)) {
            validateNumericFormat(value, context);
        }

        // Gestione tag in modo più flessibile
        if (options_.require_explicit_string_tags) {
            // Per valori non numerici, verifica la presenza di un tag
            if (!isNumericValue(value) && node.Tag().empty()) {
                // Eccezione solo per stringhe "significative"
                if (value.length() > 0) {
                    throw ValidationError(
                        "Non-empty string values require an explicit tag in strict mode",
                        context.currentLocation()
                    );
                }
            }
        }
    }
    /**
     * @brief Validate sequence (list/array) nodes
     * 
     * @param node Sequence YAML node
     * @param context Current validation context
     * @param depth Current validation depth
     * 
     * @details
     * Validates sequence-specific rules:
     * - Maximum length
     * - Empty sequence handling
     * - Recursive item validation
     */
    void validateSequence(const YAML::Node& node, ValidationContext& context, std::size_t depth) {
        if (node.size() > options_.max_sequence_length) {
            throw ValidationError(
                "Sequence exceeds maximum length",
                context.currentLocation()
            );
        }

        if (!options_.allow_empty_sequences && node.size() == 0) {
            throw ValidationError(
                "Empty sequences are not allowed",
                context.currentLocation()
            );
        }

        std::size_t index = 0;
        for (const auto& item : node) {
            context.pushLocation(ValidationError::Location(
                static_cast<std::size_t>(item.Mark().line + 1),
                static_cast<std::size_t>(item.Mark().column + 1),
                "sequence item " + std::to_string(index + 1)
            ));
            validateNode(item, context, depth + 1);
            context.popLocation();
            ++index;
        }
    }


    /**
     * @brief Check if a string represents a numeric value
     * 
     * @param value String to check
     * @return true if the string is a valid numeric representation
     * @return false otherwise
     */
    bool isNumericValue(const std::string& value) const {
        try {
            size_t pos;
            if (value.find('.') != std::string::npos) {
                std::stod(value, &pos);
            } else {
                std::stoll(value, &pos);
            }
            return pos == value.length();
        } catch (...) {
            return false;
        }
    }

    /**
     * @brief Validate numeric format with detailed checks
     * 
     * @param value Numeric string to validate
     * @param context Current validation context
     * 
     * @throws ValidationError for invalid numeric formats
     */
    void validateNumericFormat(const std::string& value, ValidationContext& context) {
        // Implementa una validazione numerica semplice senza regex
        bool valid = true;
        bool has_dot = false;
        bool has_e = false;
        bool has_sign = false;
        
        for (size_t i = 0; i < value.length(); ++i) {
            char c = value[i];
            if (i == 0 && (c == '+' || c == '-')) {
                has_sign = true;
            } else if (c == '.') {
                if (has_dot || has_e) {
                    valid = false;
                    break;
                }
                has_dot = true;
            } else if (c == 'e' || c == 'E') {
                if (has_e || i == 0) {
                    valid = false;
                    break;
                }
                has_e = true;
            } else if (c == '+' || c == '-') {
                if (!has_e || i == 0) {
                    valid = false;
                    break;
                }
            } else if (c < '0' || c > '9') {
                valid = false;
                break;
            }
        }

        if (!valid) {
            throw ValidationError(
                "Invalid numeric format: " + value,
                context.currentLocation()
            );
        }
    }

    /**
     * @brief Get a human-readable context for a YAML node
     * 
     * @param node YAML node
     * @return Descriptive context string
     */
    std::string getNodeContext(const YAML::Node& node) const {
        switch (node.Type()) {
            case YAML::NodeType::Scalar:
                return "scalar value";
            case YAML::NodeType::Sequence:
                return "sequence";
            default:
                return "unknown";
        }
    }
};

} // namespace dpt::core