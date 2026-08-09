/**
 * ProblemSelector.jsx
 *
 * Compact search-select for all 250 registered problems.
 *
 * Search supports:
 *   - Partial title match (case-insensitive)
 *   - Full or prefix LeetCode number  ("206" → Reverse Linked List)
 *   - Words anywhere in the title     ("binary" → all Binary * problems)
 *
 * Usage:
 *   <ProblemSelector
 *     selectedId={problemId}
 *     onSelect={(problemId, starterCode) => { … }}
 *   />
 *
 * onSelect receives BOTH the problem_id and the ready-to-use starter_code
 * from the backend registry — no hardcoded templates, no second API call.
 */
import { memo, useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { Search, ChevronDown, X } from 'lucide-react';
import { fetchProblems } from '@/lib/runSolution';

// ── palette matching the app's dark CSS variables ───────────────────────────
const C = {
  bg:       '#111111',
  dropdown: '#131313',
  border:   '#1C1C1C',
  hover:    '#1A1A1A',
  active:   '#222222',
  text:     '#E8E8E8',
  muted:    '#666666',
  inputBg:  '#0D0D0D',
  easy:     '#10b981',
  medium:   '#f59e0b',
  hard:     '#ef4444',
};

const DIFF_COLOR = { Easy: C.easy, Medium: C.medium, Hard: C.hard };

function ProblemSelector({ selectedId, onSelect, className = '' }) {
  const [problems, setProblems] = useState([]);
  const [open, setOpen]         = useState(false);
  const [query, setQuery]       = useState('');
  const [focused, setFocused]   = useState(-1);  // keyboard nav index

  const inputRef     = useRef(null);
  const listRef      = useRef(null);
  const containerRef = useRef(null);

  // ── Load problem list once ───────────────────────────────────────────────
  useEffect(() => {
    fetchProblems().then(setProblems).catch(() => {});
  }, []);

  // ── Auto-focus input when dropdown opens ────────────────────────────────
  useEffect(() => {
    if (open) {
      // small timeout so the dropdown is mounted before focus
      const id = setTimeout(() => inputRef.current?.focus(), 20);
      return () => clearTimeout(id);
    } else {
      setFocused(-1);
    }
  }, [open]);

  // ── Close on Escape ──────────────────────────────────────────────────────
  useEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === 'Escape') { e.stopPropagation(); setOpen(false); }
    };
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  }, [open]);

  // ── Filtered + sorted results ────────────────────────────────────────────
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) {
      // No query → show all, sorted by LC number
      return [...problems].sort((a, b) => (a.leetcode_number ?? 9999) - (b.leetcode_number ?? 9999));
    }

    const isNum = /^\d+$/.test(q);
    const scored = problems
      .map((p) => {
        const title   = (p.title || '').toLowerCase();
        const lcStr   = p.leetcode_number != null ? String(p.leetcode_number) : '';
        const pattern = (p.pattern || '').toLowerCase();

        let score = 0;
        if (isNum) {
          if (lcStr === q)               score = 1000;  // exact LC match
          else if (lcStr.startsWith(q)) score = 800;   // prefix LC match
        }
        if (title === q)                 score = Math.max(score, 900);  // exact title
        if (title.startsWith(q))         score = Math.max(score, 700);  // title prefix
        if (title.includes(q))           score = Math.max(score, 500);  // title contains
        if (pattern.includes(q))         score = Math.max(score, 200);  // pattern match
        // word-by-word match
        if (score === 0) {
          const words = q.split(/\s+/);
          if (words.every((w) => title.includes(w))) score = 400;
        }
        return { p, score };
      })
      .filter(({ score }) => score > 0)
      .sort((a, b) => b.score - a.score || (a.p.leetcode_number ?? 9999) - (b.p.leetcode_number ?? 9999));

    return scored.map(({ p }) => p);
  }, [problems, query]);

  // Reset focused index when filter results change
  useEffect(() => { setFocused(-1); }, [filtered]);

  const selected = useMemo(
    () => problems.find((p) => p.problem_id === selectedId),
    [problems, selectedId]
  );

  // ── Select a problem ─────────────────────────────────────────────────────
  const handleSelect = useCallback((p) => {
    onSelect?.(p.problem_id, p.starter_code || '');
    setOpen(false);
    setQuery('');
  }, [onSelect]);

  // ── Keyboard navigation inside the dropdown ──────────────────────────────
  const handleInputKeyDown = useCallback((e) => {
    if (!open) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setFocused((f) => Math.min(f + 1, filtered.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setFocused((f) => Math.max(f - 1, 0));
    } else if (e.key === 'Enter') {
      if (focused >= 0 && filtered[focused]) {
        e.preventDefault();
        handleSelect(filtered[focused]);
      }
    }
  }, [open, filtered, focused, handleSelect]);

  // Scroll focused row into view
  useEffect(() => {
    if (focused < 0 || !listRef.current) return;
    const row = listRef.current.children[focused];
    row?.scrollIntoView({ block: 'nearest' });
  }, [focused]);

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <div ref={containerRef} className={`relative shrink-0 ${className}`} style={{ zIndex: 50 }}>

      {/* ── Trigger button ─────────────────────────────────────────────── */}
      <button
        onClick={() => setOpen((o) => !o)}
        style={{
          display: 'flex', alignItems: 'center', gap: 5,
          padding: '3px 8px', borderRadius: 4,
          border: `1px solid ${open ? '#333' : C.border}`,
          background: open ? '#1A1A1A' : C.bg,
          color: selected ? C.text : C.muted,
          fontSize: 11, cursor: 'pointer', whiteSpace: 'nowrap',
          transition: 'border-color 0.1s, background 0.1s',
        }}
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <Search style={{ width: 10, height: 10, flexShrink: 0 }} />
        <span style={{ maxWidth: 180, overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {selected
            ? (selected.leetcode_number
                ? `LC ${selected.leetcode_number} · ${selected.title}`
                : selected.title)
            : 'Search problems…'}
        </span>
        <ChevronDown style={{
          width: 9, height: 9, flexShrink: 0, opacity: 0.4,
          transform: open ? 'rotate(180deg)' : 'none',
          transition: 'transform 0.15s',
        }} />
      </button>

      {/* ── Dropdown ───────────────────────────────────────────────────── */}
      {open && (
        <>
          {/* Click-outside backdrop */}
          <div
            style={{ position: 'fixed', inset: 0, zIndex: 49 }}
            onMouseDown={() => setOpen(false)}
          />

          <div
            role="dialog"
            style={{
              position: 'absolute', zIndex: 51,
              top: 'calc(100% + 4px)', left: 0,
              width: 320, maxHeight: 380,
              display: 'flex', flexDirection: 'column',
              background: C.dropdown,
              border: `1px solid #2A2A2A`,
              borderRadius: 5,
              boxShadow: '0 10px 30px rgba(0,0,0,0.7)',
              overflow: 'hidden',
            }}
          >
            {/* Search input row */}
            <div style={{
              display: 'flex', alignItems: 'center', gap: 6,
              padding: '7px 8px',
              borderBottom: `1px solid ${C.border}`,
              background: C.inputBg,
              flexShrink: 0,
            }}>
              <Search style={{ width: 11, height: 11, color: C.muted, flexShrink: 0 }} />
              <input
                ref={inputRef}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleInputKeyDown}
                placeholder="Title or LC number…"
                autoComplete="off"
                spellCheck={false}
                style={{
                  flex: 1, background: 'transparent',
                  border: 'none', outline: 'none',
                  color: C.text, fontSize: 11,
                  caretColor: C.text,
                }}
              />
              {query ? (
                <button
                  onMouseDown={(e) => { e.preventDefault(); setQuery(''); inputRef.current?.focus(); }}
                  style={{ color: C.muted, lineHeight: 1, background: 'none', border: 'none', cursor: 'pointer', padding: '0 2px', fontSize: 14 }}
                  aria-label="Clear search"
                >
                  <X style={{ width: 10, height: 10 }} />
                </button>
              ) : null}
            </div>

            {/* Results list */}
            <div
              ref={listRef}
              role="listbox"
              style={{ flex: 1, overflowY: 'auto' }}
            >
              {filtered.length === 0 ? (
                <div style={{ padding: '16px 12px', textAlign: 'center', fontSize: 11, color: C.muted }}>
                  {query ? `No problems match "${query}"` : 'No problems loaded yet'}
                </div>
              ) : (
                filtered.map((p, idx) => {
                  const isActive  = p.problem_id === selectedId;
                  const isFocused = idx === focused;
                  return (
                    <button
                      key={p.problem_id}
                      role="option"
                      aria-selected={isActive}
                      onClick={() => handleSelect(p)}
                      onMouseEnter={() => setFocused(idx)}
                      style={{
                        display: 'block', width: '100%', textAlign: 'left',
                        padding: '6px 10px', cursor: 'pointer',
                        background: isFocused ? C.hover : isActive ? C.active : 'transparent',
                        border: 'none',
                        borderBottom: `1px solid ${C.border}`,
                        outline: 'none',
                      }}
                    >
                      {/* Title + difficulty */}
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                        <span style={{
                          fontSize: 11, color: C.text, fontWeight: 500,
                          overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap',
                          flex: 1,
                        }}>
                          {p.title}
                        </span>
                        {p.difficulty && (
                          <span style={{
                            fontSize: 9, flexShrink: 0,
                            color: DIFF_COLOR[p.difficulty] || C.muted,
                            fontWeight: 600,
                          }}>
                            {p.difficulty}
                          </span>
                        )}
                      </div>
                      {/* LC number + pattern */}
                      <div style={{ fontSize: 9, color: C.muted, marginTop: 1 }}>
                        {p.leetcode_number ? `LC ${p.leetcode_number}` : ''}
                        {p.leetcode_number && p.pattern ? ' · ' : ''}
                        {p.pattern || ''}
                      </div>
                    </button>
                  );
                })
              )}
            </div>

            {/* Footer: result count */}
            <div style={{
              padding: '4px 10px', flexShrink: 0,
              borderTop: `1px solid ${C.border}`,
              fontSize: 9, color: C.muted, textAlign: 'right',
              background: C.bg,
            }}>
              {query
                ? `${filtered.length} of ${problems.length} problems`
                : `${problems.length} problems`}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default memo(ProblemSelector);
