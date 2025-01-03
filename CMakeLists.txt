cmake_minimum_required(VERSION 3.10)
project(DPT VERSION 1.0)

find_package(Python3 3.11 COMPONENTS Interpreter Development REQUIRED)

set(PYTHON_SOURCES
    ${CMAKE_SOURCE_DIR}/src/main.py
    ${CMAKE_SOURCE_DIR}/src/MainWindow.py
    ${CMAKE_SOURCE_DIR}/src/Timeline.py
    ${CMAKE_SOURCE_DIR}/src/TimelineView.py
    ${CMAKE_SOURCE_DIR}/src/MusicItem.py
    ${CMAKE_SOURCE_DIR}/src/ParamDialog.py
    ${CMAKE_SOURCE_DIR}/src/RenameDialog.py
    ${CMAKE_SOURCE_DIR}/src/SettingsDialog.py
)

set(VENV_DIR ${CMAKE_BINARY_DIR}/venv)
set(REQUIREMENTS ${CMAKE_SOURCE_DIR}/requirements.txt)

add_custom_command(
    OUTPUT ${VENV_DIR}/built
    COMMAND ${Python3_EXECUTABLE} -m venv ${VENV_DIR}
    COMMAND ${VENV_DIR}/bin/pip install -r ${REQUIREMENTS}
    COMMAND ${CMAKE_COMMAND} -E touch ${VENV_DIR}/built
    DEPENDS ${REQUIREMENTS}
)

add_custom_target(venv ALL 
    DEPENDS ${VENV_DIR}/built
)

add_custom_target(run
    COMMAND ${VENV_DIR}/bin/python ${CMAKE_SOURCE_DIR}/src/main.py
    DEPENDS venv
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/src
)

install(FILES ${PYTHON_SOURCES} DESTINATION bin)
install(FILES settings.json DESTINATION etc)

add_custom_target(clean-all
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_SOURCE_DIR}/clean-all.cmake
)