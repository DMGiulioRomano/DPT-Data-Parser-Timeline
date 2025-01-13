// src/core/YamlParser.cpp
#include "YamlParser.hpp"
#include "YamlValidation.hpp"
#include <sstream>

namespace dpt::core {

/**
 * @brief Costruttore della classe YamlParser.
 * @param options Opzioni di parsing.
 */
YamlParser::YamlParser(ParseOptions options) 
    : m_options(std::move(options)) {}

/**
 * @brief Effettua il parsing di un nodo YAML.
 * @param node Nodo YAML da parsare.
 * @return Puntatore condiviso a MetadataValue risultante dal parsing.
 * @throw std::runtime_error se il nodo è indefinito o se la validazione dello schema fallisce.
 */
MetadataPtr YamlParser::parse(const YAML::Node& node) {
    if (!node.IsDefined()) {
        throw std::runtime_error("Undefined YAML node");
    }

    // In strict mode, require explicit type tags for strings
    if (m_options.strict_mode && node.Type() == YAML::NodeType::Scalar) {
        std::string value = node.Scalar();
        // Skip numeric values
        try {
            std::stod(value);
            // If parsing as double succeeds, it's a number, so skip tag check
            return parseScalar(node);
        } catch (...) {
            // Non-numeric scalar in strict mode requires a tag
            if (node.Tag().empty()) {
                throw std::runtime_error("Explicit tag required for non-numeric string in strict mode");
            }
        }
    }

    // Always validate if schema validation is enabled
    if (m_options.validate_schema) {
        ValidationContext context;
        YamlValidator::ValidationOptions validationOpts;
        // Mirror validation options from ParseOptions
        validationOpts.strict_numeric_format = m_options.strict_mode;
        validationOpts.require_explicit_string_tags = m_options.strict_mode;
        
        YamlValidator validator(validationOpts);
        try {
            validator.validate(node, context);
        } catch (const ValidationError& e) {
            // Rethrow as runtime_error to match existing error handling
            throw std::runtime_error(e.what());
        }
    }

    switch (node.Type()) {
        case YAML::NodeType::Scalar:
            return parseScalar(node);
            
        case YAML::NodeType::Sequence:
            return parseSequence(node);
            
        default:
            throwParseError("Unsupported node type", node);
            // Per il compilatore, non viene mai raggiunto a causa del throw
            return nullptr;
    }
}

/**
 * @brief Effettua il parsing di una stringa YAML.
 * @param yaml_content Contenuto YAML da parsare.
 * @return Puntatore condiviso a MetadataValue risultante dal parsing.
 * @throw std::runtime_error se si verifica un errore di parsing YAML.
 */
MetadataPtr YamlParser::parse(const std::string& yaml_content) {
    try {
        YAML::Node root = YAML::Load(yaml_content); // Parsing della stringa in YAML::Node
        return parse(root); // Chiamata all'altro metodo per l'elaborazione
    } catch (const YAML::ParserException& e) {
        throw std::runtime_error(std::string("Errore di parsing YAML: ") + e.what());
    }
}

/**
 * @brief Effettua il parsing di un nodo YAML scalare.
 * @param node Nodo YAML scalare da parsare.
 * @return Puntatore condiviso a MetadataValue risultante dal parsing.
 */
MetadataPtr YamlParser::parseScalar(const YAML::Node& node) {
    std::string value = node.Scalar();
    
    // First try to parse as numeric since numbers don't need tags
    try {
        return std::make_shared<NumericValue>(node.as<int>());
    } catch (...) {
        try {
            return std::make_shared<NumericValue>(node.as<double>());
        } catch (...) {
            // Not a number, so in strict mode we need a tag
            if (m_options.strict_mode && node.Tag().empty()) {
                throw std::runtime_error("Explicit tag required for non-numeric scalar in strict mode");
            }
            return std::make_shared<StringValue>(value);
        }
    }
}

/**
 * @brief Effettua il parsing di un nodo YAML di sequenza.
 * @param node Nodo YAML di sequenza da parsare.
 * @return Puntatore condiviso a MetadataValue risultante dal parsing.
 */
MetadataPtr YamlParser::parseSequence(const YAML::Node& node) {
    ListValue::ValueType values;
    values.reserve(node.size());

    for (const auto& item : node) {
        values.push_back(parse(item));
    }

    return std::make_shared<ListValue>(values);
}

/**
 * @brief Serializza un MetadataValue in formato YAML.
 * @param value Puntatore condiviso a MetadataValue da serializzare.
 * @return Stringa YAML risultante dalla serializzazione.
 * @throw std::runtime_error se il valore è nullo o se il tipo di valore non è supportato.
 */
std::string YamlParser::serialize(const MetadataPtr& value) const {
    if (!value) {
        throw std::runtime_error("Cannot serialize null value");
    }

    if (auto list = std::dynamic_pointer_cast<ListValue>(value)) {
        std::ostringstream oss;
        oss << "[";
        bool first = true;
        for (const auto& item : list->getValues()) {
            if (!first) oss << ", ";
            first = false;
            if (auto num = std::dynamic_pointer_cast<NumericValue>(item)) {
                std::visit([&oss](auto&& val) {
                    using T = std::decay_t<decltype(val)>;
                    if constexpr (std::is_same_v<T, double>) {
                        oss.precision(2);
                        oss << std::fixed << val;
                    } else {
                        oss << val;
                    }
                }, num->getVariant());
            } else {
                oss << serialize(item);
            }
        }
        oss << "]";
        return oss.str();
    }
    else if (auto numeric = std::dynamic_pointer_cast<NumericValue>(value)) {
        std::ostringstream oss;
        std::visit([&oss, this](auto&& val) {
            using T = std::decay_t<decltype(val)>;
            if constexpr (std::is_same_v<T, double>) {
                // Determina il numero di cifre decimali
                std::ostringstream ref_oss;
                ref_oss << val;
                std::string ref_str = ref_oss.str();
                size_t decimal_pos = ref_str.find('.');
                int decimal_places = (decimal_pos != std::string::npos) ? ref_str.length() - decimal_pos - 1 : 0;

                // Tronca al numero di cifre decimali del valore di riferimento
                oss.precision(decimal_places);
                oss << std::fixed << val;
            } else {
                oss << val;
            }
        }, numeric->getVariant());
        return oss.str();
    }
    else if (auto str = std::dynamic_pointer_cast<StringValue>(value)) {
        return str->getValue();
    }

    throw std::runtime_error("Unsupported value type for serialization");
}

/**
 * @brief Valida un nodo YAML
 * 
 * Verifica la conformità del nodo YAML alle opzioni di parsing.
 * 
 * @param node Nodo YAML da validare
 * @return bool True se validazione riuscita, false altrimenti
 * @throws ValidationError In modalità strict se la validazione fallisce
 */
bool YamlParser::validateNode(const YAML::Node& node) const {
    try {
        ValidationContext context;
        YamlValidator::ValidationOptions validationOpts;
        validationOpts.strict_numeric_format = m_options.strict_mode;
        validationOpts.require_explicit_string_tags = m_options.strict_mode;
        
        YamlValidator validator(validationOpts);
        validator.validate(node, context);
        return true;
    }
    catch (const ValidationError& e) {
        if (m_options.strict_mode) {
            throw;  // In modalità strict, propaga l'errore
        }
        return false;  // In modalità non-strict, ritorna false
    }
}

/**
 * @brief Lancia un'eccezione di errore di parsing con informazioni contestuali.
 * @param msg Messaggio di errore.
 * @param node Nodo YAML che ha causato l'errore.
 * @throw std::runtime_error con il messaggio di errore e le informazioni sul nodo.
 */
void YamlParser::throwParseError(const std::string& msg, const YAML::Node& node) const {
    std::ostringstream error;
    error << msg;
    const auto mark = node.Mark();
    if (mark.line != -1 && mark.column != -1) {
        error << " at line " << node.Mark().line + 1
              << ", column " << node.Mark().column + 1;
    }
    throw std::runtime_error(error.str());
}

} // namespace dpt::core