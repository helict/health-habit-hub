import { renderLocalizedView } from './defaultController.js';

export function renderAccessibilityStatement(req, res) {
  renderLocalizedView(req, res, 'accessibility');
}
