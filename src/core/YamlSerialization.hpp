// src/core/YamlSerialization.hpp
#pragma once

#include "MetadataValue.hpp"
#include <yaml-cpp/yaml.h>

namespace dpt::core {

// Funzione per serializzare MetadataValue in YAML
YAML::Node serialize(const MetadataPtr& value);

// Funzione per deserializzare YAML in MetadataValue
MetadataPtr deserialize(const YAML::Node& node);

} // namespace dpt::core