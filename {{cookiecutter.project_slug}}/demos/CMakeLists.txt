# ref.: https://cmake.org/examples/

# Add executable called "demo_message" that is built from the source files "demo_message.cpp".
add_executable(demo_message demo_message.cpp)

# Link the executable to the {{cookiecutter.library_name}} library. Since the {{cookiecutter.library_name}} library has
# public include directories we will use those link directories when building
# demo_message.
target_include_directories({{cookiecutter.library_name}} PUBLIC ../include/)
target_link_libraries(demo_message LINK_PUBLIC {{cookiecutter.library_name}})
