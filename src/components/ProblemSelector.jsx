/**
 * ProblemSelector.jsx
 *
 * Compact search-select for the 250 registered problems.
 * Searches by title (partial, case-insensitive) AND by LeetCode number.
 *
 * Usage:
 *   <ProblemSelector
 *     selectedId={problemId}
 *     onSelect={(problemId, starterCode) => { … }}
 *   />
 *
 * onSelect receives BOTH the problem_id string and the ready-to-use
 * starter_code string so the parent can load it into the Monaco editor
 * immediately — no second API call needed.
 */
import { memo, useState, useEffect, useRef, useCallback } from 'react';
import { Search, ChevronDown } from 'lucide-react';
import { fetchProblems } from '@/lib/runSolution';

const DIFF_COLORS = {
  Easy:   'text-emerald-500',
  Medium: 'text-amber-500',
  Hard:   'text-rose-500',
};

// ── palette (matches the dark index.css variables) ─────────────────────────
const S = {
  bg:        '#111111',
  dropdown:  '#131313',
  border:    '#1C1C1C',
  hoverBg:   '#1A1A1A',
  activeBg:  '#222222',
  text:      '#E8E8E8',
  muted:     '#666666',
  inputBg:   '#0D0D0D',
};

function ProblemSelector({ selectedId, onSelect, className = '' }) {
  const [problems, setProblems]   = useState([]);
  const [open, setOpen]           = useState(false);
  const [query, setQuery]         = useState('');
  const inputRef                  = useRef(null);
  const containerRef              = useRef(null);

  // Load problem list once
  useEffect(() => {
    fetchProblems().then(setProblems).catch(() => {});
  }, []);

  // Focus the search input whenever the dropdown opens
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 30);
    }
  }, [open]);

  // Close on Escape
  useEffect(() => {
    if (!open) return;
    const handler = (e) => { if (e.key === 'Escape') setOpen(false); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [open]);

  // Filter: match title (partial) OR leetcode_number (exact or prefix)
  const filtered = problems.filter((p) => {
    if (!query.trim()) return true;
    const q = query.toLowerCase().trim();
    const titleMatch  = p.title.toLowerCase().includes(q);
    const lcNum       = p.leetcode_number != null ? String(p.leetcode_number) : '';
    const lcMatch     = lcNum.startsWith(q) || lcNum === q;
    return titleMatch || lcMatch;
  });

  // Sort: exact LC number match first, then title alphabetically
  const sorted = [...filtered].sort((a, b) => {
    const q = query.trim();
    if (q && !isNaN(q)) {
      const aExact = String(a.leetcode_number) === q ? 0 : 1;
      const bExact = String(b.leetcode_number) === q ? 0 : 1;
      if (aExact !== bExact) return aExact - bExact;
    }
    return (a.leetcode_number ?? 9999) - (b.leetcode_number ?? 9999);
  });

  const selected = problems.find((p) => p.problem_id === selectedId);

  const handleSelect = useCallback((p) => {
    onSelect?.(p.problem_id, p.starter_code || '');
    setOpen(false);
    setQuery('');
  }, [onSelect]);

  return (
    <div ref={containerRef} className={`relative shrink-0 ${className}`}>
      {/* Trigger button */}
      <button
        onClick={() => setOpen((o) => !o)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
          padding: '4px 8px',
          borderRadius: '4px',
          border: `1px solid ${S.border}`,
          background: S.bg,
          color: selected ? S.text : S.muted,
          fontSize: '11px',
          cursor: 'pointer',
          whiteSpace: 'nowrap',
        }}
      >
        <Search style={{ width: 10, height: 10, flexShrink: 0 }} />
        <span style={{ maxWidth: 150, overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {selected
            ? `${selected.title}${selected.leetcode_number ? ` · LC ${selected.leetcode_number}` : ''}`
            : 'Search problems…'}
        </span>
        <ChevronDown style={{ width: 10, height: 10, flexShrink: 0, opacity: 0.5 }} />
      </button>

      {/* Dropdown */}
      {open && (
        <>
          {/* Click-outside backdrop */}
          <div
            style={{ position: 'fixed', inset: 0, zIndex: 40 }}
            onClick={() => setOpen(false)}
          />

          <div
            style={{
              position: 'absolute',
              zIndex: 50,
              top: 'calc(100% + 4px)',
              left: 0,
              width: 300,
              maxHeight: 340,
              display: 'flex',
              flexDirection: 'column',
              background: S.dropdown,
              border: `1px solid ${S.border}`,
              borderRadius: 5,
              boxShadow: '0 8px 24px rgba(0,0,0,0.6)',
              overflow: 'hidden',
            }}
          >
            {/* Search input */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                padding: '6px 8px',
                borderBottom: `1px solid ${S.border}`,
                background: S.inputBg,
              }}
            >
              <Search style={{ width: 11, height: 11, color: S.muted, flexShrink: 0 }} />
              <input
                ref={inputRef}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Name or LC number…"
                style={{
                  flex: 1,
                  background: 'transparent',
                  border: 'none',
                  outline: 'none',
                  color: S.text,
                  fontSize: 11,
                }}
              />
              {query && (
                <button
                  onClick={() => setQuery('')}
                  style={{ color: S.muted, fontSize: 12, lineHeight: 1, background: 'none', border: 'none', cursor: 'pointer' }}
                >
                  ×
                </button>
              )}
            </div>

            {/* Results list */}
            <div style={{ flex: 1, overflowY: 'auto' }}>
              {sorted.length === 0 && (
                <div style={{ padding: '14px 10px', textAlign: 'center', fontSize: 11, color: S.muted }}>
                  No problems match "{query}"
                </div>
              )}
              {sorted.map((p) => {
                const isActive = p.problem_id === selectedId;
                return (
                  <button
                    key={p.problem_id}
                    onClick={() => handleSelect(p)}
                    style={{
                      display: 'block',
                      width: '100%',
                      textAlign: 'left',
                      padding: '6px 10px',
                      background: isActive ? S.activeBg : 'transparent',
                      border: 'none',
                      cursor: 'pointer',
                      borderBottom: `1px solid ${S.border}`,
                    }}
                    onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = S.hoverBg; }}
                    onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = 'transparent'; }}
                  >
                    {/* Title row */}
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 6 }}>
                      <span style={{ fontSize: 11, color: S.text, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {p.title}
                      </span>
                      {p.difficulty && (
                        <span style={{ fontSize: 9, flexShrink: 0, color: DIFF_COLORS[p.difficulty] || S.muted }}>
                          {p.difficulty}
                        </span>
                      )}
                    </div>
                    {/* Subtitle row */}
                    <div style={{ fontSize: 9, color: S.muted, marginTop: 1 }}>
                      {p.leetcode_number ? `LC ${p.leetcode_number}` : ''}
                      {p.leetcode_number && p.pattern ? ' · ' : ''}
                      {p.pattern || ''}
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Footer: total count */}
            <div
              style={{
                padding: '4px 10px',
                borderTop: `1px solid ${S.border}`,
                fontSize: 9,
                color: S.muted,
                textAlign: 'right',
              }}
            >
              {sorted.length} / {problems.length} problems
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default memo(ProblemSelector);
