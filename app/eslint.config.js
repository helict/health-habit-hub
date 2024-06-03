import globals from "globals";
import pluginJs from "@eslint/js";
import json from "eslint-plugin-json";
import html from "eslint-plugin-html";
import ejs from "@angelventura/eslint-plugin-ejs";

export default [
  { languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  json.configs.recommended,
  { files: ["**/*.html"], plugins: { html } },
  { plugins: { ejs } },
];
