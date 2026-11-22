import React from 'react';
import { ExternalLink } from 'lucide-react';

/**
 * Clean, safe Markdown Renderer component for conversational chat bubbles.
 * Parses headings, bold, lists, numbered steps, links, and blockquotes.
 * Eliminates raw '###' and '####' artifacts, keeping mobile layout compact and legible.
 */
export default function MarkdownRenderer({ content, className = '' }) {
  if (!content) return null;

  // Split lines
  const rawLines = content.split('\n');

  const renderFormattedInline = (text) => {
    if (!text) return null;

    // Pattern for links [label](url) and bold **bold**
    const parts = [];
    let remaining = text;
    let keyIdx = 0;

    // Regex to match [text](url) OR **bold**
    const inlineRegex = /(\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)|\*\*([^*]+)\*\*|•\s*)/g;
    let match;
    let lastIndex = 0;

    while ((match = inlineRegex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        parts.push(text.substring(lastIndex, match.index));
      }

      if (match[1]?.startsWith('[') && match[3]) {
        // Safe link
        const label = match[2];
        const url = match[3];
        parts.push(
          <a
            key={`link-${keyIdx++}`}
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-indigo-600 dark:text-indigo-400 font-semibold hover:underline inline-flex items-center gap-0.5 break-all"
          >
            <span>{label}</span>
            <ExternalLink className="w-3 h-3 inline-block shrink-0 opacity-70" />
          </a>
        );
      } else if (match[4]) {
        // Bold
        parts.push(
          <strong key={`bold-${keyIdx++}`} className="font-extrabold text-slate-900 dark:text-white">
            {match[4]}
          </strong>
        );
      } else if (match[0].startsWith('•')) {
        parts.push(
          <span key={`bullet-${keyIdx++}`} className="text-indigo-500 mr-1.5 font-bold">
            •
          </span>
        );
      }

      lastIndex = inlineRegex.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }

    return parts;
  };

  const elements = [];
  let listItems = [];
  let inList = false;

  const flushList = () => {
    if (listItems.length > 0) {
      elements.push(
        <ul key={`ul-${elements.length}`} className="space-y-1.5 my-1.5 pl-1">
          {listItems.map((item, idx) => (
            <li key={idx} className="flex items-start gap-2 text-xs sm:text-sm">
              <span className="text-indigo-500 font-bold shrink-0 mt-0.5">•</span>
              <div className="flex-1 leading-relaxed">{renderFormattedInline(item)}</div>
            </li>
          ))}
        </ul>
      );
      listItems = [];
      inList = false;
    }
  };

  for (let i = 0; i < rawLines.length; i++) {
    let line = rawLines[i].trim();

    // Strip raw markdown headers (### or ####)
    if (line.startsWith('####')) {
      flushList();
      const headingText = line.replace(/^####\s*/, '');
      elements.push(
        <h4 key={`h4-${i}`} className="font-bold text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400 mt-2.5 mb-1">
          {renderFormattedInline(headingText)}
        </h4>
      );
      continue;
    }
    if (line.startsWith('###')) {
      flushList();
      const headingText = line.replace(/^###\s*/, '');
      elements.push(
        <h3 key={`h3-${i}`} className="font-extrabold text-sm text-slate-900 dark:text-white mt-3 mb-1">
          {renderFormattedInline(headingText)}
        </h3>
      );
      continue;
    }
    if (line.startsWith('##')) {
      flushList();
      const headingText = line.replace(/^##\s*/, '');
      elements.push(
        <h2 key={`h2-${i}`} className="font-extrabold text-base text-slate-900 dark:text-white mt-3.5 mb-1.5">
          {renderFormattedInline(headingText)}
        </h2>
      );
      continue;
    }

    // Numbered step (e.g. "1. Step description")
    const stepMatch = line.match(/^(\d+)\.\s+(.*)$/);
    if (stepMatch) {
      flushList();
      const num = stepMatch[1];
      const stepText = stepMatch[2];
      elements.push(
        <div key={`step-${i}`} className="flex items-start gap-2.5 my-1.5 bg-slate-100/60 dark:bg-slate-800/40 p-2 rounded-xl border border-slate-200/50 dark:border-slate-800/60">
          <span className="w-5 h-5 rounded-full bg-indigo-600 text-white text-[11px] font-extrabold flex items-center justify-center shrink-0 mt-0.5">
            {num}
          </span>
          <div className="flex-1 text-xs sm:text-sm leading-relaxed text-slate-700 dark:text-slate-200">
            {renderFormattedInline(stepText)}
          </div>
        </div>
      );
      continue;
    }

    // Bullet line
    if (line.startsWith('- ') || line.startsWith('* ') || line.startsWith('• ')) {
      const itemText = line.replace(/^[-*•]\s*/, '');
      listItems.push(itemText);
      inList = true;
      continue;
    }

    // Blockquote
    if (line.startsWith('>')) {
      flushList();
      const quoteText = line.replace(/^>\s*/, '');
      elements.push(
        <blockquote key={`quote-${i}`} className="p-2.5 rounded-xl bg-amber-500/10 border-l-4 border-amber-500 text-amber-900 dark:text-amber-200 text-xs leading-relaxed my-2">
          {renderFormattedInline(quoteText)}
        </blockquote>
      );
      continue;
    }

    // Empty line
    if (!line) {
      flushList();
      continue;
    }

    // Regular paragraph
    flushList();
    elements.push(
      <p key={`p-${i}`} className="text-xs sm:text-sm leading-relaxed my-1 text-slate-800 dark:text-slate-100">
        {renderFormattedInline(line)}
      </p>
    );
  }

  flushList();

  return <div className={`space-y-1 ${className}`}>{elements}</div>;
}
