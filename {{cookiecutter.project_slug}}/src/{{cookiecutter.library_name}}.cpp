/**
 **************************************************
 * @file     {{cookiecutter.library_name}}.cpp
 * @author   {{cookiecutter.full_name}}
 * @date     {% now 'local', '%Y-%m-%d' %}
 * @brief Some brief description about this module
 *
 */

/** @mainpage {{cookiecutter.project_name}}
 *
 * This is a cool project that does such and such.
 *
 */

#include <{{cookiecutter.library_name}}/{{cookiecutter.library_name}}.hpp>

/*! @brief about {{cookiecutter.cpp_namespace}}
*
*  some bla about {{cookiecutter.cpp_namespace}}
*/
namespace {{cookiecutter.cpp_namespace}} {

    /*! @brief about message()
    *
    *  some bla about message()
    * @param recipient The thing or person that shall be greeted.
    * @return message
    */
    std::string message(const std::string& recipient)
    {
        const std::string greeting { "Hello" };
        return recipient.empty() ? greeting : greeting + ", " + recipient;
    }

} /* end namespace '{{cookiecutter.cpp_namespace}}' */
