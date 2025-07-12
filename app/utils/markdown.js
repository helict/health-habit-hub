import fs from 'fs';
import path from 'path';
import { marked } from 'marked';

export function loadMarkdown(lang, page) {
  const file = path.join('app', 'content', lang, `${page}.md`);
  const md = fs.readFileSync(file, 'utf8');
  return marked.parse(md);
}