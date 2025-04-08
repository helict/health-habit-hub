import { renderLocalizedView } from "./defaultController.js";

export function renderPrivacyPolicy(req, res) {
  renderLocalizedView(req, res, 'privacy');
}
