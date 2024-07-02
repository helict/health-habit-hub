import globals from 'globals';
import pluginJs from '@eslint/js';
import json from 'eslint-plugin-json';
import html from 'eslint-plugin-html';
import ejs from '@angelventura/eslint-plugin-ejs';
import eslintConfigPrettier from 'eslint-config-prettier';

export default [
  {
    languageOptions: { globals: globals.node },
  },
  { files: ['public/**'], languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  json.configs.recommended,
  { files: ['**/*.html'], plugins: { html } },
  { plugins: { ejs } },
  eslintConfigPrettier,
  {
    ignores: [
      'public/js/thanks.js',
      'public/js/contact.js',
      'public/js/reward.js',
    ],
  },
];
