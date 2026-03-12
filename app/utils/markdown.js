import { readFile } from 'fs/promises';
import path from 'path';
import { marked } from 'marked';

export async function loadMarkdown(lang, name) {
const filePath = path.join('language', lang, `${name}.md`);  const md = await readFile(filePath, 'utf-8');
  return marked.parse(md);
}