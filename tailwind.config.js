/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './app/templates/**/*.html', // Include all HTML files in templates directory
        './app/**/*.py',             // Include Python files if they contain Tailwind classes
        './src/**/*.js',             // Include any JavaScript files
        './node_modules/flowbite/**/*.js'
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('flowbite/plugin'), // Ensure Flowbite plugin is loaded correctly
    ],
};
